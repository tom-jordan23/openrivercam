#!/usr/bin/env python3
"""Seed the harness DB with a Sukabumi-shaped backlog: FAILED rows with files.

Mirrors the station's real state as measured 2026-09-02: rows whose sync_status
is FAILED, whose remote_id is NULL, and whose file exists on disk. 30 of them,
one every 30 minutes, so the ORDER the sync picks them up is legible from the
timestamps alone.
"""
import os, shutil, sqlite3, sys
from datetime import datetime, timedelta

TEMPLATE = "/tmp/tiny.mp4"   # a real 1-second mp4, made with ffmpeg
DB = sys.argv[1]
UPLOADS = sys.argv[2]
GATEWAY = sys.argv[3]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 30

con = sqlite3.connect(DB); cur = con.cursor()

# callback_url: point ORC-OS at the mock. retry_timeout 0.0 is what the station
# actually carries, which resolves to the 150 s ceiling in both code paths.
cur.execute("DELETE FROM callback_url")
# columns per the real schema: no user/password on this table in 0.6.0
cur.execute("""INSERT INTO callback_url
    (id, created_at, url, token_refresh_end_point, token_refresh, token_access,
     token_expiration, retry_timeout, remote_site_id)
    VALUES (1, ?, ?, '/api/token/refresh/', 'seed-refresh', 'seed-access',
            ?, 0.0, 4)""",
    (datetime.now().isoformat(),
     f"http://{GATEWAY}:8099",
     (datetime.now() - timedelta(hours=1)).isoformat()))   # expired -> forces a refresh

cur.execute("UPDATE settings SET active=1, enable_daemon=1, shutdown_after_task=1, "
            "sync_file=1, sync_image=0 WHERE id=1")
if cur.rowcount == 0:
    cur.execute("""INSERT INTO settings (id, created_at, parse_dates_from_file, video_file_fmt,
                   allowed_dt, shutdown_after_task, reboot_after, enable_daemon, sync_file,
                   sync_image, active)
                   VALUES (1, ?, 1, '{%Y%m%dT%H%M%S}.mp4', 3600.0, 1, 3600.0, 1, 1, 0, 1)""",
                (datetime.now().isoformat(),))

# A video with NO video_config can never sync: sync_remote builds its payload
# with self.video_config.remote_id and dies on AttributeError before any
# request is sent. Already SYNCED with a remote_id, so the sync path does not
# try to push the config itself first.
cur.execute("DELETE FROM video_config")
# rvec and tvec are NOT NULL JSON columns; zeros are fine, nothing here
# reprojects anything.
cur.execute("""INSERT INTO video_config (id, name, rvec, tvec, created_at, remote_id, sync_status)
               VALUES (1, 'harness-config', '[0.0,0.0,0.0]', '[0.0,0.0,0.0]', ?, 3, 'SYNCED')""",
            (datetime.now().isoformat(),))

cur.execute("DELETE FROM video")
base = datetime(2026, 8, 25, 0, 0, 0)
made = []
for i in range(N):
    ts = base + timedelta(minutes=30 * i)
    day = ts.strftime("%Y%m%d")
    name = ts.strftime("%Y%m%dT%H%M%S") + ".mp4"
    rel = f"videos/{day}/1/{name}"
    full = os.path.join(UPLOADS, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    # These must be DECODABLE, not merely present. A 4 KB block of zeros gets
    # as far as "There are N videos left to synchronize" and then dies in
    # cvtColor with "(-215:Assertion failed) !_src.empty()" - the sync path
    # opens the file. Size is still irrelevant: the mock, not the disk,
    # supplies the transfer time.
    shutil.copyfile(TEMPLATE, full)
    # Both enums are stored by NAME, not value. Writing the integer 4 here
    # yields LookupError("'4' is not among the defined enum values") the moment
    # SQLAlchemy hydrates the row - which is how the first run of this rig
    # failed, in the seed rather than in ORC-OS.
    cur.execute("""INSERT INTO video (timestamp, status, file, created_at, sync_status, video_config_id)
                   VALUES (?, 'DONE', ?, ?, 'FAILED', 1)""", (ts.isoformat(), rel, ts.isoformat()))
    made.append(name)

con.commit()
print(f"seeded {N} FAILED rows with files, {made[0]} .. {made[-1]}")
print("sync_status tally:", dict(cur.execute(
    "select sync_status, count(*) from video group by 1").fetchall()))
con.close()
