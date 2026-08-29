# /// script
# requires-python = ">=3.9"
# ///
"""Run every probe, snapshot the curated free-tier data alongside the probed
results, and regenerate README.md. Usage:

    python3 bench/run_all.py            # writes results/<today>/
    python3 bench/run_all.py 2026-08-27 # explicit date dir
"""
import datetime
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT
import probe_unauth
import probe_docs
import probe_latency
import probe_transparency
import generate_readme
import generate_results


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    out_dir = ROOT / "results" / date
    out_dir.mkdir(parents=True, exist_ok=True)

    print("== unauthenticated surface ==")
    probe_unauth.main(out_dir)
    print("== docs quality signals ==")
    probe_docs.main(out_dir)
    print("== transparency ==")
    probe_transparency.main(out_dir)
    print("== latency (n=20 per vendor, takes a few minutes) ==")
    probe_latency.main(out_dir)

    # Snapshot the curated free-tier claims as they stood on this run date.
    shutil.copy(ROOT / "data" / "free_tier.json", out_dir / "free_tier.json")
    print(f"snapshotted data/free_tier.json into {out_dir}")

    generate_readme.main(date)
    generate_results.main(date)


if __name__ == "__main__":
    main()
