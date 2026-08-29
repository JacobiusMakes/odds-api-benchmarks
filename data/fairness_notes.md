## Fairness notes: what each vendor does well

A benchmark maintained by one vendor's founder owes you this section. Based on the latest committed results and the cited vendor pages:

- **The Odds API** runs a public status page with visible uptime history and status update history, which ParlayAPI's live status page does not show (ParlayAPI's page shows current per-source freshness, not historical uptime). Its free tier requires no configuration and its pricing page states plan sizes in one screen.
- **SharpAPI** offers a free tier of 12 requests/min with no stated monthly cap (roughly 17,280/day if sustained), publishes a public status page, an llms.txt, and a machine-readable OpenAPI spec that this benchmark's probes validated.
- **TheRundown** offers the largest stated daily free allowance in this comparison (20,000 data points/day per its pricing page), covers prediction-market exchanges (Kalshi, Polymarket, Novig, ProphetX), and its reference endpoints answered keyless probes with real JSON. It has also been the fastest keyless-200 endpoint in this repo's latency probe, faster than ParlayAPI's keyless endpoint in recent committed runs; see the latest latency table and [RESULTS.md](RESULTS.md) for current numbers.
- **OddsPapi** claims the largest bookmaker count in this comparison (350+ per its own pages, including sharp books and exchanges) and publishes an llms.txt. Its build-your-own pricing calculator lets you pay for only the books and sports you need.
- **SportsGameOdds** publishes both an llms.txt and a machine-readable OpenAPI spec that this benchmark's probes validated, and prices per event object rather than per market/book combination, which can be materially cheaper for wide market coverage; its pricing page states plan terms plainly.
- **ParlayAPI** (the maintainer's product) answered the most keyless probes in this run, but the probe list is curated by the maintainer (competitor keyless endpoints are added by PR), and note what it lacks versus the others: no public uptime/incident history was detected on its status page, its headline book count (30+ sportsbooks per its own pages) is smaller than most competitors' headline counts in this comparison, and its keyless endpoint has not been the fastest in this repo's own latency probe.

If any of this is stale or wrong, open a PR with the vendor's current page and read date.
