#!/usr/bin/env python3
"""Mock of the LiveORC endpoints fetch_timeseries.py touches, matching the
response shapes verified against production on 2026-09-09.

WHY THIS EXISTS
    fetch_timeseries.py is provided to a partner, so its behaviour must be
    known before release. Every authenticated code path requires a credential,
    however, and testing those paths against production places load on a small
    instance for a question that does not concern the data itself.

    This serves the same shapes locally: [] for /api/site/ without ?institute,
    the timestamp/h/q_* row schema, startDateTime/endDateTime/fields filtering,
    401 without a bearer token, and 403 at a non-member site.

USAGE
    python3 mock_liveorc.py &
    export LIVEORC_BASE=http://127.0.0.1:8731
    export LIVEORC_EMAIL=any@example.local LIVEORC_PASSWORD=any
    ./fetch_timeseries.py --list-sites
    ./fetch_timeseries.py --site 4 --start 2026-08-08 --fields timestamp,h,q_50

    Rows span 2026-08-01 to 2026-08-10. A --start outside that range returns no
    rows, which exercises the header-only output case.

    Stop the server by port rather than by name: `pkill -f mock_liveorc.py`
    matches its own shell command line and terminates the calling shell.

This is a test fixture rather than something IPB requires. It is safe to
include, but it may be removed if the bundle should contain only the files in
active use.
"""
import json, datetime as dt
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

FIELDS = ["id","timestamp","h","q_05","q_25","q_50","q_75","q_95","q_raw",
          "v_av","v_bulk","wetted_surface","wetted_perimeter",
          "fraction_velocimetry","misc","creator","site","video"]

ROWS = []
base = dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc)
for i in range(40):
    t = base + dt.timedelta(hours=6*i)
    ROWS.append({
        "id": 5000+i, "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "h": round(1.10 + 0.01*i, 3), "q_05": 3.1, "q_25": 4.2,
        "q_50": round(5.0 + 0.05*i, 2), "q_75": 6.4, "q_95": 7.9,
        "q_raw": 5.5, "v_av": 0.61, "v_bulk": 0.48,
        "wetted_surface": 9.2, "wetted_perimeter": 11.4,
        "fraction_velocimetry": 0.83, "misc": None,
        "creator": 1, "site": 4, "video": 3000+i,
    })

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, code, payload, ctype="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path == "/api/token/":
            n = int(self.headers.get("Content-Length", 0))
            creds = json.loads(self.rfile.read(n) or b"{}")
            if not creds.get("email") or not creds.get("password"):
                return self._send(401, {"detail": "No active account found with the given credentials"})
            return self._send(200, {"access": "mock.access.token", "refresh": "mock.refresh.token"})
        self._send(404, {"detail": "Not found."})

    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            return self._send(401, {"detail": "Authentication credentials were not provided."})

        if u.path == "/api/site/":
            # returns [] unless ?institute is supplied
            if q.get("institute") != ["1"]:
                return self._send(200, [])
            return self._send(200, [{"id": 3, "name": "Jakarta"},
                                    {"id": 4, "name": "Sukabumi City"},
                                    {"id": 2, "name": "Test site"}])

        if u.path == "/api/site/4/timeseries/":
            rows = ROWS
            if "startDateTime" in q:
                rows = [r for r in rows if r["timestamp"] >= q["startDateTime"][0]]
            if "endDateTime" in q:
                rows = [r for r in rows if r["timestamp"] <= q["endDateTime"][0]]
            if "fields" in q:
                keep = [f for f in q["fields"][0].split(",") if f in FIELDS]
                rows = [{k: r[k] for k in keep} for r in rows]
            return self._send(200, rows)

        if u.path.startswith("/api/site/9"):
            return self._send(403, {"detail": "You do not have permission to perform this action"})
        self._send(404, {"detail": "Not found."})

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8731), H).serve_forever()
