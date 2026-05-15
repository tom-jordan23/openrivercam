"""Sensor CSV upload endpoint for ORC stations.

Stations PUT files to /sensors/upload/<station>/<filename> with a per-station
bearer token. Files are written atomically (tmp + rename) under
ORC_SENSORS_DIR/<station>/.

Environment:
    ORC_SENSORS_DIR     Filesystem root for uploaded files. Default /var/orc/sensors.
    ORC_UPLOAD_TOKENS   Comma-separated station:token pairs.
                        Example: sukabumi:abc123,jakarta:def456
"""
import logging
import os
import re
import secrets
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request

LOG = logging.getLogger("sensor-upload")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

UPLOAD_ROOT = Path(os.environ.get("ORC_SENSORS_DIR", "/var/orc/sensors"))

TOKENS: dict[str, str] = {}
for pair in os.environ.get("ORC_UPLOAD_TOKENS", "").split(","):
    pair = pair.strip()
    if not pair or ":" not in pair:
        continue
    station, token = pair.split(":", 1)
    TOKENS[station.strip()] = token.strip()

if not TOKENS:
    LOG.warning("ORC_UPLOAD_TOKENS empty — no stations can authenticate")
else:
    LOG.info("loaded tokens for stations: %s", sorted(TOKENS))

try:
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
except OSError as e:
    # In production the host bind-mount supplies UPLOAD_ROOT pre-created with
    # the right ownership; we shouldn't crash here if that didn't happen.
    # Per-upload mkdir will retry and surface the error per-request.
    LOG.warning("could not create UPLOAD_ROOT=%s at startup (%s); upload requests will retry", UPLOAD_ROOT, e)

STATION_RE = re.compile(r"^[a-z][a-z0-9-]{1,30}$")
FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")

app = FastAPI(title="ORC sensor upload", docs_url=None, redoc_url=None)


def _check_auth(station: str, authorization: Optional[str]) -> None:
    expected = TOKENS.get(station)
    if not expected:
        raise HTTPException(status_code=401, detail="unknown station")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    presented = authorization[len("Bearer "):]
    if not secrets.compare_digest(presented, expected):
        raise HTTPException(status_code=401, detail="bad token")


@app.put("/sensors/upload/{station}/{filename}")
async def upload(
    station: str,
    filename: str,
    request: Request,
    authorization: Optional[str] = Header(default=None),
):
    if not STATION_RE.match(station):
        raise HTTPException(status_code=400, detail="invalid station name")
    if not FILENAME_RE.match(filename) or ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="invalid filename")
    _check_auth(station, authorization)

    target_dir = UPLOAD_ROOT / station
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / filename
    tmp = target.with_suffix(target.suffix + ".tmp")

    size = 0
    try:
        with tmp.open("wb") as fp:
            async for chunk in request.stream():
                fp.write(chunk)
                size += len(chunk)
        os.replace(tmp, target)
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
        raise

    client = request.client.host if request.client else "?"
    LOG.info("upload ok station=%s file=%s size=%d from=%s", station, filename, size, client)
    return {"ok": True, "station": station, "filename": filename, "size": size}


@app.get("/sensors/health")
def health():
    return {"ok": True, "stations": sorted(TOKENS)}
