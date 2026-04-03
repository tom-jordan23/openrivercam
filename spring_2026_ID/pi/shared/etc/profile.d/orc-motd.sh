#!/bin/sh
# Show ORC station status on every interactive shell
# (update-motd.d scripts don't auto-run on Raspberry Pi OS / Debian)
#
# Sourced from /etc/bash.bashrc (all interactive shells), not profile.d
# (login shells only). Guard with ORC_MOTD_SHOWN to avoid double-fire
# when bash.bashrc and profile both run on login.
if [ -n "$PS1" ] && [ -z "$ORC_MOTD_SHOWN" ] && [ -d /etc/update-motd.d ]; then
    cat /etc/motd 2>/dev/null
    run-parts /etc/update-motd.d/ 2>/dev/null
    export ORC_MOTD_SHOWN=1
fi
