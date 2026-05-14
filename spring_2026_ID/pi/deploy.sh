#!/usr/bin/env bash
#
# deploy.sh — ORC station configuration management
#
# Checks configuration state, reports results, then optionally fixes failures.
# Replaces both the old deploy.sh (fix-only) and orc-preflight (check-only).
#
# Usage:
#   deploy.sh <site> [options]
#
# Arguments:
#   site:  sukabumi | jakarta
#
# Options:
#   --check            Check only, no fixes (replaces orc-preflight)
#   --yes              Apply fixes without prompting
#   --skip-packages    Skip apt/pip checks (for offline or pre-installed)
#   --skip-config-txt  Skip /boot/firmware/config.txt checks
#   -h|--help          Show this help
#
# Run this script ON the Pi as the pi user (it will sudo as needed).
#
# Flow:
#   1. Parse args, validate site
#   2. Run all checks with FIXING=0 — report PASS/FAIL/WARN
#   3. Show summary (N pass, N fail, N warn)
#   4. If no failures — done
#   5. If --check flag — exit with status (no fixes)
#   6. Prompt "Apply N fixes? [y/N]" (unless --yes)
#   7. Create backup dir, run all checks again with FIXING=1
#   8. Show final summary
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
CHECK_ONLY=0
AUTO_YES=0
SKIP_PACKAGES=0
SKIP_CONFIG_TXT=0

# Runtime state
FIXING=0
PASS=0
FAIL=0
WARN=0
FIXED=0
FAILURES=()   # descriptions of failures, for the "Fixes needed:" list
BACKUP_CREATED=0

# ─── Parse arguments ──────────────────────────────────────────────
usage() {
    sed -n '2,/^$/p' "$0" | sed 's/^# \?//'
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        sukabumi|jakarta)   SITE="$arg" ;;
        --check)            CHECK_ONLY=1 ;;
        --yes)              AUTO_YES=1 ;;
        --skip-packages)    SKIP_PACKAGES=1 ;;
        --skip-config-txt)  SKIP_CONFIG_TXT=1 ;;
        --help|-h)          usage ;;
        *) echo "Unknown argument: $arg"; usage ;;
    esac
done

if [ -z "$SITE" ]; then
    echo "ERROR: Site name required (sukabumi or jakarta)"
    usage
fi

SITE_DIR="$PI_DIR/$SITE"

# ─── Validate directories ─────────────────────────────────────────
if [ ! -d "$SHARED_DIR" ]; then
    echo "ERROR: Shared directory not found: $SHARED_DIR"
    exit 1
fi
if [ ! -d "$SITE_DIR" ]; then
    echo "ERROR: Site directory not found: $SITE_DIR"
    exit 1
fi

# ─── Reporting functions ──────────────────────────────────────────
# All output also tees to the report file.
_tee() { echo "$1" | tee -a "$REPORT_FILE"; }

pass()  {
    local msg="  [\033[32mPASS\033[0m] $1"
    printf "%b\n" "$msg"
    printf "  [PASS] %s\n" "$1" >> "$REPORT_FILE"
    PASS=$((PASS+1))
}

fail()  {
    local msg="  [\033[31mFAIL\033[0m] $1"
    printf "%b\n" "$msg"
    printf "  [FAIL] %s\n" "$1" >> "$REPORT_FILE"
    FAIL=$((FAIL+1))
    FAILURES+=("$1")
}

warn()  {
    local msg="  [\033[33mWARN\033[0m] $1"
    printf "%b\n" "$msg"
    printf "  [WARN] %s\n" "$1" >> "$REPORT_FILE"
    WARN=$((WARN+1))
}

fixed() {
    local msg="  [\033[36mFIXD\033[0m] $1"
    printf "%b\n" "$msg"
    printf "  [FIXD] %s\n" "$1" >> "$REPORT_FILE"
    FIXED=$((FIXED+1))
}

section() {
    printf "\n" | tee -a "$REPORT_FILE"
    printf "=== %s ===\n" "$1" | tee -a "$REPORT_FILE"
}

reset_counters() {
    PASS=0; FAIL=0; WARN=0; FIXED=0
    FAILURES=()
}

# ─── Backup helper ────────────────────────────────────────────────
backup_file() {
    local dest="$1"
    [ "$FIXING" -ne 1 ] && return
    [ ! -f "$dest" ] && return

    # Create backup dir on first use
    if [ "$BACKUP_CREATED" -eq 0 ]; then
        mkdir -p "$BACKUP_DIR"
        BACKUP_CREATED=1
    fi

    local backup_path="$BACKUP_DIR$dest"
    mkdir -p "$(dirname "$backup_path")"
    cp "$dest" "$backup_path" 2>/dev/null || true
}

# ─── Header ───────────────────────────────────────────────────────
{
    echo "=== ORC Station Deploy: $SITE ==="
    echo "Timestamp: $TIMESTAMP"
    echo "Repo root: $REPO_ROOT"
} | tee -a "$REPORT_FILE"

if [ -f /proc/device-tree/model ]; then
    MODEL=$(tr -d '\0' < /proc/device-tree/model)
    echo "Hardware: $MODEL" | tee -a "$REPORT_FILE"
fi

# ══════════════════════════════════════════════════════════════════
# SECTION FUNCTIONS
# Each section function reads FIXING to decide whether to fix.
# ══════════════════════════════════════════════════════════════════

# ─── Packages ─────────────────────────────────────────────────────
run_packages() {
    [ "$SKIP_PACKAGES" -eq 1 ] && return

    section "Packages"

    # apt packages
    local apt_pkgs="dnsmasq modemmanager gpiod minicom chrony ffmpeg"
    local need_apt_update=0
    local missing_apt=""
    for pkg in $apt_pkgs; do
        if dpkg -s "$pkg" >/dev/null 2>&1; then
            pass "$pkg installed"
        else
            if [ "$FIXING" -eq 1 ]; then
                [ "$need_apt_update" -eq 0 ] && { sudo apt-get update -qq 2>/dev/null; need_apt_update=1; }
                sudo apt-get install -y -qq "$pkg" 2>/dev/null
                if dpkg -s "$pkg" >/dev/null 2>&1; then
                    fixed "$pkg installed"
                else
                    fail "$pkg not installed"
                fi
            else
                fail "$pkg not installed"
                missing_apt="$missing_apt $pkg"
            fi
        fi
    done

    # pip (system) packages — requests, smbus2, pyyaml are required
    # pyserial is optional (debugging only); serial import alias tested separately
    local pip_pkgs="requests pyserial smbus2 pyyaml"
    local pip_imports="requests smbus2 yaml"
    for mod in $pip_imports; do
        if python3 -c "import $mod" 2>/dev/null; then
            pass "python3 $mod available"
        else
            if [ "$FIXING" -eq 1 ]; then
                # shellcheck disable=SC2086
                pip install --break-system-packages --quiet $pip_pkgs 2>/dev/null
                if python3 -c "import $mod" 2>/dev/null; then
                    fixed "python3 $mod available"
                else
                    fail "python3 $mod not available"
                fi
            else
                fail "python3 $mod not available"
            fi
        fi
    done

    # pyserial (imports as 'serial') — optional, useful for debugging
    if python3 -c "import serial" 2>/dev/null; then
        pass "python3 serial (pyserial) available"
    else
        warn "python3 serial (pyserial) not available (optional — debugging only)"
    fi

    # pip (sudo, LED) packages
    local led_pkgs="adafruit-blinka adafruit-circuitpython-neopixel adafruit-blinka-raspberry-pi5-neopixel"
    if python3 -c "import neopixel" 2>/dev/null; then
        pass "python3 neopixel (LED status) available"
    else
        if [ "$FIXING" -eq 1 ]; then
            # shellcheck disable=SC2086
            sudo pip install --break-system-packages --quiet $led_pkgs 2>/dev/null
            if python3 -c "import neopixel" 2>/dev/null; then
                fixed "python3 neopixel (LED status) available"
            else
                fail "python3 neopixel (LED status) not available"
            fi
        else
            fail "python3 neopixel (LED status) not available"
        fi
    fi

    # User in dialout group
    if id -nG pi | grep -qw dialout; then
        pass "pi is in dialout group"
    else
        if [ "$FIXING" -eq 1 ]; then
            sudo usermod -aG dialout pi
            fixed "pi added to dialout group (re-login required)"
        else
            fail "pi is NOT in dialout group (needed for serial/modem access)"
        fi
    fi
}

# ─── Overlay files ────────────────────────────────────────────────
# Shared state across check and fix passes for file deployment
OVERLAY_DIFFS=()   # list of "src|dest" pairs that differ

_check_overlay_file() {
    local src="$1"
    local base_dir="$2"
    local relative="${src#$base_dir/}"

    # Special case: update-motd.d/ lives at top level in repo but goes to /etc/
    if [[ "$relative" == update-motd.d/* ]]; then
        relative="etc/$relative"
    fi

    local dest="/$relative"

    if [ -f "$dest" ] && sudo cmp -s "$src" "$dest"; then
        pass "$dest (up to date)"
    else
        if [ -f "$dest" ]; then
            fail "$dest (differs from overlay)"
        else
            fail "$dest (missing)"
        fi
        OVERLAY_DIFFS+=("$src|$dest|$base_dir")
    fi
}

_fix_overlay_file() {
    local src="$1"
    local dest="$2"
    local dest_dir
    dest_dir="$(dirname "$dest")"

    backup_file "$dest"
    sudo mkdir -p "$dest_dir"
    sudo cp "$src" "$dest"

    case "$dest" in
        /usr/local/bin/*)
            sudo chmod +x "$dest" ;;
        /etc/update-motd.d/*)
            sudo chmod +x "$dest" ;;
        /etc/profile.d/*.sh)
            sudo chmod +x "$dest" ;;
        /etc/NetworkManager/system-connections/*.nmconnection)
            sudo chmod 600 "$dest"
            sudo chown root:root "$dest" ;;
        /etc/udev/rules.d/*)
            sudo chmod 644 "$dest"
            sudo chown root:root "$dest" ;;
        /etc/systemd/logind.conf.d/*)
            sudo chmod 644 "$dest"
            sudo chown root:root "$dest"
            sudo systemctl kill -s HUP systemd-logind 2>/dev/null || true ;;
    esac

    # Verify the fix landed — promote from FAIL to FIXD
    if sudo cmp -s "$src" "$dest"; then
        FAIL=$((FAIL-1))
        fixed "$dest"
    else
        fail "$dest (copy failed — still differs after fix)"
    fi
}

run_overlay_files() {
    section "Overlay Files"
    OVERLAY_DIFFS=()

    # Walk shared/ then site/ (site overrides shared).
    # Skip shared files that have a site-specific override, since the site
    # version is authoritative and the shared version will always differ.
    while IFS= read -r -d '' file; do
        [ "$(basename "$file")" = ".gitkeep" ] && continue
        local relative="${file#$SHARED_DIR/}"
        if [ -f "$SITE_DIR/$relative" ]; then
            continue  # site override exists — skip shared version
        fi
        _check_overlay_file "$file" "$SHARED_DIR"
    done < <(find "$SHARED_DIR" -type f -print0 | sort -z)

    while IFS= read -r -d '' file; do
        [ "$(basename "$file")" = ".gitkeep" ] && continue
        # Skip non-overlay files that live in the site dir but aren't deployed to the Pi
        case "$(basename "$file")" in
            *.wpi|station_mode) continue ;;
        esac
        _check_overlay_file "$file" "$SITE_DIR"
    done < <(find "$SITE_DIR" -type f -print0 | sort -z)

    # camtool.py — source of truth lives outside pi/shared/
    local camtool_src="$REPO_ROOT/camera/camtool.py"
    if [ -f "$camtool_src" ]; then
        if [ -f /usr/local/bin/camtool.py ] && cmp -s "$camtool_src" /usr/local/bin/camtool.py; then
            pass "/usr/local/bin/camtool.py (up to date)"
        else
            if [ -f /usr/local/bin/camtool.py ]; then
                fail "/usr/local/bin/camtool.py (differs from camera/camtool.py)"
            else
                fail "/usr/local/bin/camtool.py (missing)"
            fi
            OVERLAY_DIFFS+=("$camtool_src|/usr/local/bin/camtool.py|camtool")
        fi
    else
        warn "camera/camtool.py not found at $camtool_src — camera config management unavailable"
    fi

    # profile-night/image.xml — IR-tuned image params for night captures.
    # Pushed by orc-camera-profile-switch (invoked from orc-capture) on
    # day → night transitions. Source of truth lives outside pi/shared/.
    local profile_night_src="$REPO_ROOT/camera/profiles/profile-night/image.xml"
    local profile_night_dest="/home/pi/camera_profiles/profiles/profile-night/image.xml"
    if [ -f "$profile_night_src" ]; then
        if [ -f "$profile_night_dest" ] && cmp -s "$profile_night_src" "$profile_night_dest"; then
            pass "$profile_night_dest (up to date)"
        else
            if [ -f "$profile_night_dest" ]; then
                fail "$profile_night_dest (differs from camera/profiles/profile-night/image.xml)"
            else
                fail "$profile_night_dest (missing — night camera profile will not be available)"
            fi
            OVERLAY_DIFFS+=("$profile_night_src|$profile_night_dest|profile-night")
        fi
    else
        warn "camera/profiles/profile-night/image.xml not found at $profile_night_src — night profile switching disabled"
    fi

    # Fix phase: apply all diffs
    if [ "$FIXING" -eq 1 ] && [ "${#OVERLAY_DIFFS[@]}" -gt 0 ]; then
        for entry in "${OVERLAY_DIFFS[@]}"; do
            local src dest base_dir
            src="${entry%%|*}"
            dest="${entry#*|}"
            dest="${dest%|*}"
            _fix_overlay_file "$src" "$dest"
        done
        # After file changes, reload systemd units and udev rules
        sudo systemctl daemon-reload
        sudo udevadm control --reload-rules
        sudo udevadm trigger
    fi
}

# ─── Directories ──────────────────────────────────────────────────
run_directories() {
    section "Directories"

    local dirs=(
        /var/log/orc/sensors
        /var/lib/orc-sensors
        /var/lib/orc-camera
        /mnt/usb
        /etc/orc-sensors
        /etc/orc
        /usr/local/lib/orc-sensors
        /usr/local/lib/orc-led-status
        /etc/chrony/conf.d
        /etc/systemd/system/dnsmasq.service.d
        /home/pi/camera_profiles
    )

    for d in "${dirs[@]}"; do
        if [ -d "$d" ]; then
            pass "$d exists"
        else
            if [ "$FIXING" -eq 1 ]; then
                sudo mkdir -p "$d"
                if [[ "$d" == /var/log/orc* ]]; then
                    sudo chown -R pi:pi /var/log/orc
                elif [[ "$d" == /var/lib/orc-sensors || "$d" == /var/lib/orc-camera ]]; then
                    sudo chown pi:pi "$d"
                fi
                fixed "$d created"
            else
                fail "$d missing"
            fi
        fi
    done

    # /var/log/orc writable by pi
    if [ -d /var/log/orc ] && [ -w /var/log/orc ]; then
        pass "/var/log/orc writable by pi"
    elif [ -d /var/log/orc ]; then
        if [ "$FIXING" -eq 1 ]; then
            sudo chown -R pi:pi /var/log/orc
            fixed "/var/log/orc ownership fixed (pi:pi)"
        else
            fail "/var/log/orc exists but not writable by pi"
        fi
    fi

    # /var/lib/orc-sensors writable by pi (rg15_acc.txt lives here)
    if [ -d /var/lib/orc-sensors ] && [ -w /var/lib/orc-sensors ]; then
        pass "/var/lib/orc-sensors writable by pi"
    elif [ -d /var/lib/orc-sensors ]; then
        if [ "$FIXING" -eq 1 ]; then
            sudo chown pi:pi /var/lib/orc-sensors
            fixed "/var/lib/orc-sensors ownership fixed (pi:pi)"
        else
            fail "/var/lib/orc-sensors exists but not writable by pi (rg15 will fail)"
        fi
    fi

    # USB drive (optional, for archive/spare). NOT used for live captures.
    # We tried symlinking ~/Videos -> /mnt/usb/incoming but hit EXDEV: ORC-OS's
    # check_new_videos uses os.rename to move captures into .ORC-OS/tmp (on the
    # SD rootfs), and os.rename can't cross filesystems. The proper fix is
    # upstream (shutil.move); until then, keep ~/Videos on the rootfs.
    if [ -b /dev/sda1 ]; then
        local usb_uuid
        usb_uuid=$(sudo blkid -s UUID -o value /dev/sda1 2>/dev/null || true)
        if [ -n "$usb_uuid" ]; then
            if grep -q "/mnt/usb" /etc/fstab 2>/dev/null; then
                pass "/mnt/usb in fstab (UUID=$usb_uuid)"
            else
                if [ "$FIXING" -eq 1 ]; then
                    echo "UUID=$usb_uuid /mnt/usb ext4 defaults,noatime,nofail 0 2" | sudo tee -a /etc/fstab > /dev/null
                    sudo mount -a 2>/dev/null || true
                    fixed "/mnt/usb added to fstab (UUID=$usb_uuid)"
                else
                    fail "/mnt/usb not in fstab (USB drive detected at /dev/sda1)"
                fi
            fi
        fi
    fi

    # ~/Videos must be a plain directory on the OS rootfs (same FS as .ORC-OS/tmp).
    if [ -L /home/pi/Videos ]; then
        if [ "$FIXING" -eq 1 ]; then
            rm -f /home/pi/Videos
            mkdir -p /home/pi/Videos
            fixed "~/Videos symlink removed, plain directory restored (avoids ORC-OS EXDEV bug)"
        else
            fail "~/Videos is a symlink (causes ORC-OS EXDEV bug — should be plain directory on rootfs)"
        fi
    elif [ ! -d /home/pi/Videos ]; then
        if [ "$FIXING" -eq 1 ]; then
            mkdir -p /home/pi/Videos
            fixed "~/Videos directory created"
        else
            fail "~/Videos missing"
        fi
    else
        pass "~/Videos is a plain directory on rootfs"
    fi
}

# ─── config.txt ───────────────────────────────────────────────────
run_config_txt() {
    [ "$SKIP_CONFIG_TXT" -eq 1 ] && return

    section "config.txt"

    local config_txt=""
    if [ -f /boot/firmware/config.txt ]; then
        config_txt="/boot/firmware/config.txt"
    elif [ -f /boot/config.txt ]; then
        config_txt="/boot/config.txt"
    fi

    if [ -z "$config_txt" ]; then
        if [ -f /etc/udev/rules.d/90-qemu.rules ]; then
            warn "config.txt not accessible (/boot/firmware not mounted — expected with 90-qemu.rules)"
        else
            fail "config.txt not found (neither /boot/firmware/config.txt nor /boot/config.txt)"
        fi
        return
    fi

    local lines=(
        "enable_uart=1:UART for rain gauge"
        "dtoverlay=uart0:Explicit UART0 enable on GPIO 14/15"
        "dtoverlay=disable-bt:Free UART0 from Bluetooth contention"
        "dtparam=i2c_arm=on:I2C for SHT40 sensor"
        "dtoverlay=w1-gpio:1-Wire for DS18B20 temperature probe (GPIO 4)"
        "usb_max_current_enable=1:Raise USB port current limit for LTE modem"
    )

    for entry in "${lines[@]}"; do
        local line="${entry%%:*}"
        local desc="${entry#*:}"
        if grep -q "^${line}$" "$config_txt"; then
            pass "$config_txt: $line ($desc)"
        else
            if [ "$FIXING" -eq 1 ]; then
                backup_file "$config_txt"
                echo "$line" | sudo tee -a "$config_txt" > /dev/null
                fixed "$config_txt: $line added ($desc)"
            else
                fail "$config_txt: $line missing ($desc)"
            fi
        fi
    done

    # cmdline.txt — Samsung FIT Plus UAS quirk
    # The UAS driver causes boot-time USB enumeration storms when the Samsung
    # FIT Plus (0781:5583) is plugged in alongside the LTE modem. Both uas
    # and usb-storage are kernel built-ins, so modprobe.d quirks don't work —
    # cmdline.txt is the only option. This MUST be applied BEFORE inserting the
    # USB drive. See BOOT_FAILURE_ANALYSIS.md and TODO-015.
    local cmdline_txt=""
    local cmdline_dir
    cmdline_dir="$(dirname "$config_txt")"
    if [ -f "$cmdline_dir/cmdline.txt" ]; then
        cmdline_txt="$cmdline_dir/cmdline.txt"
    fi

    if [ -n "$cmdline_txt" ]; then
        local uas_quirk="usb-storage.quirks=0781:5583:u"
        if grep -q "$uas_quirk" "$cmdline_txt"; then
            pass "$cmdline_txt: Samsung FIT UAS quirk present"
        else
            if [ "$FIXING" -eq 1 ]; then
                backup_file "$cmdline_txt"
                # cmdline.txt is a single line — append the quirk with a space
                sudo sed -i "s/$/ ${uas_quirk}/" "$cmdline_txt"
                fixed "$cmdline_txt: Samsung FIT UAS quirk added (reboot required)"
            else
                fail "$cmdline_txt: Samsung FIT UAS quirk missing ($uas_quirk) — USB drive will cause boot storms"
            fi
        fi
    else
        if [ -f /etc/udev/rules.d/90-qemu.rules ]; then
            warn "cmdline.txt not accessible (/boot/firmware not mounted) — cannot verify UAS quirk"
        else
            fail "cmdline.txt not found — cannot apply Samsung FIT UAS quirk"
        fi
    fi

    # cmdline.txt — serial console must be disabled for rain gauge UART
    # The kernel default console=serial0,115200 claims ttyAMA0 (GPIO 14/15)
    # with 0600 root:root permissions, blocking the RG-15 rain gauge.
    if [ -n "$cmdline_txt" ]; then
        if grep -q "console=serial0" "$cmdline_txt"; then
            if [ "$FIXING" -eq 1 ]; then
                backup_file "$cmdline_txt"
                sudo sed -i 's/console=serial0,[0-9]* //' "$cmdline_txt"
                fixed "$cmdline_txt: serial console removed (frees ttyAMA0 for rain gauge — reboot required)"
            else
                fail "$cmdline_txt: console=serial0 present — blocks rain gauge access to ttyAMA0"
            fi
        else
            pass "$cmdline_txt: serial console not present (ttyAMA0 free for rain gauge)"
        fi
    fi
}

# ─── System config ────────────────────────────────────────────────
run_system_config() {
    section "System Config"

    # PAM MOTD — disable to prevent double-display on SSH login
    # (.bashrc handles it via MOTD_SHOWN guard)
    if grep -q "^session.*pam_motd.so" /etc/pam.d/sshd 2>/dev/null; then
        if [ "$FIXING" -eq 1 ]; then
            backup_file /etc/pam.d/sshd
            sudo sed -i 's/^session    optional     pam_motd.so/#&/' /etc/pam.d/sshd
            fixed "PAM MOTD disabled in /etc/pam.d/sshd"
        else
            fail "PAM MOTD enabled in /etc/pam.d/sshd (causes double MOTD on SSH login)"
        fi
    else
        pass "PAM MOTD disabled in /etc/pam.d/sshd"
    fi

    # /etc/profile.d/orc-motd.sh — remove if present (.bashrc handles it)
    if [ -f /etc/profile.d/orc-motd.sh ]; then
        if [ "$FIXING" -eq 1 ]; then
            sudo rm -f /etc/profile.d/orc-motd.sh
            fixed "/etc/profile.d/orc-motd.sh removed (.bashrc handles MOTD)"
        else
            fail "/etc/profile.d/orc-motd.sh present (conflicts with .bashrc MOTD block)"
        fi
    else
        pass "/etc/profile.d/orc-motd.sh absent (correct)"
    fi

    # Cloud-init disabled
    if [ -f /etc/cloud/cloud-init.disabled ]; then
        pass "cloud-init disabled"
    else
        if [ "$FIXING" -eq 1 ]; then
            sudo touch /etc/cloud/cloud-init.disabled
            fixed "cloud-init disabled"
        else
            fail "cloud-init not disabled (/etc/cloud/cloud-init.disabled missing)"
        fi
    fi

    # Timezone via timedatectl
    local tz_current
    tz_current=$(timedatectl show --property=Timezone --value 2>/dev/null || echo "unknown")
    if [ "$tz_current" = "UTC" ] || [ "$tz_current" = "Etc/UTC" ]; then
        pass "Timezone is UTC (timedatectl)"
    else
        if [ "$FIXING" -eq 1 ]; then
            sudo timedatectl set-timezone UTC
            fixed "Timezone set to UTC (was: $tz_current)"
        else
            fail "Timezone is $tz_current (should be UTC) — white screen bug if wrong"
        fi
    fi

    # /etc/timezone — ORC-OS reads this; a wrong value crashes the frontend
    local etc_tz
    etc_tz=$(cat /etc/timezone 2>/dev/null || echo "")
    if [ "$etc_tz" = "UTC" ]; then
        pass "/etc/timezone is UTC"
    else
        if [ "$FIXING" -eq 1 ]; then
            echo "UTC" | sudo tee /etc/timezone > /dev/null
            fixed "/etc/timezone set to UTC (was: ${etc_tz:-empty})"
        else
            fail "/etc/timezone is '${etc_tz:-empty}' (should be UTC — causes frontend white screen)"
        fi
    fi

    # Persistent journal
    if grep -q "^Storage=persistent" /etc/systemd/journald.conf 2>/dev/null; then
        pass "Persistent journal enabled (journald.conf)"
    else
        if [ "$FIXING" -eq 1 ]; then
            sudo sed -i 's/^#\?Storage=.*/Storage=persistent/' /etc/systemd/journald.conf
            if ! grep -q "^SystemMaxUse=" /etc/systemd/journald.conf; then
                sudo sed -i 's/^#\?SystemMaxUse=.*/SystemMaxUse=50M/' /etc/systemd/journald.conf
            fi
            sudo systemctl restart systemd-journald
            fixed "Persistent journal enabled (50M cap)"
        else
            fail "Persistent journal not enabled (journald.conf Storage != persistent)"
        fi
    fi

    # /boot/firmware fstab nofail
    if [ -f /etc/fstab ]; then
        if grep -q "/boot/firmware" /etc/fstab; then
            if grep "/boot/firmware" /etc/fstab | grep -q "nofail"; then
                pass "/boot/firmware fstab entry has nofail"
            else
                if [ "$FIXING" -eq 1 ]; then
                    backup_file /etc/fstab
                    sudo sed -i '/\/boot\/firmware/ s/defaults/defaults,nofail/' /etc/fstab
                    fixed "/boot/firmware fstab entry: nofail added"
                else
                    fail "/boot/firmware fstab entry missing nofail"
                fi
            fi
        else
            warn "/boot/firmware not in fstab (expected if 90-qemu.rules remaps mmcblk0)"
        fi
    fi

    # Getty autologin — disable leftover autologin from upstream image
    # The stock image auto-logins as hcwinsemius which doesn't exist, causing
    # a getty restart loop (~every 5s) that floods the journal.
    local autologin_conf="/etc/systemd/system/getty@tty1.service.d/autologin.conf"
    if [ -f "$autologin_conf" ]; then
        if [ "$FIXING" -eq 1 ]; then
            sudo rm -f "$autologin_conf"
            sudo systemctl daemon-reload
            sudo systemctl restart getty@tty1.service 2>/dev/null || true
            fixed "Getty autologin disabled (removed $autologin_conf)"
        else
            fail "Getty autologin still enabled ($autologin_conf — causes login loop)"
        fi
    else
        pass "Getty autologin disabled (no autologin.conf override)"
    fi

    # .bashrc MOTD block (MOTD_SHOWN guard)
    local bashrc="/home/pi/.bashrc"
    if [ -f "$bashrc" ]; then
        if grep -q "run-parts /etc/update-motd.d" "$bashrc" 2>/dev/null; then
            # Check for unguarded duplicate block from older deploy.sh versions
            if grep -q "^cat /etc/motd" "$bashrc" 2>/dev/null; then
                if [ "$FIXING" -eq 1 ]; then
                    backup_file "$bashrc"
                    sed -i '/^# ORC station status on every new terminal$/d' "$bashrc"
                    sed -i '/^cat \/etc\/motd 2>\/dev\/null$/d' "$bashrc"
                    sed -i '/^run-parts \/etc\/update-motd.d\/ 2>\/dev\/null$/d' "$bashrc"
                    fixed "$bashrc: removed duplicate unguarded MOTD block"
                else
                    fail "$bashrc has duplicate unguarded MOTD block (conflicts with MOTD_SHOWN guard)"
                fi
            else
                pass "$bashrc has MOTD_SHOWN-guarded block"
            fi
        else
            if [ "$FIXING" -eq 1 ]; then
                backup_file "$bashrc"
                cat >> "$bashrc" << 'MOTD'

# Display MOTD (static + dynamic scripts from /etc/update-motd.d/)
if [ -z "$MOTD_SHOWN" ]; then
    [ -f /etc/motd ] && cat /etc/motd
    [ -d /etc/update-motd.d ] && run-parts /etc/update-motd.d 2>/dev/null
    export MOTD_SHOWN=1
fi
MOTD
                fixed "$bashrc: MOTD_SHOWN-guarded block added"
            else
                fail "$bashrc missing MOTD block (run-parts /etc/update-motd.d)"
            fi
        fi
    else
        warn "/home/pi/.bashrc not found"
    fi
}

# ─── Witty Pi 5 ───────────────────────────────────────────────────
run_witty_pi() {
    section "Witty Pi 5"

    # wp5 command available
    if command -v wp5 >/dev/null 2>&1; then
        pass "Witty Pi 5 software installed (wp5)"
    else
        if [ "$FIXING" -eq 1 ]; then
            local wp5_deb="/tmp/wp5_latest.deb"
            wget -q https://www.uugear.com/repo/WittyPi5/wp5_latest.deb -O "$wp5_deb" \
                && sudo apt install -y "$wp5_deb" \
                && rm -f "$wp5_deb" \
                && fixed "Witty Pi 5 software installed (wp5)" \
                || fail "Witty Pi 5 software install failed — install wp5_latest.deb manually"
        else
            fail "Witty Pi 5 software not installed (wp5 not found)"
        fi
    fi

    # wp5d daemon running (check only — started by systemd)
    if systemctl is-active --quiet wp5d 2>/dev/null; then
        pass "Witty Pi 5 daemon running (wp5d)"
    else
        warn "Witty Pi 5 daemon not running (wp5d) — start with: sudo systemctl start wp5d"
    fi

    # RTC synced to system clock
    if command -v wp5 >/dev/null 2>&1; then
        if [ "$FIXING" -eq 1 ]; then
            printf '1\n14\n' | timeout 30 wp5 >/dev/null 2>&1 || true
            fixed "Witty Pi 5 RTC synced to system clock"
        else
            # RTC drift check (check-only)
            local wp5_rtc
            wp5_rtc=$(echo "14" | wp5 2>/dev/null | grep "RTC Time:" | head -1 | sed 's/.*RTC Time: //' || true)
            if [ -n "$wp5_rtc" ]; then
                local sys_epoch rtc_epoch drift
                sys_epoch=$(date -u +%s)
                rtc_epoch=$(date -u -d "$wp5_rtc" +%s 2>/dev/null || echo "0")
                if [ "$rtc_epoch" -ne 0 ]; then
                    drift=$(( sys_epoch - rtc_epoch ))
                    drift=${drift#-}  # absolute value
                    if [ "$drift" -le 5 ]; then
                        pass "Witty Pi 5 RTC in sync with system clock (${wp5_rtc})"
                    else
                        warn "Witty Pi 5 RTC drift: ${drift}s (RTC: ${wp5_rtc}) — sync with: printf '1\\n14\\n' | wp5"
                    fi
                fi
            fi
        fi
    fi

    # orc-api.service depends on wp5d.service
    if [ -f /etc/systemd/system/orc-api.service ]; then
        if grep -q "wp5d.service" /etc/systemd/system/orc-api.service; then
            pass "orc-api.service depends on wp5d.service"
        else
            if [ "$FIXING" -eq 1 ]; then
                backup_file /etc/systemd/system/orc-api.service
                sudo sed -i 's/After=network.target/After=network.target wp5d.service/' /etc/systemd/system/orc-api.service
                sudo systemctl daemon-reload
                fixed "orc-api.service: wp5d.service dependency added"
            else
                fail "orc-api.service missing wp5d.service dependency (early reboot risk)"
            fi
        fi
    else
        warn "orc-api.service not found at /etc/systemd/system/ (ORC-OS not installed?)"
    fi

    # orc-rpi5-power-management.service disabled (replaced by Witty Pi 5)
    if systemctl list-unit-files orc-rpi5-power-management.service >/dev/null 2>&1; then
        if systemctl is-enabled orc-rpi5-power-management.service >/dev/null 2>&1; then
            if [ "$FIXING" -eq 1 ]; then
                sudo systemctl disable orc-rpi5-power-management.service 2>/dev/null || true
                sudo systemctl stop orc-rpi5-power-management.service 2>/dev/null || true
                fixed "orc-rpi5-power-management.service disabled (replaced by Witty Pi 5)"
            else
                fail "orc-rpi5-power-management.service enabled (conflicts with Witty Pi 5)"
            fi
        else
            pass "orc-rpi5-power-management.service disabled (correct)"
        fi
    else
        pass "orc-rpi5-power-management.service not present (correct)"
    fi
}

# ─── Power button (Pi 5 J2 header) ────────────────────────────────
# The J2 header connects to RP1 firmware, not Linux GPIO. Three layers:
#   1. Short press while running  → RP1 emits KEY_POWER → logind → poweroff
#   2. Long press (~5s) while running → RP1 force-cuts power (hardware, always works)
#   3. Short press while halted   → RP1 wakes PMIC (requires WAKE_ON_GPIO=1)
#
# Layers 2 and 3 are firmware. Layer 1 depends on Linux. We verify:
#   - EEPROM: POWER_OFF_ON_HALT=0 and WAKE_ON_GPIO=1 (bootloader config)
#   - Input device: RP1 exposes "pwr_button" to Linux (/proc/bus/input/devices)
#   - logind drop-in is deployed (handled by run_overlay_files)
run_power_button() {
    section "Power Button"

    # EEPROM config — governs whether a button press can wake the Pi and
    # whether `halt` leaves the Pi in a wakeable state.
    if command -v rpi-eeprom-config >/dev/null 2>&1; then
        local ee_cfg
        ee_cfg=$(sudo rpi-eeprom-config 2>/dev/null || true)

        if [ -z "$ee_cfg" ]; then
            warn "rpi-eeprom-config returned no output (not a Pi 5? EEPROM unreadable?)"
        else
            # WAKE_ON_GPIO: default 1. A button press only wakes the Pi from halt
            # if this is 1. If unset, default applies — treat as PASS.
            local wake_val
            wake_val=$(echo "$ee_cfg" | grep -E "^WAKE_ON_GPIO=" | cut -d= -f2 | tr -d '[:space:]')
            if [ -z "$wake_val" ] || [ "$wake_val" = "1" ]; then
                pass "EEPROM WAKE_ON_GPIO=${wake_val:-1 (default)} (button can wake from halt)"
            else
                if [ "$FIXING" -eq 1 ]; then
                    local tmp_cfg
                    tmp_cfg=$(mktemp)
                    echo "$ee_cfg" | sed 's/^WAKE_ON_GPIO=.*/WAKE_ON_GPIO=1/' > "$tmp_cfg"
                    if sudo rpi-eeprom-config --apply "$tmp_cfg" >/dev/null 2>&1; then
                        fixed "EEPROM WAKE_ON_GPIO set to 1 (reboot required)"
                    else
                        fail "EEPROM WAKE_ON_GPIO: rpi-eeprom-config --apply failed"
                    fi
                    rm -f "$tmp_cfg"
                else
                    fail "EEPROM WAKE_ON_GPIO=$wake_val (should be 1 — button cannot wake from halt)"
                fi
            fi

            # POWER_OFF_ON_HALT: default 0. If 1, `halt` fully powers off and
            # the Pi needs button press to restart — surprises ops staff.
            local poh_val
            poh_val=$(echo "$ee_cfg" | grep -E "^POWER_OFF_ON_HALT=" | cut -d= -f2 | tr -d '[:space:]')
            if [ -z "$poh_val" ] || [ "$poh_val" = "0" ]; then
                pass "EEPROM POWER_OFF_ON_HALT=${poh_val:-0 (default)} (halt keeps Pi in wakeable state)"
            else
                if [ "$FIXING" -eq 1 ]; then
                    local tmp_cfg
                    tmp_cfg=$(mktemp)
                    echo "$ee_cfg" | sed 's/^POWER_OFF_ON_HALT=.*/POWER_OFF_ON_HALT=0/' > "$tmp_cfg"
                    if sudo rpi-eeprom-config --apply "$tmp_cfg" >/dev/null 2>&1; then
                        fixed "EEPROM POWER_OFF_ON_HALT set to 0 (reboot required)"
                    else
                        fail "EEPROM POWER_OFF_ON_HALT: rpi-eeprom-config --apply failed"
                    fi
                    rm -f "$tmp_cfg"
                else
                    fail "EEPROM POWER_OFF_ON_HALT=$poh_val (should be 0 — halt would require button press to restart)"
                fi
            fi
        fi
    else
        warn "rpi-eeprom-config not available — cannot verify EEPROM power-button settings"
    fi

    # RP1 exposes the J2 header to Linux as an input device named "pwr_button".
    # If this is missing, either RP1 firmware is wedged or the kernel driver is
    # not loaded — short-press shutdown will not work (long-press force-off
    # still will, since it's pure firmware).
    if [ -r /proc/bus/input/devices ]; then
        if grep -q 'Name="pwr_button"' /proc/bus/input/devices; then
            pass "RP1 pwr_button input device present (/proc/bus/input/devices)"
        else
            fail "RP1 pwr_button input device MISSING — short-press shutdown will not work (long-press force-off still functional via RP1 firmware)"
        fi
    else
        warn "/proc/bus/input/devices not readable — cannot verify pwr_button device"
    fi

    # Effective logind HandlePowerKey setting. The overlay file covers the
    # on-disk config; this cross-checks that logind actually loaded it.
    # (busctl is provided by systemd and always available.)
    if command -v busctl >/dev/null 2>&1; then
        local effective_hpk
        effective_hpk=$(busctl get-property org.freedesktop.login1 /org/freedesktop/login1 \
            org.freedesktop.login1.Manager HandlePowerKey 2>/dev/null \
            | awk '{print $2}' | tr -d '"' || true)
        if [ "$effective_hpk" = "poweroff" ]; then
            pass "logind HandlePowerKey=poweroff (effective, via busctl)"
        elif [ -n "$effective_hpk" ]; then
            # The overlay file fix reloads logind, so if this still shows wrong
            # after a fix pass, the drop-in is being overridden somewhere.
            fail "logind HandlePowerKey=$effective_hpk (should be poweroff — check for overriding drop-ins under /etc/systemd/logind.conf.d/ or /run/systemd/logind.conf.d/)"
        else
            warn "logind HandlePowerKey: busctl returned empty (logind not running?)"
        fi
    fi
}

# ─── Services ─────────────────────────────────────────────────────
_ensure_service_enabled() {
    local svc="$1"
    if systemctl is-enabled "$svc" >/dev/null 2>&1; then
        pass "$svc enabled"
    else
        if [ "$FIXING" -eq 1 ]; then
            sudo systemctl enable "$svc" 2>/dev/null \
                && fixed "$svc enabled" \
                || fail "$svc enable failed"
        else
            fail "$svc not enabled"
        fi
    fi
}

_ensure_service_disabled() {
    local svc="$1"
    if ! systemctl list-unit-files "$svc" >/dev/null 2>&1; then
        pass "$svc not present (correct)"
        return
    fi
    if systemctl is-enabled "$svc" >/dev/null 2>&1; then
        if [ "$FIXING" -eq 1 ]; then
            sudo systemctl disable "$svc" 2>/dev/null || true
            sudo systemctl stop "$svc" 2>/dev/null || true
            fixed "$svc disabled"
        else
            fail "$svc is enabled (should be disabled)"
        fi
    else
        pass "$svc disabled (correct)"
    fi
}

_check_service_running() {
    local svc="$1"
    if systemctl is-enabled "$svc" >/dev/null 2>&1; then
        if systemctl is-active "$svc" >/dev/null 2>&1; then
            pass "$svc enabled and running"
        else
            fail "$svc enabled but NOT running"
        fi
    else
        fail "$svc not enabled"
    fi
}

run_services() {
    section "Services"

    # Enable
    _ensure_service_enabled dnsmasq
    _ensure_service_enabled chrony
    _ensure_service_enabled orc-sensors.timer
    _ensure_service_enabled orc-sensors-upload.timer
    _ensure_service_enabled orc-led-status.service
    _ensure_service_enabled orc-led-off.service
    _ensure_service_enabled orc-boot-usb-log.service
    _ensure_service_enabled orc-maintenance-check.service

    # Disable
    # orc-gpio-relays uses active-low logic incompatible with Electronics-Salon relay module
    _ensure_service_disabled orc-gpio-relays.service

    # Check running (services managed by ORC-OS or systemd — no auto-restart here)
    # orc-led-off is Type=oneshot with RemainAfterExit=yes: it must be "active
    # (exited)" now so its ExecStop fires at shutdown. If enabled but never
    # started since the last boot, the backstop won't run.
    for svc in orc-api orc-led-status orc-led-off dnsmasq NetworkManager ModemManager chrony; do
        _check_service_running "$svc"
    done

    # Static orc-capture.service — remove if present (replaced by ORC-OS managed timer)
    if [ -f /etc/systemd/system/orc-capture.service ] && [ ! -L /etc/systemd/system/orc-capture.service ]; then
        if [ "$FIXING" -eq 1 ]; then
            sudo systemctl stop orc-capture.service 2>/dev/null || true
            sudo systemctl disable orc-capture.service 2>/dev/null || true
            sudo rm -f /etc/systemd/system/orc-capture.service
            sudo systemctl daemon-reload
            fixed "static orc-capture.service removed (replaced by ORC-OS managed timer)"
        else
            fail "static orc-capture.service present (should be removed — ORC-OS manages the timer)"
        fi
    else
        pass "no static orc-capture.service (correct — ORC-OS manages timer)"
    fi

    # orc-capture ORC-OS import
    local orc_capture_json="$PI_DIR/orc-capture-service.json"
    local orc_capture_last="/home/pi/.ORC-OS/.orc-capture-service.json.deployed"
    if [ -f "$orc_capture_json" ]; then
        if [ -f "$orc_capture_last" ] && cmp -s "$orc_capture_json" "$orc_capture_last"; then
            pass "orc-capture service definition matches ORC-OS (up to date)"
        else
            if [ "$FIXING" -eq 1 ]; then
                if /home/pi/venv/orc-os/bin/orc service import --preserve-env --deploy "$orc_capture_json"; then
                    cp "$orc_capture_json" "$orc_capture_last"
                    fixed "orc-capture service imported into ORC-OS"
                else
                    fail "orc-capture service import failed — configure manually via ORC-OS web UI"
                fi
            else
                fail "orc-capture service definition not imported into ORC-OS"
            fi
        fi
    else
        warn "orc-capture-service.json not found at $orc_capture_json — import manually via ORC-OS web UI"
    fi
}

# ─── Credentials (check only) ─────────────────────────────────────
run_credentials() {
    section "Credentials"

    # Always look in pi's home — deploy.sh typically runs under sudo so $HOME is /root.
    if ls ~pi/.orc_deploy_* 1>/dev/null 2>&1; then
        local creds
        creds=$(ls ~pi/.orc_deploy_* | tr '\n' ' ')
        pass "Camera credentials found: $creds"
    else
        warn "No camera credentials found (~pi/.orc_deploy_*)"
        warn "  Create with: echo 'BASE_PASSWD=<camera_password>' > ~pi/.orc_deploy_$SITE"
    fi

    if [ -f ~pi/.ssh/authorized_keys ]; then
        local key_count
        key_count=$(grep -c "^ssh-" ~pi/.ssh/authorized_keys 2>/dev/null || echo "0")
        pass "~pi/.ssh/authorized_keys exists ($key_count key(s))"
    else
        warn "~pi/.ssh/authorized_keys not found (SSH key login unavailable)"
    fi

    # Sensor upload credentials (out-of-band — deploy.sh will not generate keys)
    local upload_conf=/etc/orc/sensors-upload.conf
    if [ -f "$upload_conf" ]; then
        # shellcheck source=/dev/null
        local upload_enabled="" upload_key="" upload_known="" upload_host=""
        # Read values in a subshell so sourcing doesn't leak
        eval "$(
            . "$upload_conf"
            printf 'upload_enabled=%q\n' "${ENABLED:-0}"
            printf 'upload_key=%q\n'     "${SSH_KEY:-}"
            printf 'upload_known=%q\n'   "${KNOWN_HOSTS:-/home/pi/.ssh/known_hosts}"
            printf 'upload_host=%q\n'    "${REMOTE_HOST:-}"
        )"

        if [ "$upload_enabled" != "1" ]; then
            warn "sensors-upload disabled in $upload_conf (set ENABLED=1 after key + server setup)"
        else
            # SSH key file — warn (not fail) and do not auto-create
            if [ -z "$upload_key" ]; then
                fail "sensors-upload: SSH_KEY not set in $upload_conf"
            elif [ ! -f "$upload_key" ]; then
                warn "sensors-upload: SSH key $upload_key missing — generate with:"
                warn "  sudo -u pi ssh-keygen -t ed25519 -N '' -C orc-sensors-upload@\$(hostname) -f $upload_key"
            else
                pass "sensors-upload: SSH key $upload_key present"
                local key_mode key_owner
                key_mode=$(stat -c '%a' "$upload_key" 2>/dev/null || echo "")
                key_owner=$(stat -c '%U' "$upload_key" 2>/dev/null || echo "")
                if [ "$key_mode" = "600" ] && [ "$key_owner" = "pi" ]; then
                    pass "sensors-upload: SSH key mode 600 pi:pi"
                else
                    if [ "$FIXING" -eq 1 ]; then
                        sudo chmod 600 "$upload_key"
                        sudo chown pi:pi "$upload_key"
                        fixed "sensors-upload: SSH key perms set to 600 pi:pi"
                    else
                        fail "sensors-upload: SSH key has mode=$key_mode owner=$key_owner (want 600 pi)"
                    fi
                fi
            fi

            # known_hosts entry for REMOTE_HOST
            if [ -n "$upload_host" ] && [ -f "$upload_known" ]; then
                if grep -q -E "(^|,)$upload_host([ ,]|$)" "$upload_known" 2>/dev/null \
                   || ssh-keygen -F "$upload_host" -f "$upload_known" >/dev/null 2>&1; then
                    pass "sensors-upload: known_hosts has $upload_host"
                else
                    warn "sensors-upload: $upload_host not in $upload_known — prime with:"
                    warn "  sudo -u pi ssh-keyscan -H $upload_host >> $upload_known"
                fi
            elif [ -n "$upload_host" ]; then
                warn "sensors-upload: $upload_known missing (first scp will accept host key on TOFU)"
            fi
        fi
    fi
}

# ─── Configuration checks (check only) ────────────────────────────
run_config_checks() {
    section "Configuration"

    # dnsmasq bind-dynamic
    if [ -f /etc/dnsmasq.d/maintenance.conf ]; then
        if grep -q "^bind-dynamic" /etc/dnsmasq.d/maintenance.conf; then
            pass "/etc/dnsmasq.d/maintenance.conf: bind-dynamic present"
        elif grep -q "^bind-interfaces" /etc/dnsmasq.d/maintenance.conf; then
            if [ "$FIXING" -eq 1 ]; then
                backup_file /etc/dnsmasq.d/maintenance.conf
                sudo sed -i 's/^bind-interfaces$/bind-dynamic/' /etc/dnsmasq.d/maintenance.conf
                fixed "/etc/dnsmasq.d/maintenance.conf: bind-interfaces replaced with bind-dynamic"
            else
                fail "/etc/dnsmasq.d/maintenance.conf: bind-interfaces (should be bind-dynamic)"
            fi
        else
            warn "/etc/dnsmasq.d/maintenance.conf: missing bind directive"
        fi
    else
        fail "/etc/dnsmasq.d/maintenance.conf not found"
    fi

    # camera-net NM connection at 192.168.50.1/24
    if nmcli -t -f NAME con show 2>/dev/null | grep -q "camera-net"; then
        local cam_ip
        cam_ip=$(nmcli -t -f ipv4.addresses con show camera-net 2>/dev/null || true)
        if echo "$cam_ip" | grep -q "192.168.50.1/24"; then
            pass "camera-net connection: 192.168.50.1/24"
        else
            fail "camera-net connection: wrong IP ($cam_ip — expected 192.168.50.1/24)"
        fi
    else
        fail "camera-net NetworkManager connection not found"
    fi

    # poe-relay in PATH
    if command -v poe-relay >/dev/null 2>&1; then
        pass "poe-relay found at $(command -v poe-relay)"
    else
        fail "poe-relay not found in PATH"
    fi

    # camtool.py in PATH
    if command -v camtool.py >/dev/null 2>&1; then
        pass "camtool.py found at $(command -v camtool.py)"
    else
        fail "camtool.py not found in PATH"
    fi

    # LED status config
    if [ -f /etc/orc/led-status.yaml ]; then
        pass "/etc/orc/led-status.yaml present"
    else
        fail "/etc/orc/led-status.yaml not found"
    fi

    # LED-off backstop: the WS2812B is on an always-on 5V rail, so the Pi
    # must explicitly drive it to (0,0,0) on shutdown or it holds its last
    # color indefinitely. Two layers:
    #   1. orc-led-status.service — SIGTERM handler + ExecStopPost=--off
    #   2. orc-led-off.service    — oneshot whose ExecStop runs last at shutdown
    if systemctl cat orc-led-status.service 2>/dev/null | grep -q "^ExecStopPost=.*--off"; then
        pass "orc-led-status.service has ExecStopPost --off (primary LED-off path)"
    else
        fail "orc-led-status.service missing ExecStopPost --off (LED will hold last color after shutdown)"
    fi
    if systemctl cat orc-led-off.service 2>/dev/null | grep -q "^ExecStop=.*--off"; then
        pass "orc-led-off.service has ExecStop --off (LED-off backstop)"
    else
        fail "orc-led-off.service missing ExecStop --off (no backstop if orc-led-status fails at shutdown)"
    fi

    # orc-sensors config
    if [ -d /etc/orc-sensors ] && ls /etc/orc-sensors/*.conf >/dev/null 2>&1; then
        local sensor_count
        sensor_count=$(ls /etc/orc-sensors/*.conf 2>/dev/null | wc -l)
        pass "/etc/orc-sensors/ has $sensor_count sensor config(s)"
    else
        warn "/etc/orc-sensors/ not found or empty (sensor logging will not run)"
    fi

    # Sensor log dir writable
    local sensor_log_dir="/var/log/orc/sensors"
    local first_conf
    first_conf=$(ls /etc/orc-sensors/*.conf 2>/dev/null | head -1 || true)
    if [ -n "$first_conf" ]; then
        local conf_log_dir
        conf_log_dir=$(grep "^LOG_DIR=" "$first_conf" 2>/dev/null | cut -d= -f2 | sed 's/#.*//' | xargs || true)
        [ -n "$conf_log_dir" ] && sensor_log_dir="$conf_log_dir"
    fi
    if [ -d "$sensor_log_dir" ] && [ -w "$sensor_log_dir" ]; then
        pass "sensor log directory writable ($sensor_log_dir)"
    elif [ -d "$sensor_log_dir" ]; then
        fail "sensor log directory exists but not writable ($sensor_log_dir)"
    else
        warn "sensor log directory does not exist yet ($sensor_log_dir) — created on first run"
    fi

    # QEMU 90-qemu.rules (critical — do NOT remove)
    local qemu_rules="/etc/udev/rules.d/90-qemu.rules"
    if [ -f "$qemu_rules" ]; then
        if grep -q 'KERNEL=="sda", SYMLINK+="mmcblk0"' "$qemu_rules"; then
            pass "90-qemu.rules present (required for boot — do NOT remove)"
        else
            warn "90-qemu.rules exists but has unexpected contents"
        fi
    else
        fail "90-qemu.rules MISSING — system may not survive a reboot! Restore immediately."
    fi

    # /etc/hosts camera entry
    if grep -q "192\.168\.50\.[0-9].*camera\|camera.*192\.168\.50\.[0-9]" /etc/hosts 2>/dev/null; then
        local cam_host_line
        cam_host_line=$(grep "192\.168\.50\.[0-9].*camera" /etc/hosts 2>/dev/null | head -1)
        pass "/etc/hosts: camera entry ($cam_host_line)"
    else
        warn "/etc/hosts: missing camera hostname entry"
    fi

    # camera_profiles directory
    if [ -d /home/pi/camera_profiles ]; then
        local profile_count
        profile_count=$(find /home/pi/camera_profiles -name "*.xml" 2>/dev/null | wc -l)
        if [ "$profile_count" -gt 0 ]; then
            pass "~/camera_profiles/ has $profile_count XML profile(s)"
        else
            warn "~/camera_profiles/ exists but empty (run: camtool.py pull <camera>)"
        fi
    else
        fail "~/camera_profiles/ not found"
    fi

    # Day/night profile switching — verify the paths declared in
    # /etc/orc-capture.conf actually point at existing files. The
    # profile-night XML is auto-synced in run_overlay_files; the day
    # profile (typically ~/camera_profiles/common/image.xml) is operator-
    # populated and only warned on if missing so we don't clobber edits.
    local day_path night_path
    day_path=$(grep "^DAY_PROFILE_PATH=" /etc/orc-capture.conf 2>/dev/null | cut -d= -f2 | sed 's/#.*//' | xargs || true)
    night_path=$(grep "^NIGHT_PROFILE_PATH=" /etc/orc-capture.conf 2>/dev/null | cut -d= -f2 | sed 's/#.*//' | xargs || true)
    if [ -n "$day_path" ]; then
        if [ -f "$day_path" ]; then
            pass "DAY_PROFILE_PATH points at existing file ($day_path)"
        else
            warn "DAY_PROFILE_PATH ($day_path) does not exist — day profile push will fail"
        fi
    else
        warn "DAY_PROFILE_PATH not set in /etc/orc-capture.conf"
    fi
    if [ -n "$night_path" ]; then
        if [ -f "$night_path" ]; then
            pass "NIGHT_PROFILE_PATH points at existing file ($night_path)"
        else
            fail "NIGHT_PROFILE_PATH ($night_path) does not exist — night profile push will fail"
        fi
    else
        warn "NIGHT_PROFILE_PATH not set in /etc/orc-capture.conf"
    fi

    # orc-camera-profile-switch should be in PATH after overlay sync
    if command -v orc-camera-profile-switch >/dev/null 2>&1; then
        pass "orc-camera-profile-switch found at $(command -v orc-camera-profile-switch)"
    else
        fail "orc-camera-profile-switch not found in PATH (day/night profile switching disabled)"
    fi
}

# ─── Hardware (check only) ─────────────────────────────────────────
run_hardware() {
    section "Hardware"

    # Pi 5 model
    local pi_model
    pi_model=$(tr -d '\0' < /proc/device-tree/model 2>/dev/null || echo "unknown")
    if echo "$pi_model" | grep -q "Pi 5"; then
        pass "Raspberry Pi 5 detected ($pi_model)"
    else
        warn "Expected Pi 5, found: $pi_model"
    fi

    # USB flash drive
    if lsblk -o NAME,MODEL 2>/dev/null | grep -qi "FIT.*Plus\|Samsung.*FIT\|SanDisk.*3\.2"; then
        local usb_model
        usb_model=$(lsblk -o MODEL -n /dev/sda 2>/dev/null | xargs || true)
        pass "USB flash drive detected (${usb_model:-unknown})"
    elif [ -b /dev/sda ]; then
        local usb_model
        usb_model=$(lsblk -o MODEL -n /dev/sda 2>/dev/null | xargs || true)
        warn "USB block device found but unrecognized model: ${usb_model:-unknown}"
    else
        warn "No USB storage device detected"
    fi

    # LTE modem — deployed: Huawei ME906s (12d1:15c1); spare: Quectel EG25-G (2c7c:0125)
    local mm_list
    mm_list=$(mmcli -L 2>/dev/null || true)
    local lsusb_out
    lsusb_out=$(lsusb 2>/dev/null || true)
    if echo "$mm_list" | grep -qi "huawei\|ME906"; then
        pass "LTE modem detected (Huawei ME906s)"
    elif echo "$mm_list" | grep -qi "quectel\|EG25"; then
        pass "LTE modem detected (Quectel EG25-G)"
    elif echo "$mm_list" | grep -q "/Modem/"; then
        pass "LTE modem detected via ModemManager ($(echo "$mm_list" | head -1 | xargs))"
    elif echo "$lsusb_out" | grep -qi "12d1:15c1\|huawei"; then
        warn "Huawei USB device found but ModemManager doesn't see it yet"
    elif echo "$lsusb_out" | grep -qi "2c7c\|quectel"; then
        warn "Quectel USB device found but ModemManager doesn't see it yet"
    else
        fail "LTE modem not detected (expected Huawei ME906s or Quectel EG25-G)"
    fi

    # I2C bus + sensors
    local i2c_scan=""
    if [ -e /dev/i2c-1 ]; then
        pass "I2C bus available (/dev/i2c-1)"
        if command -v i2cdetect >/dev/null 2>&1; then
            i2c_scan=$(i2cdetect -y 1 2>/dev/null || true)
            if echo "$i2c_scan" | grep -q "44"; then
                pass "SHT40 sensor detected on I2C (0x44)"
            else
                warn "I2C available but SHT40 (0x44) not detected"
            fi
            if echo "$i2c_scan" | grep -q "51"; then
                pass "Witty Pi 5 HAT+ detected on I2C (0x51)"
            else
                fail "Witty Pi 5 HAT+ NOT detected on I2C (0x51) — check GPIO header seating and CR2032 battery"
            fi
        fi
    else
        fail "I2C bus not available (/dev/i2c-1 missing — check dtparam=i2c_arm=on in config.txt)"
    fi

    # DS18B20 on 1-Wire
    if ls /sys/bus/w1/devices/28-* >/dev/null 2>&1; then
        pass "DS18B20 temperature probe detected on 1-Wire bus"
    else
        warn "DS18B20 not detected on 1-Wire bus (check GPIO 4 + 4.7k pull-up)"
    fi

    # RG-15 rain gauge on UART (ttyAMA0)
    if [ -c /dev/ttyAMA0 ]; then
        # Query gauge: send R, read response
        local rg15_response=""
        if command -v python3 >/dev/null 2>&1; then
            rg15_response=$(python3 -c "
import serial, time
try:
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=3)
    ser.reset_input_buffer()
    ser.write(b'R\n')
    time.sleep(0.5)
    print(ser.read(256).decode('ascii', errors='replace').strip())
    ser.close()
except Exception as e:
    print(f'ERROR:{e}')
" 2>/dev/null || true)
        fi

        if [ -z "$rg15_response" ]; then
            warn "RG-15: no response on /dev/ttyAMA0 (gauge not connected or pyserial missing)"
        elif echo "$rg15_response" | grep -q "^ERROR:"; then
            warn "RG-15: UART error — ${rg15_response#ERROR:}"
        elif echo "$rg15_response" | grep -q " mm"; then
            pass "RG-15 rain gauge responding in metric mode ($rg15_response)"
        elif echo "$rg15_response" | grep -q " in"; then
            if [ "$FIXING" -eq 1 ]; then
                # Send M command to switch to metric (persists in EEPROM)
                python3 -c "
import serial, time
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=3)
ser.write(b'M\n')
time.sleep(0.5)
ser.close()
" 2>/dev/null
                fixed "RG-15: switched to metric mode (mm) — stored in gauge EEPROM"
            else
                fail "RG-15 responding in imperial units (inches) — need metric (mm)"
            fi
        else
            warn "RG-15: unexpected response format: $rg15_response"
        fi
    else
        warn "RG-15: /dev/ttyAMA0 not available (check UART config in config.txt)"
    fi

    # Witty Pi 5 RTC drift (check only — fix is in run_witty_pi)
    # Skipped here if already covered in run_witty_pi

    # usb_max_current_enable in config.txt
    if grep -q "^usb_max_current_enable=1" /boot/firmware/config.txt 2>/dev/null; then
        pass "usb_max_current_enable=1 in config.txt"
    else
        if [ -f /etc/udev/rules.d/90-qemu.rules ]; then
            warn "usb_max_current_enable=1 not verified (config.txt not accessible — 90-qemu.rules)"
        else
            fail "usb_max_current_enable=1 missing from config.txt (modem may trigger USB over-current)"
        fi
    fi

    # /boot/firmware mounted
    if mountpoint -q /boot/firmware 2>/dev/null; then
        pass "/boot/firmware mounted"
    else
        if [ -f /etc/udev/rules.d/90-qemu.rules ]; then
            warn "/boot/firmware not mounted (expected — 90-qemu.rules remaps mmcblk0 to USB)"
        else
            fail "/boot/firmware not mounted (config.txt inaccessible)"
        fi
    fi
}

# ─── Network (check only) ─────────────────────────────────────────
run_network() {
    section "Network"

    # eth0 IP
    local eth0_ip
    eth0_ip=$(ip -4 -o addr show eth0 2>/dev/null | awk '{print $4}')
    if [ -n "$eth0_ip" ]; then
        if echo "$eth0_ip" | grep -q "192.168.50.1/24"; then
            pass "eth0: $eth0_ip"
        else
            warn "eth0: $eth0_ip (expected 192.168.50.1/24)"
        fi
    else
        warn "eth0: no IP address (PoE relay may be off — normal if relay is off)"
    fi

    # PoE relay state (GPIO 24)
    local poe_state
    poe_state=$(pinctrl get 24 2>/dev/null || true)
    if echo "$poe_state" | grep -q "| --"; then
        pinctrl set 24 ip 2>/dev/null || true
        poe_state=$(pinctrl get 24 2>/dev/null || true)
    fi
    if echo "$poe_state" | grep -q "| hi"; then
        pass "PoE relay: ON (GPIO 24 HIGH)"
    elif echo "$poe_state" | grep -q "| lo"; then
        warn "PoE relay: OFF (GPIO 24 LOW) — camera/eth0 unpowered"
    else
        warn "PoE relay: unknown state (GPIO 24 not readable)"
    fi

    # Camera reachability via DHCP leases
    local lease_file="/var/lib/misc/dnsmasq.leases"
    if [ -n "$eth0_ip" ]; then
        local found_camera=0
        if [ -f "$lease_file" ]; then
            while read -r _ts mac cam_ip _hostname _id; do
                [ "$cam_ip" = "192.168.50.1" ] && continue
                if ping -c 1 -W 2 "$cam_ip" >/dev/null 2>&1; then
                    pass "Camera at $cam_ip ($mac): reachable"
                else
                    warn "Camera at $cam_ip ($mac): DHCP lease active but not responding"
                fi
                found_camera=1
            done < "$lease_file"
        fi
        [ "$found_camera" -eq 0 ] && warn "No DHCP leases — no cameras detected on eth0"

        # Camera supplement light check (ANNKE C1200 reverts to eventIntelligence on power cycle)
        local cam_pass=""
        for f in ~pi/.orc_deploy_*; do
            [ -f "$f" ] || continue
            cam_pass=$(grep "^BASE_PASSWD=" "$f" 2>/dev/null | cut -d= -f2 || true)
            break
        done
        if [ -n "$cam_pass" ] && [ -f "$lease_file" ]; then
            while read -r _ts _mac cam_ip _hostname _id; do
                [ "$cam_ip" = "192.168.50.1" ] && continue
                if ping -c 1 -W 1 "$cam_ip" >/dev/null 2>&1; then
                    local light_mode
                    light_mode=$(curl -s --digest -u "admin:${cam_pass}" \
                        "http://${cam_ip}/ISAPI/Image/channels/1" 2>/dev/null \
                        | grep -o '<supplementLightMode>[^<]*</supplementLightMode>' \
                        | sed 's/<[^>]*>//g' || true)
                    if [ "$light_mode" = "irLight" ]; then
                        pass "Camera $cam_ip: supplementLightMode = irLight"
                    elif [ -n "$light_mode" ]; then
                        fail "Camera $cam_ip: supplementLightMode = $light_mode (should be irLight — white LED flash risk)"
                    fi
                fi
            done < "$lease_file"
        fi
    else
        warn "Skipping camera checks (eth0 has no IP)"
    fi
}

# ─── ORC-OS (check only) ──────────────────────────────────────────
run_orc_os() {
    section "ORC-OS"

    # orc-api service
    if systemctl is-active --quiet orc-api 2>/dev/null; then
        pass "orc-api service active"
    else
        fail "orc-api service not active"
    fi

    # API responds on port 5000
    if curl -s --max-time 5 http://localhost:5000 >/dev/null 2>&1; then
        pass "ORC-OS API responds on port 5000"
    else
        warn "ORC-OS API not responding on port 5000 (service may still be starting)"
    fi
}

# ─── Remote access (check only) ───────────────────────────────────
run_remote_access() {
    section "Remote Access"

    # deploy.sh typically runs under sudo, whose PATH excludes pi's ~/.local/bin etc.
    # Check current PATH, then look in pi's home directly.
    local newt_path=""
    if command -v newt >/dev/null 2>&1; then
        newt_path=$(command -v newt)
    else
        for p in ~pi/.local/bin/newt ~pi/bin/newt /opt/newt/newt; do
            if [ -x "$p" ]; then newt_path="$p"; break; fi
        done
    fi
    if [ -n "$newt_path" ]; then
        pass "newt binary available ($newt_path)"
    else
        warn "newt not found (Pangolin remote access unavailable)"
    fi
}

# ══════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════

run_all_checks() {
    run_packages
    run_overlay_files
    run_directories
    run_config_txt
    run_system_config
    run_witty_pi
    run_power_button
    run_services
    run_credentials
    run_config_checks
    run_hardware
    run_network
    run_orc_os
    run_remote_access
}

print_summary() {
    local mode="$1"
    printf "\n" | tee -a "$REPORT_FILE"
    printf "═══════════════════════════════════\n" | tee -a "$REPORT_FILE"
    if [ "$mode" = "fix" ]; then
        printf "  \033[32mPASS\033[0m: %-4d  \033[36mFIXD\033[0m: %-4d  \033[33mWARN\033[0m: %d\n" \
            "$PASS" "$FIXED" "$WARN"
        printf "  PASS: %-4d  FIXD: %-4d  WARN: %d\n" \
            "$PASS" "$FIXED" "$WARN" >> "$REPORT_FILE"
    else
        printf "  \033[32mPASS\033[0m: %-4d  \033[31mFAIL\033[0m: %-4d  \033[33mWARN\033[0m: %d\n" \
            "$PASS" "$FAIL" "$WARN"
        printf "  PASS: %-4d  FAIL: %-4d  WARN: %d\n" \
            "$PASS" "$FAIL" "$WARN" >> "$REPORT_FILE"
    fi
    printf "═══════════════════════════════════\n" | tee -a "$REPORT_FILE"
}

# ── Phase 1: Check pass ────────────────────────────────────────────
FIXING=0
reset_counters

echo "" | tee -a "$REPORT_FILE"
echo "=== Check Phase ===" | tee -a "$REPORT_FILE"

run_all_checks

# Capture check-phase counts before reset
CHECK_PASS=$PASS
CHECK_FAIL=$FAIL
CHECK_WARN=$WARN
CHECK_FAILURES=("${FAILURES[@]+"${FAILURES[@]}"}")

print_summary "check"

# ── No failures: done ─────────────────────────────────────────────
if [ "$CHECK_FAIL" -eq 0 ]; then
    if [ "$CHECK_WARN" -gt 0 ]; then
        echo "" | tee -a "$REPORT_FILE"
        echo "Warnings are informational — review but may not need action." | tee -a "$REPORT_FILE"
    fi
    echo "" | tee -a "$REPORT_FILE"
    echo "All checks passed." | tee -a "$REPORT_FILE"
    echo "Report: $REPORT_FILE"
    exit 0
fi

# ── Print fixes needed ────────────────────────────────────────────
echo "" | tee -a "$REPORT_FILE"
echo "Fixes needed:" | tee -a "$REPORT_FILE"
for i in "${!CHECK_FAILURES[@]}"; do
    printf "  %d. %s\n" "$((i+1))" "${CHECK_FAILURES[$i]}" | tee -a "$REPORT_FILE"
done

# ── --check flag: exit without fixing ────────────────────────────
if [ "$CHECK_ONLY" -eq 1 ]; then
    echo "" | tee -a "$REPORT_FILE"
    echo "Check-only mode (--check). Run without --check to apply fixes." | tee -a "$REPORT_FILE"
    echo "Report: $REPORT_FILE"
    exit 1
fi

# ── Prompt (unless --yes) ─────────────────────────────────────────
if [ "$AUTO_YES" -eq 0 ]; then
    echo ""
    printf "Apply %d fix(es)? [y/N] " "$CHECK_FAIL"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Aborted. No changes made."
        exit 1
    fi
fi

# ── Phase 2: Fix pass ─────────────────────────────────────────────
FIXING=1
reset_counters

echo "" | tee -a "$REPORT_FILE"
echo "=== Fix Phase ===" | tee -a "$REPORT_FILE"

run_all_checks

print_summary "fix"

# ── Final status ──────────────────────────────────────────────────
echo "" | tee -a "$REPORT_FILE"
if [ "$FAIL" -eq 0 ]; then
    echo "All failures resolved." | tee -a "$REPORT_FILE"
else
    echo "WARNING: $FAIL failure(s) remain after fix pass — manual intervention required." | tee -a "$REPORT_FILE"
    echo "" | tee -a "$REPORT_FILE"
    echo "Remaining failures:" | tee -a "$REPORT_FILE"
    for i in "${!FAILURES[@]}"; do
        printf "  %d. %s\n" "$((i+1))" "${FAILURES[$i]}" | tee -a "$REPORT_FILE"
    done
fi

if [ "$BACKUP_CREATED" -eq 1 ]; then
    echo "" | tee -a "$REPORT_FILE"
    echo "Backup: $BACKUP_DIR" | tee -a "$REPORT_FILE"
fi
echo "Report: $REPORT_FILE" | tee -a "$REPORT_FILE"

echo "" | tee -a "$REPORT_FILE"
echo "Next steps:" | tee -a "$REPORT_FILE"
echo "  1. Set root password: sudo passwd root" | tee -a "$REPORT_FILE"
echo "  2. Set camera credentials (as pi user): echo 'BASE_PASSWD=<password>' > ~pi/.orc_deploy_$SITE" | tee -a "$REPORT_FILE"
echo "  3. Verify camera network: ping 192.168.50.100 (after PoE relay on)" | tee -a "$REPORT_FILE"
echo "  4. Configure camera via camtool.py (if camera replaced)" | tee -a "$REPORT_FILE"
echo "  5. Open ORC-OS web UI and configure:" | tee -a "$REPORT_FILE"
echo "     - Disk management, LiveORC callback URL, daemon settings" | tee -a "$REPORT_FILE"
echo "     - Services > capture: Enable, then Start" | tee -a "$REPORT_FILE"
echo "     - Pangolin remote access (server URL, not proxy URL)" | tee -a "$REPORT_FILE"
echo "  6. Reboot and verify: sudo reboot" | tee -a "$REPORT_FILE"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
