# LiveORC media volume — incident and migration runbook

**Incident date:** 2026-08-10
**Instance:** `i-01d5ccd8c3d4a3858` (`LiveORC-Server`, t3.large, us-east-1c)

Moving LiveORC's `MEDIA_ROOT` off the container's ephemeral writable layer
and onto a dedicated EBS volume, after that layer filled the root disk and
took the whole host down.

## What happened

The root filesystem hit 100%. Every symptom traced back to that one fact,
but none of them said so:

| Symptom | Actual cause |
|---|---|
| Session Manager: `Plugin with name Standard_Stream not found` | agent couldn't write its session plugin working files |
| Run Command: exit 1, `Output(0)`, `Error(0)`, instant | agent couldn't write the script or its stdout/stderr files |
| LiveORC down | `mnt-s3-storage.mount` failed → `liveorc.service` dependency failed |
| `mnt-s3-storage.mount` failed | `s3fs: There is no enough disk space for used as cache` |
| CPU pinned ~98% for a week | LiveORC/celery retrying failed writes |
| `growpart` never expanded the volume after resize | cloud-init died with `OSError: [Errno 28] No space left on device` |

The empty-output Run Command failure is the useful signature: a command
that reaches the agent, returns exit 1 instantly, and produces zero bytes on
**both** streams has not run at all — the agent could not write it to disk.

## Root cause

`MEDIA_ROOT` is `/liveorc/media` (`LiveORC/settings.py:126`,
`os.path.join(BASE_DIR, 'media')` with `BASE_DIR=/liveorc`).

Nothing was mounted there. The compose bind pointed at
`/liveorc/data/media` — a path Django never writes to:

```yaml
- ${LORC_STORAGE_DIR}:/liveorc/data/media:z     # wrong target
```

So every upload landed in the container's **writable layer**: 26 GB of
`videos/`, 1.3 GB of `keyframe/`, 9.5 MB of `thumb/`, accumulated from
2026-05-14 to 2026-07-29 until the 50 GB root volume was exhausted.
`liveorc_webapp` was then SIGKILLed (exit 137).

The mismatch is the residue of an **abandoned S3 migration**: `.env` still
declares `LORC_STORAGE_DIR=lorc_media` (the named volume from the original
design) while the *running* container carried a `/mnt/s3-storage` bind from
the attempt. The mount was left pointing somewhere harmless instead of being
removed, so it looked inert — and was, which is exactly why nobody noticed
that media had nowhere to go.

**This was silent.** No error was ever raised. Writes succeeded; they just
went somewhere with no persistence, no backup, and a hard ceiling.

### Two latent landmines this exposed

1. **`REPROCESS_RUNBOOK.md` claimed a media backup was unnecessary** because
   "the video bytes live in MinIO/S3, not Postgres". They did not. Any
   `docker compose up --force-recreate` during the reprocess work would have
   destroyed 26 GB of video with no backup and no warning.
2. **Nothing guarded the mount.** `liveorc.service` required the *s3fs*
   mount but not a mount at `MEDIA_ROOT`, so the one condition that actually
   mattered went unchecked.

## Why EBS and not S3

S3 was tried first and abandoned. Two independent blockers, both still valid:

- **LiveORC's storage backend is all-or-nothing.** There is no mode where
  only media bytes go to S3 — the whole stack moves or nothing does.
  Prod runs `FileSystemStorage` (see commit `3889bf3`), and the reprocess
  toolkit depends on it: `prod_reprocess.sh` execs inside the webapp
  specifically so it reads the *local* media volume.
- **Cross-filesystem operations.** `rename(2)` and `link(2)` fail with
  `EXDEV` across a mount boundary. s3fs additionally has no hardlink support
  at all and implements rename as copy-and-delete.

The second constraint applies to **any** mount at `/liveorc/media`,
including EBS — see Phase 0 and Phase 5b below. It is a boundary problem,
not an S3 problem; EBS only avoids the missing-primitive half of it.

## Target layout

```
EBS gp3 150 GiB → /var/lib/liveorc-media → bind → /liveorc/media   (MEDIA_ROOT)
s3://openrivercam-video/backups/                                    (DB backups; never mounted)
```

Media growth is ~10 GB/month, so 150 GiB is roughly a year of headroom.
EBS grows online (up to four modifications per volume per rolling 24 h since
January 2026 — the old 6-hour cooldown is gone).

Keeping backups in S3 *unmounted* is deliberate: anything mounted at
`MEDIA_ROOT` is inside Django's media tree, and `nginx` serves
`/media/admin-interface` directly from it.

## Migration

### Phase 0 — Pre-flight

```bash
IMG=$(sudo docker inspect liveorc_webapp --format '{{.Config.Image}}')
UPPER=$(sudo docker inspect liveorc_webapp --format '{{.GraphDriver.Data.UpperDir}}')

# Which operations cross the mount boundary? Decides whether 5b is needed.
sudo docker run --rm --entrypoint bash "$IMG" -lc '
  grep -rn "os\.rename\|os\.link\|os\.replace\|shutil\.move" /liveorc --include=*.py \
    | grep -v site-packages | head -20
  echo "=== temp dir ==="
  grep -rn "FILE_UPLOAD_TEMP_DIR" /liveorc --include=*.py | grep -v site-packages | head'

systemctl cat liveorc.service --no-pager
sudo docker run --rm --entrypoint bash "$IMG" -lc 'ls -la /liveorc/media/ 2>/dev/null'
```

Interpreting the first command:

- **Only Django's storage layer** — `file_move_safe()` already falls back to
  a streaming copy on `EXDEV`. Safe; skip 5b.
- **`os.rename`/`shutil.move` from a temp dir into `MEDIA_ROOT`** — point
  that temp dir at the same volume (`FILE_UPLOAD_TEMP_DIR`). Skip 5b.
- **`os.link` into `MEDIA_ROOT`** — hardlinks cannot cross filesystems and
  have no fallback. Do 5b.

### Phase 1 — DB backup

```bash
cd /opt/LiveORC && sudo docker compose up -d db
cd ~/openrivercam/spring_2026_ID/liveorc_server/reprocess
sudo ./backup_liveorc_db.sh
aws s3 sync ./liveorc-backups/ s3://openrivercam-video/backups/
```

The database is not at risk — `db` uses named volume `liveorc_lorc_data` and
is untouched — but it is 1.6 MB and it is the rollback if the recreate
misbehaves.

### Phase 2 — Create and attach

Console → EC2 → Volumes → **Create volume**: gp3, **150 GiB**,
**us-east-1c** (must match the instance; EBS cannot cross AZs), tag
`Name=liveorc-media`. Then **Attach volume** → `i-01d5ccd8c3d4a3858`,
device `/dev/sdf`.

### Phase 3 — Format and mount

```bash
lsblk       # STOP. Confirm the ~150G empty disk (likely nvme1n1).
            # nvme0n1 is 80G and holds /. mkfs on the wrong one is unrecoverable.

sudo mkfs.ext4 -L liveorc-media /dev/nvme1n1
sudo mkdir -p /var/lib/liveorc-media
echo 'LABEL=liveorc-media /var/lib/liveorc-media ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
sudo mount -a
findmnt /var/lib/liveorc-media
```

`LABEL=` because NVMe device numbering is not stable across reboots.
`nofail` so a missing volume cannot wedge the boot.

### Phase 4 — Seed and copy

```bash
# Only if Phase 0 showed content shipped at /liveorc/media (e.g. admin-interface):
CID=$(sudo docker create "$IMG")
sudo docker cp "$CID:/liveorc/media/." /var/lib/liveorc-media/
sudo docker rm "$CID"

sudo rsync -aHAX --info=progress2 "$UPPER/liveorc/media/" /var/lib/liveorc-media/
```

Mounting over `/liveorc/media` masks anything the image ships there, which is
why the seed step comes first.

### Phase 5 — Verify (gate)

```bash
sudo find "$UPPER/liveorc/media" -type f | wc -l
sudo find /var/lib/liveorc-media -type f -not -path '*/admin-interface/*' | wc -l
sudo du -sb "$UPPER/liveorc/media" /var/lib/liveorc-media
sudo rsync -aHAXn --itemize-changes "$UPPER/liveorc/media/" /var/lib/liveorc-media/ | head
```

An empty `--itemize-changes` means every file is present at the right size,
mtime, and permissions. Then snapshot the volume — this is the media backup
the old runbook wrongly assumed already existed.

#### Phase 5b — only if Phase 0 found `os.link` into `MEDIA_ROOT`

`/liveorc/data` must share the filesystem with `/liveorc/media`:

```bash
sudo mkdir -p /var/lib/liveorc-media/{media,data}
sudo mv /var/lib/liveorc-media/{videos,keyframe,thumb} /var/lib/liveorc-media/media/
DATAVOL=$(sudo docker inspect liveorc_webapp \
  --format '{{range .Mounts}}{{if eq .Destination "/liveorc/data"}}{{.Source}}{{end}}{{end}}')
sudo rsync -aHAX "$DATAVOL/" /var/lib/liveorc-media/data/
```

Then bind both paths in Phase 6 instead of one.

### Phase 6 — Repoint ⚠️ point of no return

Recreating the container **deletes the 28.6 GB writable layer**. Only proceed
once Phase 5 passed.

```
/opt/LiveORC/.env          LORC_STORAGE_DIR=/var/lib/liveorc-media
/opt/LiveORC/compose       - ${LORC_STORAGE_DIR}:/liveorc/media:z
liveorc.service            RequiresMountsFor=/var/lib/liveorc-media
```

```bash
sudo systemctl disable --now 'mnt-s3\x2dstorage.mount'
sudo systemctl daemon-reload
```

**Keep the mount dependency.** LiveORC should refuse to start when its media
volume is absent. That guard is precisely what was missing, and its absence
is why ten weeks of uploads went into a container layer without one error.

Do **not** pass `--renew-anon-volumes` — the webapp's `/liveorc/data`
anonymous volume must be carried across, and `docker compose up` reuses it by
default. A manual `docker rm` followed by `up` would orphan it.

### Phase 7 — Recreate and verify

```bash
cd /opt/LiveORC && sudo docker compose up -d
sudo docker ps -as --format '{{.Names}}\t{{.Status}}\t{{.Size}}'
df -h / /var/lib/liveorc-media
sudo docker exec liveorc_webapp ls /liveorc/media/videos | head
```

Expect `liveorc_webapp` in MB not GB, `/` at roughly 20 GB of 77 GB, and
`/var/lib/liveorc-media` around 26 GB.

Then open an existing video in the UI (proves stored paths resolve) and
upload a new one (proves writes land on the volume), watching for `EXDEV`:

```bash
sudo docker logs -f liveorc_webapp 2>&1 | grep -i "errno 18\|cross-device\|EXDEV"
```

### Phase 8 — Confirm the divergence

```bash
df -h /                              # flat as uploads arrive
sudo du -sh /var/lib/liveorc-media   # grows instead
```

That divergence is the whole point: media growth can no longer reach root.

## Root volume repair (already done, recorded for reference)

The root volume was grown 50 → 80 GiB, but the partition and filesystem were
not: cloud-init's `growpart` runs at boot and had died with `ENOSPC`. With a
disk that full the automatic path cannot work, so it was done by hand:

```bash
sudo growpart /dev/nvme0n1 1
sudo resize2fs /dev/nvme0n1p1
```

`/` went from 48 G/100% to 77 G/62%. Both are safe online on a mounted ext4
root. If a full disk ever blocks `growpart` again, free ~1 GB first
(`journalctl --vacuum-size=200M`, `apt-get clean`) so it has scratch space.

## Follow-ups

- [ ] Disk-space alarm on `/`. Its absence is why this ran for ten weeks.
      Needs the CloudWatch agent (EC2 metrics do not cover EBS disk usage) or
      a cron check.
- [ ] Correct `REPROCESS_RUNBOOK.md` — "the video bytes live in MinIO/S3" is
      false for this deployment, and it made "no media backup needed" unsafe.
- [ ] Document the media volume and the `RequiresMountsFor` guard in
      `README.md`.
- [ ] Snapshot schedule for the media volume (DLM lifecycle policy).
- [ ] Decide retention for `s3://openrivercam-video/orc_site4.tgz` (642 MB,
      2026-06-08).
