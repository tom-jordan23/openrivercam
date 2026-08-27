# LiveORC host files

Version-controlled copies of the three host files **we own** that make LiveORC's
media land on the dedicated EBS volume. Before this directory existed they lived
only on the EC2 instance, with no backup — the same single-copy problem the
media migration itself was fixing.

| File | Installed at | Owner |
|---|---|---|
| `start-liveorc.sh` | `/opt/LiveORC/start-liveorc.sh` | **ours** — local wrapper, survives a LiveORC upgrade |
| `verify-media-mount.sh` | `/usr/local/bin/verify-media-mount.sh` | **ours** — replaces `verify-s3mount.sh` |
| `liveorc.service` | `/etc/systemd/system/liveorc.service` | **ours** |
| `mnt-s3-storage.mount` | `/etc/systemd/system/mnt-s3\x2dstorage.mount` | **ours** — operator convenience, nothing depends on it |

## What is deliberately NOT here

`/opt/LiveORC/docker-compose.yml` is **upstream-owned**. Its media bind
destination is the actual 2026-08-10 bug (`/liveorc/data/media` where
`MEDIA_ROOT` is `/liveorc/media`), and it has to be fixed in place, because
`liveorc.sh` builds an explicit `-f` list and so never auto-loads
`docker-compose.override.yml`. A LiveORC upgrade will revert that fix silently.

Keeping a full copy here would invite someone to overwrite upstream's file with
a stale one. Instead: `/opt/LiveORC/docker-compose.yml.orig` holds the
pre-edit original for diffing, and Guard 1 in `start-liveorc.sh` refuses to
start if the bind was reverted.

## Deploying

```bash
git -C ~/code/git/openrivercam pull
cd ~/code/git/openrivercam/spring_2026_ID/liveorc_server/liveorc-host

sudo cp /opt/LiveORC/start-liveorc.sh /opt/LiveORC/start-liveorc.sh.orig
sudo install -m 0755 start-liveorc.sh     /opt/LiveORC/start-liveorc.sh
sudo install -m 0755 verify-media-mount.sh /usr/local/bin/verify-media-mount.sh
sudo install -m 0644 liveorc.service       /etc/systemd/system/liveorc.service
sudo systemctl daemon-reload
```

Installing these does **not** restart anything. `liveorc.service` is
`Type=oneshot` + `RemainAfterExit`, and `daemon-reload` only re-reads units.

## The S3 convenience mount

`/mnt/s3-storage` is kept for operator convenience only. It is **not** part of
LiveORC's storage path — media lives on the EBS volume at
`/var/lib/liveorc-media`.

Two properties must hold, and both were violated before 2026-08-27:

1. **Nothing depends on it.** `liveorc.service` used to carry `Requires=`,
   `After=`, `RequiresMountsFor=` and `AssertPathIsMountPoint` against this
   mount, so an s3fs failure took the whole application down. The unit also
   carried `Before=docker.service`, putting it ahead of Docker at boot.
2. **It cannot fill the root disk.** `use_cache` has no size limit of its own
   and s3fs caches whole objects, so `ensure_diskfree=10240` keeps 10 GB free
   on `/`. A full root disk took this host down on 2026-08-10.

## The two guards

`start-liveorc.sh` carries both, because it is the one file in this chain that
an upgrade cannot touch:

1. **Config** — refuses to start if `docker-compose.yml`'s media bind is no
   longer `/liveorc/media`.
2. **Reality** — after start, checks the *running container's mount table*
   rather than any config file. Config can be right while the container is
   wrong.

Guard 2's `grep -F --` needs that `--`. The pattern begins with `-`, so without
it grep parses the pattern as options, exits 2 with no output, and the guard
reports a healthy mount as missing — failing every start with a misleading
error.
