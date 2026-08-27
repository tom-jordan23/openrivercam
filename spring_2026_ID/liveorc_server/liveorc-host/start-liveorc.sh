#!/bin/bash
# LiveORC startup — media on the dedicated EBS volume at /var/lib/liveorc-media.
#
# Installed at /opt/LiveORC/start-liveorc.sh
#
# This is a LOCAL wrapper, NOT part of upstream LiveORC, so edits here survive a
# version upgrade. That is exactly why both guards below live in this file and
# not in docker-compose.yml, which upstream owns and an upgrade overwrites.
#
# See MEDIA_VOLUME_RUNBOOK.md for the 2026-08-10 incident these guards prevent.

cd /opt/LiveORC

# --- Guard 1: config -------------------------------------------------------
# A LiveORC upgrade replaces docker-compose.yml and reverts the media bind
# destination to /liveorc/data/media — a path Django never writes to, because
# MEDIA_ROOT is /liveorc/media. Uploads then land in the container's writable
# layer and vanish on the next recreate. That cost 26 GB of video and took the
# host down on 2026-08-10, silently, over ten weeks.
if ! grep -qF '${LORC_STORAGE_DIR}:/liveorc/media' /opt/LiveORC/docker-compose.yml; then
    echo "FATAL: docker-compose.yml media bind is not /liveorc/media." >&2
    echo "A LiveORC upgrade has probably reverted it. See MEDIA_VOLUME_RUNBOOK.md." >&2
    exit 1
fi

./liveorc.sh start \
  --hostname openrivercam.endlessprojects.info \
  --port 8000 \
  --ssl \
  --storage-local \
  --storage-dir /var/lib/liveorc-media \
  --detached

# --- Repair: nginx SSL config ----------------------------------------------
# LiveORC 0.3.0 generates nginx-ssl.conf from a template that uses the
# standalone `ssl on;` directive. nginx REMOVED that in 1.25.1, and the image
# ships nginx 1.26.3 — so from a clean container nginx dies with
#   [emerg] unknown directive "ssl" in /liveorc/nginx/nginx-ssl.conf:32
# gunicorn still runs, so the container looks healthy while the site is down.
#
# This bit us on 2026-08-27: the container had run since May and was only ever
# `docker start`ed, so a hand-patched nginx-ssl.conf had been living in the
# writable layer. The media migration's recreate deleted it and the site went
# down — the same "critical state in exactly one place" failure the migration
# itself was fixing.
#
# Both seds are idempotent and match nothing once upstream fixes the template,
# so this self-retires rather than masking a future fix. That is why the repair
# lives here and not in a :ro bind mount over the template.
NGINX_FIX='s/^\( *\)listen 8000 deferred;/\1listen 8000 ssl deferred;/; /^ *ssl on;$/d'
for f in /liveorc/nginx/nginx-ssl.conf.template /liveorc/nginx/nginx-ssl.conf; do
    docker exec liveorc_webapp sed -i "$NGINX_FIX" "$f" 2>/dev/null
done

# Start nginx if the entrypoint's attempt died on the unpatched config.
if ! docker exec liveorc_webapp pgrep -x nginx >/dev/null 2>&1; then
    echo "nginx not running after start; starting it against the patched config"
    docker exec -d liveorc_webapp nginx -c /liveorc/nginx/nginx-ssl.conf
    sleep 2
fi

if ! docker exec liveorc_webapp pgrep -x nginx >/dev/null 2>&1; then
    echo "FATAL: nginx is not running in liveorc_webapp." >&2
    echo "gunicorn may be up while the site is unreachable. Check:" >&2
    echo "  docker logs liveorc_webapp | grep emerg" >&2
    exit 1
fi

# --- Guard 2: reality ------------------------------------------------------
# Config is not evidence; the mount table is. Guard 1 can pass while the
# container still comes up wrong.
for _ in $(seq 1 30); do
    docker inspect liveorc_webapp >/dev/null 2>&1 && break
    sleep 2
done

# NOTE: the `--` is required. The pattern starts with '-', so without it grep
# parses it as options, exits 2 with no output, and this guard reports a
# perfectly good mount as missing.
MOUNT=$(docker inspect liveorc_webapp \
    --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' \
    2>/dev/null | grep -F -- '-> /liveorc/media')

if [ -z "$MOUNT" ]; then
    echo "FATAL: /liveorc/media is NOT a mount in liveorc_webapp." >&2
    echo "Media would accumulate in the writable layer and be lost." >&2
    exit 1
fi

echo "LiveORC started; media mount OK: $MOUNT"
