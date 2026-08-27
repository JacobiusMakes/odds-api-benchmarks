# /// script
# requires-python = ">=3.9"
# ///
"""Probe each vendor's documented public endpoints WITHOUT any API key.

Records the raw HTTP outcome of each probe. A 200 with JSON means the vendor
offers a genuinely keyless surface. A 401/403 means the endpoint exists but
requires a key. This is a statement about signup friction, not data quality.
"""
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_vendors, fetch, looks_like_json, write_result, ROOT


def classify(result):
    if result["error"]:
        return "unreachable"
    s = result["status"]
    if s == 200 and looks_like_json(result):
        return "keyless_json"
    if s == 200:
        return "keyless_non_json"
    if s in (401, 403):
        return "requires_key"
    if s == 422:
        return "keyless_validation_error"
    return f"http_{s}"


def main(out_dir):
    vendors = load_vendors()
    out = {
        "probe": "unauthenticated_surface",
        "run_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "note": "Each probe is a single GET with no API key. Classification: keyless_json = works without signup; requires_key = 401/403.",
        "vendors": {},
    }
    for vid, v in vendors.items():
        probes = []
        for p in v["unauth_probes"]:
            r = fetch(p["url"])
            probes.append({
                "label": p["label"],
                "url": p["url"],
                "documented_at": p.get("documented_at"),
                "status": r["status"],
                "classification": classify(r),
                "error": r["error"],
            })
            print(f"  {v['name']}: {r['status']} {p['url']}")
        keyless = [p for p in probes if p["classification"].startswith("keyless")]
        out["vendors"][vid] = {
            "name": v["name"],
            "keyless_endpoints_found": len(keyless),
            "probes": probes,
        }
    write_result(out_dir, "unauth", out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT / "results" / datetime.date.today().isoformat()
    main(out)
