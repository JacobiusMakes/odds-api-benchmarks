# odds-api-benchmarks

[![ParlayAPI p50](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FJacobiusMakes%2Fodds-api-benchmarks%2Fmain%2Fbadge-latency.json)](RESULTS.md) badge = ParlayAPI's own p50 from the latest weekly run, single vantage point; full table with every vendor, caveats included, in [RESULTS.md](RESULTS.md).

Reproducible, no-key-required benchmarks of sports odds APIs: [ParlayAPI](https://parlay-api.com), [The Odds API](https://the-odds-api.com), [OddsPapi](https://oddspapi.io), [SharpAPI](https://sharpapi.io), [SportsGameOdds](https://sportsgameodds.com), [TheRundown](https://therundown.io).

> **Disclosure:** this repo is maintained by ParlayAPI's founder. That is exactly why every number here is produced by a script you can run yourself, from this repo alone, with no API keys and no accounts. If a cell is wrong, the probe or the citation is wrong, and a PR fixes it. **PRs from competitors are welcome and will be merged if honest.**

Latest run: **2026-09-07**, committed under [`results/2026-09-07/`](results/2026-09-07/). A GitHub Action re-runs the probes weekly (Monday 06:00 UTC). See [METHODOLOGY.md](METHODOLOGY.md) for scope and limitations, which are significant: v1 measures only what is measurable without paid keys. It says nothing about paid-tier data quality, odds accuracy, or update speed.

## Run it yourself

```bash
git clone https://github.com/JacobiusMakes/odds-api-benchmarks
cd odds-api-benchmarks
python3 bench/run_all.py   # stdlib only; uv run bench/run_all.py also works
```

That reruns every probe from your machine and regenerates this README from your results.

## 1. Try-before-signup surface (probed live)

Single GET to each vendor's documented endpoints with **no API key**. Raw outcomes in [`results/2026-09-07/unauth.json`](results/2026-09-07/unauth.json).

| Vendor | Keyless endpoints found | Probe outcomes |
|---|---|---|
| ParlayAPI | 6 of 6 probed | `200` /v1/sandbox/sports; `200` /live/api/sports; `200` /v1/meta/credit-costs; `200` /v1/meta/source-quality; `200` /v1/calc/kelly; `200` /v1/prediction-markets/search |
| The Odds API | 0 of 1 probed | `401` /v4/sports |
| OddsPapi | 0 of 1 probed | `401` /v4/sports |
| SharpAPI | 0 of 1 probed | `401` /api/v1/odds |
| SportsGameOdds | 0 of 1 probed | `401` /v2/sports |
| TheRundown | 2 of 2 probed | `200` /api/v2/sports; `200` /api/v2/affiliates |

Probe targets and the docs page documenting each are listed in [`data/vendors.json`](data/vendors.json). If a vendor has a keyless endpoint this benchmark missed, PR the URL and it will be probed next run.

## 2. Free tier terms (vendor claims, cited)

These are the vendors' own claims from their own public pages, quoted with source URL and read date. They are **not** measurements. Snapshot: [`results/2026-09-07/free_tier.json`](results/2026-09-07/free_tier.json).

| Vendor | Free allowance | Card required | Free tier delay | Book count claim | Source |
|---|---|---|---|---|---|
| ParlayAPI | 1,000 credits/month per the pricing page (the homepage phrases it as 1,000 requests/month; per-endpoint credit costs are published at /v1/meta/credit-costs) | No ('no credit card required') | Not stated as a delay; free tier includes 48 hours of historical access | '30+ sportsbooks' on both the homepage and the pricing page | [parlay-api.com/pricing](https://parlay-api.com/pricing) (read 2026-08-29), [parlay-api.com](https://parlay-api.com/) (read 2026-08-29) |
| The Odds API | 500 credits/month (Starter plan) | Not stated on the cited page | Not stated on the cited page | 'over 40 bookmakers' globally | [the-odds-api.com](https://the-odds-api.com/) (read 2026-08-27) |
| OddsPapi | Not published as a fixed number on the pricing page (the page is a build-your-own-plan calculator); a vendor blog post describes a free tier of 250 requests | 'No credit card required' per vendor blog | Not stated on the cited pages | '350+ bookmakers' (homepage claims 300+ in one section and 350+ elsewhere; both numbers appear on vendor pages) | [oddspapi.io/us/pricing](https://oddspapi.io/us/pricing) (read 2026-08-27), [oddspapi.io](https://oddspapi.io/) (read 2026-08-27), [oddspapi.io/blog/free-odds-api-350-bookmakers](https://oddspapi.io/blog/free-odds-api-350-bookmakers/) (read 2026-08-27) |
| SharpAPI | 12 requests/min (~17,280/day), no monthly cap stated | No ('no credit card') | 60s data delay on free tier; pre-match only (live polling requires Pro+) | 2 sportsbooks on free tier (DraftKings, FanDuel); '40+ US sportsbooks' overall | [sharpapi.io/pricing](https://sharpapi.io/pricing) (read 2026-08-27) |
| SportsGameOdds | 2,500 objects/month (Amateur plan), 10 requests/min | Not stated on the cited page | 10-minute update frequency on free tier | 9 bookmakers on free tier; 82+ on top plans | [sportsgameodds.com/pricing](https://sportsgameodds.com/pricing) (read 2026-08-27) |
| TheRundown | 20,000 data points/day and 200,000/month, 1 req/sec | No ('No credit card') | 5-minute delay on free tier | '20+ sportsbooks and exchanges' including Kalshi, Polymarket, Novig, ProphetX; free tier includes 3 sportsbooks | [therundown.io/pricing/api](https://therundown.io/pricing/api) (read 2026-08-27), [docs.therundown.io/quickstart](https://docs.therundown.io/quickstart) (read 2026-08-27) |

## 3. Docs quality signals (probed live)

Raw outcomes in [`results/2026-09-07/docs.json`](results/2026-09-07/docs.json). "no" means not found at the candidate URLs in `data/vendors.json`; PR the correct URL if one exists elsewhere.

| Vendor | Machine-readable OpenAPI spec | llms.txt |
|---|---|---|
| ParlayAPI | yes ([spec](https://parlay-api.com/openapi.json)) | yes ([llms.txt](https://parlay-api.com/llms.txt)) |
| The Odds API | not found at probed URLs | not found at probed URLs |
| OddsPapi | not found at probed URLs | yes ([llms.txt](https://oddspapi.io/llms.txt)) |
| SharpAPI | yes ([spec](https://docs.sharpapi.io/openapi.json)) | yes ([llms.txt](https://sharpapi.io/llms.txt)) |
| SportsGameOdds | yes ([spec](https://sportsgameodds.com/openapi.json)) | yes ([llms.txt](https://sportsgameodds.com/llms.txt)) |
| TheRundown | not found at probed URLs | yes ([llms.txt](https://therundown.io/llms.txt)) |

## 4. Transparency (probed live)

Raw outcomes in [`results/2026-09-07/transparency.json`](results/2026-09-07/transparency.json). History columns are shallow keyword checks against the fetched HTML; JS-rendered status pages can under-report, so treat a "no" here as "not detected", not "absent".

| Vendor | Public status page | Uptime history detected | Incident/update history detected |
|---|---|---|---|
| ParlayAPI | yes ([link](https://parlay-api.com/status)) | no | no |
| The Odds API | yes ([link](https://status.the-odds-api.com/)) | yes | yes |
| OddsPapi | not found at probed URLs | n/a | n/a |
| SharpAPI | yes ([link](https://status.sharpapi.io/)) | yes | yes |
| SportsGameOdds | not found at probed URLs | n/a | n/a |
| TheRundown | not found at probed URLs | n/a | n/a |

## 5. Public endpoint latency, one vantage point (probed live)

n=20 sequential GETs per target, median and p90 of total round-trip time. Raw samples context in [`results/2026-09-07/latency.json`](results/2026-09-07/latency.json). A p50/p95 summary table with success rates is regenerated into [RESULTS.md](RESULTS.md) on every run, along with the badge data in `badge-latency.json`.

**Caveats, do not skip:** Single vantage point. Includes TLS + full response for small payloads. 401 responses measure auth-rejection latency, not data latency. Not comparable to odds update frequency.

| Vendor | Target | Statuses seen | Median | p90 |
|---|---|---|---|---|
| ParlayAPI | keyless API endpoint /live/api/sports | [200] | 198 ms | 686 ms |
| The Odds API | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 128 ms | 208 ms |
| OddsPapi | API edge: /v4/sports (returns 401 without key; measures edge round trip only) | [401] | 198 ms | 210 ms |
| SharpAPI | API edge: /api/v1/odds (returns 401 without key; measures edge round trip only) | [401, 429] | 196 ms | 200 ms |
| SportsGameOdds | API edge: /v2/sports (returns 401 without key; measures edge round trip only) | [401] | 105 ms | 195 ms |
| TheRundown | keyless API endpoint /api/v2/sports | [200] | 100 ms | 128 ms |

## Fairness notes: what each vendor does well

A benchmark maintained by one vendor's founder owes you this section. Based on the latest committed results and the cited vendor pages:

- **The Odds API** runs a public status page with visible uptime history and status update history, which ParlayAPI's live status page does not show (ParlayAPI's page shows current per-source freshness, not historical uptime). Its free tier requires no configuration and its pricing page states plan sizes in one screen.
- **SharpAPI** offers a free tier of 12 requests/min with no stated monthly cap (roughly 17,280/day if sustained), publishes a public status page, an llms.txt, and a machine-readable OpenAPI spec that this benchmark's probes validated.
- **TheRundown** offers the largest stated daily free allowance in this comparison (20,000 data points/day per its pricing page), covers prediction-market exchanges (Kalshi, Polymarket, Novig, ProphetX), and its reference endpoints answered keyless probes with real JSON. It has also been the fastest keyless-200 endpoint in this repo's latency probe, faster than ParlayAPI's keyless endpoint in recent committed runs; see the latest latency table and [RESULTS.md](RESULTS.md) for current numbers.
- **OddsPapi** claims the largest bookmaker count in this comparison (350+ per its own pages, including sharp books and exchanges) and publishes an llms.txt. Its build-your-own pricing calculator lets you pay for only the books and sports you need.
- **SportsGameOdds** publishes both an llms.txt and a machine-readable OpenAPI spec that this benchmark's probes validated, and prices per event object rather than per market/book combination, which can be materially cheaper for wide market coverage; its pricing page states plan terms plainly.
- **ParlayAPI** (the maintainer's product) answered the most keyless probes in this run, but the probe list is curated by the maintainer (competitor keyless endpoints are added by PR), and note what it lacks versus the others: no public uptime/incident history was detected on its status page, its headline book count (30+ sportsbooks per its own pages) is smaller than most competitors' headline counts in this comparison, and its keyless endpoint has not been the fastest in this repo's own latency probe.

If any of this is stale or wrong, open a PR with the vendor's current page and read date.

## Contributing

PRs welcome, including and especially from the vendors benchmarked here. Ground rules: every claim needs either a probe script that reproduces it or a citation to a vendor's own page with URL and read date. Fixes to probe targets, added vendors, and corrections to stale free-tier terms are all fair game. Marketing copy is not.

## License

MIT. Results data is factual output of the probes and carries no warranty.
