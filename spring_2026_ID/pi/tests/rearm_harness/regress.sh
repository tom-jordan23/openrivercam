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
scn "R01 healthy, fresh stamp -> not due" 3600 "$C" X=1
scn "R02 stamp 24h old -> re-arm" $D "$C" X=1
scn "R03 no stamp -> re-arm" none "$C" X=1
scn "R04 not in use -> re-arm then abort" 3600 "$C" F_INUSE=0
scn "R05 wrong version" $D "$C" F_VERSION=5.1.0
scn "R06 script absent" $D 'SCHEDULE_SCRIPT=nope.wpi\n' X=1
scn "R07 duplicate names" $D "$C" F_SCRIPTS=prod_30.wpi,prod_30.wpi
scn "R08 prefix name only" $D "$C" F_SCRIPTS=prod_30.wpi.bak,maint.wpi
scn "R09 case variant" $D "$C" F_SCRIPTS=PROD_30.WPI,maint.wpi
scn "R10 regex chars in name" $D 'SCHEDULE_SCRIPT=prod+30.wpi\n' F_SCRIPTS=prod+30.wpi,x
scn "R11 regex char only matches as regex (prod_3.wpi vs prod_30.wpi)" $D 'SCHEDULE_SCRIPT=prod_3.wpi\n' F_SCRIPTS=prod_30.wpi,x
scn "R12 item number 10" $D "$C" F_SCRIPTS=a,b,c,d,e,f,g,h,i,prod_30.wpi
scn "R13 REARM_INTERVAL_H=abc" 3600 "${C}REARM_INTERVAL_H=abc\n" X=1
scn "R14 conf missing" $D NOCONF X=1
scn "R15 empty SCHEDULE_SCRIPT" $D 'SCHEDULE_SCRIPT=\n' X=1

