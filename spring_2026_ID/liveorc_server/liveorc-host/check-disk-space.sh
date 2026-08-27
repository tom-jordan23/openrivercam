#!/bin/bash
# Disk-space check for the LiveORC host.
#
# Installed at /usr/local/bin/check-disk-space.sh, run by disk-space-check.timer.
#
# The absence of any disk monitoring is why the 2026-08-10 outage ran for ten
# weeks: 26 GB of video accumulated in a container writable layer, filled the
# root volume, and the first symptom anyone saw was the host being unreachable.
#
# Emits a CloudWatch metric when it can (namespace ORC/Disk, metric
# UsedPercent, dimension MountPoint) so an alarm can be attached, and always
# logs to the journal. Journal output alone is not an alarm — see the runbook
# follow-up about wiring an SNS notification to the CloudWatch alarm.

WARN_PCT="${WARN_PCT:-75}"
CRIT_PCT="${CRIT_PCT:-85}"
MOUNTS="${MOUNTS:-/ /var/lib/liveorc-media}"

rc=0

for mp in $MOUNTS; do
    mountpoint -q "$mp" 2>/dev/null || [ "$mp" = "/" ] || {
        echo "WARNING: $mp is not a mount point - media may be on the root disk" >&2
        rc=1
        continue
    }

    pct=$(df --output=pcent "$mp" 2>/dev/null | tail -1 | tr -dc '0-9')
    [ -n "$pct" ] || { echo "ERROR: could not read usage for $mp" >&2; rc=1; continue; }

    avail=$(df -h --output=avail "$mp" 2>/dev/null | tail -1 | tr -d ' ')

    if [ "$pct" -ge "$CRIT_PCT" ]; then
        echo "CRITICAL: $mp is ${pct}% full (${avail} free, threshold ${CRIT_PCT}%)" >&2
        rc=2
    elif [ "$pct" -ge "$WARN_PCT" ]; then
        echo "WARNING: $mp is ${pct}% full (${avail} free, threshold ${WARN_PCT}%)" >&2
        [ "$rc" -lt 1 ] && rc=1
    else
        echo "OK: $mp is ${pct}% full (${avail} free)"
    fi

    # Best effort. No credentials or no permission must not fail the check.
    aws cloudwatch put-metric-data \
        --namespace ORC/Disk \
        --metric-name UsedPercent \
        --unit Percent \
        --value "$pct" \
        --dimensions MountPoint="$mp" \
        --region us-east-1 >/dev/null 2>&1 \
        || echo "note: could not publish CloudWatch metric for $mp (metric-only alarms unavailable)"
done

exit $rc
