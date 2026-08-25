#!/usr/bin/env python3
"""probe_media_access.py — how does a JWT client actually fetch media bytes?

WHY
    The Phase 1 inventory measured zero bytes: all 9547 HEAD requests against the
    `file`/`keyframe`/`image`/`thumbnail` URLs returned no Content-Length, and
    unauthenticated those URLs 404 from Django while /media/admin-interface/ 403s
    from nginx. So nginx's media root does not contain the video tree — Django
    serves it through a view, and the suspicion is that view authenticates by
    SESSION COOKIE, not by the JWT the API issues.

    That distinction decides TODO-114's whole design. If the raw media URLs are
    unreachable with a token, the mirror must pull bytes through the DRF actions
    (/playback/, /image/, /thumbnail/) instead, and the manifest's asset URLs are
    identifiers rather than fetch targets.

WHAT IT TOUCHES
    Nothing. GET and HEAD only, against ONE video record, plus the token POST.
    It downloads at most 2 KB per URL — enough to identify the content, not
    enough to matter to the disk this workstream is about.

USAGE
    export LIVEORC_EMAIL=... LIVEORC_PASSWORD=...
    ./probe_media_access.py --site 4 --video-id 1480
"""

import argparse
import importlib.util
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

_spec = importlib.util.spec_from_file_location("orc_inventory", Path(__file__).with_name("orc_inventory.py"))
_inv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_inv)

SNIFF = 2048


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects are part of the answer here — a 302 to /accounts/login/ is the
    signature of a session-authenticated view rejecting a token client."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def probe(url, token=None, method="GET"):
    # The SSL context belongs to the handler: OpenerDirector.open() takes no
    # context= kwarg, unlike the urlopen() convenience wrapper.
    opener = urllib.request.build_opener(
        NoRedirect, urllib.request.HTTPSHandler(context=ssl.create_default_context())
    )
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with opener.open(req, timeout=60) as r:
            body = r.read(SNIFF) if method == "GET" else b""
            return r.status, dict(r.headers), body
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read(SNIFF)
        except Exception:
            pass
        return e.code, dict(e.headers or {}), body


def identify(body):
    """What did we actually get back — media, an HTML page, or a login form?"""
    if not body:
        return "(empty)"
    if body[:3] == b"\xff\xd8\xff":
        return "JPEG bytes"
    if body[4:8] == b"ftyp":
        return "MP4 bytes"
    if body[:8] == b"\x89PNG\r\n\x1a\n":
        return "PNG bytes"
    low = body[:600].lower()
    if b"<html" in low or b"<!doctype" in low:
        hint = ""
        if b"login" in low or b"password" in low:
            hint = " — LOGIN PAGE"
        elif b"not found" in low:
            hint = " — 404 page"
        return f"HTML{hint}"
    return f"other: {body[:40]!r}"


def show(label, url, token, method="GET"):
    status, headers, body = probe(url, token=token, method=method)
    cl = headers.get("Content-Length") or headers.get("content-length") or "-"
    ct = (headers.get("Content-Type") or headers.get("content-type") or "-").split(";")[0]
    loc = headers.get("Location") or headers.get("location")
    print(f"  {label:26s} {method:4s} {status:<4} len={cl:<12} {ct:<26} {identify(body)}")
    if loc:
        print(f"  {'':26s}      -> redirect: {loc}")
    return status, cl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--base", default=_inv.DEFAULT_BASE)
    args = ap.parse_args()

    email, password = os.environ.get("LIVEORC_EMAIL"), os.environ.get("LIVEORC_PASSWORD")
    if not email or not password:
        sys.exit("ERROR: set LIVEORC_EMAIL and LIVEORC_PASSWORD")

    api = _inv.Api(args.base, email, password)
    status, video = api.get_json(f"/api/site/{args.site}/video/{args.video_id}/")
    if status != 200 or not video:
        sys.exit(f"ERROR: could not read video {args.video_id} (HTTP {status})")

    print(f"\nVideo {args.video_id} at site {args.site}\n")

    print("A. Raw media URLs from the serializer, WITH the JWT")
    for field in _inv.ASSET_FIELDS:
        if video.get(field):
            show(field, video[field], api.access, method="HEAD")
            show(field, video[field], api.access, method="GET")
    print()

    print("B. Same URLs with NO credentials (for comparison)")
    for field in _inv.ASSET_FIELDS:
        if video.get(field):
            show(field, video[field], None, method="GET")
    print()

    print("C. DRF action routes, WITH the JWT")
    for action in ("playback", "image", "thumbnail"):
        url = f"{args.base}/api/site/{args.site}/video/{args.video_id}/{action}/"
        show(action, url, api.access, method="HEAD")
        show(action, url, api.access, method="GET")
    print()

    print("Read the 'identify' column: real bytes mean that route is a usable")
    print("fetch target for the mirror. HTML — especially a login page — means it")
    print("is not, whatever status code it returned.\n")


if __name__ == "__main__":
    main()
