# LiveORC server-side additions

Services that run alongside LiveORC on the same EC2 host **without modifying
LiveORC's container or config**. Currently:

- **`sensor-upload/`** — FastAPI endpoint receiving sensor CSV uploads from
  Pi stations. Terminates TLS directly on port 8443 with a self-signed
  certificate. Authenticated via per-station bearer token. Writes files
  atomically under `/var/orc/sensors/<station>/`.

Future additions (Grafana, CSV ingester to TimescaleDB) will land in the
same docker-compose file alongside `sensor-upload`.

## Architecture

```
Pi station --HTTPS PUT :8443--> orc-sensor-upload container
    (curl --cacert pinned)        - uvicorn terminates TLS
                                  - 10-year self-signed cert (NOT a public CA)
                                  - writes to /var/orc/sensors/<station>/
```

**Why self-signed?** LiveORC's letsencrypt volume turns out to be empty
(LiveORC writes certs to a container-internal path that isn't on the
persistent volume), so we can't share their cert. Getting our own LE cert
would require either coordinating port 80 with LiveORC for HTTP-01 or
adding a DNS-01 plugin with API credentials — neither is worth the
complexity for an internal Pi→server channel. Self-signed + Pi-side
pinning gives us TLS without the renewal or coupling cost.

The Pi pins against our cert via `curl --cacert`, so MITM with a
public-CA-issued cert for our hostname won't work either.

**LiveORC is untouched.** Its container, nginx, port mappings, network,
volumes — all unchanged. We share only the host EC2 instance.

## First-time deployment

### 1. Get this directory onto the server

```bash
# If you have the repo cloned (e.g., ~/openrivercam):
sudo mkdir -p /opt/orc-additions
sudo rsync -a --exclude='.env' --exclude='certs/' \
    ~/openrivercam/spring_2026_ID/liveorc_server/ /opt/orc-additions/
sudo chown -R $USER:$USER /opt/orc-additions
cd /opt/orc-additions
```

**Do NOT use `rsync --delete`** — it would wipe `.env` and `certs/` on the
server (both are server-local, not in the repo). The `--exclude` flags
are belt-and-braces in case someone forgets.

### 2. Generate the self-signed cert

```bash
sudo ./bootstrap-cert.sh
```

This creates `/opt/orc-additions/certs/{fullchain,privkey}.pem` with a
10-year validity. The script refuses to overwrite an existing cert.

### 3. Commit the public cert to the repo

The Pi side needs to pin against this cert. Copy the public half (NOT the
private key) into the repo:

```bash
cp /opt/orc-additions/certs/fullchain.pem \
   ~/openrivercam/spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem
cd ~/openrivercam && git add spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem
git commit -m "Add self-signed CA cert for sensor-upload (Pi-side pinning)"
git push
```

The cert is a public artifact — committing it is fine. The private key
stays on the server and is gitignored.

### 4. Generate per-station tokens

```bash
python3 -c 'import secrets; print("sukabumi:" + secrets.token_urlsafe(32))'
python3 -c 'import secrets; print("jakarta:"  + secrets.token_urlsafe(32))'
```

Store **each token in the password manager**.

### 5. Create `.env`

```bash
cp .env.example .env && chmod 600 .env
$EDITOR .env   # paste the comma-separated station:token pairs
```

`.env` is gitignored. Never commit it.

### 6. Create the upload directory on the host

```bash
sudo mkdir -p /var/orc/sensors
sudo chmod 0755 /var/orc/sensors
# Container runs as root and writes here directly — no chown needed.
```

### 7. Open AWS Security Group for port 8443

In the EC2 console → Security Groups → SG attached to the LiveORC instance:

- Type: `Custom TCP`
- Port: `8443`
- Source: `0.0.0.0/0`
- Description: `orc-sensor-upload (station CSV ingest)`

### 8. Bring up the service

```bash
sudo docker compose --env-file .env up -d --build
sudo docker ps --filter name=orc-sensor-upload
sudo docker logs orc-sensor-upload --tail 20
```

Expect to see `loaded tokens for stations: ['jakarta', 'sukabumi']` and
`Uvicorn running on https://0.0.0.0:8443`.

### 9. Smoke test from the open internet

```bash
TOKEN=<paste sukabumi token>
SERVER_CERT=~/openrivercam/spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem

curl --cacert "$SERVER_CERT" -sS \
    https://openrivercam.endlessprojects.info:8443/sensors/health
# Expect: {"ok":true,"stations":["jakarta","sukabumi"]}

echo "ts,value
$(date -u +%FT%TZ),42" | curl --cacert "$SERVER_CERT" -sS -X PUT \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: text/csv" \
    --data-binary @- \
    https://openrivercam.endlessprojects.info:8443/sensors/upload/sukabumi/smoke-$(date -u +%FT%TZ).csv
# Expect: {"ok":true,...}

sudo ls -la /var/orc/sensors/sukabumi/
```

`--cacert` is required because the cert is self-signed. Without it, curl
refuses to connect with `unable to get local issuer certificate`.

## Day-2 operations

### Adding a new station

1. Generate a new token: `python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`
2. Append to `ORC_UPLOAD_TOKENS` in `.env` (e.g., `,ipb:<token>`)
3. `sudo docker compose --env-file .env up -d` to apply (recreates the container)
4. Install the token on that station's Pi (Pi-side docs in `pi/README.md`)

### Rotating a station's token

1. Generate new token
2. Update `.env` (replace the old value)
3. `sudo docker compose --env-file .env up -d`
4. Update the Pi's `~pi/.orc_deploy_<site>` and trigger the upload to verify
5. The old token is invalidated immediately on container restart

### Rotating the server cert

10-year cert; we should never need this in practice. But if compromised:

1. Remove the old cert: `sudo rm /opt/orc-additions/certs/{fullchain,privkey}.pem`
2. Re-run `sudo ./bootstrap-cert.sh`
3. Copy the new `fullchain.pem` into the repo at
   `spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem`, commit, push
4. Restart the container: `sudo docker compose --env-file .env up -d`
5. Each Pi must pull + re-deploy to pick up the new pinned cert before
   their next upload will succeed. Stale Pis will start logging cert
   verification failures — that's the rotation in flight.

### Inspecting recent uploads

```bash
sudo docker logs --tail 100 orc-sensor-upload
sudo ls -la /var/orc/sensors/sukabumi/
```

### What `liveorc.sh rebuild` does to us

Nothing. LiveORC's container rebuild does not touch our service, our
certs, our `.env`, our network, or our volumes. The isolation is by
design.

## Files in this directory

| File | Role | Tracked? |
|------|------|----------|
| `docker-compose.yml` | Service definitions | Yes |
| `.env.example` | Template for the secrets file | Yes |
| `.env` | Real tokens; server-local | No (gitignored) |
| `bootstrap-cert.sh` | One-shot cert generator | Yes |
| `certs/fullchain.pem` | Public cert; copy of repo's CA pin | No (gitignored) |
| `certs/privkey.pem` | Private key; stays on server | No (gitignored) |
| `sensor-upload/app.py` | FastAPI endpoint (~85 lines) | Yes |
| `sensor-upload/Dockerfile` | python:3.12-slim + fastapi + uvicorn | Yes |
| `README.md` | This file | Yes |
