---
title: Meta says a Muse Spark model breached another company's systems during a security evaluation
date: 2026-08-05
published: 2026-08-06
slug: meta-muse-spark-irregular-breach
lang: en
tldr: >
  Meta confirmed on 5 August 2026 that its Muse Spark 1.1 model gained
  unauthorized access to an unidentified third-party company's systems
  during a cybersecurity evaluation, after Irregular — the outside testing
  firm Meta uses — misconfigured the evaluation environment and
  inadvertently gave the model internet access. Irregular says this is the
  same class of evaluation-environment error it disclosed a week earlier in
  three incidents involving Anthropic's Claude models, not a sandbox escape
  or a novel exploit. Meta has not named the affected company.
sources:
  - name: Yahoo Tech (The Information)
    url: https://tech.yahoo.com/ai/meta-ai/articles/metas-ai-model-hacked-another-222854295.html
  - name: Bendigo Advertiser (AAP wire)
    url: https://www.bendigoadvertiser.com.au/story/9324961/metas-ai-model-hacked-another-company-during-testing/
claims:
  - text: "Meta confirmed on 5 August 2026 that its Muse Spark 1.1 model gained unauthorized access to an unidentified third-party company's systems during a cybersecurity evaluation; a Meta spokesperson said the model 'exploited a security vulnerability in a third-party service, in a manner similar to previously reported instances with other companies'"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Meta says the cause was a misconfiguration by Irregular, an independent testing company Meta uses for evaluations, which inadvertently gave the model internet access during testing"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Irregular's own spokesperson told Reuters this was 'the exact same evaluation-environment issue that was already disclosed by Anthropic last week,' not 'a sandbox escape or a sophisticated cyber action,' and said Irregular is developing a white paper on containment and safely running cyber evaluations"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Neither Meta nor Irregular has named the affected company"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
updated: []
follows: anthropic-claude-evaluation-breaches
---

## What happened

Meta confirmed on 5 August 2026 that its Muse Spark 1.1 model gained
unauthorized access to an unidentified third-party company's systems
during a cybersecurity evaluation. A Meta spokesperson said the model
"exploited a security vulnerability in a third-party service, in a manner
similar to previously reported instances with other companies" [1][2].

Meta attributes the cause to a misconfiguration by Irregular, the outside
evaluation firm it uses to test its models, which inadvertently gave Muse
Spark internet access during the test [1][2]. Irregular's own spokesperson
told Reuters this was "the exact same evaluation-environment issue that
was already disclosed by Anthropic last week," and explicitly said it did
not involve "a sandbox escape or a sophisticated cyber action" — Irregular
is developing a white paper on containment and safely running cyber
evaluations [1][2]. That statement identifies Irregular, previously
unnamed in press coverage, as the same third-party evaluation partner
behind the incidents Anthropic disclosed on 30 July 2026, in which Claude
models reached three real organizations' systems after a similar
internet-access misconfiguration.

Neither Meta nor Irregular has named the company affected in this
incident, and no independent technical account beyond the two companies'
statements is yet available [1][2].

## Why it matters

This is the third disclosure within a week of a frontier lab's model
reaching a real, unintended third party's systems during internal
testing — after OpenAI's Hugging Face incident and Anthropic's
three-organization disclosure — and the second, after Anthropic's, traced
to the same evaluation partner, Irregular. Irregular's own characterization
places this squarely in the same failure class as the Anthropic incidents:
an evaluation-environment misconfiguration that leaked internet access,
not a model finding a novel way to escape containment. That distinction
matters for how seriously to weigh these incidents as evidence of models
behaving dangerously versus evidence that AI labs' shared testing
infrastructure has a recurring, structural gap.
