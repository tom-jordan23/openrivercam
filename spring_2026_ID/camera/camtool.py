#!/usr/bin/env python3
"""Camera configuration management via Hikvision ISAPI.

Stores camera configs as XML files in git and can pull/push/diff/verify
them against live ANNKE C1200 (Hikvision OEM) cameras over HTTP.

Requires: requests (pip install requests)
"""

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

try:
    import xml.etree.ElementTree as ET
except ImportError:
    sys.exit("Fatal: xml.etree.ElementTree not available")

try:
    import requests
    from requests.auth import HTTPDigestAuth
except ImportError:
    sys.exit(
        "Missing dependency: requests\n"
        "Install with: pip install requests"
    )

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent

HIK_NS = "http://www.hikvision.com/ver20/XMLSchema"
ET.register_namespace("", HIK_NS)

ENDPOINTS = {
    "streaming_101":    "/ISAPI/Streaming/channels/101",
    "streaming_102":    "/ISAPI/Streaming/channels/102",
    "image":            "/ISAPI/Image/channels/1",
    "ircutfilter":      "/ISAPI/Image/channels/1/ircutFilter",
    "ispmode":          "/ISAPI/Image/channels/1/ISPMode",
    "time":             "/ISAPI/System/time",
    "ntp":              "/ISAPI/System/time/NtpServers/1",
    "overlays":         "/ISAPI/System/Video/inputs/channels/1/overlays",
    "ftp":              "/ISAPI/System/Network/ftp",
    "motion_detection": "/ISAPI/System/Video/inputs/channels/1/motionDetection",
}

# Fields that change every read — skip when comparing
VOLATILE_FIELDS = {"currentDeviceTime", "upTime", "bootTime"}

# Sensitive fields scrubbed on pull, injected on push
# Maps XML tag → env var name
SENSITIVE_FIELDS = {
    "password": "FTP_PASSWORD",
    "ftpPassword": "FTP_PASSWORD",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_env(env_path: Path) -> dict:
    """Load KEY=VALUE pairs from a .env file (no dependency)."""
    env = {}
    if not env_path.is_file():
        return env
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("\"'")
    return env


def get_password(args) -> str:
    """Resolve camera password: CLI flag > env var > .env file."""
    if args.password:
        return args.password
    if os.environ.get("CAMERA_PASSWORD"):
        return os.environ["CAMERA_PASSWORD"]
    env = load_env(SCRIPT_DIR / ".env")
    if env.get("CAMERA_PASSWORD"):
        return env["CAMERA_PASSWORD"]
    print("Error: No password provided.", file=sys.stderr)
    print("  Use --password, CAMERA_PASSWORD env var, or camera/.env file", file=sys.stderr)
    sys.exit(1)


def load_cameras() -> dict:
    """Load cameras.json manifest."""
    path = SCRIPT_DIR / "cameras.json"
    if not path.is_file():
        sys.exit(f"Error: {path} not found")
    with open(path) as f:
        data = json.load(f)
    return data["cameras"]


def get_camera(name: str) -> dict:
    """Look up a camera by name."""
    cameras = load_cameras()
    if name not in cameras:
        available = ", ".join(sorted(cameras.keys()))
        sys.exit(f"Error: Unknown camera '{name}'\nAvailable: {available}")
    return cameras[name]


def resolve_config_path(camera: dict, endpoint: str) -> Path | None:
    """Resolve config file using layered lookup: camera-specific > common."""
    site = camera["site"]
    cam = camera["camera"]
    filename = f"{endpoint}.xml"

    # Camera-specific path
    specific = SCRIPT_DIR / site / cam / filename
    if specific.is_file():
        return specific

    # Common baseline
    common = SCRIPT_DIR / "common" / filename
    if common.is_file():
        return common

    return None


def camera_specific_dir(camera: dict) -> Path:
    """Return the camera-specific config directory."""
    return SCRIPT_DIR / camera["site"] / camera["camera"]


def make_session(camera: dict, password: str, timeout: int) -> tuple:
    """Create an HTTP session with digest auth. Returns (session, base_url)."""
    session = requests.Session()
    session.auth = HTTPDigestAuth(camera["username"], password)
    session.timeout = timeout
    base_url = f"http://{camera['host']}"
    return session, base_url


def isapi_get(session, base_url: str, path: str, timeout: int) -> requests.Response:
    """GET an ISAPI endpoint."""
    url = f"{base_url}{path}"
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp


def isapi_put(session, base_url: str, path: str, xml_body: str, timeout: int) -> requests.Response:
    """PUT XML to an ISAPI endpoint."""
    url = f"{base_url}{path}"
    headers = {"Content-Type": "application/xml"}
    resp = session.put(url, data=xml_body, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp


def pretty_xml(root: ET.Element) -> str:
    """Serialize an ElementTree root to pretty-printed XML string."""
    ET.indent(root)
    return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"


def parse_xml(text: str) -> ET.Element:
    """Parse XML text into an Element."""
    return ET.fromstring(text)


def scrub_sensitive(root: ET.Element) -> ET.Element:
    """Replace sensitive field values with placeholder tokens."""
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag in SENSITIVE_FIELDS and elem.text and elem.text.strip():
            placeholder = SENSITIVE_FIELDS[tag]
            elem.text = f"<{placeholder}>"
    return root


def inject_sensitive(root: ET.Element) -> ET.Element:
    """Replace placeholder tokens with real values from env."""
    env = load_env(SCRIPT_DIR / ".env")
    env.update(os.environ)
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag in SENSITIVE_FIELDS and elem.text:
            placeholder = f"<{SENSITIVE_FIELDS[tag]}>"
            if elem.text.strip() == placeholder:
                var_name = SENSITIVE_FIELDS[tag]
                if var_name in env:
                    elem.text = env[var_name]
                else:
                    print(f"  Warning: {var_name} not set, leaving placeholder", file=sys.stderr)
    return root


def elements_to_dict(root: ET.Element) -> dict:
    """Flatten XML element tree to a dict of path → text for comparison."""
    result = {}

    def _walk(elem, prefix=""):
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag in VOLATILE_FIELDS:
            return
        path = f"{prefix}/{tag}" if prefix else tag
        if elem.text and elem.text.strip():
            result[path] = elem.text.strip()
        for child in elem:
            _walk(child, path)

    _walk(root)
    return result


def diff_xml(local_root: ET.Element, live_root: ET.Element) -> list[str]:
    """Compare local vs live XML. Returns list of diff lines."""
    local_d = elements_to_dict(local_root)
    live_d = elements_to_dict(live_root)

    all_keys = sorted(set(local_d.keys()) | set(live_d.keys()))
    diffs = []
    for key in all_keys:
        lv = local_d.get(key)
        rv = live_d.get(key)
        if lv == rv:
            continue
        if lv is None:
            diffs.append(f"  + {key} = {rv}  (live only)")
        elif rv is None:
            diffs.append(f"  - {key} = {lv}  (local only)")
        else:
            diffs.append(f"  ~ {key}: {lv} -> {rv}")
    return diffs


def resolve_endpoints(args_endpoints: list[str]) -> list[str]:
    """Resolve which endpoints to operate on."""
    if args_endpoints:
        for ep in args_endpoints:
            if ep not in ENDPOINTS:
                available = ", ".join(sorted(ENDPOINTS.keys()))
                sys.exit(f"Error: Unknown endpoint '{ep}'\nAvailable: {available}")
        return args_endpoints
    return list(ENDPOINTS.keys())


def backup_live_config(
    session, base_url: str, camera_name: str, camera: dict,
    endpoints: list[str], timeout: int, verbose: bool,
) -> Path:
    """Back up live camera config for the given endpoints before a push.

    Creates camera/backups/<camera_name>/<YYYYMMDD_HHMMSS>/ and writes one
    XML file per endpoint.  Returns the backup directory path.
    """
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = SCRIPT_DIR / "backups" / camera_name / stamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    for ep in endpoints:
        isapi_path = ENDPOINTS[ep]
        try:
            if verbose:
                print(f"  backup GET {isapi_path}")
            resp = isapi_get(session, base_url, isapi_path, timeout)
            root = parse_xml(resp.text)
            root = scrub_sensitive(root)
            xml_str = pretty_xml(root)
            (backup_dir / f"{ep}.xml").write_text(xml_str)
        except Exception as exc:
            print(f"  Warning: backup failed for {ep}: {exc}", file=sys.stderr)

    return backup_dir


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_info(args):
    """Print device info (model, firmware, serial, MAC)."""
    camera = get_camera(args.camera_name)
    password = get_password(args)
    session, base_url = make_session(camera, password, args.timeout)

    print(f"Camera: {args.camera_name} ({camera['host']})")
    print()

    try:
        resp = isapi_get(session, base_url, "/ISAPI/System/deviceInfo", args.timeout)
        root = parse_xml(resp.text)

        fields = [
            "deviceName", "deviceID", "model", "serialNumber",
            "macAddress", "firmwareVersion", "firmwareReleasedDate",
            "encoderVersion", "hardwareVersion", "deviceType",
        ]
        for field in fields:
            elem = root.find(f".//{{{HIK_NS}}}{field}")
            if elem is None:
                elem = root.find(f".//{field}")
            if elem is not None and elem.text:
                label = field[0].upper() + field[1:]
                print(f"  {label}: {elem.text}")
    except requests.exceptions.ConnectionError:
        sys.exit(f"Error: Cannot connect to {camera['host']}")
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            sys.exit(f"Error: Authentication failed for {args.camera_name} ({camera['host']})")
        raise


def cmd_pull(args):
    """Download live config from camera and save to XML files."""
    camera = get_camera(args.camera_name)
    password = get_password(args)
    session, base_url = make_session(camera, password, args.timeout)
    endpoints = resolve_endpoints(args.endpoints)
    out_dir = camera_specific_dir(camera)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Pulling from {args.camera_name} ({camera['host']}) -> {out_dir.relative_to(SCRIPT_DIR)}/")

    errors = 0
    for ep in endpoints:
        path = ENDPOINTS[ep]
        try:
            if args.verbose:
                print(f"  GET {path}")
            resp = isapi_get(session, base_url, path, args.timeout)
            root = parse_xml(resp.text)
            root = scrub_sensitive(root)
            xml_str = pretty_xml(root)

            out_file = out_dir / f"{ep}.xml"
            out_file.write_text(xml_str)
            print(f"  {ep}: saved ({len(xml_str)} bytes)")
        except requests.exceptions.ConnectionError:
            print(f"  {ep}: ERROR - cannot connect to {camera['host']}", file=sys.stderr)
            errors += 1
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            print(f"  {ep}: ERROR - HTTP {status}", file=sys.stderr)
            errors += 1

    # Remove .gitkeep if we wrote real files
    gitkeep = out_dir / ".gitkeep"
    if gitkeep.is_file() and any(out_dir.glob("*.xml")):
        gitkeep.unlink()

    if errors:
        print(f"\n{errors} endpoint(s) failed", file=sys.stderr)
        sys.exit(1)


def cmd_push(args):
    """Upload local XML configs to camera."""
    camera = get_camera(args.camera_name)
    password = get_password(args)
    endpoints = resolve_endpoints(args.endpoints)

    if not args.dry_run:
        session, base_url = make_session(camera, password, args.timeout)

    print(f"Pushing to {args.camera_name} ({camera['host']})")
    if args.dry_run:
        print("  (dry run — no changes will be made)")

    # Auto-backup live config before pushing
    if not args.dry_run and not args.no_backup:
        pushable = [ep for ep in endpoints if resolve_config_path(camera, ep) is not None]
        if pushable:
            backup_dir = backup_live_config(
                session, base_url, args.camera_name, camera,
                pushable, args.timeout, args.verbose,
            )
            print(f"  Backed up live config to {backup_dir.relative_to(SCRIPT_DIR)}/")

    errors = 0
    skipped = 0
    for ep in endpoints:
        config_path = resolve_config_path(camera, ep)
        if config_path is None:
            if args.verbose:
                print(f"  {ep}: skipped (no config file)")
            skipped += 1
            continue

        isapi_path = ENDPOINTS[ep]
        source = config_path.relative_to(SCRIPT_DIR)

        try:
            root = parse_xml(config_path.read_text())
            root = inject_sensitive(root)
            xml_body = ET.tostring(root, encoding="unicode", xml_declaration=True)

            if args.dry_run:
                print(f"  {ep}: would PUT {isapi_path} from {source}")
                continue

            if args.verbose:
                print(f"  PUT {isapi_path} from {source}")
            resp = isapi_put(session, base_url, isapi_path, xml_body, args.timeout)

            # Check for ISAPI-level error in response
            if resp.text:
                try:
                    resp_root = parse_xml(resp.text)
                    status_elem = resp_root.find(f".//{{{HIK_NS}}}statusString")
                    if status_elem is None:
                        status_elem = resp_root.find(".//statusString")
                    if status_elem is not None and status_elem.text != "OK":
                        print(f"  {ep}: WARNING - camera responded: {status_elem.text}", file=sys.stderr)
                except ET.ParseError:
                    pass

            print(f"  {ep}: pushed from {source}")
        except requests.exceptions.ConnectionError:
            print(f"  {ep}: ERROR - cannot connect to {camera['host']}", file=sys.stderr)
            errors += 1
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            print(f"  {ep}: ERROR - HTTP {status}", file=sys.stderr)
            errors += 1
        except ET.ParseError as e:
            print(f"  {ep}: ERROR - invalid XML in {source}: {e}", file=sys.stderr)
            errors += 1

    if skipped and args.verbose:
        print(f"\n{skipped} endpoint(s) skipped (no config file)")
    if errors:
        print(f"\n{errors} endpoint(s) failed", file=sys.stderr)
        sys.exit(1)


def cmd_diff(args):
    """Show differences between local config and live camera."""
    camera = get_camera(args.camera_name)
    password = get_password(args)
    session, base_url = make_session(camera, password, args.timeout)
    endpoints = resolve_endpoints(args.endpoints)

    print(f"Comparing {args.camera_name} ({camera['host']}) local vs live")

    total_diffs = 0
    skipped = 0
    for ep in endpoints:
        config_path = resolve_config_path(camera, ep)
        if config_path is None:
            if args.verbose:
                print(f"  {ep}: skipped (no config file)")
            skipped += 1
            continue

        isapi_path = ENDPOINTS[ep]
        try:
            local_root = parse_xml(config_path.read_text())

            if args.verbose:
                print(f"  GET {isapi_path}")
            resp = isapi_get(session, base_url, isapi_path, args.timeout)
            live_root = parse_xml(resp.text)
            live_root = scrub_sensitive(live_root)

            diffs = diff_xml(local_root, live_root)
            if diffs:
                source = config_path.relative_to(SCRIPT_DIR)
                print(f"\n[{ep}] ({source})")
                for line in diffs:
                    print(line)
                total_diffs += len(diffs)
            elif args.verbose:
                print(f"  {ep}: OK (matches)")
        except requests.exceptions.ConnectionError:
            print(f"  {ep}: ERROR - cannot connect to {camera['host']}", file=sys.stderr)
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            print(f"  {ep}: ERROR - HTTP {status}", file=sys.stderr)

    if total_diffs == 0:
        print("\nNo differences found.")
    else:
        print(f"\n{total_diffs} difference(s) found.")


def cmd_verify(args):
    """Like diff but exits 0 (match) or 1 (drift) for scripting."""
    camera = get_camera(args.camera_name)
    password = get_password(args)
    session, base_url = make_session(camera, password, args.timeout)
    endpoints = resolve_endpoints(args.endpoints)

    has_drift = False
    has_error = False
    for ep in endpoints:
        config_path = resolve_config_path(camera, ep)
        if config_path is None:
            continue

        isapi_path = ENDPOINTS[ep]
        try:
            local_root = parse_xml(config_path.read_text())

            if args.verbose:
                print(f"  GET {isapi_path}")
            resp = isapi_get(session, base_url, isapi_path, args.timeout)
            live_root = parse_xml(resp.text)
            live_root = scrub_sensitive(live_root)

            diffs = diff_xml(local_root, live_root)
            if diffs:
                has_drift = True
                if args.verbose:
                    print(f"  {ep}: DRIFT ({len(diffs)} differences)")
            elif args.verbose:
                print(f"  {ep}: OK")
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            print(f"  {ep}: ERROR - {e}", file=sys.stderr)
            has_error = True

    if has_error:
        sys.exit(2)
    if has_drift:
        if not args.verbose:
            print("DRIFT")
        sys.exit(1)
    if not args.verbose:
        print("OK")
    sys.exit(0)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="camtool.py",
        description="Camera configuration management via Hikvision ISAPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s info sukabumi-cam1
              %(prog)s pull jakarta-cam1
              %(prog)s pull jakarta-cam1 streaming_101 image
              %(prog)s diff sukabumi-cam1
              %(prog)s push jakarta-cam2 overlays --dry-run
              %(prog)s verify sukabumi-cam1

            endpoints:
              """ + ", ".join(sorted(ENDPOINTS.keys()))
        ),
    )
    parser.add_argument(
        "--password", metavar="PWD",
        help="Camera password (or set CAMERA_PASSWORD env var, or use .env file)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print detailed output",
    )
    parser.add_argument(
        "--timeout", type=int, default=10, metavar="N",
        help="HTTP timeout in seconds (default: 10)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # info
    p_info = sub.add_parser("info", help="Print device model, firmware, serial, MAC")
    p_info.add_argument("camera_name", help="Camera name from cameras.json")

    # pull
    p_pull = sub.add_parser("pull", help="Download live config to XML files")
    p_pull.add_argument("camera_name", help="Camera name from cameras.json")
    p_pull.add_argument("endpoints", nargs="*", help="Specific endpoints (default: all)")

    # push
    p_push = sub.add_parser("push", help="Upload XML files to camera")
    p_push.add_argument("camera_name", help="Camera name from cameras.json")
    p_push.add_argument("endpoints", nargs="*", help="Specific endpoints (default: all)")
    p_push.add_argument("--no-backup", action="store_true",
                        help="Skip automatic pre-push backup of live config")

    # diff
    p_diff = sub.add_parser("diff", help="Show differences (local vs live)")
    p_diff.add_argument("camera_name", help="Camera name from cameras.json")
    p_diff.add_argument("endpoints", nargs="*", help="Specific endpoints (default: all)")

    # verify
    p_verify = sub.add_parser("verify", help="Check config drift (exit 0=match, 1=drift, 2=error)")
    p_verify.add_argument("camera_name", help="Camera name from cameras.json")
    p_verify.add_argument("endpoints", nargs="*", help="Specific endpoints (default: all)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "info": cmd_info,
        "pull": cmd_pull,
        "push": cmd_push,
        "diff": cmd_diff,
        "verify": cmd_verify,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
