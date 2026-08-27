# Methodology

## What v1 measures, and what it deliberately does not

This benchmark compares sports odds APIs on the dimensions that can be measured **without paid API keys and without creating accounts**. That constraint is the point: anyone can rerun every probe from a clean machine and get the same class of results. It is also the biggest limitation, so read this section before quoting anything:

**Limitations, prominent by design:**

1. **No paid-tier data quality comparison.** v1 says nothing about odds accuracy, market depth, update speed, WebSocket performance, or historical data quality on paid plans. Those require keys for every vendor and a much more careful experimental design. That is the v2 ambition, not a v1 claim.
2. **Single vantage point for latency.** Latency numbers come from one machine on one network at one time of day. They measure the responsiveness of each vendor's public surface from that vantage point only. Where a vendor has no keyless endpoint, the target returns 401 and the number is auth-rejection latency at the edge, which is not comparable to a 200 serving real JSON. The latency table lists the statuses seen for exactly this reason.
3. **Free tier terms are vendor claims, not measurements.** Section 2 of the README quotes each vendor's own pricing page with URL and read date. Vendors change terms without notice; the read date bounds what we knew and when.
4. **"Not found" means "not found at the probed URLs".** OpenAPI, llms.txt, and status page checks probe the candidate URLs listed in `data/vendors.json`. A vendor may publish these elsewhere. PRs adding the correct URL are merged and take effect on the next run.
5. **Shallow HTML checks.** Status page history detection greps fetched HTML for keywords. JS-only status pages can under-report. A "no" is "not detected", never "proven absent".
6. **Vendor selection.** The six vendors are the ones the maintainer knows to be commonly compared. Adding a vendor is a PR to `data/vendors.json` plus a row in `data/free_tier.json` with citations.

## Probes

All probes are stdlib-only Python, sequential, with a 15s timeout and an honest User-Agent identifying this repo. Each writes one JSON file into `results/<date>/`.

| Probe | Script | What it records |
|---|---|---|
| Try-before-signup surface | `bench/probe_unauth.py` | HTTP status of a single keyless GET to each documented endpoint, classified (keyless JSON / requires key / etc.) |
| Docs signals | `bench/probe_docs.py` | Whether a machine-validated OpenAPI spec and an llms.txt exist at candidate URLs. Specs are validated by content (an `openapi`/`swagger` key), not just a 200. |
| Transparency | `bench/probe_transparency.py` | Whether a public status page answers 200, and keyword-level detection of uptime and incident history on it |
| Latency | `bench/probe_latency.py` | n=20 sequential GETs per vendor to its most public endpoint, 250ms apart, after one discarded warm-up. Median, p90, min, max, and the set of HTTP statuses seen |
| Free tier snapshot | `bench/run_all.py` | Copies `data/free_tier.json` (curated claims with citations) into the dated results directory so the claims are versioned with the run |

## Reproducing

```bash
python3 bench/run_all.py
```

No dependencies beyond Python 3.9+. `uv run bench/run_all.py` works identically. The run takes a few minutes, almost all of it in the latency probe. Results land in `results/<today>/` and `README.md` is regenerated from them.

Individual probes run standalone: `python3 bench/probe_docs.py [results/dir]`.

## Scheduled runs

`.github/workflows/bench.yml` reruns everything weekly (Monday 06:00 UTC) and on manual dispatch from GitHub's hosted runners, committing the dated results and the regenerated README. GitHub runners are a different vantage point than the maintainer's machine; the latency file records the platform it ran on.

## Fairness commitments

- The README carries a permanent disclosure that the maintainer is ParlayAPI's founder.
- The README includes a maintained section naming what each competitor does better, generated from `data/fairness_notes.md`.
- Comparative claims about competitors come only from their own pages, cited with URL and read date, or from probe output committed to this repo.
- PRs from competitors are welcome and will be merged if honest, including PRs that make ParlayAPI look worse.
