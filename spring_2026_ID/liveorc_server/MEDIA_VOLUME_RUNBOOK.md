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

## ⚠️ Until this migration runs: do not let systemd start LiveORC

`liveorc.service` → `start-liveorc.sh` → `liveorc.sh start` → `docker
compose up -d`, which **recreates `liveorc_webapp` and destroys the 26 GB in
its writable layer.** The unit is `WantedBy=multi-user.target`, so a plain
reboot is enough to trigger it.

While the media still lives in the container layer:

```bash
sudo systemctl disable liveorc.service   # survives reboot; does not stop what is running
sudo docker start db rabbitmq liveorc_webapp   # the safe way to bring LiveORC up
```

`docker start` reuses the existing container and its layer. `docker compose
up`, `--force-recreate`, `docker rm`, and `docker system prune` all destroy
it. Re-enable the unit in Phase 6, once media is on the EBS volume and a
recreate is harmless.

Take an EBS snapshot of the **root** volume before any of this — the 26 GB
exists in exactly one place, and that is the only thing standing between a
stray command and permanent loss.

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

#### Result — run 2026-08-10 on `localdevices/liveorc`

| Check | Result | Consequence |
|---|---|---|
| `os.link` / `os.rename` / `os.replace` / `shutil.move` in app code | **none** | **Skip 5b.** `/liveorc/data` stays on `/`. Only Django's `file_move_safe()` crosses the boundary, and it falls back to a copy on `EXDEV`. |
| `FILE_UPLOAD_TEMP_DIR` | **unset** | Uploads use the system temp dir and cross the boundary via that same fallback. No action. |
| Image content at `/liveorc/media` | **`admin-interface/`** | **Phase 4's seed step is mandatory.** The bind mount masks it, and nginx serves `/media/admin-interface` directly — skipping the seed breaks the Django admin theme with no error in the app log. |
| `liveorc.service` | **five separate s3fs couplings** | Phase 6 rewrites all of them; see there. |

`UPPER` for this migration:
`/var/lib/docker/overlay2/6e92d3cd47b783469b9cdbb914011237b65d1880394a86f2f92ea57a6c89048f/diff`

#### Result — the three Phase 6 inputs, read 2026-08-17

```bash
cat /opt/LiveORC/start-liveorc.sh
cat /usr/local/bin/verify-s3mount.sh
grep -rn "s3-storage" /opt/LiveORC/ /etc/systemd/system/ 2>/dev/null
```

| File | Finding | Consequence for Phase 6 |
|---|---|---|
| `start-liveorc.sh` | `./liveorc.sh start --hostname … --port 8000 --ssl --storage-local --storage-dir /mnt/s3-storage --detached` | Confirms `--storage-dir` is the control point. It is a **local wrapper, not upstream**, so editing it does not fight a LiveORC upgrade. |
| `verify-s3mount.sh` | `mountpoint -q` **plus a write test** (`touch .test`) | **Rewrite, do not drop.** The write test catches a mount that is present but read-only — which `AssertPathIsMountPoint` does not. Rename it too; a file called `verify-s3mount.sh` guarding an EBS volume is the same naming rot that hid the original misconfiguration. |
| `grep -rn "s3-storage"` | 3 files, 5 hits | **The grep undercounts.** `After=` and `Requires=` name the unit as `mnt-s3\x2dstorage.mount` — systemd-escaped, so the literal `s3-storage` does not match. Using this grep as the checklist leaves two dependencies pointed at a dead mount. Use `grep -n 's3' /etc/systemd/system/liveorc.service` instead. |

`--ssl` also explains the TLS cert in the writable layer: `liveorc.sh` runs
certbot for `--hostname` at container start. The recreate re-obtains it, so
the cert is **not** a storage risk and Phase 6 needs nothing for it. Only
caveat: Let's Encrypt allows 5 duplicate certs per week, so repeated
recreates while debugging can exhaust it.

**Closed 2026-08-17.** That grep was run: `liveorc.sh` builds an explicit
`-f` list (lines 313–418), so `docker-compose.override.yml` is never
auto-loaded and the destination fix has to be made in `docker-compose.yml`
itself. Nothing about Phase 6 is still undetermined — see "Upgrade-safety:
an override file will NOT work here" under Phase 6 for the finding and its
consequence.

### Phase 1 — DB backup

`db` is already running, so **skip the `docker compose up -d db`** an earlier
draft of this runbook called for. Every `docker compose` command against
`/opt/LiveORC` is an avoidable risk while media is still in the writable layer;
the only one that should run is Phase 7's, and that goes through systemd.

```bash
cd ~/code/git/openrivercam/spring_2026_ID/liveorc_server/reprocess
sudo ./backup_liveorc_db.sh
aws s3 sync ./liveorc-backups/ s3://openrivercam-video/backups/
```

The database is not at risk — `db` uses named volume `liveorc_lorc_data` and
is untouched — but it is 1.6 MB and it is the rollback if the recreate
misbehaves.

#### Result — run 2026-08-27

Pre-flight first: `liveorc_webapp`'s `UpperDir` still matched the hash recorded
on 2026-08-10, so the writable layer holding the media had never been recreated.
`liveorc.service` `disabled`/`inactive` with the containers up — correct, they
were started by hand. All seven containers showed `Up 45 hours` (a reboot or
daemon restart around 2026-08-25): Docker restarted them under
`unless-stopped` and the writable layer survived. **A restart is not a
recreate**, and the disabled unit is why nothing ran `compose up`.

`/` had grown 48 G/62% → **51 G/66%** since the root repair. That ~3 GB is the
resumed Sukabumi uploads still landing in the container layer.

Backup `20260827-125253`, PostgreSQL 16.4:

| | |
|---|---|
| `api_timeseries` rows | **3488** |
| `api_video` rows | **3189** |
| `api_timeseries.csv` | 678477 B — `317e4bf5957e9ae1` |
| `api_timeseries.sql` | 699396 B — `3bb0c16e074bc681` |
| `api_video.csv` | 217786 B — `19efa62e2abccaca` |
| `liveorc_full.dump` | 474464 B — `09f3fa5d684d3a66` |

**`s3://openrivercam-video/backups/` was empty before this sync.** The three
earlier backups (`20260626-161006`, `20260629-141301`, `20260701-134258`) had
existed only on the host — the same instance disk this migration exists to stop
depending on. All four are now in S3.

`manifest.txt` reports its own size as 488 B while S3 shows 531 B. Not
corruption: the `stat`/`sha256sum` loop runs inside the redirect that writes the
file, so the manifest's line about itself describes a partially-written file.
Every other row is trustworthy; the `manifest.txt` row is not, and cannot be.

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
# REQUIRED — Phase 0 confirmed the image ships /liveorc/media/admin-interface.
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

#### Result — Phases 3–5 run 2026-08-27

Volume `liveorc-media`, 150 GiB gp3, us-east-1c, attached to
`i-01d5ccd8c3d4a3858` as `/dev/sdf`, surfacing as `/dev/nvme1n1`.
ext4 UUID **`158ee1aa-a1b6-4146-a6cd-a446955bd6c7`**. `fstab` mounts it by
`LABEL=liveorc-media`, and `daemon-reload` generated
`var-lib-liveorc\x2dmedia.mount` — loaded, active, exactly the escaped name
Phase 6 expects.

The old s3fs line in `/etc/fstab` is **commented out**. So the
`mnt-s3\x2dstorage.mount` unit that `liveorc.service` still requires is a
standalone unit file, not fstab-generated — Phase 6's retirement has to target
the unit, and the already-commented fstab line is not sufficient.

Copy: seed first (25.6 kB of `admin-interface`), then 32,189,265,846 B in
9,775 files at 125 MB/s, 4m04s.

| Check | Source (writable layer) | Destination (volume) |
|---|---|---|
| files | 9775 | 9775 |
| bytes | 32,189,265,846 | 32,189,286,505 |
| `rsync -n --itemize-changes` | **empty — PASS** | |

Destination exceeds source by 20,659 B: the seeded `admin-interface`, which
exists only there by design.

**Media had grown 26 GB → 31 GB** since the 2026-08-10 incident, and the host
carried **2643 mp4s against the mirror's 2630** — 13 videos uploaded after the
TODO-114 pull on 08-25. The gate is unaffected (all 9775 files copied), but the
independent mirror now covers 2630 of 2643 videos, and uploads are demonstrably
still arriving. Anything landing in the writable layer between this gate and
Phase 7 is deleted by the recreate while its DB row survives.

#### Phase 5b — ~~NOT NEEDED~~ (Phase 0, 2026-08-10)

Phase 0 found no `os.link` anywhere in the application code, so
`/liveorc/data` may stay on the root filesystem and the layout below is
**not** used. Retained only in case a future image adds hardlinking.

<details><summary>Unused: collapse /liveorc/data onto the media volume</summary>

`/liveorc/data` must share the filesystem with `/liveorc/media`:

```bash
sudo mkdir -p /var/lib/liveorc-media/{media,data}
sudo mv /var/lib/liveorc-media/{videos,keyframe,thumb} /var/lib/liveorc-media/media/
DATAVOL=$(sudo docker inspect liveorc_webapp \
  --format '{{range .Mounts}}{{if eq .Destination "/liveorc/data"}}{{.Source}}{{end}}{{end}}')
sudo rsync -aHAX "$DATAVOL/" /var/lib/liveorc-media/data/
```

Then bind both paths in Phase 6 instead of one.

</details>

### Phase 6 — Repoint (edits only — nothing restarts)

Every change here is a file edit. Nothing is recreated and nothing is
destroyed, so this phase is reversible and can be reviewed before committing to
Phase 7. **Phase 7 is the point of no return** — that is where the container is
recreated and the 28.6 GB writable layer is deleted. Do not run Phase 7 until
Phase 5's `--itemize-changes` came back empty and the media-volume snapshot
completed.

```
/opt/LiveORC/start-liveorc.sh   --storage-dir /var/lib/liveorc-media   ← the real control point
/opt/LiveORC/compose            - ${LORC_STORAGE_DIR}:/liveorc/media:z
/opt/LiveORC/.env               LORC_STORAGE_DIR=/var/lib/liveorc-media  (belt-and-braces only)
```

**`start-liveorc.sh` is what actually sets the storage dir**, by passing
`--storage-local --storage-dir /mnt/s3-storage` to `liveorc.sh` on the
command line. That overrides `.env`, which is why `.env` reads
`LORC_STORAGE_DIR=lorc_media` (a named volume) while the running container
carries a `/mnt/s3-storage` bind. Editing `.env` alone changes nothing.

#### ⚠️ Both halves of the path must change, or this migration is a no-op

`--storage-dir` sets the **source** of the bind. The compose file sets its
**destination**, and that destination is the bug:

```
      source                          destination
--storage-dir /mnt/s3-storage   →   /liveorc/data/media    ← Django never writes here
                                    /liveorc/media         ← MEDIA_ROOT, where it must go
```

Repoint `--storage-dir` at the EBS volume and nothing else, and the migration
completes cleanly, verifies green, and **media still accumulates in the
writable layer** — the volume is faithfully bound to a directory nothing
uses. The failure is silent, exactly as the original was.

Checklist for Phase 6, both required:

- [ ] `start-liveorc.sh`: `--storage-dir /mnt/s3-storage` → `/var/lib/liveorc-media`
- [ ] compose bind: `${LORC_STORAGE_DIR}:/liveorc/data/media:z` → `${LORC_STORAGE_DIR}:/liveorc/media:z`

```bash
# 1. source — local wrapper, safe to edit
sudo sed -i 's#--storage-dir /mnt/s3-storage#--storage-dir /var/lib/liveorc-media#' \
    /opt/LiveORC/start-liveorc.sh

# 2. destination — upstream file, the actual bug. Keep the original for diffing
#    against whatever a future upgrade ships.
sudo cp /opt/LiveORC/docker-compose.yml /opt/LiveORC/docker-compose.yml.orig
sudo sed -i 's#:/liveorc/data/media:z#:/liveorc/media:z#' /opt/LiveORC/docker-compose.yml

grep -n storage-dir      /opt/LiveORC/start-liveorc.sh
grep -n LORC_STORAGE_DIR /opt/LiveORC/docker-compose.yml
```

Verify in the *running* container before declaring success — the source of
truth is the mount table, not the config:

```bash
sudo docker inspect liveorc_webapp \
  --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' \
  | grep media          # must show /var/lib/liveorc-media -> /liveorc/media
```

#### Upgrade-safety: an override file will NOT work here

Settled 2026-08-17. `liveorc.sh` builds an **explicit `-f` list**:

```
liveorc.sh:313   command="docker compose -f docker-compose.yml"
liveorc.sh:324   command+=" -f docker-compose.rabbitmq.yml"
liveorc.sh:390   command+=" -f docker-compose.s3.yml"
liveorc.sh:402   command+=" -f docker-compose.postgis.yml"
liveorc.sh:418   command+=" -f docker-compose.ssl.yml"
```

Compose auto-loads `docker-compose.override.yml` **only when no `-f` is
given**, so an override file here is silently ignored. The destination fix has
to be made in `/opt/LiveORC/docker-compose.yml` itself, which is upstream-owned
and will be reverted by a LiveORC upgrade — silently, sending media straight
back to the writable layer.

`start-liveorc.sh` is a **local wrapper, not upstream**, so the durable defense
goes there. See "Guards" in Phase 6.

#### Ownership, confirmed from the host 2026-08-27

`/opt/LiveORC` is a **git checkout of `localdevices/LiveORC`**, so ownership is
checkable rather than inferred:

| Path | `git -C /opt/LiveORC` says | Ours? |
|---|---|---|
| `start-liveorc.sh` | `??` untracked | **ours** |
| `docker-compose.yml` | tracked | upstream |
| `.env` | tracked, and already ` M` modified | upstream, long since edited locally |
| any `*.service` | not tracked at all | **ours** |
| `/usr/local/bin/verify-*.sh` | outside the checkout | **ours** |

**"An upgrade reverts it *silently*" was wrong.** `liveorc.sh` has no upgrade
subcommand — `git pull|fetch|checkout|reset|upgrade)` matches nothing in it — so
an upgrade is a hand-run `git pull`. Against a modified tracked file, `git pull`
**aborts** ("Your local changes would be overwritten by merge"); it does not
quietly overwrite. The edit also stays permanently visible in `git status`.
A silent revert requires someone to force it (`git reset --hard`,
`git checkout .`). Guard 1 is the backstop for that case, not the only defense.

`.env` being already modified means a `git pull` would halt on it first,
regardless of what we do to `docker-compose.yml`.

**No env-var escape hatch.** Checked in the image: `settings.py:126` is
`MEDIA_ROOT = os.path.join(BASE_DIR, 'media')` — hardcoded, no environment
override. `MEDIA_ROOT` cannot be moved to meet the existing bind, so changing
the bind destination in upstream's `docker-compose.yml` is the only route.

The full confirmed chain, matching what `docker inspect` shows on the running
container:

```
--storage-dir /mnt/s3-storage → LORC_STORAGE_DIR → docker-compose.yml:8
                                ${LORC_STORAGE_DIR}:/liveorc/data/media:z
```

`.env`'s `LORC_STORAGE_DIR=lorc_media` is dead text — `--storage-dir` overrides
it. Leave it alone. Do not touch `docker-compose.s3.yml` (its
`${LORC_STORAGE_DIR}:/data` bind only applies with `--storage-s3`, which this
deployment does not pass).

Note the original intent was already correct — someone meant media to land
on the mount. It never did, because the bind targets `/liveorc/data/media`
while `MEDIA_ROOT` is `/liveorc/media`. A single path component is the
entire outage.

`liveorc.service` couples to s3fs in **five** places (Phase 0). Every one
moves to the media volume — leaving any behind keeps a dead mount able to
take LiveORC down, which is exactly what happened:

```ini
# was → now
RequiresMountsFor=/mnt/s3-storage        → /var/lib/liveorc-media
After=docker.service mnt-s3\x2dstorage.mount     → docker.service var-lib-liveorc\x2dmedia.mount
Requires=docker.service mnt-s3\x2dstorage.mount  → docker.service var-lib-liveorc\x2dmedia.mount
AssertPathIsMountPoint=/mnt/s3-storage   → /var/lib/liveorc-media
ExecStartPre=/usr/local/bin/verify-s3mount.sh    → rewrite + rename (see below)
Description=LiveORC Server with S3 Storage       → LiveORC Server
```

**Do not use `grep -rn "s3-storage"` as this checklist.** `After=` and
`Requires=` name the unit as `mnt-s3\x2dstorage.mount`, systemd-escaped, so
the literal string does not match and those two lines are missed. Use:

```bash
grep -n 's3' /etc/systemd/system/liveorc.service    # expect 5 hits
```

**Rewrite `verify-s3mount.sh` rather than dropping it.** It does a real write
test (`touch .test`), which catches a mount that is present but read-only —
something `AssertPathIsMountPoint` cannot detect. Rename it to
`verify-media-mount.sh` and point it at `/var/lib/liveorc-media`; a script
called `verify-s3mount.sh` guarding an EBS volume is the same naming rot that
kept the original misconfiguration invisible.

The systemd unit name for `/var/lib/liveorc-media` must be exact — derive it
rather than typing it:

```bash
systemd-escape -p --suffix=mount /var/lib/liveorc-media
# → var-lib-liveorc\x2dmedia.mount
```

`fstab` (Phase 3) generates that unit automatically, so no `.mount` file is
written by hand. Verify it exists **before** editing the service:

```bash
systemctl status "$(systemd-escape -p --suffix=mount /var/lib/liveorc-media)"
```

Then retire s3fs and reload. **Nothing restarts in this phase** — the recreate
is Phase 7:

```bash
sudo systemctl disable --now 'mnt-s3\x2dstorage.mount'
sudo systemctl daemon-reload
```

**Keep the mount dependency, pointed at the right mount.** LiveORC should
refuse to start when its media volume is absent. The guard was never missing —
it was aimed at a 4 KB s3fs mount nothing used, while the real media path had
no guard at all. That inversion is why ten weeks of uploads went into a
container layer without one error, and why a disk-full s3fs failure took the
application down.

#### Guards — in `start-liveorc.sh`, because that file is ours

Edit 2 above lives in an upstream file, so a LiveORC upgrade reverts it and the
failure is silent. `start-liveorc.sh` is a local wrapper and survives, so the
durable defense belongs there. Add both: the first refuses to start a
misconfigured stack, the second verifies reality rather than config.

```bash
# --- BEFORE ./liveorc.sh start ---

# A LiveORC upgrade replaces docker-compose.yml and reverts the media bind
# destination. Uploads then land in the container's writable layer and vanish
# on the next recreate. That cost 26 GB and a host outage on 2026-08-10.
if ! grep -q '${LORC_STORAGE_DIR}:/liveorc/media' /opt/LiveORC/docker-compose.yml; then
    echo "FATAL: docker-compose.yml media bind is not /liveorc/media." >&2
    echo "A LiveORC upgrade has probably reverted it. See MEDIA_VOLUME_RUNBOOK.md." >&2
    exit 1
fi
```

```bash
# --- AFTER ./liveorc.sh start ---

# Config is not evidence; the mount table is.
for _ in $(seq 1 30); do
    docker inspect liveorc_webapp >/dev/null 2>&1 && break
    sleep 2
done
MOUNT=$(docker inspect liveorc_webapp \
    --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' \
    2>/dev/null | grep -F '-> /liveorc/media')
if [ -z "$MOUNT" ]; then
    echo "FATAL: /liveorc/media is NOT a mount in liveorc_webapp." >&2
    echo "Media would accumulate in the writable layer and be lost." >&2
    exit 1
fi
echo "media mount OK: $MOUNT"
```

Do **not** pass `--renew-anon-volumes` — the webapp's `/liveorc/data`
anonymous volume must be carried across, and `docker compose up` reuses it by
default. A manual `docker rm` followed by `up` would orphan it.

### Phase 7 — ⚠️ Recreate and verify

Start through **systemd**, not compose directly:

```bash
sudo systemctl start liveorc.service
```

**Never `cd /opt/LiveORC && docker compose up -d` here.** That bypasses
`start-liveorc.sh`, so it passes no `--storage-dir` and neither guard runs —
`LORC_STORAGE_DIR` falls back to `.env`'s `lorc_media` named volume, and the
migration is silently undone. Going through the unit also exercises the real
boot path end to end, which is the thing that has to work at the next reboot.

First, the only check that actually proves the migration worked — the running
container's mount table, not any config file:

```bash
sudo docker inspect liveorc_webapp \
  --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' | grep media
```

Must print `/var/lib/liveorc-media -> /liveorc/media`. If it still shows
`/liveorc/data/media`, the destination edit did not take: media is going to the
writable layer exactly as before. Stop and fix it before any upload arrives.

```bash
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

### Phase 9 — Re-enable boot

Only once Phase 7's mount check passed:

```bash
sudo systemctl enable liveorc.service
systemctl is-enabled liveorc.service      # enabled
```

`liveorc.service` has been disabled since 2026-08-10 because it runs
`docker compose up -d`, which recreates the webapp and would have destroyed the
26 GB. That is now safe — a recreate loses nothing once media is on the volume —
and leaving it disabled would mean LiveORC silently fails to return after a
reboot.

#### Result — Phases 6-9 run 2026-08-27

Phase 6 installed three files we own (`start-liveorc.sh`, `verify-media-mount.sh`,
`liveorc.service`) from version control at `liveorc-host/`, plus the one upstream
edit — `docker-compose.yml` line 8, `/liveorc/data/media` -> `/liveorc/media`,
with `.orig` kept. s3 references in the unit went 5 -> 0.

Phase 7 succeeded on the second attempt. **Both failures were guards working.**

**Failure 1 — the mount guard.** `ExecStartPre` inherits `User=ubuntu`, but the
volume is `root:root` and the webapp writes media as uid 0 from inside the
container. The write test failed and the start was refused. Fixed with
`ExecStartPre=+`, which runs that command as root — and tests the real failure
mode (filesystem mounted read-only) rather than an irrelevant one.
`verify-s3mount.sh` only ever passed because s3fs used `allow_other`.

**Failure 2 — nginx.** See ISS-FIELD-005. LiveORC 0.3.0's nginx template uses
`ssl on;`, removed in nginx 1.25.1, while its own image ships 1.26.3. A
hand-patched config had been living in the writable layer since May with no copy
anywhere; the recreate deleted it and the site went down. Repaired durably in
`start-liveorc.sh`. **This is the same failure class as the media itself** —
critical state in exactly one place — and the migration is what exposed it.

Result: writable layer 31 GB -> **56.1 kB**, `/` 51 G/66% -> **21 G/27%**, image
unchanged at `sha256:2f0b38cc7891...` (no version moved under the station), and
a full `systemctl restart` exercised the real boot path end to end:

```
verify-media-mount.sh: Mount point /var/lib/liveorc-media verified successfully
Storage: local volume at: /var/lib/liveorc-media
LiveORC started; media mount OK: /var/lib/liveorc-media -> /liveorc/media
```

`/mnt/s3-storage` was **kept** at Tom's request as an operator convenience, but
decoupled: nothing depends on it, `Before=docker.service` removed, and
`ensure_diskfree=10240` added so its unbounded object cache cannot fill `/`.

**Found along the way, not caused by this work:** `LORC_DEFAULT_NODES=0` in
`.env` (`git diff` shows a local `1 -> 0`), so no `liveorc_worker` exists and no
video has been processed since the August outage. See ISS-FIELD-006.

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

- [x] Disk-space check on `/` **and** `/var/lib/liveorc-media` — 2026-08-27.
      `check-disk-space.sh` + `disk-space-check.timer`, every 15 min, warn 75% /
      critical 85%. Also asserts the media path is still a *mount point*: if the
      volume ever fails to mount, media silently returns to the root disk.
- [ ] **Attach an SNS notification to the CloudWatch alarm.** The check
      publishes `ORC/Disk / UsedPercent`, but journal output is not an alarm —
      nobody reads it. Creating the alarm and its email subscription is console
      work and is the last piece of "we would find out next time".
- [ ] **After any LiveORC upgrade**, re-check the media bind — the destination
      fix is in an upstream file and will be reverted:
      `diff /opt/LiveORC/docker-compose.yml.orig /opt/LiveORC/docker-compose.yml`
      The `start-liveorc.sh` guards make this loud rather than silent, but the
      fix still has to be reapplied by hand.
- [x] Corrected `REPROCESS_RUNBOOK.md` (2026-08-27) — the "video bytes live in
      MinIO/S3" claim is gone, with a note explaining why it was dangerous
      rather than a silent edit.
- [ ] Document the media volume and the `RequiresMountsFor` guard in
      `README.md`.
- [ ] Snapshot schedule for the media volume (DLM lifecycle policy).
- [ ] Decide retention for `s3://openrivercam-video/orc_site4.tgz` (642 MB,
      2026-06-08).
