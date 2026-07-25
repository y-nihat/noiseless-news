# noiseless-news

An autonomous news site for artificial intelligence that publishes **only what it can
verify across independent sources** — and shows its work.

**Live site: https://y-nihat.github.io/noiseless-news/** · [Türkçe](https://y-nihat.github.io/noiseless-news/tr/)

Articles are written and verified by AI agents following the rules in
[`policy/verification.md`](policy/verification.md), with no per-article human
review before publication. Every article lists its sources; every verdict's
evidence log is committed to this repository.

## Why

Most AI news competes for attention: clickbait headlines, recycled press releases,
single-source rumors. This project inverts the incentive. A pipeline scans a fixed,
public registry of named sources every night, decomposes candidate stories into factual
claims, verifies each claim against independent evidence (walking citations back to
primary sources), discards anything that is attention-bait without substance, and then
writes compact articles — headline included — from the verified claims only. Every
article lists its sources; every verdict's evidence trail is committed to this
repository, so any reader can audit why we said what we said.

If nothing meets the bar on a given day, the site says so. That is a feature.

## How it works

```
ingest → triage → verify (claims + evidence) → synthesize (EN → TR) → publish
```

Ingest and publish are deterministic Python. Triage, verification and synthesis
are steps inside one nightly agent cycle that reads `policy/` at run start.

- **Deterministic ingest** from RSS/Atom feeds, the arXiv API, and other registered
  sources (`policy/sources.yaml`) — rate-limited, deduplicated, no LLM involved.
- **Claim-level verification** by AI agents following the rules in
  `policy/verification.md`: source tiers, independence requirements, and per-claim-type
  standards of proof. Community sources (YouTube, Hacker News, X) are used for
  discovery only, never as confirmation.
- **Bilingual output**: English is canonical; Turkish articles are generated from the
  finished English article with identical structure.
- **Static publishing** to GitHub Pages. No trackers, no ads, no engagement metrics.

## Running locally

Everything runs in Docker — no local installs required.

```sh
cp .env.example .env      # add your credentials
docker compose build
docker compose run --rm pipeline pytest          # unit tests
docker compose run --rm pipeline python -m noiseless.run validate-sources
docker compose run --rm pipeline python -m noiseless.run ingest
```

Outputs land in `data/` (pipeline artifacts, committed as an audit trail) and
`content/` (published articles).

## Status

Running. The pipeline has published on most nights since 9 July 2026, in English
and Turkish, unattended.

- **Nightly** (`.github/workflows/nightly.yml`) — up to six cycles between 01:00
  and 04:20 Istanbul. Each cycle re-ingests the feeds, re-checks open stories,
  triages, verifies, and publishes what clears the bar. Caps: 4 stories per
  cycle, 12 per night, 15 searches per story.
- **Daytime ingest** (`.github/workflows/ingest.yml`) — 13:00 and 19:00 Istanbul,
  deterministic feed capture only, no model calls.
- **Deploy** (`.github/workflows/deploy.yml`) — rebuilds and publishes the site
  on every push to `main`.
- **Tests** (`.github/workflows/tests.yml`) — unit tests, registry validation and
  a full site build on every push and pull request.

Nightly run reports, including what was *not* published and why, are in
[`data/ledger/`](data/ledger/).

## Reading an article

Each article carries a TL;DR, the body, and a verification box listing every
factual claim with a verdict:

| Verdict | Means |
|---|---|
| `confirmed` | Met the standard of proof for its claim type (`policy/verification.md` §3) |
| `vendor-claim` | Stated by the party that benefits, published as their claim, not as fact |
| `single-source` | One source only, published as such because the claim is load-bearing context |
| `disputed` | Sources disagree; both accounts are given |

Numbered sources follow. The full reasoning behind each verdict — which outlets
were checked, which were excluded as wire relays, what the adversarial pass
tried and failed to break — is in `data/verified/<slug>.json`.

## Licence

Code is MIT; articles, policy and evidence logs are CC BY 4.0; third-party feed
material in `data/raw/` remains its publishers'. See [LICENSE](LICENSE) and
[NOTICE](NOTICE).
