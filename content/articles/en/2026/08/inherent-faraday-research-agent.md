---
title: Inherent launches Faraday AI research agent, backed by $50 million seed round
date: 2026-08-14
published: 2026-08-23
slug: inherent-faraday-research-agent
lang: en
tldr: >
  Inherent, a London AI lab founded by DeepMind alumni, released an AI
  research agent called Faraday on 14 August 2026, following a $50
  million seed round co-led by Index Ventures and Radical Ventures that
  closed in May 2026. Faraday is built around a 27-billion-parameter
  model that directs a separate, much larger model as a subordinate
  tool; Inherent says it outperformed Claude Opus 4.8 and GPT-5.5 at
  replicating published research findings on the company's own
  self-designed benchmark, a comparison no independent evaluator has yet
  confirmed.
sources:
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/22/inherent-founded-by-deepmind-alumni-says-its-ai-teammate-just-outperformed-anthropic-and-openai-at-replicating-research/
  - name: Index Ventures
    url: https://www.indexventures.com/perspectives/inherent-designing-for-discovery/
  - name: Inherent Labs
    url: https://inherentlabs.ai/research/training-to-replicate
claims:
  - text: "Inherent, a London-based AI lab founded by DeepMind alumni, raised a $50 million seed round co-led by Index Ventures and Radical Ventures, which closed in May 2026"
    type: business
    verdict: confirmed
    evidence: [1, 2]
  - text: "Inherent released an AI research agent called Faraday, built around a 27-billion-parameter model, on 14 August 2026, alongside a paper describing the Replica benchmark"
    type: announcement
    verdict: confirmed
    evidence: [3]
  - text: "Faraday directs the work of a separate, much larger model as a subordinate tool within its own pipeline, rather than operating as a standalone small model beating larger rivals unassisted"
    type: capability
    verdict: confirmed
    evidence: [3]
  - text: "Inherent says Faraday outperformed Claude Opus 4.8 and GPT-5.5 on the Replica benchmark (310 tasks drawn from 100 papers, replicating a published research figure under a time/compute budget); no independent third-party evaluation of this comparison has been published"
    type: capability
    verdict: vendor-claim
    evidence: [3]
updated: []
---

## What happened

Inherent, a London-based AI lab founded by DeepMind alumni, raised a $50
million seed round co-led by Index Ventures and Radical Ventures that
closed in May 2026 [1][2]. On 14 August 2026, the company released an AI
research agent called Faraday, built around a 27-billion-parameter
model, alongside a paper describing Replica, a benchmark of 310 tasks
drawn from 100 published papers that requires an agent to replicate a
research figure within a limited time and compute budget [3].

Faraday directs the work of a separate, much larger model as a
subordinate tool within its own pipeline, rather than operating as a
standalone small model beating larger rivals unassisted [3]. Inherent
says Faraday outperformed Claude Opus 4.8 and GPT-5.5 on the Replica
benchmark, describing a particularly pronounced advantage in
meta-learning, structural biology and materials-science tasks — but this
is Inherent's own self-designed and self-administered benchmark, and no
independent third-party evaluation of the comparison has been published
[3].

## Why it matters

Research replication is a specific, checkable slice of "AI does
science," and Faraday adds to a growing field of agents aimed at
automating parts of the research process — but until an outside
evaluator runs the same comparison, the outperformance claim is
Inherent's own marketing, not an independent result.
