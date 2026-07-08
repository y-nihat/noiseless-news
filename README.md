# noiseless-news

An autonomous news site for artificial intelligence that publishes **only what it can
verify across independent sources** — and shows its work.

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
ingest → triage/cluster → verify (claims + evidence) → synthesize (EN → TR) → publish
```

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

Early scaffolding. Roadmap: ingest ✅ (skeleton) → triage → verification agents →
synthesis → static site → nightly GitHub Actions runs.
