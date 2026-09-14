# Latest latency results

> **Disclosure:** this repo is maintained by ParlayAPI's founder. Every number below is produced by [`bench/probe_latency.py`](bench/probe_latency.py), which you can rerun yourself with no API keys. See [METHODOLOGY.md](METHODOLOGY.md) and the caveats before quoting anything.

Run date: **2026-09-14** (UTC, 2026-09-14T12:11:11.818824+00:00). Vantage point: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39` (a GitHub-hosted runner for scheduled runs). Raw samples: [`results/2026-09-14/latency.json`](results/2026-09-14/latency.json).

**Caveats, do not skip:** Single vantage point. Includes TLS + full response for small payloads. 401 responses measure auth-rejection latency, not data latency. Not comparable to odds update frequency. Rows whose status is 401 are not comparable to rows serving real data with a 200.

| Provider | What was measured | Statuses seen | p50 | p95 | Success rate | Sample size | Run date |
|---|---|---|---|---|---|---|---|
| ParlayAPI | keyless API endpoint /live/api/sports | [200] | 211 ms | 859 ms | 20/20 | 20 | 2026-09-14 |
| The Odds API | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 144 ms | 184 ms | 20/20 | 20 | 2026-09-14 |
| OddsPapi | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 210 ms | 371 ms | 20/20 | 20 | 2026-09-14 |
| SharpAPI | API edge: /api/v1/odds (returns 401 without key; measures edge round trip only) | [401, 429] | 152 ms | 154 ms | 20/20 | 20 | 2026-09-14 |
| SportsGameOdds | API edge: /v2/sports (returns 401 without key; measures edge round trip only) | [401] | 97 ms | 310 ms | 20/20 | 20 | 2026-09-14 |
| TheRundown | keyless API endpoint /api/v2/sports | [200] | 110 ms | 208 ms | 20/20 | 20 | 2026-09-14 |

A row's p50/p95 are the median and 95th percentile of total round-trip time over the sample; success rate is completed HTTP exchanges (any status) over attempts. History of all runs lives in [`results/`](results/).
