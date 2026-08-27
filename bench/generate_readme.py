# /// script
# requires-python = ">=3.9"
# ///
"""Regenerate README.md from the newest results/<date>/ directory.

Every table cell traces to a committed JSON file produced by a probe script,
or to a vendor page cited with URL + read date. Do not hand-edit README.md;
edit the probes, the data files, or data/fairness_notes.md and re-run.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT

ORDER = ["parlayapi", "the_odds_api", "oddspapi", "sharpapi", "sportsgameodds", "therundown"]


def latest_date():
    dates = sorted(p.name for p in (ROOT / "results").iterdir() if p.is_dir())
    return dates[-1]


def load(date, name):
    with open(ROOT / "results" / date / f"{name}.json") as f:
        return json.load(f)


def yn(v):
    return "yes" if v else "no"


def main(date=None):
    date = date or latest_date()
    unauth = load(date, "unauth")
    docs = load(date, "docs")
    lat = load(date, "latency")
    trans = load(date, "transparency")
    free = load(date, "free_tier")["vendors"]

    L = []
    A = L.append
    A("# odds-api-benchmarks")
    A("")
    A("Reproducible, no-key-required benchmarks of sports odds APIs: "
      "[ParlayAPI](https://parlay-api.com), [The Odds API](https://the-odds-api.com), "
      "[OddsPapi](https://oddspapi.io), [SharpAPI](https://sharpapi.io), "
      "[SportsGameOdds](https://sportsgameodds.com), [TheRundown](https://therundown.io).")
    A("")
    A("> **Disclosure:** this repo is maintained by ParlayAPI's founder. That is exactly why "
      "every number here is produced by a script you can run yourself, from this repo alone, "
      "with no API keys and no accounts. If a cell is wrong, the probe or the citation is "
      "wrong, and a PR fixes it. **PRs from competitors are welcome and will be merged if honest.**")
    A("")
    A(f"Latest run: **{date}**, committed under [`results/{date}/`](results/{date}/). "
      "A GitHub Action re-runs the probes weekly (Monday 06:00 UTC). "
      "See [METHODOLOGY.md](METHODOLOGY.md) for scope and limitations, which are significant: "
      "v1 measures only what is measurable without paid keys. It says nothing about paid-tier "
      "data quality, odds accuracy, or update speed.")
    A("")
    A("## Run it yourself")
    A("")
    A("```bash")
    A("git clone https://github.com/JacobiusMakes/odds-api-benchmarks")
    A("cd odds-api-benchmarks")
    A("python3 bench/run_all.py   # stdlib only; uv run bench/run_all.py also works")
    A("```")
    A("")
    A("That reruns every probe from your machine and regenerates this README from your results.")
    A("")

    # 1. Unauthenticated surface
    A("## 1. Try-before-signup surface (probed live)")
    A("")
    A(f"Single GET to each vendor's documented endpoints with **no API key**. "
      f"Raw outcomes in [`results/{date}/unauth.json`](results/{date}/unauth.json).")
    A("")
    A("| Vendor | Keyless endpoints found | Probe outcomes |")
    A("|---|---|---|")
    for vid in ORDER:
        v = unauth["vendors"][vid]
        parts = []
        for p in v["probes"]:
            path = p["url"].split("://", 1)[1].split("?")[0]
            path = "/" + path.split("/", 1)[1] if "/" in path else path
            parts.append(f"`{p['status']}` {path}")
        A(f"| {v['name']} | {v['keyless_endpoints_found']} of {len(v['probes'])} probed | {'; '.join(parts)} |")
    A("")
    A("Probe targets and the docs page documenting each are listed in "
      "[`data/vendors.json`](data/vendors.json). If a vendor has a keyless endpoint this "
      "benchmark missed, PR the URL and it will be probed next run.")
    A("")

    # 2. Free tier terms
    A("## 2. Free tier terms (vendor claims, cited)")
    A("")
    A("These are the vendors' own claims from their own public pages, quoted with source URL "
      "and read date. They are **not** measurements. Snapshot: "
      f"[`results/{date}/free_tier.json`](results/{date}/free_tier.json).")
    A("")
    A("| Vendor | Free allowance | Card required | Free tier delay | Book count claim | Source |")
    A("|---|---|---|---|---|---|")
    for vid in ORDER:
        f = free[vid]
        name = unauth["vendors"][vid]["name"]
        srcs = ", ".join(f"[{s['url'].split('//')[1].rstrip('/')}]({s['url']}) (read {s['read_date']})" for s in f["sources"])
        A(f"| {name} | {f['free_allowance']} | {f['card_required']} | {f['free_tier_delay']} | {f['book_count_claim']} | {srcs} |")
    A("")

    # 3. Docs signals
    A("## 3. Docs quality signals (probed live)")
    A("")
    A(f"Raw outcomes in [`results/{date}/docs.json`](results/{date}/docs.json). "
      "\"no\" means not found at the candidate URLs in `data/vendors.json`; "
      "PR the correct URL if one exists elsewhere.")
    A("")
    A("| Vendor | Machine-readable OpenAPI spec | llms.txt |")
    A("|---|---|---|")
    for vid in ORDER:
        d = docs["vendors"][vid]
        oa = d["openapi_spec"]["found"]
        ll = d["llms_txt"]["found"]
        A(f"| {d['name']} | {f'yes ([spec]({oa}))' if oa else 'not found at probed URLs'} | {f'yes ([llms.txt]({ll}))' if ll else 'not found at probed URLs'} |")
    A("")

    # 4. Transparency
    A("## 4. Transparency (probed live)")
    A("")
    A(f"Raw outcomes in [`results/{date}/transparency.json`](results/{date}/transparency.json). "
      "History columns are shallow keyword checks against the fetched HTML; JS-rendered "
      "status pages can under-report, so treat a \"no\" here as \"not detected\", not \"absent\".")
    A("")
    A("| Vendor | Public status page | Uptime history detected | Incident/update history detected |")
    A("|---|---|---|---|")
    for vid in ORDER:
        t = trans["vendors"][vid]
        sp = t["status_page"]["found"]
        A(f"| {t['name']} | {f'yes ([link]({sp}))' if sp else 'not found at probed URLs'} | "
          f"{yn(t['uptime_history_keyword_seen']) if sp else 'n/a'} | "
          f"{yn(t['incident_history_keyword_seen']) if sp else 'n/a'} |")
    A("")

    # 5. Latency
    A("## 5. Public endpoint latency, one vantage point (probed live)")
    A("")
    A(f"n={lat['n_per_target']} sequential GETs per target, median and p90 of total round-trip time. "
      f"Raw samples context in [`results/{date}/latency.json`](results/{date}/latency.json).")
    A("")
    A("**Caveats, do not skip:** " + lat["caveats"])
    A("")
    A("| Vendor | Target | Statuses seen | Median | p90 |")
    A("|---|---|---|---|---|")
    for vid in ORDER:
        e = lat["vendors"][vid]
        med = f"{e['median_s'] * 1000:.0f} ms" if e["median_s"] is not None else "n/a"
        p90 = f"{e['p90_s'] * 1000:.0f} ms" if e["p90_s"] is not None else "n/a"
        A(f"| {e['name']} | {e['target']} | {e['response_statuses_seen']} | {med} | {p90} |")
    A("")

    # Fairness notes, maintained by hand in data/fairness_notes.md
    notes = (ROOT / "data" / "fairness_notes.md").read_text().strip()
    A(notes)
    A("")
    A("## Contributing")
    A("")
    A("PRs welcome, including and especially from the vendors benchmarked here. Ground rules: "
      "every claim needs either a probe script that reproduces it or a citation to a vendor's "
      "own page with URL and read date. Fixes to probe targets, added vendors, and corrections "
      "to stale free-tier terms are all fair game. Marketing copy is not.")
    A("")
    A("## License")
    A("")
    A("MIT. Results data is factual output of the probes and carries no warranty.")
    A("")

    readme = "\n".join(L)
    for bad in ("—", "–"):
        assert bad not in readme, "em/en dash found in generated README"
    (ROOT / "README.md").write_text(readme)
    print(f"wrote {ROOT / 'README.md'} from results/{date}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
