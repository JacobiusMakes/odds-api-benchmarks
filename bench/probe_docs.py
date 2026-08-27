# /// script
# requires-python = ">=3.9"
# ///
"""Probe documentation-quality signals that can be checked live:

1. OpenAPI spec: is a machine-readable spec published at any of the candidate
   URLs in data/vendors.json? Validated by content (JSON with an "openapi" or
   "swagger" key), not just a 200, because docs sites often return HTML for
   any path.
2. llms.txt: does the vendor publish an llms.txt (plain-text site guide for
   LLM agents)? Validated as 200 + non-HTML body.

A "not found" means not found AT THE PROBED CANDIDATE URLS, which are listed
in data/vendors.json. If a vendor publishes a spec somewhere else, PR the URL.
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_vendors, fetch, write_result, ROOT


def validate_openapi(result):
    if result["error"] or result["status"] != 200:
        return False
    head = result["body_head"].lstrip()
    if head.startswith("{"):
        try:
            doc = json.loads(result["body_head"]) if len(result["body_head"]) < 2048 else None
        except json.JSONDecodeError:
            doc = None
        if doc is not None:
            return "openapi" in doc or "swagger" in doc
        # Body was truncated; check the head textually.
        return '"openapi"' in head[:500] or '"swagger"' in head[:500]
    return head.startswith("openapi:") or head.startswith("swagger:")


def validate_llms_txt(result):
    if result["error"] or result["status"] != 200:
        return False
    head = result["body_head"].lstrip().lower()
    return not head.startswith("<!doctype") and not head.startswith("<html")


def main(out_dir):
    vendors = load_vendors()
    out = {
        "probe": "docs_quality_signals",
        "run_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "note": "'found: null' means not found at the candidate URLs listed in data/vendors.json, not proof it does not exist anywhere.",
        "vendors": {},
    }
    for vid, v in vendors.items():
        openapi_found = None
        openapi_checked = []
        for url in v["openapi_candidates"]:
            r = fetch(url)
            ok = validate_openapi(r)
            openapi_checked.append({"url": url, "status": r["status"], "valid_spec": ok})
            if ok and openapi_found is None:
                openapi_found = url
        llms_found = None
        llms_checked = []
        for url in v["llms_txt_candidates"]:
            r = fetch(url)
            ok = validate_llms_txt(r)
            llms_checked.append({"url": url, "status": r["status"], "valid": ok})
            if ok and llms_found is None:
                llms_found = url
        out["vendors"][vid] = {
            "name": v["name"],
            "openapi_spec": {"found": openapi_found, "candidates_checked": openapi_checked},
            "llms_txt": {"found": llms_found, "candidates_checked": llms_checked},
        }
        print(f"  {v['name']}: openapi={openapi_found} llms.txt={llms_found}")
    write_result(out_dir, "docs", out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT / "results" / datetime.date.today().isoformat()
    main(out)
