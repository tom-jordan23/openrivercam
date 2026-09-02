#!/usr/bin/env python3
"""A LiveORC stand-in, just enough of it to exercise ORC-OS 0.6.0's sync path.

WHY NOT A REAL LiveORC
    The question is about MECHANISM - does flipping FAILED->QUEUE get picked up,
    in what order, and what happens to rows when the process dies mid-batch.
    A real LiveORC answers none of that better than a stub, and a stub can do
    something the real one cannot: hold each upload for a configurable delay, so
    a localhost test can imitate the 5.3 s a 9.2 MB clip actually takes over the
    Telkomsel link. Throughput is field-bound and is NOT what this measures.

ENDPOINTS  (taken from callback_url.py and video.sync_remote)
    POST /api/token/          -> access + refresh
    POST /api/token/refresh/  -> access + refresh
    GET  /api/version         -> version probe
    POST /api/video/          -> the upload. Sleeps UPLOAD_DELAY, returns an id.
                                 Fails every FAIL_EVERY-th request if asked, so
                                 the FAILED path can be exercised too.
"""
import json, os, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "5.3"))   # field-measured per clip
FAIL_EVERY = int(os.getenv("FAIL_EVERY", "0"))           # 0 = never fail
PORT = int(os.getenv("PORT", "8099"))

_lock = threading.Lock()
_next_id = [9000]
_seen = []


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass  # the transcript below is the record, not access logs

    def do_GET(self):
        if self.path.rstrip("/").endswith("/api/version"):
            return self._send(200, {"version": "0.3.0"})
        return self._send(200, {})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        p = self.path.rstrip("/")

        if p.endswith("/api/token") or p.endswith("/api/token/refresh"):
            return self._send(200, {"access": "test-access-token", "refresh": "test-refresh-token"})

        if "/video" in p:
            with _lock:
                idx = len(_seen) + 1
                _next_id[0] += 1
                vid = _next_id[0]
            # Imitate the link: hold the connection for the transfer time.
            time.sleep(UPLOAD_DELAY)
            fail = FAIL_EVERY and (idx % FAIL_EVERY == 0)
            stamp = time.strftime("%H:%M:%S")
            # Recover the clip's timestamp from the multipart body so the ORDER
            # of arrival can be read off the transcript - that is the point.
            ts = ""
            try:
                s = raw.decode("latin-1")
                k = s.find('name="timestamp"')
                if k > 0:
                    ts = s[k:k + 200].split("\r\n\r\n")[1].split("\r\n")[0]
            except Exception:
                pass
            with _lock:
                _seen.append((stamp, ts, "FAIL" if fail else "ok"))
            print(f"{stamp}  #{idx:<3} {ts:<22} {'-> 500 FAIL' if fail else '-> 201 ok  id=' + str(vid)}",
                  flush=True)
            if fail:
                return self._send(500, {"detail": "induced failure"})
            return self._send(201, {"id": vid, "timestamp": ts or "2026-01-01T00:00:00Z", "status": 4})

        return self._send(200, {})


if __name__ == "__main__":
    print(f"mock LiveORC on :{PORT}  upload_delay={UPLOAD_DELAY}s  fail_every={FAIL_EVERY or 'never'}",
          flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
