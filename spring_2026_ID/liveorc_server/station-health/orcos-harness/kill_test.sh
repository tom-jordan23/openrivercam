#!/usr/bin/env bash
# Interruption test: does a batch cut off mid-flight recover by itself?
#
# Source says sync_remote sets the row to QUEUE *before* attempting the upload,
# "so that syncing may be re-attempted upon reboot". If that holds, clips killed
# in flight stay QUEUE and the next boot picks them up with no re-flip. That
# matters: ~45% of real wakes are cut short.
set -u
SP="$1"
say(){ printf '\n[%s] %s\n' "$(date -u +%H:%M:%S)" "$*"; }
dbq(){ docker exec orc-api python3 -c "
import sqlite3;con=sqlite3.connect('/app/data/orc-os.db')
print('   tally:', dict(con.execute('select sync_status,count(*) from video group by 1').fetchall()))
"; }

say "re-seed: 30 FAILED rows, remote_id NULL, clean slate"
docker exec orc-api python3 /tmp/seed.py /app/data/orc-os.db /app/data/uploads 172.19.0.1 30 >/dev/null 2>&1
docker exec orc-api python3 -c "
import sqlite3;con=sqlite3.connect('/app/data/orc-os.db')
rows=con.execute(\"select id from video where sync_status='FAILED' order by timestamp desc limit 12\").fetchall()
con.executemany('update video set sync_status=? where id=?',[('QUEUE',r[0]) for r in rows]);con.commit()
print('   flipped 12 newest to QUEUE')
"
: > "$SP/rig/mock.log"

say "boot"
docker restart orc-api >/dev/null 2>&1
say "waiting t+60 for the sync to start, then 30s of uploads (~5 clips)"
sleep 92

say "KILL - SIGKILL to PID 1, mid-batch"
docker kill orc-api >/dev/null 2>&1
say "uploads that completed before the kill:"
cat "$SP/rig/mock.log" | sed 's/^/   /'

say "state immediately after the kill (container down, DB on the volume)"
docker start orc-api >/dev/null 2>&1; sleep 6
docker exec orc-api python3 -c "
import sqlite3;con=sqlite3.connect('/app/data/orc-os.db')
print('   by sync_status:', dict(con.execute('select sync_status,count(*) from video group by 1').fetchall()))
print('   rows still QUEUE (should be the un-uploaded remainder):')
for r in con.execute(\"select id,timestamp,sync_status,remote_id from video where sync_status='QUEUE' order by timestamp desc\"):
    print('     ',r)
"

say "NOW: does the next boot retry them WITHOUT a re-flip?"
: > "$SP/rig/mock.log"
docker restart orc-api >/dev/null 2>&1
sleep 130
say "uploads on the boot after the kill (no re-flip was done):"
cat "$SP/rig/mock.log" | sed 's/^/   /'
say "final state"
docker exec orc-api python3 -c "
import sqlite3;con=sqlite3.connect('/app/data/orc-os.db')
print('   by sync_status:', dict(con.execute('select sync_status,count(*) from video group by 1').fetchall()))
"
