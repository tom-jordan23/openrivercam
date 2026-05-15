#!/bin/bash
# bootstrap-cert.sh — generate the self-signed cert for sensor-upload.
#
# Run this once on the server, then commit the resulting fullchain.pem to
# the repo (so Pi stations can pin against it). The private key NEVER
# leaves the server.
#
# Run from /opt/orc-additions/ (or wherever the docker-compose.yml lives).

set -euo pipefail

CERT_DIR="$(dirname "$0")/certs"
HOSTNAME="${HOSTNAME_OVERRIDE:-openrivercam.endlessprojects.info}"
DAYS=3650   # 10-year cert; we never renew (operator regenerates on rotation)

if [ -f "$CERT_DIR/fullchain.pem" ] || [ -f "$CERT_DIR/privkey.pem" ]; then
    echo "ERROR: cert already exists at $CERT_DIR/. Refusing to overwrite."
    echo "       To rotate, remove the existing files manually first."
    exit 1
fi

mkdir -p "$CERT_DIR"
chmod 0755 "$CERT_DIR"

echo "Generating 10-year self-signed cert for $HOSTNAME..."
openssl req -x509 -newkey rsa:4096 -nodes \
    -keyout "$CERT_DIR/privkey.pem" \
    -out    "$CERT_DIR/fullchain.pem" \
    -days   "$DAYS" \
    -subj   "/CN=$HOSTNAME" \
    -addext "subjectAltName=DNS:$HOSTNAME"

chmod 0644 "$CERT_DIR/fullchain.pem"
chmod 0600 "$CERT_DIR/privkey.pem"

echo
echo "Done. Files:"
ls -la "$CERT_DIR/"
echo
echo "Next steps:"
echo "  1. Copy $CERT_DIR/fullchain.pem into the repo at:"
echo "     spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem"
echo "  2. Commit + push the public cert. The private key stays on the server."
echo "  3. Bring up the container:"
echo "     sudo docker compose --env-file .env up -d --build"
