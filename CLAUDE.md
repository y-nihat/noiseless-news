# noiseless-news — Working Conventions

Autonomous, bilingual AI-news site: publishes only multi-source-verified information,
filters clickbait, writes its own headlines/articles, lists sources under every article.

## Non-negotiable rules

- **NEVER** add `Co-Authored-By`, "Generated with Claude Code", or any AI-attribution
  line to commit messages, PR bodies, or file headers. Commits must appear to come
  solely from the repository owner. Write commit messages in plain, human style.
- **No local installs.** Everything runs through Docker Compose:
  `docker compose run --rm pipeline <command>`. Outputs are volume-mapped into the repo.
- **Commit regularly** in small logical units. Every pipeline change ships with pytest
  unit tests, run inside Docker: `docker compose run --rm pipeline pytest`.
- `.env` holds `CLAUDE_CODE_OAUTH_TOKEN`. Never commit it, never print its value.
  In CI it lives as a GitHub Actions secret.
- **Local dev hygiene:** the nightly CI run owns `data/` (including
  `data/state/seen_ids.json`). Before any local run that writes `data/`, `git pull`
  first; for experiments, pass a scratch dir (`ingest --data-dir /tmp/nn-data`)
  so local state never diverges from CI.

## Model & credit policy

- Web research / verification agents: **Sonnet 5** (`claude-sonnet-5`), `effort: max`.
- Cheap mechanical passes (triage, dedup assist) may use Haiku.
- Batch runs happen **nightly** (~03:00 Europe/Istanbul = 00:00 UTC) to conserve credits.
- Every agentic stage has hard budget caps (max stories per run, max tool calls per story).

## Architecture (5 file-based stages)

```
ingest (deterministic Python, no LLM)  → data/raw/YYYY-MM-DD/*.json
triage/cluster (LLM, cheap)            → data/clusters/
verify (Agent SDK: claims+evidence)    → data/verified/<story>.json
synthesize (EN article, then TR)       → content/articles/{en,tr}/YYYY/MM/slug.md
publish (Astro → GitHub Pages)         → static site
```

- `data/` is committed: git history is the public audit trail.
- Story lifecycle lives in `data/ledger/` (candidate → verifying → published/watching/dropped);
  nightly runs reconcile new items against open stories before creating new ones.
- All editorial behavior is defined in `policy/verification.md` and `policy/sources.yaml` —
  agents read these at run start. Tune the documents, not the code.

## Bilingual rule

English is canonical (sources are foreign). Turkish articles are generated from the
**finished English article**, mirroring its structure semantically — never translated
from raw sources. Same slug, parallel trees under `content/articles/en/` and `/tr/`.

## Source curation (delegated to the agent — owner decision, 2026-07-08)

- `policy/sources.yaml` is the single registry: named sources, tiers 0–3, statuses
  active/candidate/retired, optional per-source `delay_seconds`.
- The agent owns expanding, evaluating, promoting, demoting, and retiring sources per
  `policy/source-lifecycle.md` — always via commits, never silently.
- Discovery keywords live in `policy/discovery.yaml`; run-specific queries are appended
  at run time, recurring ones proposed via commits.
- Live-check the registry:
  `docker compose run --rm pipeline python -m noiseless.run validate-sources --live`
  (only `active` sources are checked/ingested; candidates are re-checked by the
  periodic source-review pass).

## Verification principles (summary — full rules in policy/verification.md)

- Verify **claims**, not articles. Claim types have different standards of proof.
- Tier 3 sources (YouTube transcripts, HN, X, newsletters) are discovery only — never confirmation.
- Independence rule: N outlets citing the same press release/tweet = 1 source.
- Multi-agent protocol: the verifier is a fresh context that did not draft the story,
  plus an adversarial falsification pass before publish.
- Keyword web searches are used to cross-check claims across sources.
