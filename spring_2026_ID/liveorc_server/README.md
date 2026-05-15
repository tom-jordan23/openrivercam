# LiveORC server-side additions

Services that run alongside LiveORC on the same EC2 host **without modifying
LiveORC's container or config**. Currently:

- **`sensor-upload/`** — FastAPI endpoint receiving sensor CSV uploads from
  Pi stations. Terminates TLS directly on port 8443. Authenticated via
  per-station bearer token. Writes files atomically under
  `/var/orc/sensors/<station>/`.

Future additions (Grafana, CSV ingester to TimescaleDB) will land in the
same docker-compose file alongside `sensor-upload`.

## Architecture

```
Pi station --HTTPS PUT :8443--> orc-sensor-upload container
                                  - uvicorn terminates TLS
                                  - reuses LiveORC's letsencrypt cert
                                    via read-only volume mount
                                  - writes to /var/orc/sensors/<station>/
```

**LiveORC is untouched.** Its container/nginx are not modified — we share
only the letsencrypt cert volume (mounted read-only).

## First-time deployment

These steps assume LiveORC is already running on this host and you have
shell access.

### 1. Get this directory onto the server

```bash
# If you have the repo cloned (e.g., ~/openrivercam):
sudo mkdir -p /opt/orc-additions
sudo rsync -a --delete ~/openrivercam/spring_2026_ID/liveorc_server/ /opt/orc-additions/
sudo chown -R $USER:$USER /opt/orc-additions
cd /opt/orc-additions
```

### 2. Generate per-station tokens

```bash
python3 -c 'import secrets; print("sukabumi:" + secrets.token_urlsafe(32))'
python3 -c 'import secrets; print("jakarta:"  + secrets.token_urlsafe(32))'
```

Store **each token in the password manager** alongside the station's other
credentials — these are installed on the corresponding Pi later.

### 3. Create `.env`

```bash
cp .env.example .env && chmod 600 .env
$EDITOR .env   # paste the comma-separated station:token pairs
```

`.env` is gitignored. Never commit it.

### 4. Create the upload directory on the host

```bash
sudo mkdir -p /var/orc/sensors
sudo chmod 0755 /var/orc/sensors
# Container runs as root and writes here directly — no chown needed.
```

### 5. Confirm LiveORC's letsencrypt volume is named `liveorc_letsencrypt`

```bash
sudo docker volume ls | grep letsencrypt
```

Should show `liveorc_letsencrypt`. If LiveORC was deployed from a
non-standard project name and the volume is `<otherproject>_letsencrypt`,
edit `volumes.liveorc_letsencrypt.name` in `docker-compose.yml`.

### 6. Open AWS Security Group for port 8443

In the EC2 console → Security Groups → the SG attached to your LiveORC
instance → Edit inbound rules:

- Type: `Custom TCP`
- Port: `8443`
- Source: `0.0.0.0/0` (or restrict to known station egress IPs; Indonesian
  carriers use NAT64 so source IPs are unstable — `0.0.0.0/0` plus the
  per-station bearer token is the pragmatic choice)
- Description: `orc-sensor-upload (station CSV ingest)`

### 7. Bring up the service

```bash
cd /opt/orc-additions
sudo docker compose --env-file .env up -d --build
sudo docker ps --filter name=orc-sensor-upload --format '{{.Names}} {{.Status}}'
sudo docker logs orc-sensor-upload --tail 20
```

You should see `loaded tokens for stations: ['jakarta', 'sukabumi']` and
`Uvicorn running on https://0.0.0.0:8443`.

### 8. Smoke test from the open internet

```bash
TOKEN=<paste sukabumi token>
curl -sS https://openrivercam.endlessprojects.info:8443/sensors/health
# Expect: {"ok":true,"stations":["jakarta","sukabumi"]}

echo "ts,value
$(date -u +%FT%TZ),42" | curl -sS -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/csv" \
  --data-binary @- \
  https://openrivercam.endlessprojects.info:8443/sensors/upload/sukabumi/smoke-$(date -u +%FT%TZ).csv
# Expect: {"ok":true,"station":"sukabumi","filename":"...","size":N}

sudo ls -la /var/orc/sensors/sukabumi/
```

If you get TLS errors, see "Cert renewal" below.

## Day-2 operations

### Cert renewal

LiveORC's certbot renews the cert in `liveorc_letsencrypt` every ~60 days
(default Let's Encrypt schedule). Our container has the cert files
**mounted at startup**, so uvicorn loads them once and doesn't auto-refresh.
We need to restart the container periodically to pick up renewed certs.

The pragmatic fix is a weekly restart cron. As root on the EC2 host:

```bash
sudo tee /etc/cron.weekly/orc-sensor-upload-restart > /dev/null <<'EOF'
#!/bin/sh
# Restart orc-sensor-upload weekly so uvicorn picks up renewed LE certs.
docker restart orc-sensor-upload
EOF
sudo chmod 0755 /etc/cron.weekly/orc-sensor-upload-restart
```

The container restart is fast (~3 s). In-flight uploads during the restart
will fail and the Pi retries on next wake — idempotent PUT + watermark
make this safe.

If a cert renewal happens and we miss the restart, certificates won't
expire mid-flight; we just need to restart before the 90-day hard expiry.

### Adding a new station

1. Generate a new token: `python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`
2. Append to `ORC_UPLOAD_TOKENS` in `.env` (e.g., `,ipb:<token>`)
3. `sudo docker compose --env-file .env up -d` to apply (recreates the container)
4. Install the token on that station's Pi (Pi-side docs in `pi/README.md`)

### Rotating a station's token

1. Generate new token
2. Update `.env` (replace the old value)
3. `sudo docker compose --env-file .env up -d`
4. Update the Pi's `~pi/.orc_deploy_<site>` and restart any in-flight upload
5. The old token is invalidated immediately on container restart

Plan a brief gap between server restart and Pi update — uploads in that
window will 401 and retry on the next wake cycle, which is fine.

### Inspecting recent uploads

```bash
sudo docker logs --tail 100 orc-sensor-upload
sudo ls -la /var/orc/sensors/sukabumi/
```

### What `liveorc.sh rebuild` does to us

LiveORC's rebuild process drops and recreates the LiveORC container, but
the `liveorc_letsencrypt` named volume persists. So our service continues
working through a LiveORC rebuild — no action required from us. (This is
the whole reason we chose this architecture.)

If LiveORC ever changes the cert file paths inside its volume (e.g., a
different hostname or domain config), we'll need to update the
`--ssl-keyfile` / `--ssl-certfile` args in `sensor-upload/Dockerfile`.

## Files in this directory

| File | Role |
|------|------|
| `docker-compose.yml` | Defines `sensor-upload` (and future services). External named volume `liveorc_letsencrypt`. |
| `.env.example` | Template for the secrets file. Real `.env` is gitignored. |
| `sensor-upload/app.py` | FastAPI endpoint (~85 lines) |
| `sensor-upload/Dockerfile` | python:3.12-slim + fastapi + uvicorn. Runs as root to read LE privkey. |
| `README.md` | This file |
