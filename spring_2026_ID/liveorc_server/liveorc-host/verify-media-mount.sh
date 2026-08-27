#!/bin/bash
# Verify the LiveORC media volume is mounted and writable before starting
# dependent services.
#
# Installed at /usr/local/bin/verify-media-mount.sh
#
# Replaces verify-s3mount.sh, which guarded /mnt/s3-storage — a 4 KB s3fs mount
# nothing used — while the real media path had no guard at all. That inversion
# is why ten weeks of uploads went into a container writable layer without one
# error being raised.

check_mount() {
    local mount_point="$1"

    if ! mountpoint -q "$mount_point"; then
        echo "Mount point $mount_point not mounted"
        return 1
    fi

    # The write test matters as much as the mountpoint check: systemd's
    # AssertPathIsMountPoint cannot detect a mount that is present but
    # read-only, which is what ext4 does when it hits errors.
    if ! touch "$mount_point/.test" 2>/dev/null; then
        echo "Mount point $mount_point not writable"
        return 1
    fi

    rm -f "$mount_point/.test"
    echo "Mount point $mount_point verified successfully"
    return 0
}

check_mount "/var/lib/liveorc-media" || exit 1
