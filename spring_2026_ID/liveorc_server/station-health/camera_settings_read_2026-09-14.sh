set -u
echo "=== CAMERA SETTINGS READ $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Does the live camera run the image and streaming profiles the repo says it
# does? Asked 2026-09-14 after the transect-swap test (B) pointed at daytime
# lighting and camera settings rather than the transect. The repo's
# streaming_101.xml sets GovLength 50, yet mirrored clips carry a keyframe
# every 13 frames, so the repo cannot be assumed to describe the camera.
#
# READ-ONLY.
#   Station: cat, sha256sum, journalctl. Nothing is written.
#   Camera:  HTTP GET only, and only inside orc-capture's settle window, which
#            sits after the camera answers ping and before the profile switch
#            and the RTSP capture. No PUT, no POST. The password goes to curl on
#            stdin, never on the command line.
#
# Timing: the grab lands ~30 s into a wake. orc-capture powers the camera
# relay on at its start and off when capture finishes, so section C waits for
# ISAPI to answer and then reads three endpoints, a few seconds in total.

P=/home/pi/camera_profiles
echo
echo "=== A. profile-switch state and window ==="
echo "  state file: $(cat /var/lib/orc-camera/active-profile 2>&1)"
grep -E '^(NIGHT_START|NIGHT_END|DAY_PROFILE_PATH|NIGHT_PROFILE_PATH|RTSP_PATH|CAMERA_SETTLE_TIME|RELAY_MODE)=' /etc/orc-capture.conf 2>&1 | sed 's/^/  /'
echo "  --- deployed profile files (sha256) ---"
sha256sum $P/common/image.xml $P/profiles/profile-night/image.xml $P/common/streaming_101.xml /etc/orc-capture.conf /usr/local/bin/orc-capture /usr/local/bin/orc-camera-profile-switch 2>&1 | sed 's/^/  /'

echo
echo "=== B. profile-switch history in the retained journal ==="
journalctl --no-pager -o short-iso 2>/dev/null | grep -E 'orc-camera-profile-switch' \
  | grep -viE 'no change needed' | tail -25 | cut -c1-200 | sed 's/^/  /'
echo "  --- 'no change needed' lines, count: $(journalctl --no-pager 2>/dev/null | grep -c 'orc-camera-profile-switch.*no change needed')"
echo "  --- orc-capture warnings about the switch or enforcement ---"
journalctl --no-pager -o short-iso 2>/dev/null | grep -E 'orc-capture' | grep -iE 'profile-switch failed|enforce|WARN|ERROR' \
  | tail -10 | cut -c1-200 | sed 's/^/  /'

echo
echo "=== C. live camera settings, GET only ==="
IP=$(grep -E '^CAMERA_IP=' /etc/orc-capture.conf | cut -d= -f2 | awk '{print $1}')
PASS=$(bash -c 'for f in ~/.orc_deploy_*; do [ -f "$f" ] && . "$f"; done; printf %s "${CAMERA_PASS:-${BASE_PASSWD:-}}"' 2>/dev/null)
[ -n "$PASS" ] || echo "  no camera password found in ~/.orc_deploy_* — section C skipped"
get() { printf 'user = "admin:%s"\n' "$PASS" | curl -s -m 6 --digest -K - -w '\n__HTTP %{http_code}\n' "http://$IP$1"; }
if [ -n "$PASS" ]; then
  up=0
  for i in $(seq 1 45); do
    code=$(printf 'user = "admin:%s"\n' "$PASS" | curl -s -o /dev/null -m 3 --digest -K - -w '%{http_code}' "http://$IP/ISAPI/System/deviceInfo")
    if [ "$code" = "200" ]; then up=1; echo "  ISAPI answered after ~$((i*2))s of polling"; break; fi
    sleep 2
  done
  if [ "$up" = 1 ]; then
    for ep in /ISAPI/Image/channels/1 /ISAPI/Streaming/channels/101 /ISAPI/Image/channels/1/ircutFilter; do
      echo "  ##### GET $ep"
      get "$ep" | sed 's/^/    /'
    done
    echo "  ##### deviceInfo (model, firmware)"
    get /ISAPI/System/deviceInfo | grep -E 'model|firmwareVersion|firmwareReleasedDate|__HTTP' | sed 's/^/    /'
  else
    echo "  ISAPI did not answer within ~90 s (camera off or still booting)"
  fi
fi
unset PASS

echo
echo "=== D. the deployed profile XML bodies, for a local diff against the repo ==="
for f in $P/common/image.xml $P/profiles/profile-night/image.xml $P/common/streaming_101.xml; do
  echo "  ##### $f"; sed 's/^/    /' "$f" 2>&1
done
echo "=== END ==="
