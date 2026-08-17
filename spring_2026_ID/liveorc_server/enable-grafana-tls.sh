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
HOOK_DIR="/etc/letsencrypt/renewal-hooks/deploy"
HOOK="$HOOK_DIR/restart-orc-grafana.sh"

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

# ------------------------------------------------------------- cert discovery
hdr "Locating a publicly trusted cert for $HOSTNAME_FQDN"

CERTDIR=""
for d in "/etc/letsencrypt/live/$HOSTNAME_FQDN" /etc/letsencrypt/live/*/; do
    [ -f "$d/fullchain.pem" ] && [ -f "$d/privkey.pem" ] || continue
    if openssl x509 -in "$d/fullchain.pem" -noout -checkhost "$HOSTNAME_FQDN" >/dev/null 2>&1; then
        CERTDIR="${d%/}"; break
    fi
done

if [ -z "$CERTDIR" ]; then
    say "  not in the standard certbot layout; searching..."
    while read -r f; do
        [ -f "${f%/*}/privkey.pem" ] || continue
        if openssl x509 -in "$f" -noout -checkhost "$HOSTNAME_FQDN" >/dev/null 2>&1; then
            CERTDIR="${f%/*}"; break
        fi
    # /var/lib/docker is pruned: a hit inside a container's overlay layer is
    # not a stable host path and cannot be bind-mounted.
    done < <(find /etc /opt /srv /var \
                  -path /var/lib/docker -prune -o \
                  -path "$STACK_DIR" -prune -o \
                  -name fullchain.pem -print 2>/dev/null)
fi

[ -n "$CERTDIR" ] || die "no cert for $HOSTNAME_FQDN found outside $STACK_DIR.
      The Let's Encrypt cert may live inside the LiveORC nginx container.
      Find it with:  sudo docker exec <nginx-container> ls /etc/letsencrypt/live/"

CERT="$CERTDIR/fullchain.pem"
KEY="$CERTDIR/privkey.pem"
ok "found $CERT"

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

# Resolve symlinks: certbot's live/ contains links into ../../archive/, which
# is why the whole /etc/letsencrypt tree gets mounted, not just live/.
MOUNT_SRC="/etc/letsencrypt"
case "$CERTDIR" in
    /etc/letsencrypt/*) IN_CONT_DIR="/letsencrypt/${CERTDIR#/etc/letsencrypt/}" ;;
    *) MOUNT_SRC="$CERTDIR"; IN_CONT_DIR="/letsencrypt" ;;
esac
say "    mount  : $MOUNT_SRC -> /letsencrypt (ro)"
say "    in-ctr : $IN_CONT_DIR/fullchain.pem"

if [ "$MODE" = "check" ]; then
    hdr "Check only — nothing changed"
    say "Re-run without --check to apply."
    exit 0
fi

# -------------------------------------------------------------------- verify
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

# ------------------------------------------------------------------ rollback
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
    restart_grafana
    wait_for_grafana || die "grafana did not come back up"
    ok "reverted to the self-signed cert"
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

cat > "$OVERRIDE" <<EOF
# Generated by enable-grafana-tls.sh — do not edit by hand.
#
# Points orc-grafana at the host's Let's Encrypt cert so stakeholders reach
# the dashboard without a browser warning. Lives in an override rather than
# docker-compose.yml because the deploy rsync replaces docker-compose.yml
# and would silently revert the change.
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
      - $MOUNT_SRC:/letsencrypt:ro
EOF
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
say "    Grafana reads the cert once, at startup. After certbot renews,"
say "    it keeps serving the OLD cert until restarted."
if [ -d /etc/letsencrypt ]; then
    mkdir -p "$HOOK_DIR"
    cat > "$HOOK" <<EOF
#!/bin/sh
# Installed by enable-grafana-tls.sh. Grafana caches its cert at startup, so
# a renewal only takes effect after a restart. || true so a failure here can
# never fail the renewal itself.
docker restart $CONTAINER >/dev/null 2>&1 || true
EOF
    chmod 0755 "$HOOK"
    ok "installed deploy hook $HOOK"
else
    warn "no /etc/letsencrypt — install a restart hook wherever renewal runs:"
    warn "  docker restart $CONTAINER"
fi
say "    cert expires: $NOTAFTER"

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
