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
