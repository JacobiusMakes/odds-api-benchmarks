# Latest latency results

> **Disclosure:** this repo is maintained by ParlayAPI's founder. Every number below is produced by [`bench/probe_latency.py`](bench/probe_latency.py), which you can rerun yourself with no API keys. See [METHODOLOGY.md](METHODOLOGY.md) and the caveats before quoting anything.

Run date: **2026-10-05** (UTC, 2026-10-05T13:59:09.260758+00:00). Vantage point: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39` (a GitHub-hosted runner for scheduled runs). Raw samples: [`results/2026-10-05/latency.json`](results/2026-10-05/latency.json).

**Caveats, do not skip:** Single vantage point. Includes TLS + full response for small payloads. 401 responses measure auth-rejection latency, not data latency. Not comparable to odds update frequency. Rows whose status is 401 are not comparable to rows serving real data with a 200.

| Provider | What was measured | Statuses seen | p50 | p95 | Success rate | Sample size | Run date |
|---|---|---|---|---|---|---|---|
| ParlayAPI | keyless API endpoint /live/api/sports | [200] | 372 ms | 1804 ms | 20/20 | 20 | 2026-10-05 |
| The Odds API | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 56 ms | 135 ms | 20/20 | 20 | 2026-10-05 |
| OddsPapi | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 136 ms | 164 ms | 20/20 | 20 | 2026-10-05 |
| SharpAPI | API edge: /api/v1/odds (returns 401 without key; measures edge round trip only) | [401, 429] | 28 ms | 46 ms | 20/20 | 20 | 2026-10-05 |
| SportsGameOdds | API edge: /v2/sports (returns 401 without key; measures edge round trip only) | [401] | 65 ms | 97 ms | 20/20 | 20 | 2026-10-05 |
| TheRundown | keyless API endpoint /api/v2/sports | [200] | 34 ms | 57 ms | 20/20 | 20 | 2026-10-05 |

A row's p50/p95 are the median and 95th percentile of total round-trip time over the sample; success rate is completed HTTP exchanges (any status) over attempts. History of all runs lives in [`results/`](results/).
