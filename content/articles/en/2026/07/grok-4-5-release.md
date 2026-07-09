---
title: xAI releases Grok 4.5, positions it on price and token efficiency rather than raw benchmark scores
date: 2026-07-09
slug: grok-4-5-release
lang: en
tldr: >
  xAI, now publishing under the SpaceXAI brand, released Grok 4.5 on 8 July 2026 at
  $2/$6 per million input/output tokens with a 500,000-token context window. Elon
  Musk called it "roughly comparable to Opus 4.7"; on xAI's own benchmark chart it
  trails Anthropic's Opus 4.8 and Claude Fable 5 on SWE-Bench Pro while using
  markedly fewer output tokens per task.
sources:
  - name: xAI News (SpaceXAI)
    url: https://x.ai/news/grok-4-5
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/08/spacexai-releases-grok-4-5-which-elon-describes-as-an-opus-class-model/
  - name: InfoWorld
    url: https://www.infoworld.com/article/4194895/spacexai-launches-grok-4-5-touts-lower-coding-task-costs-than-ai-rivals.html
claims:
  - text: "xAI, operating under the SpaceXAI brand, released Grok 4.5 on 8 July 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Grok 4.5 is priced at $2 per million input tokens and $6 per million output tokens, with a 500,000-token context window"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "Musk described Grok 4.5 as roughly comparable to Opus 4.7 in capability; on xAI's own SWE-Bench Pro chart it scores behind Opus 4.8 and Claude Fable 5, while using about 4x fewer output tokens per resolved task than Opus 4.8"
    type: capability
    verdict: vendor-claim
    evidence: [2, 3]
updated: []
---

## What happened

xAI — now publishing its announcements under the SpaceXAI brand — released Grok
4.5 on 8 July 2026 [1][2]. The model is priced at $2 per million input tokens and
$6 per million output tokens, with a 500,000-token context window [1][3].

Elon Musk described the model as "roughly comparable to Opus 4.7," Anthropic's
prior-generation flagship, rather than claiming it beats Anthropic's current
model [2]. xAI's own benchmark chart, cited by multiple outlets, puts Grok 4.5
behind both Opus 4.8 and Claude Fable 5 on the SWE-Bench Pro coding benchmark,
but shows it resolving tasks using roughly four times fewer output tokens than
Opus 4.8 — the company's central pitch is efficiency and price rather than
topping the leaderboard [2][3].

## Why it matters

Grok 4.5 arrives positioned as a value option in the coding-agent market rather
than a benchmark leader: xAI is not disputing that it trails Opus 4.8 and Claude
Fable 5 on raw capability, betting instead that lower per-task cost and token
usage will win developers who don't need the top score on every benchmark. The
capability comparisons come from xAI's own reporting and have not yet been
independently reproduced — treat the specific benchmark gaps as the company's
account until third-party evaluations appear.
