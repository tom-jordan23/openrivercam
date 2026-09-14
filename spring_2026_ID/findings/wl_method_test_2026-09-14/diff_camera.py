"""Diff the station's deployed profile XMLs and the live ISAPI responses
against the repo's copies (test A).

Usage: python3 diff_camera.py <grab output .txt>
"""
import re
import sys
import xml.etree.ElementTree as ET

REPO = "/home/tjordan/code/git/openrivercam/spring_2026_ID/camera"
text = open(sys.argv[1], errors="replace").read()


def flat_xml(x):
    x = x[x.find("<?xml") if "<?xml" in x else x.find("<"):]
    x = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", x)
    x = re.sub(r"<(/?)\w+:", r"<\1", x)
    x = re.sub(r"\s\w+:(\w+)=", r" \1=", x)
    out = {}

    def walk(e, p):
        kids = list(e)
        if not kids:
            t = (e.text or "").strip()
            if t:
                out[f"{p}/{e.tag}"] = t
        for k in kids:
            walk(k, f"{p}/{e.tag}" if p else e.tag)

    walk(ET.fromstring(x.strip()), "")
    return out


def block(start_marker, end_markers):
    i = text.find(start_marker)
    if i < 0:
        return None
    j = min([k for k in (text.find(m, i + len(start_marker)) for m in end_markers) if k > 0] or [len(text)])
    body = text[i + len(start_marker):j]
    return "\n".join(re.sub(r"^ {2,6}", "", ln) for ln in body.splitlines())


def show(name, repo_path, other):
    try:
        a = flat_xml(open(repo_path).read())
    except Exception as e:  # noqa: BLE001
        print(f"## {name}: cannot parse repo copy: {e}")
        return
    if other is None:
        print(f"## {name}: not present in grab")
        return
    body = other.split("__HTTP")[0]
    try:
        b = flat_xml(body)
    except Exception as e:  # noqa: BLE001
        print(f"## {name}: cannot parse grab copy ({e}); first 300 chars:\n{body[:300]}")
        return
    diffs = [(k, a.get(k, "<absent>"), b.get(k, "<absent>")) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    print(f"## {name}: {len(diffs)} differing leaves (repo vs grab)")
    for k, x, y in diffs:
        print(f"   {k.split('/', 1)[-1][:64]:64} repo={x[:22]:22} live={y[:22]}")


D = "=== D."
show("deployed common/image.xml", f"{REPO}/common/image.xml",
     block("##### /home/pi/camera_profiles/common/image.xml", ["#####", "=== END"]))
show("deployed profile-night/image.xml", f"{REPO}/profiles/profile-night/image.xml",
     block("##### /home/pi/camera_profiles/profiles/profile-night/image.xml", ["#####", "=== END"]))
show("deployed common/streaming_101.xml", f"{REPO}/common/streaming_101.xml",
     block("##### /home/pi/camera_profiles/common/streaming_101.xml", ["=== END"]))
print("\n# live camera, compared with the repo profile that should be active now")
show("LIVE image vs repo NIGHT profile", f"{REPO}/profiles/profile-night/image.xml",
     block("##### GET /ISAPI/Image/channels/1\n", ["##### GET", "#####", "=== D."]))
show("LIVE image vs repo DAY profile", f"{REPO}/common/image.xml",
     block("##### GET /ISAPI/Image/channels/1\n", ["##### GET", "#####", "=== D."]))
show("LIVE streaming_101 vs repo", f"{REPO}/common/streaming_101.xml",
     block("##### GET /ISAPI/Streaming/channels/101", ["##### GET", "#####", "=== D."]))
