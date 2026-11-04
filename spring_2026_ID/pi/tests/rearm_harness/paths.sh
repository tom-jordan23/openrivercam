#!/bin/bash
H=$(dirname "$(readlink -f "$0")"); export PATH=$H/bin:$PATH H_JOURNAL=$H/run/journal H_STATE=$H/run/wpstate
T=$(date -u -d '2026-11-04 10:00:00' +%s)
scn() { # name stamp conf env...
  local name=$1 stamp=$2 conf=$3; shift 3
  rm -rf $H/run; mkdir -p $H/run/state; : > $H_JOURNAL; : > $H_STATE
  [ "$conf" != NOCONF ] && printf '%b' "$conf" > $H/run/conf
  case $stamp in none) ;; empty) : > $H/run/state/stamp;; part) printf '%s' "${T:0:4}" > $H/run/state/stamp;; trail) echo "$((T-90000))abc" > $H/run/state/stamp;; multi) printf '%s\n%s\n' $((T-90000)) $((T-10)) > $H/run/state/stamp;; ro) echo $((T-90000)) > $H/run/state/stamp; chmod 555 $H/run/state; chmod 444 $H/run/state/stamp;; *) echo $((T-stamp)) > $H/run/state/stamp;; esac
  env "$@" bash $H/rearm.sh >$H/run/stdout 2>&1; rc=$?
  echo "## $name  rc=$rc chose=[$(tr '\n' ';' < $H_STATE)] stamp=[$(cat $H/run/state/stamp 2>/dev/null | head -c 30 | tr '\n' '|')]"
  sed 's/^[^ ]* /     /' $H/run/last 2>/dev/null | cut -c1-200
  [ -s $H/run/stdout ] && sed 's/^/   OUT /' $H/run/stdout | head -3
  chmod -R u+w $H/run 2>/dev/null
}
C='SCHEDULE_SCRIPT=prod_30.wpi\n'; D=86400
scn "P1 path 1: after choose the header shows in-use but NO armed startup" $D "$C" F_STARTUP=""
scn "P2 path 2: wp5 killed by the 90 s timeout after the choice was sent" $D "$C" F_HANG=choose
