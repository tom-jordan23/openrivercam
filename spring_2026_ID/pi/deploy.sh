#!/usr/bin/env bash
#
# deploy.sh — Apply ORC station overlays to a freshly flashed ORC-OS image
#
# Usage:
#   deploy.sh <site> [options]
#
# Arguments:
#   site:  sukabumi | jakarta
#
# Options:
#   --skip-packages    Skip apt/pip install (for offline or pre-installed)
#   --skip-config-txt  Skip /boot/firmware/config.txt modifications
#   --dry-run          Show what would be done without executing
#   --help             Show this help
#
# Prerequisites:
#   1. Flash ORC-OS image with Pi Imager (set hostname, enable SSH, WiFi)
#   2. First boot complete (ORC-OS init, filesystem expand, auto-reboot)
#   3. SSH access to the Pi
#   4. This repo cloned or copied to the Pi (or run remotely via SSH)
#
# Run this script ON the Pi as the pi user (it will sudo as needed).
#

set -euo pipefail

# ─── Configuration ─────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PI_DIR="$SCRIPT_DIR"
SHARED_DIR="$PI_DIR/shared"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/tmp/orc-deploy-backup-${TIMESTAMP}"
REPORT_FILE="/tmp/orc-deploy-report-${TIMESTAMP}.txt"

SITE=""
SKIP_PACKAGES=0
SKIP_CONFIG_TXT=0
DRY_RUN=0

# ─── Parse arguments ──────────────────────────────────────────────
usage() {
    sed -n '2,/^$/p' "$0" | sed 's/^# \?//'
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        sukabumi|jakarta) SITE="$arg" ;;
        --skip-packages)  SKIP_PACKAGES=1 ;;
        --skip-config-txt) SKIP_CONFIG_TXT=1 ;;
        --dry-run)        DRY_RUN=1 ;;
        --help|-h)        usage ;;
        *) echo "Unknown argument: $arg"; usage ;;
    esac
done

if [ -z "$SITE" ]; then
    echo "ERROR: Site name required (sukabumi or jakarta)"
    usage
fi

SITE_DIR="$PI_DIR/$SITE"

# ─── Helpers ──────────────────────────────────────────────────────
log()  { echo "$(date '+%H:%M:%S') [deploy] $1"; echo "$1" >> "$REPORT_FILE"; }
warn() { echo "$(date '+%H:%M:%S') [deploy] WARN: $1" >&2; echo "WARN: $1" >> "$REPORT_FILE"; }
err()  { echo "$(date '+%H:%M:%S') [deploy] ERROR: $1" >&2; echo "ERROR: $1" >> "$REPORT_FILE"; }

run() {
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  DRY RUN: $*"
    else
        "$@"
    fi
}

# ─── Validation ───────────────────────────────────────────────────
log "=== ORC Station Deploy: $SITE ==="
log "Timestamp: $TIMESTAMP"
log "Repo root: $REPO_ROOT"

if [ ! -d "$SHARED_DIR" ]; then
    err "Shared directory not found: $SHARED_DIR"
    exit 1
fi

if [ ! -d "$SITE_DIR" ]; then
    err "Site directory not found: $SITE_DIR"
    exit 1
fi

# Check if running on a Pi
if [ -f /proc/device-tree/model ]; then
    MODEL=$(cat /proc/device-tree/model | tr -d '\0')
    log "Hardware: $MODEL"
else
    warn "Not running on a Raspberry Pi (or /proc/device-tree/model not found)"
fi

# ─── Phase 1: Backup current state ───────────────────────────────
log ""
log "--- Phase 1: Backup ---"

mkdir -p "$BACKUP_DIR"

# Backup files that will be overwritten
backup_file() {
    local dest="$1"
    if [ -f "$dest" ]; then
        local backup_path="$BACKUP_DIR$dest"
        mkdir -p "$(dirname "$backup_path")"
        cp "$dest" "$backup_path" 2>/dev/null || true
    fi
}

log "Backup directory: $BACKUP_DIR"

# ─── Phase 2: Package installation ───────────────────────────────
log ""
log "--- Phase 2: Packages ---"

if [ "$SKIP_PACKAGES" -eq 1 ]; then
    log "Skipping package installation (--skip-packages)"
else
    log "Installing system packages..."
    run sudo apt update -qq
    run sudo apt install -y -qq dnsmasq modemmanager gpiod minicom chrony ffmpeg

    log "Installing Python packages..."
    run pip install --break-system-packages --quiet requests pyserial smbus2 pyyaml

    log "Installing LED status packages (sudo, Pi 5 PIO)..."
    run sudo pip install --break-system-packages --quiet \
        adafruit-blinka \
        adafruit-circuitpython-neopixel \
        adafruit-blinka-raspberry-pi5-neopixel

    log "Adding pi user to dialout group..."
    run sudo usermod -aG dialout pi
fi

# ─── Phase 3: Deploy overlay files ───────────────────────────────
log ""
log "--- Phase 3: Overlay files ---"

deploy_count=0

deploy_file() {
    local src="$1"
    local base_dir="$2"  # shared/ or site/
    local relative="${src#$base_dir/}"

    # Special case: update-motd.d/ lives at top level in repo but goes to /etc/
    if [[ "$relative" == update-motd.d/* ]]; then
        relative="etc/$relative"
    fi

    local dest="/$relative"
    local dest_dir="$(dirname "$dest")"

    # Backup existing file
    backup_file "$dest"

    log "  $dest"

    if [ "$DRY_RUN" -eq 0 ]; then
        sudo mkdir -p "$dest_dir"
        sudo cp "$src" "$dest"

        # Set permissions based on destination
        case "$dest" in
            /usr/local/bin/*)
                sudo chmod +x "$dest"
                ;;
            /etc/update-motd.d/*)
                sudo chmod +x "$dest"
                ;;
            /etc/profile.d/*.sh)
                sudo chmod +x "$dest"
                ;;
            /etc/NetworkManager/system-connections/*.nmconnection)
                sudo chmod 600 "$dest"
                sudo chown root:root "$dest"
                ;;
        esac
    fi

    deploy_count=$((deploy_count + 1))
}

# Deploy shared files first
log "Deploying shared files..."
while IFS= read -r -d '' file; do
    [ "$(basename "$file")" = ".gitkeep" ] && continue
    deploy_file "$file" "$SHARED_DIR"
done < <(find "$SHARED_DIR" -type f -print0 | sort -z)

# Deploy site-specific files (overwrite shared where applicable)
log "Deploying $SITE-specific files..."
while IFS= read -r -d '' file; do
    [ "$(basename "$file")" = ".gitkeep" ] && continue
    deploy_file "$file" "$SITE_DIR"
done < <(find "$SITE_DIR" -type f -print0 | sort -z)

log "Deployed $deploy_count files"

# Deploy camtool.py from camera/ directory (source of truth lives outside pi/shared/)
CAMTOOL_SRC="$REPO_ROOT/camera/camtool.py"
if [ -f "$CAMTOOL_SRC" ]; then
    backup_file /usr/local/bin/camtool.py
    log "  /usr/local/bin/camtool.py (from camera/camtool.py)"
    if [ "$DRY_RUN" -eq 0 ]; then
        sudo cp "$CAMTOOL_SRC" /usr/local/bin/camtool.py
        sudo chmod +x /usr/local/bin/camtool.py
    fi
    deploy_count=$((deploy_count + 1))
else
    warn "camtool.py not found at $CAMTOOL_SRC — camera config management unavailable"
fi

# ─── Phase 4: Create directories ─────────────────────────────────
log ""
log "--- Phase 4: Directories ---"

run sudo mkdir -p /var/log/orc/sensors
run sudo chown -R pi:pi /var/log/orc
run sudo mkdir -p /mnt/usb
run sudo mkdir -p /etc/orc-sensors
run sudo mkdir -p /etc/orc
run sudo mkdir -p /usr/local/lib/orc-sensors
run sudo mkdir -p /usr/local/lib/orc-led-status
run sudo mkdir -p /etc/chrony/conf.d
run sudo mkdir -p /etc/systemd/system/dnsmasq.service.d
run mkdir -p /home/pi/camera_profiles

# Create Videos directory or symlink
if [ -b /dev/sda1 ]; then
    log "USB drive detected at /dev/sda1"
    USB_UUID=$(sudo blkid -s UUID -o value /dev/sda1 2>/dev/null || true)
    if [ -n "$USB_UUID" ]; then
        if ! grep -q "/mnt/usb" /etc/fstab; then
            log "Adding USB drive to fstab (UUID=$USB_UUID)"
            if [ "$DRY_RUN" -eq 0 ]; then
                echo "UUID=$USB_UUID /mnt/usb ext4 defaults,noatime,nofail 0 2" | sudo tee -a /etc/fstab > /dev/null
            fi
        fi
        run sudo mount -a 2>/dev/null || true
        run sudo mkdir -p /mnt/usb/incoming
        run sudo chown pi:pi /mnt/usb/incoming

        if [ ! -L /home/pi/Videos ]; then
            log "Creating Videos symlink -> /mnt/usb/incoming"
            run rm -rf /home/pi/Videos
            run ln -s /mnt/usb/incoming /home/pi/Videos
        fi
    fi
else
    warn "USB drive not detected. Add fstab entry manually after inserting drive."
    if [ ! -d /home/pi/Videos ] && [ ! -L /home/pi/Videos ]; then
        run mkdir -p /home/pi/Videos
    fi
fi

log "Directories created"

# ─── Phase 5: config.txt modifications ────────────────────────────
log ""
log "--- Phase 5: config.txt ---"

if [ "$SKIP_CONFIG_TXT" -eq 1 ]; then
    log "Skipping config.txt modifications (--skip-config-txt)"
else
    CONFIG_TXT=""
    if [ -f /boot/firmware/config.txt ]; then
        CONFIG_TXT="/boot/firmware/config.txt"
    elif [ -f /boot/config.txt ]; then
        CONFIG_TXT="/boot/config.txt"
    fi

    if [ -n "$CONFIG_TXT" ]; then
        log "Modifying $CONFIG_TXT (append only)"
        backup_file "$CONFIG_TXT"

        append_if_missing() {
            local line="$1"
            local desc="$2"
            if ! grep -q "^${line}$" "$CONFIG_TXT"; then
                log "  Adding: $line ($desc)"
                if [ "$DRY_RUN" -eq 0 ]; then
                    echo "$line" | sudo tee -a "$CONFIG_TXT" > /dev/null
                fi
            else
                log "  Already present: $line"
            fi
        }

        # Removed: ML-2020 RTC battery connector failed on both boards. Using Witty Pi 5 HAT+ CR2032 RTC instead.
        # append_if_missing "dtparam=rtc_bbat_vchg=3000000" "RTC battery charging (ML-2020)"
        append_if_missing "enable_uart=1" "UART for rain gauge"
        append_if_missing "dtparam=i2c_arm=on" "I2C for SHT40 sensor"
        append_if_missing "usb_max_current_enable=1" "USB current limit for Quectel modem (GPIO 5V rail has no PD negotiation)"
    else
        warn "config.txt not found — skipping. Add RTC/UART/I2C settings manually."
    fi
fi

# ─── Phase 6: System configuration ───────────────────────────────
log ""
log "--- Phase 6: System config ---"

# Disable cloud-init
if [ ! -f /etc/cloud/cloud-init.disabled ]; then
    log "Disabling cloud-init"
    run sudo touch /etc/cloud/cloud-init.disabled
fi

# Verify timezone is UTC
TZ_CURRENT=$(timedatectl show --property=Timezone --value 2>/dev/null || echo "unknown")
if [ "$TZ_CURRENT" != "UTC" ] && [ "$TZ_CURRENT" != "Etc/UTC" ]; then
    log "Setting timezone to UTC (was: $TZ_CURRENT)"
    run sudo timedatectl set-timezone UTC
else
    log "Timezone already UTC"
fi

# Add nofail to boot fstab entry (prevent boot failure if boot partition has issues)
if [ -f /etc/fstab ]; then
    if grep -q "/boot/firmware" /etc/fstab && ! grep "/boot/firmware" /etc/fstab | grep -q "nofail"; then
        log "Adding nofail to /boot/firmware fstab entry"
        if [ "$DRY_RUN" -eq 0 ]; then
            sudo sed -i '/\/boot\/firmware/ s/defaults/defaults,nofail/' /etc/fstab
        fi
    fi
fi

# Show ORC station status on every new terminal (appended to pi user's .bashrc)
BASHRC="/home/pi/.bashrc"
if [ -f "$BASHRC" ]; then
    if ! grep -q "run-parts /etc/update-motd.d/" "$BASHRC" 2>/dev/null; then
        log "Adding ORC MOTD to $BASHRC"
        if [ "$DRY_RUN" -eq 0 ]; then
            echo "" >> "$BASHRC"
            echo "# ORC station status on every new terminal" >> "$BASHRC"
            echo "cat /etc/motd 2>/dev/null" >> "$BASHRC"
            echo "run-parts /etc/update-motd.d/ 2>/dev/null" >> "$BASHRC"
        fi
    fi
fi

# ─── Phase 6b: Witty Pi 5 HAT+ software ─────────────────────────
log ""
log "--- Phase 6b: Witty Pi 5 ---"

if command -v wp5 >/dev/null 2>&1; then
    log "Witty Pi 5 software already installed (wp5)"
else
    log "Installing Witty Pi 5 software..."
    WP5_DEB="/tmp/wp5_latest.deb"
    if [ "$DRY_RUN" -eq 0 ]; then
        wget -q https://www.uugear.com/repo/WittyPi5/wp5_latest.deb -O "$WP5_DEB" \
            && sudo apt install -y "$WP5_DEB" \
            && rm -f "$WP5_DEB" \
            && log "Witty Pi 5 software installed" \
            || warn "Witty Pi 5 software install failed — install manually"
    fi
fi

# Sync system time to Witty Pi 5 RTC (RTC may have stale time on first install)
if command -v wp5 >/dev/null 2>&1 && [ "$DRY_RUN" -eq 0 ]; then
    log "Syncing system time to Witty Pi 5 RTC..."
    echo "1" | wp5 >/dev/null 2>&1 && echo "14" | wp5 >/dev/null 2>&1
    log "RTC sync complete"
fi

# Disable ORC-OS native RTC power management (Pi 5 ML-2020 battery failed;
# Witty Pi 5 HAT+ now owns RTC and power scheduling)
if systemctl list-unit-files orc-rpi5-power-management.service >/dev/null 2>&1; then
    log "Disabling orc-rpi5-power-management.service (replaced by Witty Pi 5)"
    run sudo systemctl disable orc-rpi5-power-management.service 2>/dev/null || true
    run sudo systemctl stop orc-rpi5-power-management.service 2>/dev/null || true
fi

# ─── Phase 7: Service enablement ─────────────────────────────────
log ""
log "--- Phase 7: Services ---"

run sudo systemctl daemon-reload

enable_service() {
    local svc="$1"
    log "  Enabling: $svc"
    run sudo systemctl enable "$svc" 2>/dev/null || warn "Failed to enable $svc"
}

disable_service() {
    local svc="$1"
    log "  Disabling: $svc"
    run sudo systemctl disable "$svc" 2>/dev/null || true
}

enable_service dnsmasq
enable_service chrony
enable_service orc-capture.service
enable_service orc-sensors.timer
enable_service orc-led-status.service
enable_service orc-boot-usb-log.service

# Disable conflicting ORC-OS relay service (active-low, incompatible with our hardware)
disable_service orc-gpio-relays.service

# ─── Phase 8: Credential check ───────────────────────────────────
log ""
log "--- Phase 8: Credentials ---"

CRED_MISSING=0

if ls ~/.orc_deploy_* 1>/dev/null 2>&1; then
    log "Camera credentials found: $(ls ~/.orc_deploy_*)"
else
    warn "No camera credentials found (~/.orc_deploy_*)"
    warn "  Create with: echo 'BASE_PASSWD=<camera_password>' > ~/.orc_deploy_$SITE"
    CRED_MISSING=1
fi

if [ ! -f ~/.ssh/authorized_keys ]; then
    warn "No SSH authorized_keys found"
    CRED_MISSING=1
fi

if [ "$CRED_MISSING" -eq 1 ]; then
    warn "Some credentials are missing — see warnings above"
fi

# ─── Phase 9: Verification ───────────────────────────────────────
log ""
log "--- Phase 9: Verification ---"

if [ -x /usr/local/bin/orc-preflight ] && [ "$DRY_RUN" -eq 0 ]; then
    log "Running orc-preflight..."
    /usr/local/bin/orc-preflight || warn "orc-preflight reported issues (see above)"
else
    log "Skipping orc-preflight (dry run or not installed)"
fi

# ─── Summary ──────────────────────────────────────────────────────
log ""
log "=== Deploy complete for $SITE ==="
log "Files deployed: $deploy_count"
log "Backup at: $BACKUP_DIR"
log "Report at: $REPORT_FILE"
log ""

if [ "$CRED_MISSING" -eq 1 ]; then
    log "ACTION REQUIRED: Set up missing credentials (see warnings above)"
fi

log "Next steps:"
log "  1. Set root password: sudo passwd root"
log "  2. Set camera credentials: echo 'BASE_PASSWD=<password>' > ~/.orc_deploy_$SITE"
log "  3. Verify camera network: ping 192.168.50.100 (after PoE relay on)"
log "  4. Configure camera via camtool.py (if camera replaced)"
log "  5. Reboot and verify: sudo reboot"
