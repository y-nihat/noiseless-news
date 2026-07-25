# Article File Format

Published articles are markdown files with YAML frontmatter, one per language:
`content/articles/en/YYYY/MM/<slug>.md` and `content/articles/tr/YYYY/MM/<slug>.md`
(same slug; the Turkish version is a semantic mirror of the finished English one).

```markdown
---
title: Plain factual headline written by us — never a source headline
date: 2026-07-09
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
updated: []                      # changelog entries, e.g. "2026-07-10: added independent confirmation"
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
