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
scn "T01 header cut inside RTC line, stamp fresh" 3600 "$C" F_CUT_HDR="RTC Time: 2026-11-04 10:0"
scn "T02 header cut before startup line, stamp fresh" 3600 "$C" F_CUT_HDR="Schedule next shutdown [04 10:25:00]"
scn "T03 header cut inside startup brackets, stamp fresh" 3600 "$C" F_CUT_HDR="Schedule next startup [05 10:3"
scn "T04 header cut before 'in use' line, stamp fresh" 3600 "$C" F_CUT_HDR="Schedule next startup [05 10:30:00]"
scn "T05 wp5 prints nothing, exit 0" $D "$C" F_CUT_HDR="< V" F_VERSION=
scn "T06 wp5 crashes (exit 139) after header" 3600 "$C" F_EXIT=139
scn "T07 list cut after '[1] prod_30.wpi' (real: prod_30.wpi.bak)" $D "$C" F_SCRIPTS=prod_30.wpi.bak,maint.wpi F_CUT_LIST="[1] prod_30.wpi"
scn "T08 list cut mid-name" $D "$C" F_CUT_LIST="[1] prod_3"
scn "T09 list cut before the scripts" $D "$C" F_CUT_LIST="on disk:"
scn "T10 list cut mid item number (item 12 -> '[1')" $D "$C" F_SCRIPTS=a,b,c,d,e,f,g,h,i,j,k,prod_30.wpi F_CUT_LIST="[11] k
 [1"
scn "T11 empty stamp" empty "$C" X=1
scn "T12 partial stamp (4 digits)" part "$C" X=1
scn "T13 stamp with trailing garbage" trail "$C" X=1
scn "T14 two-line stamp" multi "$C" X=1
scn "T15 stamp dir read-only (disk full / ro fs)" ro "$C" X=1
scn "T16 conf empty file" 3600 "" X=1
scn "T17 conf truncated mid-assignment" 86400 "SCHEDULE_SCRIPT=prod_3" X=1
scn "T18 conf quote left open" 86400 'SCHEDULE_SCRIPT="prod_30.wpi\n' X=1
scn "T19 conf value with space" 86400 'SCHEDULE_SCRIPT=my script.wpi\n' X=1
scn "T20 conf CRLF" 86400 'SCHEDULE_SCRIPT=prod_30.wpi\r\n' X=1
scn "T21 REARM_INTERVAL_H empty" 3600 "${C}REARM_INTERVAL_H=\n" X=1
scn "T22 REARM_INTERVAL_H negative" 3600 "${C}REARM_INTERVAL_H=-1\n" X=1
scn "T23 RTC year 2000 (dead RTC battery)" 3600 "$C" F_RTC="2000-01-01 00:00:05"
scn "T24 RTC impossible date" 3600 "$C" F_RTC="2026-13-45 99:99:99"
scn "T25 RTC time cut to date only" 3600 "$C" F_CUT_HDR="RTC Time: 2026-11-04"
