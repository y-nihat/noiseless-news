---
title: Moonshot AI launches Kimi K3 via API, holds back model weights until 27 July
date: 2026-07-17
slug: kimi-k3-release
lang: en
tldr: >
  Chinese AI lab Moonshot launched Kimi K3 on 16 July 2026, giving API access
  immediately while full model weights are due to follow on 27 July. Moonshot
  describes it as a 2.8-trillion-parameter Mixture-of-Experts model with a
  1-million-token context window; the parameter count, architecture details,
  and benchmark comparisons are the company's own figures and have not yet
  been independently reproduced.
sources:
  - name: Moonshot AI (Kimi)
    url: https://www.kimi.com/blog/kimi-k3
  - name: VentureBeat
    url: https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems
  - name: Axios
    url: https://www.axios.com/2026/07/17/china-ai-kimi-k3-open-source-anthropic-opus
  - name: Tom's Hardware
    url: https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-releases-2-8-trillion-parameter-kimi-k3
claims:
  - text: "Moonshot AI launched Kimi K3 on 16 July 2026, with API access available immediately"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Moonshot says full model weights will be released by 27 July 2026, meaning K3 is API-only for now rather than already available as an open-weight download"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Moonshot describes K3 as a 2.8-trillion-parameter Mixture-of-Experts model (16 of 896 experts active per token) with a 1-million-token context window"
    type: capability
    verdict: vendor-claim
    evidence: [1, 4]
  - text: "Moonshot and press coverage describe K3 as set to be the largest open-weight model released once its weights ship, and cite internal benchmark comparisons placing it near or ahead of some rival models"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2, 4]
updated: []
---

## What happened

Moonshot AI, the Beijing-based lab behind the Kimi model family, launched Kimi
K3 on 16 July 2026, making it available through its API immediately [1][2][3].
Full model weights are due to follow on 27 July, so for now K3 is accessible
only through Moonshot's hosted API rather than as a downloadable open-weight
release [1][2].

Moonshot's own announcement describes K3 as a 2.8-trillion-parameter
Mixture-of-Experts model, activating 16 of 896 experts per token, with a
1-million-token context window [1][4]. The company and multiple outlets have
framed it as set to become the largest open-weight model released once the
weights are public, and cite internal benchmark comparisons placing it
competitively against rival frontier models [1][2][4]. Those parameter counts,
architecture details, and benchmark results all trace back to Moonshot's own
materials — no independent party has yet reproduced them, and press coverage
so far repeats the company's own figures rather than testing them
separately.

## Why it matters

K3 lands as the latest entrant in a run of large Chinese open-weight model
releases this year, continuing Moonshot's Kimi line. Its practical
significance — whether it holds up against rivals on independently run
benchmarks, and whether "largest open-weight model" survives contact with
publicly downloadable weights — can't be assessed until the 27 July weight
release. Until then, treat the scale and performance claims as Moonshot's own
account.
