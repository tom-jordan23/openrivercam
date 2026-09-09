#!/usr/bin/env python3
"""
fetch_timeseries.py — pull discharge and water-level time series out of
LiveOpenRiverCam over the REST API.

Written for IPB University's dashboard work. Standard library only: no pip
install, runs on any Python 3.9+.

WHAT IT DOES
    1. Exchanges an email + password for a JWT access token.
    2. Lists the sites the account can see (this is where the ?institute=
       parameter matters — see the README).
    3. Pulls the time series for one site, optionally bounded by a date range.
    4. Writes CSV to stdout or to a file.

WHAT IT DELIBERATELY DOES NOT DO
    It never downloads video or image bytes. Serving media through LiveORC is
    expensive per byte and a bulk pull has taken the server down before. Time
    series and metadata are cheap; media is not. See the README.

USAGE
    export LIVEORC_EMAIL='ipb-dashboard@liveorc.local'
    read -rs LIVEORC_PASSWORD && export LIVEORC_PASSWORD

    # everything at the Sukabumi site, as CSV on stdout
    ./fetch_timeseries.py --site 4

    # one month, only the columns a dashboard usually wants, to a file
    ./fetch_timeseries.py --site 4 \
        --start 2026-08-01 --end 2026-09-01 \
        --fields timestamp,h,q_50,q_05,q_95 \
        --out sukabumi-august.csv

    # what sites does this account see?
    ./fetch_timeseries.py --list-sites

    # raw JSON instead of CSV, for a loader that wants to parse it
    ./fetch_timeseries.py --site 4 --json

INCREMENTAL PULLS
    A dashboard should not re-download the whole record on every refresh. Keep
    the timestamp of the newest row you hold and pass it as --start next time:

        ./fetch_timeseries.py --site 4 --start 2026-09-08T06:00:00Z

    The bound is inclusive on both ends, so drop or de-duplicate the first row.
    A pull that finds nothing new writes a header-only CSV rather than an empty
    file, so a loader reading it sees zero rows instead of a parse error.
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("LIVEORC_BASE", "https://openrivercam.endlessprojects.info")

# The account is a member of exactly one institute. GET /api/site/ returns an
# empty list without this parameter, which looks identical to "there is no
# data". It is not optional.
INSTITUTE = int(os.environ.get("LIVEORC_INSTITUTE", "1"))

TIMEOUT = 60

# Columns worth plotting, in a sensible order. The API returns more than this;
# pass --fields to choose your own, or --fields '' for everything.
DEFAULT_FIELDS = "timestamp,h,q_50,q_05,q_25,q_75,q_95,q_raw,v_av,v_bulk,fraction_velocimetry"


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def request(path, token=None, params=None, method="GET", body=None):
    """One HTTP call. Returns (status, parsed-or-raw-body)."""
    url = BASE.rstrip("/") + path
    if params:
        # drop empty values so an unset --start does not become ?startDateTime=
        params = {k: v for k, v in params.items() if v not in (None, "")}
        if params:
            url += "?" + urllib.parse.urlencode(params)

    data = json.dumps(body).encode() if body is not None else None
    headers = {"Accept": "application/json"}
    if data:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode()
            ctype = resp.headers.get("Content-Type", "")
            if "json" in ctype:
                return resp.status, json.loads(raw)
            return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        try:
            return exc.code, json.loads(raw)
        except ValueError:
            return exc.code, raw
    except urllib.error.URLError as exc:
        die(f"could not reach {BASE}: {exc.reason}")


def get_token():
    """Exchange credentials for a JWT pair.

    Note the login field is `email`, not `username`. The access token is valid
    for 6 hours; POST /api/token/refresh/ with the refresh token renews it.
    A long-running dashboard should refresh rather than re-send the password.
    """
    email = os.environ.get("LIVEORC_EMAIL")
    password = os.environ.get("LIVEORC_PASSWORD")
    if not email or not password:
        die("set LIVEORC_EMAIL and LIVEORC_PASSWORD in the environment")

    status, payload = request(
        "/api/token/", method="POST", body={"email": email, "password": password}
    )
    if status != 200:
        die(f"authentication failed ({status}): {payload}")
    return payload["access"], payload["refresh"]


def refresh_token(refresh):
    """Renew an expired access token.

    Refresh tokens rotate: the response carries a NEW refresh token and the one
    you sent is blacklisted. Always store what comes back.
    """
    status, payload = request(
        "/api/token/refresh/", method="POST", body={"refresh": refresh}
    )
    if status != 200:
        die(f"token refresh failed ({status}): {payload}")
    return payload["access"], payload.get("refresh", refresh)


def list_sites(token):
    status, payload = request("/api/site/", token=token, params={"institute": INSTITUTE})
    if status != 200:
        die(f"could not list sites ({status}): {payload}")
    return payload


def fetch_timeseries(token, site, start=None, end=None, fields=None):
    """GET /api/site/{site}/timeseries/.

    The endpoint is not paginated — the whole matching set comes back in one
    response — so bound it with --start/--end rather than pulling everything
    on every dashboard refresh.

    The date filters are camelCase (startDateTime / endDateTime), unlike every
    other parameter in the API. Both are inclusive.
    """
    params = {"startDateTime": start, "endDateTime": end}
    if fields:
        # drf-queryfields: trims the response to the columns you name
        params["fields"] = fields

    status, payload = request(
        f"/api/site/{site}/timeseries/", token=token, params=params
    )
    if status == 403:
        die(
            f"403 on site {site}. The account is not a member of the institute "
            f"that owns it. Check --site, and see the README on membership."
        )
    if status != 200:
        die(f"could not fetch time series ({status}): {payload}")
    return payload


def write_csv(rows, fields, handle):
    # honour the requested column order; fall back to whatever the API sent
    if fields:
        columns = [f for f in fields.split(",") if f]
    else:
        columns = list(rows[0].keys()) if rows else []

    if not columns:
        # nothing came back and --fields was cleared, so there is no way to know
        # what the columns should have been
        print("no rows matched, and no --fields to derive a header from",
              file=sys.stderr)
        return

    writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
    # header first, even with no rows: an incremental pull that finds nothing
    # new should produce a header-only file, not an empty one. A zero-byte file
    # makes csv.DictReader yield nothing and pandas raise EmptyDataError, so
    # "no new data" would look like a broken download.
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    if not rows:
        print("no rows matched — wrote the header only", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Pull LiveOpenRiverCam time series over the REST API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--site", type=int, help="site id (Sukabumi is 4)")
    parser.add_argument("--list-sites", action="store_true",
                        help="show the sites this account can read, then exit")
    parser.add_argument("--start", help="ISO 8601 lower bound, e.g. 2026-08-01 "
                                        "or 2026-08-01T00:00:00Z (inclusive)")
    parser.add_argument("--end", help="ISO 8601 upper bound (inclusive)")
    parser.add_argument("--fields", default=DEFAULT_FIELDS,
                        help="comma-separated columns; pass '' for all of them")
    parser.add_argument("--json", action="store_true",
                        help="emit raw JSON instead of CSV")
    parser.add_argument("--out", help="write to this file instead of stdout")
    args = parser.parse_args()

    if not args.site and not args.list_sites:
        parser.error("give --site, or --list-sites to find one")

    access, _refresh = get_token()

    if args.list_sites:
        sites = list_sites(access)
        if not sites:
            die(f"no sites visible for institute {INSTITUTE} — is the id right?")
        for site in sites:
            print(f"{site['id']}\t{site.get('name', '')}")
        return

    rows = fetch_timeseries(access, args.site, args.start, args.end, args.fields)
    print(f"{len(rows)} rows from site {args.site}", file=sys.stderr)

    handle = open(args.out, "w", newline="") if args.out else sys.stdout
    try:
        if args.json:
            json.dump(rows, handle, indent=2)
            handle.write("\n")
        else:
            write_csv(rows, args.fields, handle)
    finally:
        if args.out:
            handle.close()
            print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
