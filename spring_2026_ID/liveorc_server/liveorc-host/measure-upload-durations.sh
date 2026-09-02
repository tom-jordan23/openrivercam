#!/usr/bin/env bash
# measure-upload-durations.sh — what does a real video upload cost, measured
# from the server end?
#
# WHY THIS EXISTS
#   The record has claimed 5.2-5.5 s for a 9.2 MB clip (~1.74 MB/s) since
#   2026-09-01, and every throughput estimate rests on it - including the
#   five-day upload projection for the 10.69 GB backlog. Tracing it on
#   2026-09-02 found no derivation anywhere: not in the commit that introduced
#   it, not in any of the 40 grabs under data/station-forensics/. It appears as
#   an assertion.
#
#   A station-side probe on 2026-09-02 measured ~167 KB/s - ten times slower,
#   which would put a 9.2 MB clip at ~54 s rather than 5.2 s. That is one
#   sample from one wake, on :8443 to the sensor-upload service rather than the
#   real video path, so it should not overturn the record on its own.
#
#   This is the independent check, and it costs no metered bytes: the server
#   already logged the 37 video POSTs that SUCCEEDED. If nginx records
#   $request_time, those are real durations for the real endpoint over the real
#   link - the exact number in dispute, measured from the other end.
#
# WHAT IT DEPENDS ON
#   Whether the log format carries $request_time at all. The default `combined`
#   format does NOT. Section A prints the format first, so a null result is
#   read as "not recorded" rather than "no delay" - the first pass of
#   diagnose-sync-failures.sh made exactly that mistake with the empty log
#   files, and the correction is worth not repeating.
#
#   nginx logs to stdout in this container, so the history is in
#   `docker logs liveorc_webapp`, NOT /var/log/nginx (those files are zero
#   bytes, dated the image build).
#
# READ-ONLY. Nothing is changed, nothing restarted.
set -u
W=liveorc_webapp
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "0. IS sensor-upload ACTUALLY ANSWERING? — do this one first"
# Added after wake 3, and it may invalidate everything measured from the
# station. Across three wakes, 17 PUTs to :8443, time_starttransfer was
# 0.000000 EVERY time - not one response byte has ever come back. TLS
# terminates fine (uvicorn answers the handshake), the body goes out, and then
# nothing returns.
#
# A wedged application behind a working TLS listener produces exactly that
# signature. If sensor-upload is hung, then all 17 "link failures" are an
# artifact of probing a dead service and say nothing about Telkomsel at all.
# This has to be excluded before any of the station numbers are written up.
echo "  --- is the container up, and how long has it been up ---"
$D ps --filter name=orc-sensor-upload --format "  {{.Names}}  {{.Status}}  {{.Ports}}" 2>&1
echo "  --- does it answer its OWN health endpoint, from the host ---"
curl -sk --max-time 10 -w "\n  http=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n" \
     https://localhost:8443/sensors/health 2>&1 | sed 's/^/  /'
echo "  (a prompt {\"ok\":true,...} here means the service is FINE and the fault"
echo "   is on the link. A hang or empty reply means I have been probing a wedged"
echo "   service for three wakes and the station numbers must be discarded.)"
echo "  --- recent log activity: has it served anything lately ---"
$D logs --tail 15 orc-sensor-upload 2>&1 | sed 's/^/  /'
echo "  --- and a local PUT of 64 KB, the size that failed from the station ---"
head -c 65536 /dev/urandom > /tmp/hostprobe.bin
echo "  (unauthenticated on purpose: a prompt 401 still proves the app RESPONDS)"
curl -sk --max-time 15 -T /tmp/hostprobe.bin -H "Expect:" \
     -w "\n  http=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n" \
     https://localhost:8443/sensors/upload/sukabumi/hostprobe.bin 2>&1 | sed 's/^/  /'
rm -f /tmp/hostprobe.bin

h "A. does the log format record a duration at all"
$D exec $W sh -c 'nginx -T 2>/dev/null | grep -nE "log_format|access_log"' 2>&1 | sed 's/^/  /' | head -20
echo
echo "  Look for \$request_time (total, client-visible) and \$upstream_response_time."
echo "  If NEITHER appears, durations were never recorded and sections C/D will be"
echo "  empty - that is 'not measured', NOT 'fast'. Section E is then the fallback."

h "B. the successful video POSTs, newest 40"
echo "  (201 = created. These are the uploads that worked.)"
$D logs $W 2>&1 | grep -E "POST /api/video/" | grep -E " 201 " | tail -40 | sed 's/^/  /'

h "C. duration distribution, IF the format carries one"
# Pull the last whitespace-delimited float that looks like seconds. Only
# meaningful when section A showed a time variable in the format.
$D logs $W 2>&1 | grep -E "POST /api/video/" | grep -E " 201 " \
  | grep -oE "[0-9]+\.[0-9]{3}" | sort -n \
  | awk '{v[NR]=$1; s+=$1}
         END{if(NR==0){print "  no duration-shaped field found in the 201 lines";exit}
             printf "  n=%d  min=%.3f  median=%.3f  p90=%.3f  max=%.3f  mean=%.3f\n",
                    NR, v[1], v[int(NR*0.5)+0<1?1:int(NR*0.5)], v[int(NR*0.9)<1?1:int(NR*0.9)], v[NR], s/NR}'

h "D. implied throughput at 9.2 MB per clip"
echo "  If C gave a median of T seconds, throughput is 9.2/T MB/s."
echo "    T = 5.3 s  -> 1.74 MB/s   (what the record claims)"
echo "    T = 54  s  -> 0.17 MB/s   (what the station probe measured)"
echo "  These differ by 10x. C decides which describes the real video path."

h "E. fallback if no duration is logged: request SIZE and arrival spacing"
echo "  --- body bytes received per POST, if \$request_length is in the format ---"
$D exec $W sh -c 'nginx -T 2>/dev/null | grep -E "request_length|body_bytes"' 2>&1 | sed 's/^/  /' | head -5
echo "  --- arrival timestamps of consecutive 201s (spacing bounds duration ---"
echo "      from above: a clip cannot take longer than the gap to the next one) ---"
$D logs $W -t 2>&1 | grep -E "POST /api/video/" | grep -E " 201 " | tail -15 \
  | awk '{print $1}' | sed 's/^/  /'

h "F. did ANY of the station probe bytes arrive on :8443"
# The 2026-09-02 probes PUT 2-3 MB to sensor-upload twelve times. All twelve
# failed from the station's side: curl reported the full body written, then a
# reset with no response byte. Whether the BYTES arrived is not knowable from
# the station - only this service knows. It logs "upload ok station=... size=N"
# on every completed write, so a hit here means the transfer completed and only
# the response was lost; silence means it never finished.
echo "  --- sensor-upload log lines mentioning the probe files ---"
$D logs orc-sensor-upload 2>&1 | grep -iE "linkprobe" | tail -20 | sed 's/^/  /'
echo "  (silence = no probe transfer ever completed server-side)"
echo "  --- for contrast, the last few REAL sensor CSV uploads (these are KB, not MB) ---"
$D logs orc-sensor-upload 2>&1 | grep -E "upload ok" | tail -8 | sed 's/^/  /'
echo "  (if small CSVs succeed while every multi-MB PUT fails, the fault scales"
echo "   with transfer size or duration, not with port, host or address family.)"
echo "  --- any probe leftovers on disk ---"
ls -la /var/orc/sensors/sukabumi/ 2>/dev/null | grep -iE "linkprobe|total" | sed 's/^/  /'
echo "  (delete any linkprobe-*.bin found; they are inert but they are litter)"

h "G. THE TENSION THIS MUST RESOLVE"
echo "  The record says 37 clips of ~9.2 MB synced successfully on 09-01/09-02."
echo "  Twelve probe transfers of 2-3 MB on :8443 failed in the same period."
echo "  Both cannot describe one link. Either the real video path on :443"
echo "  behaves differently from :8443 for large bodies, or those 37 did not"
echo "  move 9.2 MB each. Sections C and E decide it - and if the format has"
echo "  \$request_length, that is the direct answer: it is the body size nginx"
echo "  actually received per POST."

h "H. sanity: is the 37-in-2-days figure still what the log holds"
echo -n "  201s on /api/video/ in the whole retained log: "
$D logs $W 2>&1 | grep -E "POST /api/video/" | grep -cE " 201 "
echo -n "  500s on /api/video/: "
$D logs $W 2>&1 | grep -E "POST /api/video/" | grep -cE " 500 "
echo
echo "== END =="
