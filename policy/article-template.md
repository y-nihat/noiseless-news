# Article File Format

Published articles are markdown files with YAML frontmatter, one per language:
`content/articles/en/YYYY/MM/<slug>.md` and `content/articles/tr/YYYY/MM/<slug>.md`
(same slug; the Turkish version is a semantic mirror of the finished English one).

```markdown
---
title: Plain factual headline written by us — never a source headline
date: 2026-07-09              # when the EVENT happened — used in the byline
published: 2026-07-11         # OPTIONAL — when WE published it. Omit when it is the
                              # same day as `date`. Set it whenever verification ran
                              # past the event: the index is ordered by this, so an
                              # article dated three days ago would otherwise appear
                              # below stories the reader has already seen, on its
                              # own launch day.
slug: example-story
lang: en
tldr: >
  Two or three sentences a reader can stop after. What happened, why it matters.
sources:
  - name: OpenAI News
    url: https://openai.com/...
  - name: MIT Technology Review AI
    url: https://www.technologyreview.com/...
claims:
  - text: "X released model Y on 8 July"
    type: announcement           # announcement | capability | business | research | statement
    verdict: confirmed           # confirmed | vendor-claim | single-source | disputed
    evidence: [1]                # indices into the sources list (1-based)
  - text: "Y outperforms Z on benchmark B"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
updated: []                      # dated changelog entries, newest last. Two kinds:
                                 #   "2026-07-10: added independent confirmation"
                                 #   "correction: 2026-07-10: the round was $200M, not $300M"
                                 # Untyped entries are updates: new information on a
                                 # story that was right. A `correction:` entry says a
                                 # published claim was WRONG, and is collected onto
                                 # /corrections.html automatically. Same in both languages.
follows: earlier-story-slug      # OPTIONAL — only on follow-up articles (verification.md §8):
                                 # slug of the immediate predecessor in the same story thread.
                                 # Same value in both language versions; mirror it in the ledger entry.
---

## What happened

Compact inverted-pyramid body. Every factual sentence traceable to a numbered source.

## Why it matters

Short. No padding, no speculation beyond what the claims support.
```

Rules (enforced by policy/verification.md): publish only if every load-bearing claim
is `confirmed` or explicitly labeled; the verification box and numbered sources are
rendered automatically by the site builder from the frontmatter — do not repeat them
in the body.

## Ledger entry format

One file per story at `data/ledger/<slug>.json`, for every story ever opened —
published or not. This is the schema `noiseless.dedup.load_index` reads; the
duplicate gate (§0a) is only as sharp as these files are.

```json
{
  "slug": "example-story",
  "title": "The working headline, always — even for an unpublished story",
  "status": "published",
  "first_seen": "2026-07-09",
  "published_at": "2026-07-09",
  "langs": ["en", "tr"],
  "source_urls": ["https://example.com/the-specific-page"],
  "follows": null,
  "reason": "Why it is in this state — required for anything not published",
  "watch": ["What evidence would change the verdict"],
  "notes": ["2026-07-09 c1: dated note, appended to this array"]
}
```

Required on every entry: `slug`, `title`, `status`, `first_seen`, `source_urls`.

- **`status`** — `candidate` · `verifying` · `published` · `watching` · `dropped`.
- **`title` is required even when nothing was published.** An entry with no title
  and no URLs scores 0.0 against every future candidate, so the story becomes
  invisible to the gate that exists to catch it. The loader falls back to the
  slug, but that is a safety net, not the contract.
- **`source_urls` must be deep links**, never bare origins like
  `https://www.reuters.com/`. A bare origin is dropped as story identity and,
  in an article's `sources`, leaves the reader with nothing to audit.
- **Dated notes go in the `notes` array**, not in new top-level keys. One entry
  had grown to 37 keys of near-identical nightly prose.
- `follows` mirrors the article frontmatter for follow-ups (verification.md §8).

## Evidence log format

One file per **published** story at `data/verified/<slug>.json`. This is the
audit trail the site's credibility rests on: the article page links to it, and
`publish.py` reads it to show the verifier's reasoning under each claim. Until
2026-08-19 it was the one deliverable with no written contract, and it was the
one that got skipped.

```json
{
  "slug": "example-story",
  "checked_at": "2026-08-19T01:07:00+00:00",
  "method": "Fresh verifier + fresh adversarial falsifier, both run in cycle 5 of 2026-08-19; ...",
  "origin_items": ["data/raw/2026-08-18/techmeme.json#item-id", "..."],
  "claims": [
    {
      "text": "The exact claim text as it appears in the article, in order",
      "type": "fact",
      "verdict": "confirmed",
      "reasoning": "What was checked, against what, and why this verdict",
      "evidence": ["https://example.com/the-specific-page", "..."]
    }
  ],
  "falsifier_notes": "What the adversarial pass tried to break and what happened",
  "dedup_check": "The dedup-check result and the §8 outcome chosen"
}
```

- **The build enforces**: the file exists, parses as a JSON object, and
  `claims` is a non-empty list. An article whose log fails that is **held**
  from the site (a stub at its URL, absent from index/feed/sitemap) until it is
  repaired. Nothing else is enforced by machine today — the fields below are the
  editorial contract.
- **Written from verification that actually happened.** `method` names the
  cycle and date; a log written after publication says so ("re-verified in
  cycle N of <date>; the original log was not written when the article was
  published in cycle K of <date>"). Never written from the article text, the
  run report, the ledger prose or memory; never a stub — a log written by a
  party that did not verify is a fabricated audit trail, worse than an honest
  hold.
- **Written FIRST**, before the article: a timeout then leaves a harmless orphan
  log, never an unauditable article.
- One `claims[]` entry per article claim, in the article's order, with the same
  `text`, `type` and `verdict` — that is what lets the site match reasoning to
  claims. In-place updates that add claims append here too.
- `evidence` are deep links, never bare origins.
