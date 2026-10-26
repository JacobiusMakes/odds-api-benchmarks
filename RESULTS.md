# Latest latency results

> **Disclosure:** this repo is maintained by ParlayAPI's founder. Every number below is produced by [`bench/probe_latency.py`](bench/probe_latency.py), which you can rerun yourself with no API keys. See [METHODOLOGY.md](METHODOLOGY.md) and the caveats before quoting anything.

Run date: **2026-10-26** (UTC, 2026-10-26T12:29:47.725455+00:00). Vantage point: `Linux-7.0.0-1017-azure-x86_64-with-glibc2.43` (a GitHub-hosted runner for scheduled runs). Raw samples: [`results/2026-10-26/latency.json`](results/2026-10-26/latency.json).

**Caveats, do not skip:** Single vantage point. Includes TLS + full response for small payloads. 401 responses measure auth-rejection latency, not data latency. Not comparable to odds update frequency. Rows whose status is 401 are not comparable to rows serving real data with a 200.

| Provider | What was measured | Statuses seen | p50 | p95 | Success rate | Sample size | Run date |
|---|---|---|---|---|---|---|---|
| ParlayAPI | keyless API endpoint /live/api/sports | [200] | 349 ms | 1047 ms | 20/20 | 20 | 2026-10-26 |
| The Odds API | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 68 ms | 155 ms | 20/20 | 20 | 2026-10-26 |
| OddsPapi | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 149 ms | 265 ms | 20/20 | 20 | 2026-10-26 |
| SharpAPI | API edge: /api/v1/odds (returns 401 without key; measures edge round trip only) | [401, 429] | 39 ms | 42 ms | 20/20 | 20 | 2026-10-26 |
| SportsGameOdds | API edge: /v2/sports (returns 401 without key; measures edge round trip only) | [401] | 91 ms | 213 ms | 20/20 | 20 | 2026-10-26 |
| TheRundown | keyless API endpoint /api/v2/sports | [200] | 58 ms | 90 ms | 20/20 | 20 | 2026-10-26 |

A row's p50/p95 are the median and 95th percentile of total round-trip time over the sample; success rate is completed HTTP exchanges (any status) over attempts. History of all runs lives in [`results/`](results/).
