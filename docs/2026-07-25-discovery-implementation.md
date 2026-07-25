# Discovery report → implementation ledger

**Date:** 2026-07-25 · **From:** `c5fb95a` · **To:** `b2c8e97` · **15 pull requests, all merged.**

Every recommendation from the 24 July discovery audit has an outcome below. Nothing
was silently dropped. Where something was not done, the reason is recorded and, where
it matters, so is the condition for reconsidering it.

## What changed, at a glance

| | before | after |
|---|---|---|
| Automated tests run | never | every push and PR |
| Test count | 33 | 230 |
| Checks between agent commit and live site | none | 6 blocking + 2 advisory |
| Reader-facing pages | index + articles | + About, Corrections, Not published, feeds, sitemap, robots |
| Per-claim verifier reasoning visible | no | yes, 194 of 261 claims |
| Night cost recorded | never | per cycle |
| Ways to pause publishing | none documented | `.paused` file |
| Licence | none (all rights reserved) | MIT + CC BY 4.0 + NOTICE |

## Implemented

| # | Recommendation | PR | Notes |
|---|---|---|---|
| 1 | Run the test suite in CI | [#3](../../pull/3) | Plus `pythonpath` so `pytest` works from a fresh checkout |
| 2 | Path allowlist in `commit_push`; injection framing in the prompt | [#4](../../pull/4) | `git add -A` → `content/ data/`, with a guard that reports and reverts strays |
| 3 | Push-failure capture, zero-publish alert, cost telemetry, per-source ingest stats | [#5](../../pull/5) | A lost push now fails the job; `source_stats.jsonl` makes §4's dead-feed rule runnable |
| 4 | Dedup key fallback, bare-URL exclusion, real-shaped fixture, ledger schema | [#6](../../pull/6) | Two watching stories went from invisible to matching; 0 false strong pairs |
| 5 | Defensive parsing; atomic site build | [#7](../../pull/7) | One bad file no longer takes down the site and the duplicate gate together |
| 6 | LICENSE, NOTICE, README rewrite, architecture corrections | [#8](../../pull/8) | Three phantom stages removed from `CLAUDE.md` |
| 7 | **P0** About + corrections pages, footer disclosure, §10 naming people, §11 retractions | [#9](../../pull/9) | The accountability surface the site did not have |
| 8 | `published:` separate from event date; index re-sort; updated chip | [#10](../../pull/10) | 22 pairs backfilled from git; had to land before feeds |
| 9 | Atom feeds, sitemap, robots, canonical, hreflang, Open Graph, index `h1` | [#11](../../pull/11) | `SITE_URL` is the single constant a custom domain would change |
| 10 | Render the evidence trail; citation anchors | [#12](../../pull/12) | The highest-value change in the series; 194/261 claims show reasoning |
| 11 | Publish the held-stories record; §11a on what it may contain | [#13](../../pull/13) | Internal `reason` is never rendered — asserted by test |
| 12 | Deterministic content gate | [#14](../../pull/14) | 6 blocking checks pass today; 2 advisory warnings recorded, not hidden |
| 13 | Weekly source health, RUNBOOK, pause sentinel, contactable User-Agent | [#15](../../pull/15) | Runs the validator that had never once run |
| 14 | Cap retained feed summaries; disable raw HTML in bodies; chase pending outcomes | [#16](../../pull/16) | Redistribution, defence-in-depth, and §3's follow-up obligation |
| 15 | Per-cycle tool-activity telemetry | [#17](../../pull/17) | Makes §5's protocol claim checkable from committed data |

## Replaced with something better

**Runtime guard on the language switcher** → the content gate now fails the build when
an English article has no Turkish twin, or when their claims, sources or dates disagree.
A structural guarantee beats a runtime fallback for an invariant that has held 57/57.

**`*.jsonl` in `.gitignore` as a stray-file safety net** → superseded by the path
allowlist, and it would now silently drop the telemetry files the same audit asked for.

**Uploading the full agent stream as a workflow artifact** → replaced by committed
tool-call counts. The stream carries drafts and fetched page content; the counts answer
the same question without creating a second path for that content to escape.

## Deferred, with the condition for revisiting

| Recommendation | Why not now | Revisit when |
|---|---|---|
| Reclaim the inter-cycle `sleep`; fix the unreachable 6th cycle | The report is explicit that cost telemetry must land first and be read for a week. It landed in #5; the data does not exist yet. Removing the sleep raises spend and there is no enforced ceiling. | After ~7 nights of `night-stats.jsonl` |
| Topic pages and a paginated archive | Not urgent at 57 articles (~49 KB index). Needs a controlled vocabulary and a hand backfill, and doing it badly produces near-synonym sprawl within weeks. | Past ~150 articles, or when the index stops being scannable |
| `candidate` / `dropped` ledger states and a `ledger-write` command | The schema and the duplicate gate are fixed; adding states changes nightly agent behaviour and widens the dedup false-positive surface, which already costs coverage. Best decided alongside the sleep/pacing change. | Alongside the next cycle-prompt revision |
| Localized dates, mobile verification-block layout, three WCAG-AA colour pairs, claim-row list semantics | Real but small, and none of them blocks a reader today. Grouping them into one considered pass beats scattering them through a series about correctness. | Next UX pass |
| `claims.json` machine-readable dataset | The report's own condition: resolve the verdict-calibration question first, or the dataset makes the inconsistency machine-queryable. | After the `confirmed` badge question is settled |
| Pin `@anthropic-ai/claude-code`; pin actions to SHAs | Pinning to a version nobody has tested here trades a supply-chain risk for a "the night silently stopped working" risk. Needs a version the owner has run. | When a known-good version is chosen |
| Scope the agent's tool permissions | Restricting tools blindly could break verification in ways only visible at 03:00. The path allowlist bounds persistence, which was the actual risk. | With evidence of which tools each cycle really needs — now measurable via #17 |
| Backfill `open_obligation` on the 9 pending-outcome articles | The mechanism shipped in #16; backfilling is an editorial judgement per article about what outcome is owed. | Next time the agent re-checks each story |

## Not done — needs the owner

These are decisions, not tasks. Implementing them by inference would have been the wrong call.

1. **Repair the 5 bare-origin source URLs.** Finding the real permalinks needs research; inventing a plausible-looking URL is strictly worse than leaving a visibly broken one on a site whose proposition is that citations can be checked. The content gate now reports them on every CI run and every night report until they are fixed.
2. **Resolve `style.md` gate 1 vs `verification.md` §3.** Gate 1 requires headlines to rest on `confirmed` claims; §3's litigation row explicitly permits publication at dispute stage. Both are defensible and they contradict each other. One article sits on the wrong side of it. Settling this unblocks `--warn-as-error` and `--strict` in the night loop.
3. **The 68–80 unanswered tuning questions.** No amount of code answers them. The report's decision-queue mechanism (`data/ledger/open-questions.md`, deduplicated, read at run start) is still the right shape.
4. **Who may edit `sources.yaml`.** `CLAUDE.md` gives the agent ownership of the registry; `cycle-prompt.md`'s last line forbids editing policy files. This shipped contradictory on day two. Pick one: carve the two registry files out of the prohibition, schedule a review pass, or delete the promise.
5. **The custom domain.** `SITE_URL` is one constant. Until it changes, canonical URLs and feed ids point at the github.io origin while the wordmark says `noiseless.news`.
6. **Whether §5 describes what actually happens.** #17 makes it checkable. Confirming it, or rewriting the policy, is the more important half.
7. **Branch protection.** Not enabled, and enabling it naively on `main` would break the night loop, which pushes directly. If wanted, the shape is CODEOWNERS on `policy/`, `pipeline/` and `.github/` with the loop's data paths exempt.

## Rejected

Per the report's own "Do not build" section, and unchanged after implementation: reader
comments, on-site full-text search, an email newsletter, a framework rewrite of the site
generator, expanding beyond the AI vertical, per-source reliability scores rendered
publicly, and letting the night agent edit `policy/` freely.

## Known state at hand-off

- **CI:** 230 tests, plus registry validation, content validation and a full site build, on every push and PR.
- **Content gate:** 57 articles, **0 errors, 6 warnings** — 5 bare-origin URLs across 3 articles, 1 article with no `confirmed` claim.
- **Live site:** all new surfaces verified 200 — `/about.html`, `/held.html`, `/corrections.html`, `/feed.xml`, `/sitemap.xml`, `/robots.txt`, and the Turkish equivalents.
- **Untested locally:** Docker Desktop was unreachable from the development environment for this series, so every change was validated in CI rather than in the container. `docker compose run --rm pipeline pytest` remains the documented local command and should be run once when Docker is available.
- **The night loop has not yet run** with any of these changes. The first run under them is the night of 25–26 July; its report will carry the new footer fields, the content-gate output and the first cost figure.
