---
title: Meta releases Muse Glimmer, a 30-billion-parameter open-weight AI model
date: 2026-08-10
slug: meta-muse-glimmer-launch
lang: en
tldr: >
  Meta released Muse Glimmer on 10 August 2026, a 30-billion-parameter
  open-weight model under an Apache 2.0 license, built to run locally on a
  single consumer GPU for agentic tasks like tool calling and coding. The
  same day, CEO Mark Zuckerberg published an essay arguing AI capability
  should be broadly distributed rather than concentrated in a few labs, and
  said Meta plans to also release open weights for Muse Spark 1.2, the model
  it launched via paid API on 5 August, in the coming weeks — a stated plan,
  not yet delivered.
sources:
  - name: Meta AI Research
    url: https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
  - name: Meta Newsroom
    url: https://about.fb.com/news/2026/08/the-future-is-for-everyone/
  - name: VentureBeat AI
    url: https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now
claims:
  - text: "Meta released Muse Glimmer, a 30-billion-parameter dense model, under an Apache 2.0 license on Hugging Face on 10 August 2026, distilled from Muse Spark 1.2 and built to run locally on a single consumer GPU (around 24GB VRAM) for agentic workloads such as tool calling, coding and multi-step reasoning"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "The same day, Mark Zuckerberg published an essay, 'The Future Is for Everyone,' on Meta's own site arguing that AI capability should be broadly distributed rather than concentrated among a handful of labs, and criticizing 'closed' AI model makers"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "Zuckerberg said Meta plans to release open weights for Muse Spark 1.2 — the model Meta launched via paid API on 5 August alongside its Muse Code coding agent — in the coming weeks"
    type: statement
    verdict: vendor-claim
    evidence: [2, 3]
updated: []
follows: meta-muse-code-muse-spark-1-2
---

## What happened

Meta released Muse Glimmer on 10 August 2026, a 30-billion-parameter dense model published under an Apache 2.0 license on Hugging Face [1]. Distilled from Muse Spark 1.2, it is built to run locally on a single consumer GPU — roughly 24GB of VRAM — and is aimed at agentic workloads: tool calling, coding, and multi-step reasoning carried out on a user's own machine rather than in the cloud [1][3].

The same day, Zuckerberg published a roughly 6,500-word essay, "The Future Is for Everyone," on Meta's own newsroom site [2]. It argues that AI capability should end up broadly distributed rather than held by a small number of labs, governments or companies, and takes aim at "closed" AI model makers [2][3]. In it, Zuckerberg said Meta plans to also release open weights for Muse Spark 1.2 — so far available only through Meta's paid API since its 5 August launch alongside the Muse Code agent — in the coming weeks [2][3]. That is a stated plan, not a shipped release: Meta has previously said it would not open-source all of its most capable models, and neither Meta's blog post nor independent coverage gives a firm date.

## Why it matters

This is Meta's second open-weight move in AI within a week, after keeping Spark 1.2 API-only on 5 August, and it lands alongside rising competition from open-weight releases out of Chinese labs. The Glimmer release itself is a shipped, verifiable fact; the pledge to open-weight Meta's stronger Spark 1.2 model is not yet — whether it follows through is the next thing to check.
