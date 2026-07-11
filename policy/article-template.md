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
