#!/bin/bash
# enable-grafana-tls.sh — point orc-grafana at the host's Let's Encrypt cert.
#
# WHY
#   Grafana on :9443 serves the 10-year self-signed cert from
#   bootstrap-cert.sh, so every stakeholder gets a browser interstitial.
#   That warning is the reason the Sheet (TODO-111) was proposed as a
#   separate stakeholder surface. But port 443 on this same host already
#   presents a valid Let's Encrypt cert for this hostname — Grafana simply
#   is not pointed at it.
#
# WHAT IT TOUCHES
#   ONLY the orc-additions stack, and within it ONLY the grafana service.
#   It never runs a bare `docker compose up`, never touches /opt/LiveORC,
#   and never recreates liveorc_webapp — whose writable layer still holds
#   ~26 GB of media until TODO-112 lands.
#
#   sensor-upload on :8443 KEEPS the self-signed cert. Pi stations pin it
#   via sensor-upload-ca.pem; swapping that cert breaks every upload.
#   This script changes two Grafana env vars and nothing else.
#
# HOW THE CHANGE IS APPLIED
#   Via docker-compose.override.yml, NOT by editing docker-compose.yml.
#   That is deliberate: docker-compose.yml is replaced by every deploy
#   rsync from the git clone, which would silently revert an inline edit
#   and drop Grafana back to the self-signed cert. rsync runs without
#   --delete and the override does not exist in the repo, so the override
#   survives future deploys.
#
# USAGE
#   sudo ./enable-grafana-tls.sh --check    # discovery + validation only
#   sudo ./enable-grafana-tls.sh            # apply, verify, auto-rollback
#   sudo ./enable-grafana-tls.sh --rollback # revert to the self-signed cert
#
# Safe to re-run. Verifies the result and rolls back automatically if
# Grafana does not come back serving a publicly trusted cert.

set -euo pipefail

HOSTNAME_FQDN="${HOSTNAME_OVERRIDE:-openrivercam.endlessprojects.info}"
STACK_DIR="/opt/orc-additions"
OVERRIDE="$STACK_DIR/docker-compose.override.yml"
CONTAINER="orc-grafana"
SERVICE="grafana"
PORT=9443
WATCHER="/usr/local/bin/orc-grafana-cert-watch.sh"
CRONFILE="/etc/cron.d/orc-grafana-cert-watch"
STAMP="/var/lib/orc-grafana-cert.sha256"

MODE="apply"
[ "${1:-}" = "--check" ]    && MODE="check"
[ "${1:-}" = "--rollback" ] && MODE="rollback"

RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; BLD=$'\033[1m'; RST=$'\033[0m'
say()  { printf '%s\n' "$*"; }
ok()   { printf '%s  ok%s  %s\n'   "$GRN" "$RST" "$*"; }
warn() { printf '%s warn%s  %s\n'  "$YEL" "$RST" "$*"; }
die()  { printf '%sFAIL%s  %s\n'   "$RED" "$RST" "$*" >&2; exit 1; }
hdr()  { printf '\n%s== %s ==%s\n' "$BLD" "$*" "$RST"; }

[ "$(id -u)" -eq 0 ] || die "run with sudo"
[ -d "$STACK_DIR" ]  || die "$STACK_DIR not found — is this the LiveORC host?"

if docker compose version >/dev/null 2>&1; then
    DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
    DC=(docker-compose)
else
    die "no docker compose found"
fi
cd "$STACK_DIR"
COMPOSE=("${DC[@]}" --env-file .env)

# ---------------------------------------------------------------- preflight
hdr "Preflight"

# Every compose command against this stack evaluates ${SHEETS_SPREADSHEET_ID:?}
# for the WHOLE file once the sheets-export deploy has landed. If that var is
# missing, even a grafana-only command fails. Catch it here with a useful
# message rather than a raw compose error.
if ! "${COMPOSE[@]}" config -q 2>/tmp/gtls_cfg.err; then
    if grep -qi 'SHEETS_SPREADSHEET_ID' /tmp/gtls_cfg.err; then
        die "compose config fails: SHEETS_SPREADSHEET_ID is unset in $STACK_DIR/.env.
      The sheets-export service was deployed without its variable. Add it
      (TODO-111) or this stack cannot be operated at all:
        echo 'SHEETS_SPREADSHEET_ID=<id>' | sudo tee -a $STACK_DIR/.env"
    fi
    cat /tmp/gtls_cfg.err >&2
    die "docker compose config failed — fix the stack before changing TLS"
fi
ok "compose config parses"

docker inspect "$CONTAINER" >/dev/null 2>&1 || die "$CONTAINER not found"
ok "$CONTAINER exists"

# Snapshot the containers that must NOT be recreated. liveorc_webapp is the
# one that matters: its writable layer holds the media until TODO-112.
PROTECTED=$(docker ps --format '{{.Names}}' | grep -v "^$CONTAINER$" | sort || true)
BEFORE=$(docker inspect -f '{{.Name}} {{.Created}}' $PROTECTED 2>/dev/null | sort || true)
say "    protecting: $(echo "$PROTECTED" | tr '\n' ' ')"

# -------------------------------------------------------- verify / rollback
# Defined and handled BEFORE cert discovery on purpose: discovery can die, and
# "the cert cannot be found" is exactly when rollback needs to still work.
serves_trusted_cert() {
    # --resolve so the chain is validated against the real hostname using the
    # system CA store, exactly as a stakeholder's browser would.
    curl -sS --max-time 8 \
         --resolve "$HOSTNAME_FQDN:$PORT:127.0.0.1" \
         "https://$HOSTNAME_FQDN:$PORT/api/health" >/dev/null 2>&1
}

wait_for_grafana() {
    for _ in $(seq 1 30); do
        if curl -sSk --max-time 5 "https://127.0.0.1:$PORT/api/health" >/dev/null 2>&1; then
            return 0
        fi
        sleep 2
    done
    return 1
}

restart_grafana() {
    # Named service only. A bare `up -d` would churn the rest of the stack.
    "${COMPOSE[@]}" up -d --no-deps "$SERVICE"
}

BACKUP="$OVERRIDE.bak.$(date -u +%Y%m%dT%H%M%SZ)"

restore() {
    say ""
    warn "rolling back"
    if [ -f "$BACKUP" ]; then mv -f "$BACKUP" "$OVERRIDE"; else rm -f "$OVERRIDE"; fi
    restart_grafana >/dev/null 2>&1 || true
    wait_for_grafana && ok "grafana is back on its previous config" \
                     || die "grafana did not come back — check: docker logs $CONTAINER"
}

if [ "$MODE" = "rollback" ]; then
    hdr "Rollback"
    [ -f "$OVERRIDE" ] || die "no $OVERRIDE to remove"
    grep -q 'enable-grafana-tls.sh' "$OVERRIDE" \
        || die "$OVERRIDE was not written by this script — remove it by hand"
    rm -f "$OVERRIDE"
    rm -f "$WATCHER" "$CRONFILE" "$STAMP"
    ok "removed the override, the renewal watcher, and its cron entry"
    restart_grafana
    wait_for_grafana || die "grafana did not come back up"
    ok "reverted to the self-signed cert"
    exit 0
fi

# ------------------------------------------------------------- cert discovery
hdr "Locating a publicly trusted cert for $HOSTNAME_FQDN"

# On this host nginx and certbot both run INSIDE liveorc_webapp, and the certs
# live in the named docker volume liveorc_letsencrypt. So a plain host-path
# search finds nothing — the only cert files loose on the host are the
# self-signed pair in $STACK_DIR/certs.
#
# Named volumes are searched, container overlay layers are NOT:
# /var/lib/docker/volumes/<name>/_data is a stable path that outlives the
# container, and the volume can be mounted by name. An overlay layer is
# neither.
CERTDIR=""; SRC_KIND=""; SRC_NAME=""

try_dir() {  # $1 = directory holding fullchain.pem + privkey.pem
    [ -f "$1/fullchain.pem" ] && [ -f "$1/privkey.pem" ] || return 1
    openssl x509 -in "$1/fullchain.pem" -noout -checkhost "$HOSTNAME_FQDN" \
        >/dev/null 2>&1 || return 1
    return 0
}

# 1. Standard host-side certbot layout.
for d in "/etc/letsencrypt/live/$HOSTNAME_FQDN" /etc/letsencrypt/live/*/; do
    if try_dir "${d%/}"; then
        CERTDIR="${d%/}"; SRC_KIND="hostpath"; break
    fi
done

# 2. Docker named volumes. Mount by NAME rather than by _data path: the name
#    is the supported interface, survives a volume-driver change, and cannot
#    be silently repointed by a docker prune.
if [ -z "$CERTDIR" ]; then
    say "  not on a host path; checking docker named volumes..."
    for v in $(docker volume ls -q 2>/dev/null); do
        mp=$(docker volume inspect -f '{{.Mountpoint}}' "$v" 2>/dev/null) || continue
        [ -d "$mp" ] || continue
        for d in "$mp/live/$HOSTNAME_FQDN" "$mp"/live/*/ "$mp"; do
            if try_dir "${d%/}"; then
                CERTDIR="${d%/}"; SRC_KIND="volume"; SRC_NAME="$v"
                # Path of the cert dir relative to the volume root, so the
                # in-container path can be reconstructed after mounting.
                REL="${CERTDIR#"$mp"}"; REL="${REL#/}"
                break 2
            fi
        done
    done
fi

if [ -z "$CERTDIR" ]; then
    die "no publicly trusted cert for $HOSTNAME_FQDN found on a host path or
      in any docker named volume.

      Check what terminates TLS on :443 and where it keeps its certs:
        sudo ss -ltnp | grep ':443 '
        sudo docker ps --format '{{.Names}}\t{{.Ports}}'
      If TLS terminates inside a container, look for a volume behind it:
        sudo docker inspect <container> \\
          --format '{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}}{{\"\\n\"}}{{end}}'"
fi

CERT="$CERTDIR/fullchain.pem"
KEY="$CERTDIR/privkey.pem"
if [ "$SRC_KIND" = "volume" ]; then
    ok "found in docker volume '$SRC_NAME' at /$REL"
else
    ok "found $CERT"
fi

# ------------------------------------------------------------ cert validation
hdr "Validating"

ISSUER=$(openssl x509 -in "$CERT" -noout -issuer)
SUBJECT=$(openssl x509 -in "$CERT" -noout -subject)
NOTAFTER=$(openssl x509 -in "$CERT" -noout -enddate | cut -d= -f2)
say "    issuer : ${ISSUER#issuer=}"
say "    expires: $NOTAFTER"

[ "${ISSUER#issuer=}" != "${SUBJECT#subject=}" ] \
    || die "that cert is self-signed — it would not fix the browser warning"
ok "not self-signed"

openssl x509 -in "$CERT" -noout -checkend 604800 >/dev/null 2>&1 \
    || warn "cert expires within 7 days — renew before relying on this"

# Cert and key must actually be a pair, or Grafana starts and then fails TLS.
# Compare public keys, NOT moduli: Let's Encrypt issues ECDSA certs by default
# on this host (issuer YE1), and `openssl rsa -modulus` errors with "Not an
# RSA key" on those — which would look exactly like a mismatch.
CPUB=$(openssl x509 -in "$CERT" -noout -pubkey 2>/dev/null | openssl md5)
KPUB=$(openssl pkey -in "$KEY"  -pubout      2>/dev/null | openssl md5 || echo mismatch)
[ "$CPUB" = "$KPUB" ] || die "cert and key do not match ($CERT / $KEY)"
ok "cert and key are a matching pair ($(openssl x509 -in "$CERT" -noout -text \
      | grep -o 'id-ecPublicKey\|rsaEncryption' | head -1))"

# Grafana runs as user "0:0" so it can read a 0600 root-owned privkey.
GUSER=$(docker inspect -f '{{.Config.User}}' "$CONTAINER" 2>/dev/null || echo "")
if [ "$GUSER" = "0:0" ] || [ "$GUSER" = "0" ] || [ -z "$GUSER" ]; then
    ok "grafana runs as root (can read privkey)"
else
    warn "grafana runs as '$GUSER' — it may not be able to read $KEY"
fi

# Always mount the WHOLE tree (volume root, or /etc/letsencrypt), never just
# the live/<domain>/ directory: certbot fills live/ with symlinks into
# ../../archive/, so a narrower mount hands Grafana dangling links.
if [ "$SRC_KIND" = "volume" ]; then
    MOUNT_LINE="$SRC_NAME:/letsencrypt:ro"
    EXTERNAL_VOL="$SRC_NAME"
    IN_CONT_DIR="/letsencrypt${REL:+/$REL}"
    say "    mount  : volume $SRC_NAME -> /letsencrypt (ro)"
else
    MOUNT_SRC="/etc/letsencrypt"
    case "$CERTDIR" in
        /etc/letsencrypt/*) IN_CONT_DIR="/letsencrypt/${CERTDIR#/etc/letsencrypt/}" ;;
        *) MOUNT_SRC="$CERTDIR"; IN_CONT_DIR="/letsencrypt" ;;
    esac
    MOUNT_LINE="$MOUNT_SRC:/letsencrypt:ro"
    EXTERNAL_VOL=""
    say "    mount  : $MOUNT_SRC -> /letsencrypt (ro)"
fi
say "    in-ctr : $IN_CONT_DIR/fullchain.pem"

if [ "$MODE" = "check" ]; then
    hdr "Check only — nothing changed"
    say "Re-run without --check to apply."
    exit 0
fi

# --------------------------------------------------------------------- apply
hdr "Applying"

if [ -f "$OVERRIDE" ]; then
    cp -a "$OVERRIDE" "$BACKUP"
    say "    existing override backed up to $BACKUP"
    if ! grep -q 'enable-grafana-tls.sh' "$OVERRIDE"; then
        warn "$OVERRIDE exists and was NOT written by this script."
        warn "It will be REPLACED. Its contents:"
        sed 's/^/      | /' "$OVERRIDE"
        read -r -p "    Replace it? [y/N] " a
        [ "$a" = "y" ] || [ "$a" = "Y" ] || die "aborted"
    fi
fi

{
cat <<EOF
# Generated by enable-grafana-tls.sh — do not edit by hand.
#
# Points orc-grafana at the Let's Encrypt cert that LiveORC's own nginx uses,
# so stakeholders reach the dashboard without a browser warning. On this host
# nginx and certbot run INSIDE liveorc_webapp and keep their certs in the
# named volume below; nothing publicly trusted exists on a host path.
#
# Lives in an override rather than docker-compose.yml because the deploy rsync
# replaces docker-compose.yml and would silently revert the change.
#
# The volume is mounted READ-ONLY and declared external, so this stack can
# never create, modify, or remove it — \`docker compose down -v\` here will not
# touch LiveORC's certs.
#
# sensor-upload on :8443 deliberately still uses the self-signed cert in
# ./certs — the Pi stations pin it. Do not "unify" these.
#
# Revert with: sudo $STACK_DIR/enable-grafana-tls.sh --rollback
services:
  $SERVICE:
    environment:
      GF_SERVER_CERT_FILE: $IN_CONT_DIR/fullchain.pem
      GF_SERVER_CERT_KEY: $IN_CONT_DIR/privkey.pem
    volumes:
      - ./certs:/certs:ro
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
      - grafana_data:/var/lib/grafana
      - $MOUNT_LINE
EOF
if [ -n "$EXTERNAL_VOL" ]; then
cat <<EOF

volumes:
  $EXTERNAL_VOL:
    external: true
EOF
fi
} > "$OVERRIDE"
ok "wrote $OVERRIDE"

"${COMPOSE[@]}" config -q || { restore; die "override produced invalid compose config"; }
ok "merged config parses"

# Compose merges list-valued keys like `volumes` by appending, but the exact
# semantics have shifted between versions and a "replace" would silently drop
# Grafana's provisioning and its data volume. Assert the merged result really
# still has all four mounts before restarting anything.
MERGED=$("${COMPOSE[@]}" config 2>/dev/null)
for want in /etc/grafana/provisioning /var/lib/grafana/dashboards \
            /var/lib/grafana /letsencrypt; do
    echo "$MERGED" | grep -q "$want" \
        || { restore; die "merged config lost the $want mount — override rejected"; }
done
ok "all four grafana mounts survive the merge"

restart_grafana || { restore; die "could not restart $SERVICE"; }

wait_for_grafana || { restore; die "grafana did not come back up"; }
ok "grafana is up"

if ! serves_trusted_cert; then
    warn "grafana is up but is NOT serving a publicly trusted cert"
    restore
    die "rolled back. Check that $CERT is the cert nginx serves on :443."
fi
ok "serving a publicly trusted cert on :$PORT"

# ---------------------------------------------- confirm nothing else was hit
hdr "Confirming nothing else was touched"
AFTER=$(docker inspect -f '{{.Name}} {{.Created}}' $PROTECTED 2>/dev/null | sort || true)
if [ "$BEFORE" = "$AFTER" ]; then
    ok "no other container was recreated"
else
    warn "a protected container's create time CHANGED:"
    diff <(echo "$BEFORE") <(echo "$AFTER") | sed 's/^/      /' || true
    warn "if liveorc_webapp is in that list, check its media immediately"
fi

# ------------------------------------------------------------- renewal hook
hdr "Renewal"
say "    Grafana caches its cert at startup, so a renewed cert does not take"
say "    effect until the container restarts."
say ""
say "    certbot runs INSIDE liveorc_webapp, so a certbot --deploy-hook would"
say "    have to be installed in that container — which means modifying the"
say "    one container that must not be recreated (TODO-112). Instead, watch"
say "    the cert from the host and restart only orc-grafana when it changes."

cat > "$WATCHER" <<EOF
#!/bin/sh
# Installed by enable-grafana-tls.sh.
#
# certbot renews inside liveorc_webapp and has no way to signal us, so poll
# the cert it writes and restart orc-grafana when the bytes change. Restarting
# only on change makes this a no-op on all but ~6 days a year.
#
# Reads the volume's _data path directly. The container mounts the same volume
# BY NAME; this path is only used for reading, never mounted.
CERT="$CERT"
STAMP="$STAMP"

[ -r "\$CERT" ] || exit 0
NEW=\$(sha256sum "\$CERT" | cut -d' ' -f1)
OLD=\$(cat "\$STAMP" 2>/dev/null || echo none)
[ "\$NEW" = "\$OLD" ] && exit 0

if docker restart $CONTAINER >/dev/null 2>&1; then
    echo "\$NEW" > "\$STAMP"
    logger -t orc-grafana-cert-watch "cert changed; restarted $CONTAINER"
else
    # Leave the stamp alone so the next run retries.
    logger -t orc-grafana-cert-watch "cert changed but restart FAILED"
    exit 1
fi
EOF
chmod 0755 "$WATCHER"
ok "installed $WATCHER"

# Seed the stamp with the cert we just verified, so the first scheduled run
# does not fire a pointless restart.
sha256sum "$CERT" | cut -d' ' -f1 > "$STAMP"

cat > "$CRONFILE" <<EOF
# Installed by enable-grafana-tls.sh. Restarts orc-grafana after certbot
# (inside liveorc_webapp) renews the cert. No-op unless the cert changed.
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
17 3 * * * root $WATCHER
EOF
chmod 0644 "$CRONFILE"
ok "installed $CRONFILE (daily 03:17)"

if ! systemctl is-active --quiet cron 2>/dev/null && \
   ! systemctl is-active --quiet crond 2>/dev/null; then
    warn "no cron daemon appears to be running — the watcher will not fire."
    warn "check with: systemctl status cron crond"
fi

say "    cert expires: $NOTAFTER"
say "    test it now:  sudo $WATCHER && echo 'no-op (cert unchanged) = correct'"

hdr "Done"
say "  Stakeholder URL:  ${BLD}https://$HOSTNAME_FQDN:$PORT/d/station-overview/station-overview${RST}"
say "  No login required — anonymous Viewer is enabled."
say ""
say "  Verify from your laptop, NOT from this host:"
say "    curl -sSI https://$HOSTNAME_FQDN:$PORT/api/health | head -1"
say ""
say "  Note: :$PORT is non-standard and some corporate/mobile networks block"
say "  it. If a stakeholder cannot load it, that is the likely cause."
say "  Revert: sudo $STACK_DIR/enable-grafana-tls.sh --rollback"
