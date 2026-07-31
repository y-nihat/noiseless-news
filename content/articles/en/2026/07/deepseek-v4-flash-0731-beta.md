---
title: DeepSeek releases V4-Flash-0731 in public beta amid intensifying AI price competition
date: 2026-07-31
slug: deepseek-v4-flash-0731-beta
lang: en
tldr: >
  DeepSeek released DeepSeek-V4-Flash-0731 into public beta via its API on 31
  July 2026, a re-post-trained update of the V4-Flash model it open-sourced
  as a preview on 24 April, aimed at better agentic, coding and tool-use
  performance. V4-Pro, previewed the same day in April, was not updated.
  Pricing is unchanged, and the release lands the same week OpenAI cut prices
  on GPT-5.6 Luna, intensifying competition on cost among frontier labs.
sources:
  - name: DeepSeek API (updates log)
    url: https://api-docs.deepseek.com/updates/
  - name: DeepSeek API (V4 preview announcement)
    url: https://api-docs.deepseek.com/news/news260424/
  - name: DeepSeek API (pricing)
    url: https://api-docs.deepseek.com/quick_start/pricing
  - name: Nikkei Asia
    url: https://asia.nikkei.com/business/technology/artificial-intelligence/deepseek-releases-beta-version-of-v4-models-as-ai-price-war-heats-up
  - name: VentureBeat
    url: https://venturebeat.com/technology/ai-price-wars-openai-cuts-gpt-5-6-luna-prices-by-80-as-model-competition-shifts-toward-cost
  - name: Artificial Analysis
    url: https://artificialanalysis.ai
claims:
  - text: "DeepSeek released DeepSeek-V4-Flash-0731 into public beta via its API on 31 July 2026, a re-post-trained update of V4-Flash aimed at improved agentic, coding and tool-use performance"
    type: announcement
    verdict: confirmed
    evidence: [1, 4]
  - text: "V4-Flash was originally open-sourced on 24 April 2026 as part of a preview alongside V4-Pro; V4-Pro itself was not updated on 31 July"
    type: announcement
    verdict: confirmed
    evidence: [2, 1]
  - text: "DeepSeek reports V4-Flash-0731 scoring 82.7 on Terminal-Bench 2.1 (up from 72.1 for the V4-Pro preview and 56.9-61.8 for the prior Flash version), 54.4 on DeepSWE (up from 7.3), and 70.3 on Toolathlon"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "An independent Artificial Analysis evaluation puts V4-Flash-0731's Terminal-Bench 2.1 score at approximately 79%, close to but not matching DeepSeek's own 82.7 figure, still a large rise from the prior Flash version's roughly 62%"
    type: capability
    verdict: confirmed
    evidence: [6]
  - text: "API pricing for V4-Flash-0731 is unchanged from the preview: $0.14 per million input tokens on a cache miss, $0.0028 per million on a cache hit, and $0.28 per million output tokens"
    type: announcement
    verdict: confirmed
    evidence: [3]
  - text: "The release comes amid intensifying price competition among frontier AI labs, landing the same week OpenAI cut prices on GPT-5.6 Luna by roughly 80%"
    type: business
    verdict: confirmed
    evidence: [4, 5]
updated: []
---

## What happened

DeepSeek released DeepSeek-V4-Flash-0731 into public beta through its API
on 31 July 2026 [1]. The model is a re-post-trained update of V4-Flash,
which DeepSeek open-sourced as a preview on 24 April 2026 alongside a larger
sibling, V4-Pro [2]. Both preview models share a 1-million-token context
window; V4-Flash uses a 284-billion-parameter architecture with 13 billion
active parameters per token, versus 1.6 trillion total and 49 billion active
for V4-Pro [2]. DeepSeek's 31 July update covers only V4-Flash — V4-Pro was
not updated, and DeepSeek's own changelog for that date lists no V4-Pro
entry [1].

DeepSeek says the retraining improves agentic, coding and tool-use
performance: the company reports V4-Flash-0731 scoring 82.7 on Terminal-Bench
2.1, up from 72.1 for the April V4-Pro preview and 56.9-61.8 for the prior
Flash version, along with 54.4 on DeepSWE (versus 7.3) and 70.3 on Toolathlon
[1]. These figures come from DeepSeek itself. An independent evaluation by
Artificial Analysis puts the Terminal-Bench 2.1 score at approximately 79%
— close to but not matching DeepSeek's own 82.7 figure, and still a large
rise from the prior Flash version's roughly 62% [6]; no independent figures
for DeepSWE or Toolathlon were found. API pricing is unchanged from the preview: $0.14 per
million input tokens on a cache miss, $0.0028 per million on a cache hit, and
$0.28 per million output tokens [3]. DeepSeek's pricing page also describes a
planned peak/off-peak pricing structure, roughly doubling rates during
specific daytime windows Beijing time, which was not yet in effect at
release [3].

Independent press covered the release the same day. Nikkei Asia reported it
as part of an intensifying AI price war, noting DeepSeek's rates undercut
those of major US rivals [4]. VentureBeat separately reported that OpenAI cut
prices on GPT-5.6 Luna by roughly 80% in the same window, a move it also
frames as part of the broader cost competition among frontier labs [5].

## Why it matters

Pricing has become an active front in frontier-model competition alongside
capability, and DeepSeek's release lands in the same week as a large OpenAI
price cut — two independently reported moves that, taken together, point to
real cost pressure among the leading labs rather than an isolated marketing
claim. An independent evaluation broadly, though not exactly, confirms the
performance gains DeepSeek reports for V4-Flash-0731 over its predecessor;
DeepSeek's own higher figure remains unverified.
