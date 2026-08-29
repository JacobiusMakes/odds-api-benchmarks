# /// script
# requires-python = ">=3.9"
# ///
"""Latency of each vendor's most public endpoint, from ONE vantage point.

n=20 sequential GETs per target (plus 1 discarded warm-up), 250ms apart.
Reports median and p90 of total round-trip time.

READ THE CAVEATS: this measures the responsiveness of whatever the endpoint
returns from wherever this script runs. For vendors with no keyless endpoint
the target returns 401, so the number is edge/auth-rejection latency, NOT
data-serving latency. Numbers across vendors are not directly comparable and
say nothing about odds update speed. They answer one narrow question: how
fast does the public surface respond from this vantage point today.
"""
import datetime
import platform
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_vendors, fetch, write_result, ROOT

N = 20


def main(out_dir):
    vendors = load_vendors()
    out = {
        "probe": "public_endpoint_latency",
        "run_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "vantage_point": {
            "description": "single vantage point, see caveats",
            "platform": platform.platform(),
            "note": "Run from one machine on one network. Re-run from your own location: python3 bench/probe_latency.py",
        },
        "n_per_target": N,
        "caveats": "Single vantage point. Includes TLS + full response for small payloads. 401 responses measure auth-rejection latency, not data latency. Not comparable to odds update frequency.",
        "vendors": {},
    }
    for vid, v in vendors.items():
        t = v["latency_target"]
        fetch(t["url"])  # warm-up, discarded
        samples = []
        statuses = set()
        errors = 0
        for _ in range(N):
            r = fetch(t["url"])
            if r["error"]:
                errors += 1
            else:
                samples.append(r["elapsed_s"])
                statuses.add(r["status"])
            time.sleep(0.25)
        ordered = sorted(samples)
        entry = {
            "name": v["name"],
            "target": t["label"],
            "url": t["url"],
            "n_attempted": N,
            "n_ok": len(samples),
            "errors": errors,
            "response_statuses_seen": sorted(statuses),
            "median_s": round(statistics.median(samples), 4) if samples else None,
            "p90_s": round(ordered[max(0, int(len(samples) * 0.9) - 1)], 4) if samples else None,
            "p95_s": round(ordered[max(0, int(len(samples) * 0.95) - 1)], 4) if samples else None,
            "min_s": round(min(samples), 4) if samples else None,
            "max_s": round(max(samples), 4) if samples else None,
            "samples_s": [round(s, 4) for s in samples],
        }
        out["vendors"][vid] = entry
        print(f"  {v['name']}: median={entry['median_s']}s statuses={entry['response_statuses_seen']}")
    write_result(out_dir, "latency", out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT / "results" / datetime.date.today().isoformat()
    main(out)
