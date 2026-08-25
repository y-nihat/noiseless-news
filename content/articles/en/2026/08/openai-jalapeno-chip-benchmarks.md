---
title: OpenAI publishes first benchmark results for its Broadcom-built Jalapeño chip
date: 2026-08-25
slug: openai-jalapeno-chip-benchmarks
lang: en
tldr: >
  OpenAI published its first benchmark results on 25 August 2026 for Jalapeño,
  a custom AI inference chip built with Broadcom and unveiled in June. OpenAI
  says the chip delivers 1.5-1.9x more throughput per watt and up to 3.6x
  lower latency than Nvidia's current Blackwell-generation chips — its own
  figures, not yet independently reproduced, and measured only against
  Blackwell, not Nvidia's newer Rubin chips.
sources:
  - name: OpenAI News
    url: https://openai.com/index/jalapeno-first-results
  - name: OpenAI News
    url: https://openai.com/index/openai-broadcom-jalapeno-inference-chip
  - name: Broadcom (investor relations)
    url: https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor
  - name: SemiAnalysis
    url: https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/
  - name: Tom's Hardware
    url: https://www.tomshardware.com/tech-industry/semiconductors/openai-says-its-jalapeno-chip-beats-nvidias-gb300-in-first-published-benchmarks
claims:
  - text: "OpenAI and Broadcom jointly built Jalapeño, a custom chip for AI inference, which the companies unveiled on 24 June 2026"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "Jalapeño is designed only for AI inference and cannot be used to train AI models"
    type: announcement
    verdict: confirmed
    evidence: [3, 6]
  - text: "OpenAI and Broadcom say Jalapeño went from design start to manufacturing tape-out in about nine months"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "On 25 August 2026, OpenAI published its first Jalapeño benchmark results, saying the chip delivers 1.5-1.9x more throughput per watt and 1.7-3.6x lower latency than Nvidia's current Blackwell-generation chips (GB200/GB300), across the GPT-OSS 120B, DeepSeek R1 670B and Kimi K2.5 1T models"
    type: capability
    verdict: vendor-claim
    evidence: [1, 4, 5]
  - text: "Jalapeño's disclosed benchmarks do not include a comparison against Nvidia's next-generation Rubin chips, which were not available for testing"
    type: announcement
    verdict: confirmed
    evidence: [4, 6]
updated: []
---

## What happened

OpenAI published its first performance results for Jalapeño, the custom AI
inference chip it built with Broadcom, on 25 August 2026 [1]. OpenAI and
Broadcom first unveiled the chip on 24 June 2026 [2][3], saying it went
from design start to manufacturing tape-out in about nine months [2][3].
Jalapeño is designed only for AI inference — running trained models — and
cannot be used to train new ones [3][6].

In today's disclosure, OpenAI said Jalapeño delivers 1.5 to 1.9 times more
AI throughput per watt and 1.7 to 3.6 times lower latency than Nvidia's
current Blackwell-generation chips, the GB200 and GB300, across three
open-weight models: GPT-OSS 120B, DeepSeek R1 670B and Kimi K2.5 1T
[1][4][5]. These are OpenAI's own figures; independent analysis firm
SemiAnalysis says it watched the benchmark runs in person but did not
independently execute the full test suite itself [4], and no other
independent reproduction has yet been published. The comparison covers
only Nvidia's Blackwell family — Jalapeño's disclosed results do not
include a test against Nvidia's newer Rubin chips, which were not
available for testing [4][6].

## Why it matters

OpenAI is one of Nvidia's largest customers, so a credible in-house
inference chip would reshape both its costs and its future leverage in
hardware negotiations. But the only performance data published so far is
OpenAI's own, reviewed only by a firm OpenAI itself invited to observe,
and benchmarked only against Nvidia's previous-generation Blackwell chips.
Whether Jalapeño holds up against Rubin — the chip it will actually have
to compete with in the field — has not yet been tested.
