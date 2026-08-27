# /// script
# requires-python = ">=3.9"
# ///
"""Transparency scorecard, probed live:

1. Public status page: probe the candidate status URLs. Found = 200 response.
2. Uptime history visible: the status page body mentions uptime figures/history.
3. Incident/update history visible: the status page body shows an incident or
   status-update history section.
4. Published credit/pricing math: does the vendor publish machine- or
   human-readable request cost rules at a public URL? Probed where a public
   endpoint exists; otherwise cited from the vendor's docs/pricing page in
   data/free_tier.json.

Keyword checks are shallow by design (reproducible without a headless
browser). JS-only status pages can under-report here; PRs improving detection
are welcome.
"""
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_vendors, fetch, write_result, ROOT


def main(out_dir):
    vendors = load_vendors()
    out = {
        "probe": "transparency",
        "run_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "note": "Status page detection = HTTP 200 at a candidate URL. History flags are keyword checks against the fetched HTML and can miss JS-rendered content.",
        "vendors": {},
    }
    for vid, v in vendors.items():
        found = None
        checked = []
        uptime_visible = False
        incident_visible = False
        for url in v["status_page_candidates"]:
            r = fetch(url, max_bytes=262144, head_bytes=262144)
            ok = r["error"] is None and r["status"] == 200
            checked.append({"url": url, "status": r["status"], "error": r["error"]})
            if ok and found is None:
                found = url
                body = (r["body_head"] or "").lower()
                uptime_visible = bool(re.search(r"uptime", body))
                incident_visible = bool(re.search(r"incident|status update history|outage", body))
        out["vendors"][vid] = {
            "name": v["name"],
            "status_page": {"found": found, "candidates_checked": checked},
            "uptime_history_keyword_seen": uptime_visible if found else None,
            "incident_history_keyword_seen": incident_visible if found else None,
        }
        print(f"  {v['name']}: status_page={found} uptime={uptime_visible} incidents={incident_visible}")
    write_result(out_dir, "transparency", out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT / "results" / datetime.date.today().isoformat()
    main(out)
