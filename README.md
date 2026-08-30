# noiseless-news

An autonomous news site for artificial intelligence that publishes **only what it can
verify across independent sources** — and shows its work.

**The site is offline.** Publishing stopped on 30 August 2026 and the site that was
served at `https://y-nihat.github.io/noiseless-news/` has been taken down. Every article,
evidence log and ledger entry stays here, in English and Turkish, under
[`content/articles/`](content/articles/) and [`data/`](data/).

**Corrections and right of reply are still read.** If something here is wrong, or you are
named in an article and want to respond, [open an issue](https://github.com/y-nihat/noiseless-news/issues/new)
— the tracker stays open and this repository stays public. Publishers asking for feed
material in `data/raw/` to be removed should do the same; see [NOTICE](NOTICE).

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

**Stopped.** The pipeline ran unattended from 9 July 2026 and published 159 stories,
each in English and Turkish, the last on 26 August 2026. It was stopped on 30 August
2026: all five GitHub Actions workflows are disabled, `.paused` is present at the repo
root, and the published site has been taken down. Nothing runs on a schedule any more.

Two things the archive still owes its readers, written down here because the pages that
carried them are gone:

- **33 published stories carry `open_obligation: true`** in [`data/ledger/`](data/ledger/),
  each with a `revisit_after` date — mostly legal proceedings whose outcome this project
  said it would follow up. Those follow-ups will not be published. `policy/verification.md`
  calls a published accusation with no published outcome a defect; it is one, and it is
  recorded here rather than quietly dropped.
- **11 stories sit in `watching`** in the ledger — reported somewhere, never verified to
  the standard needed to publish them. They stay unpublished, listed in `data/ledger/`.

What ran while it was running:

- **Nightly** (`.github/workflows/nightly.yml`) — up to three cycles between 05:00
  and 07:00 Istanbul. Each cycle re-ingests the feeds, re-checks open stories,
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
