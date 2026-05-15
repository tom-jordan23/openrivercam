# LiveORC server-side additions

Services that run alongside LiveORC on the same EC2 host. Currently:

- **`sensor-upload/`** — FastAPI endpoint receiving sensor CSV uploads from
  Pi stations. Authenticated via per-station bearer token. Writes files
  atomically under `/var/orc/sensors/<station>/`.

Future additions (Grafana, CSV ingester to TimescaleDB) will land in the
same docker-compose file alongside `sensor-upload`.

## Architecture

```
Pi station --HTTPS PUT--> nginx (liveorc_webapp container)
                              |
                              | location /sensors/ proxy_pass
                              v
                          sensor-upload container --writes--> /var/orc/sensors/<station>/
```

The `sensor-upload` container joins LiveORC's docker network
(`liveorc_default`) so LiveORC's nginx can resolve `orc-sensor-upload:8001`
by container name. No new ports are exposed externally — all traffic
arrives on 443 through the existing LiveORC nginx.

## First-time deployment

These steps assume LiveORC is already running at `/opt/LiveORC/` and you
have shell access to the EC2 host.

### 1. Get this directory onto the server

```bash
# If you have the repo cloned:
sudo mkdir -p /opt/orc-additions
sudo rsync -a <repo>/spring_2026_ID/liveorc_server/ /opt/orc-additions/
sudo chown -R $USER:$USER /opt/orc-additions
cd /opt/orc-additions
```

### 2. Generate per-station tokens

```bash
python3 -c 'import secrets; print("sukabumi:" + secrets.token_urlsafe(32))'
python3 -c 'import secrets; print("jakarta:"  + secrets.token_urlsafe(32))'
```

Store **each token in the password manager** alongside the station's other
credentials — these need to be installed on the corresponding Pis later.

### 3. Create `.env`

```bash
cp .env.example .env
chmod 600 .env
$EDITOR .env   # paste the comma-separated station:token pairs
```

`.env` is gitignored. Never commit it. Token rotation procedure is below.

### 4. Create the upload directory on the host

```bash
sudo mkdir -p /var/orc/sensors
sudo chown 1001:1001 /var/orc/sensors      # UID 1001 = app user in the container
sudo chmod 0755 /var/orc/sensors
```

### 5. Confirm LiveORC's network name

```bash
docker network ls | grep liveorc
```

Expect `liveorc_default`. If it's different (e.g., LiveORC was deployed
from a non-standard directory), edit `networks.liveorc.name` in
`docker-compose.yml` accordingly.

### 6. Bring up the service

```bash
cd /opt/orc-additions
sudo docker compose --env-file .env up -d --build
sudo docker ps | grep orc-sensor-upload
sudo docker logs orc-sensor-upload --tail 20
```

You should see `loaded tokens for stations: ['jakarta', 'sukabumi']` and
`Uvicorn running on http://0.0.0.0:8001`.

### 7. Patch LiveORC's nginx with the location block

This is the bit that has to be repeated after any `liveorc.sh rebuild`
(until LiveORC's template supports drop-in includes — filed upstream).

```bash
# Add the location block to both the running config and the in-image template
NGINX_LOC='/liveorc/nginx/nginx-ssl.conf'
NGINX_TPL='/liveorc/nginx/nginx-ssl.conf.template'

sudo docker cp nginx/sensor-upload-location.conf liveorc_webapp:/tmp/sensor-upload-location.conf

# Find the closing brace of the main server { ... } block and insert before it.
# Manual edit is safest given the file structure; pattern below works if you
# trust the template's structure. Inspect the file first.
sudo docker exec liveorc_webapp sed -n '1,200p' "$NGINX_LOC" | grep -n '^[[:space:]]*}'
# (Identify the line that closes the main server { } block, then sed in.
# For a one-shot append-just-before-final-closing-brace, use a small awk:)
sudo docker exec liveorc_webapp sh -c "
  awk '/^}$/ && !done { while ((getline line < \"/tmp/sensor-upload-location.conf\") > 0) print \"    \" line; close(\"/tmp/sensor-upload-location.conf\"); done=1 } 1' \
    $NGINX_LOC > ${NGINX_LOC}.new && mv ${NGINX_LOC}.new $NGINX_LOC
"
sudo docker exec liveorc_webapp sh -c "
  awk '/^}$/ && !done { while ((getline line < \"/tmp/sensor-upload-location.conf\") > 0) print \"    \" line; close(\"/tmp/sensor-upload-location.conf\"); done=1 } 1' \
    $NGINX_TPL > ${NGINX_TPL}.new && mv ${NGINX_TPL}.new $NGINX_TPL
"

# Verify and reload
sudo docker exec liveorc_webapp nginx -t -c $NGINX_LOC
sudo docker exec liveorc_webapp nginx -s reload -c $NGINX_LOC
```

**Verify external reachability:**

```bash
curl -sS https://openrivercam.endlessprojects.info/sensors/health
# Expect: {"ok":true,"stations":["jakarta","sukabumi"]}
```

If you get a 404, the nginx patch didn't land — inspect the conf file
inside the container and adjust the insertion point manually.

### 8. Smoke test an upload

From any host with the token in hand:

```bash
TOKEN=<paste sukabumi token>
echo "ts,value\n$(date -u +%FT%TZ),42" > /tmp/smoke.csv
curl -sS -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/csv" \
  --data-binary @/tmp/smoke.csv \
  https://openrivercam.endlessprojects.info/sensors/upload/sukabumi/smoke-$(date -u +%FT%TZ).csv

sudo ls -la /var/orc/sensors/sukabumi/
```

You should see the file landed with the correct size and a fresh mtime.

## Day-2 operations

### Adding a new station

1. Generate a new token: `python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`
2. Append to `ORC_UPLOAD_TOKENS` in `.env` (e.g., `,ipb:<token>`)
3. `sudo docker compose --env-file .env up -d` to apply (recreates the container)
4. Install the token on that station's Pi (Pass 2 of this work)

### Rotating a station's token

1. Generate new token
2. Update `.env` (replace the old value)
3. `sudo docker compose --env-file .env up -d`
4. Update the Pi's config and restart the upload service
5. The old token is invalidated immediately on container restart

Plan a brief gap between server restart and Pi update — uploads in that
window will 401 and retry on the next wake cycle, which is fine.

### Inspecting recent uploads

```bash
sudo docker logs --tail 100 orc-sensor-upload
sudo ls -la /var/orc/sensors/sukabumi/
```

### Restoring after `liveorc.sh rebuild`

If you rebuild LiveORC:

1. The nginx template inside the container resets — re-apply step 7 above.
2. The `liveorc_default` network is recreated — our `sensor-upload`
   container's network attachment might break. Just
   `cd /opt/orc-additions && sudo docker compose up -d` to reattach.

## Known upstream issues (filed)

- LiveORC: nginx template doesn't support drop-in includes, forcing
  in-image patches to be re-applied after rebuilds.

## Files in this directory

| File | Role |
|------|------|
| `docker-compose.yml` | Top-level compose; defines `sensor-upload` (and future services) |
| `.env.example` | Template for the secrets file. Real `.env` is gitignored. |
| `sensor-upload/app.py` | FastAPI endpoint (~80 lines) |
| `sensor-upload/Dockerfile` | python:3.12-slim + fastapi + uvicorn |
| `nginx/sensor-upload-location.conf` | The location block to patch into LiveORC's nginx |
| `README.md` | This file |
