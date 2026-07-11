# Verification Policy

This document is the editorial constitution of noiseless-news. Every agent in the
pipeline reads it at the start of a run and must follow it exactly. It is public:
readers can audit our standards here, and the git history of this file shows every
change we have ever made to them.

## 0. Scope

The editorial scope is the **AI vertical**: models, research, labs, AI industry,
AI policy/regulation, AI litigation, and AI compute/chips. Adjacent technology
stories qualify only with an explicit AI angle (owner ruling, 2026-07-11 — e.g.
general algorithmic-feed/social-platform regulation is out of scope; an AI-chip
supply deal is in).

## 0a. Duplicate prevention (archive-wide)

We publish daily; the archive spans all dates. A story covered last week is a
duplicate today, whatever the calendar folder says — date lives with each story
in its frontmatter, ledger entry, and the story index.

- **Before opening any story**, run the deterministic gate:
  `python -m noiseless.run dedup-check --title "<working title>" --url "<primary url>"`
  It checks title similarity and shared source URLs against every article and
  ledger entry ever created.
- Exit 2 (**strong match**): do NOT create a new article. Either apply a §8
  update to the matched slug (only if genuinely new information exists) or skip.
- **Moderate matches**: read the matched article before deciding new vs update;
  justify the decision in the run report.
- The dedup-check result (matches found, decision taken) is recorded in the
  story's evidence log.

## 1. Source tiers

Sources are registered by name in `sources.yaml`. Unregistered sources found during
research may be used as evidence only if they would qualify for Tier 0–2 and are
recorded in the evidence log with a note; they must be proposed for registration.

| Tier | Role | Examples |
|---|---|---|
| 0 — Primary | Can alone confirm *announcement* claims | Official lab/company blogs, release notes, model cards, GitHub releases, regulatory filings, government/legal texts |
| 1 — Literature | Confirms *research* claims (peer-review status must be labeled) | arXiv preprints, Nature/Science journals, conference proceedings |
| 2 — Quality press | Independent confirmation; business and context claims | Established outlets with editorial standards and named authors |
| 3 — Community | **Discovery only. Never confirmation.** | YouTube transcripts, Hacker News, X/Twitter, newsletters, forums |

## 2. Independence rules

- Multiple outlets repeating the same press release, wire story, paper, or tweet count
  as **one** source (the underlying one). Trace each piece of evidence to its origin
  before counting it.
- **Wire-exclusive check (named, mandatory):** when coverage is broad but every
  account traces to a single outlet's exclusive (e.g. one Reuters story citing a
  leaked memo), the story has ONE source regardless of how many outlets relay it.
  Run this check explicitly for every business/insider story before counting sources.
- Always walk at least one hop toward the primary source (max depth 2). If a Tier-2
  article cites a paper, verify against the paper, not against another article citing it.
- Two sources are independent only if neither derives its information from the other
  or from a shared single origin.

## 3. Claim types and standards of proof

Stories are decomposed into individual factual claims. Each claim is typed:

| Claim type | Standard to publish |
|---|---|
| Announcement ("X released Y") | One Tier-0 primary source |
| Capability ("Y outperforms Z") | Independent reproduction, **or** publish labeled as *vendor claim* |
| Business (funding, acquisition, layoffs, lawsuits) | ≥2 independent sources of Tier ≤2, or a filing/court document |
| Research finding | The paper itself; label *preprint — not peer-reviewed* where applicable |
| Legal / litigation (filings, motions, allegations) | Publish at dispute stage, but every allegation strictly attributed to the filing party ("plaintiffs allege"), never stated as found fact; prefer docket/primary documents; update the article when rulings land |
| Rumor / unnamed-sources | Never published as fact. May be held internally in `watching` state |

Verdicts per claim: `confirmed` · `vendor-claim` · `single-source` · `disputed` · `unverifiable`.

**Publishing gate:** a story is published only if every load-bearing claim is
`confirmed` or explicitly labeled (`vendor-claim`, `preprint`). Any `disputed` claim
must either be resolved or presented as a documented disagreement with both sides cited.

## 4. Clickbait and substance filters

1. **Residual-substance test:** remove the headline's promise — do verifiable claims
   remain? If the claim set is empty or purely speculative, drop the item (record the
   reason in the ledger).
2. **Headline–body consistency:** if a source's own body does not support its headline,
   discard the headline; only body claims enter verification.
3. **We never reuse source headlines.** Headlines are written by us, from verified
   claims only, in plain factual language. No curiosity gaps, no superlatives that the
   claims do not support.

## 5. Multi-agent protocol

- The **verifier** is a fresh context that did not draft or triage the story. It
  receives the claims and must gather evidence itself.
- Before publishing, an **adversarial falsification pass** (another fresh context)
  attempts to break each claim: search for contradicting reports, check dates,
  check whether "new" findings are actually old.
- Cross-verification includes targeted keyword web searches, not only registered feeds.
- Disagreement between agents downgrades the claim to `disputed` and blocks publication
  until resolved with additional evidence.
- **Live-fetch rule for numbers:** any third-party numeric citation (benchmark ranking,
  leaderboard position, score) must come from a fetch of the source performed at
  publication time, and the evidence log must record the fetch timestamp. Leaderboards
  drift; recalled or search-snippet figures are not citable.

## 6. Writing rules

- Compact, inverted-pyramid articles: TL;DR (2–3 sentences) → what happened → why it
  matters → verification box (claim-by-claim status) → numbered sources.
- Every sentence containing a factual claim must be traceable to a numbered source.
- No filler, no engagement-bait, no unattributed speculation. Target ≈2-minute reads.
- Uncertainty is stated plainly ("independent confirmation is not yet available").

## 7. Bilingual rule

English articles are canonical. The Turkish version is generated from the finished
English article — identical structure, same sources, same labels — never from raw
source material. Both versions share a slug and are updated together.

## 8. Updates, follow-ups, and corrections

When the duplicate gate (§0a) links a new development to an existing story, pick
one of three outcomes — never an unlinked duplicate:

| Situation | Action |
|---|---|
| Same event, new details (extra confirmation, minor development) | **In-place update**: edit the existing article, add a dated `updated:` changelog entry |
| A NEW event in the same saga (ruling in a covered lawsuit, launch of a previewed product, follow-through or reversal of a covered announcement) | **Follow-up article**: new slug, frontmatter `follows: <original-slug>` — the site renders the whole thread ("story so far") on every member article |
| Unrelated despite surface similarity | New standalone article; note the dedup decision in the report |

- The follow-up test: could a reader who missed the original still need that
  context? If yes, it's a follow-up (`follows`), not an in-place update.
- `follows` points at the immediate predecessor; chains are allowed
  (original ← follow-up ← follow-up). The ledger entry mirrors the `follows` field.
- Errors are corrected visibly: the correction is noted in the article and logged on a
  public corrections page. The original wrong text remains available via git history.

## 9. Budget discipline

- Research/verification agents run on Sonnet 5 at max effort; hard caps apply per run
  (max stories, max tool calls per story). When the budget is hit, remaining candidates
  stay in `watching` for the next run — never lower the evidence bar to save budget.
