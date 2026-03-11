# Pi Configuration Files

Source of truth for all Raspberry Pi customizations applied on top of the
Rainbow Sensing ORC-OS base image. Files here are manually
copied to each Pi during setup — there is no automated deployment.

## Layout Convention

Files are stored under the **filesystem path they occupy on the Pi**, relative
to `/`. The top level splits into `shared/` (all sites) and per-site
directories:

```
pi/
├── shared/          # Files identical across ALL ORC sites
│   └── etc/
│       └── ...
├── sukabumi/        # Sukabumi site-specific files
│   └── etc/
│       └── ...
└── jakarta/         # Jakarta site-specific files
    └── etc/
        └── ...
```

Example: `pi/sukabumi/etc/dnsmasq.d/cameras.conf` → goes to
`/etc/dnsmasq.d/cameras.conf` on the Sukabumi Pi.

If a file exists in both `shared/` and a site directory, the **site version
wins**. In practice this means you copy `shared/` files first, then overwrite
with site-specific files.

### .gitkeep files

Empty directories aren't tracked by git. The `.gitkeep` files are zero-byte
placeholders that force git to preserve the directory structure. They have no
effect on the Pi — do not copy them. Delete a `.gitkeep` once the directory
contains a real file.

## File Inventory

<!-- Update this table whenever you add or remove a file. -->

| Repo path | Pi path | Description | Shared / Site | Credentials? | Upstream candidate? |
|-----------|---------|-------------|---------------|:------------:|:-------------------:|
| `shared/etc/dnsmasq.d/maintenance.conf` | `/etc/dnsmasq.d/maintenance.conf` | DHCP server for camera PoE network on eth0 | Shared | No | No |
| `sukabumi/etc/cloud/templates/hosts.debian.tmpl` | `/etc/cloud/templates/hosts.debian.tmpl` | Hosts file template with camera hostname | Sukabumi | No | No |
| `sukabumi/etc/NetworkManager/system-connections/camera-net.nmconnection` | `/etc/NetworkManager/system-connections/camera-net.nmconnection` | Static IP (192.168.50.1) for eth0 camera network | Sukabumi | No | No |

**Column guide:**
- **Credentials?** — Yes if the file contains passwords, keys, or secrets that
  must be filled in after copying to the Pi. Tracked files use placeholders
  (e.g. `<CAMERA_PASSWORD>`); real values are never committed.
- **Upstream candidate?** — Yes if this file should be submitted to Rainbow
  Sensing for inclusion in future base images.

## How to Apply

Copy files to a Pi over SSH. Shared files first, then site-specific:

```bash
# From the repo root — replace PI_HOST with the Pi's IP or hostname

# Shared files (all sites)
scp -r spring_2026_ID/pi/shared/etc/ PI_HOST:/tmp/shared-etc/
ssh PI_HOST 'sudo cp -r /tmp/shared-etc/* /etc/ && rm -rf /tmp/shared-etc'

# Site-specific files (example: sukabumi)
scp -r spring_2026_ID/pi/sukabumi/etc/ PI_HOST:/tmp/site-etc/
ssh PI_HOST 'sudo cp -r /tmp/site-etc/* /etc/ && rm -rf /tmp/site-etc'
```

Then restart the relevant services (e.g. `sudo systemctl restart dnsmasq`).

For a single file, direct scp is simpler:

```bash
scp spring_2026_ID/pi/sukabumi/etc/dnsmasq.d/cameras.conf PI_HOST:/tmp/
ssh PI_HOST 'sudo cp /tmp/cameras.conf /etc/dnsmasq.d/ && rm /tmp/cameras.conf'
```

## How to Add a New File

1. Create the file under the correct path:
   - `shared/` if it applies to all sites
   - `sukabumi/` or `jakarta/` if site-specific
   - Mirror the on-Pi filesystem path (e.g. a file that goes to
     `/etc/foo/bar.conf` → `pi/shared/etc/foo/bar.conf`)
2. If the file contains credentials, use placeholders (`<CAMERA_PASSWORD>`,
   `<ADMIN_KEY>`, etc.) and note it in the inventory table.
3. Update the **File Inventory** table above.
4. Commit.

## Credentials Policy

Real passwords and secrets are **never committed**. Files that need credentials
use obvious placeholders. After copying a file to the Pi, replace placeholders
with real values in-place:

```bash
ssh PI_HOST 'sudo sed -i "s/<CAMERA_PASSWORD>/actual_password/" /etc/some/config'
```

If a local-only variant is ever needed, use the `*.local` suffix (e.g.
`cameras.conf.local`) — these are gitignored.

## Rainbow Sensing Upstream

Files in `shared/` that would benefit all ORC-OS deployments are
candidates for upstream inclusion. The **Upstream candidate?** column in the
inventory table tracks which files to submit.

| File | Status | Notes |
|------|--------|-------|
| *(none yet)* | | |

When submitting upstream, include the rationale (what problem it solves, what
it replaces in the base image) so Rainbow Sensing can evaluate.
