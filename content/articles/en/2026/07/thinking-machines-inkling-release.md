---
title: Thinking Machines Lab releases Inkling, its first open-weight model
date: 2026-07-16
slug: thinking-machines-inkling-release
lang: en
tldr: >
  Thinking Machines Lab — the company Mira Murati founded after leaving OpenAI —
  released Inkling on 15 July 2026, a 975-billion-parameter open-weight
  mixture-of-experts model under an Apache 2.0 license, plus a smaller preview
  companion, Inkling-Small. It is the company's first model release. Vendor
  benchmark scores are strong but not yet independently reproduced.
sources:
  - name: Thinking Machines Lab — announcement
    url: https://thinkingmachines.ai/news/introducing-inkling/
  - name: Thinking Machines Lab — model card
    url: https://thinkingmachines.ai/model-card/inkling/
  - name: Hugging Face — Thinking Machines org
    url: https://huggingface.co/thinkingmachines
  - name: Hugging Face — Inkling announcement post
    url: https://huggingface.co/blog/thinkingmachines-inkling
claims:
  - text: "Thinking Machines Lab announced Inkling on 15 July 2026: a 975-billion-total/41-billion-active-parameter sparse mixture-of-experts model (66-layer decoder-only transformer, 256 routed experts plus 2 shared experts, 6 experts active per token), with up to 1-million-token context, trained on 45 trillion multimodal (text, image, audio, video) tokens, taking text output only"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Weights for Inkling are released under an Apache 2.0 license, downloadable on Hugging Face in BF16 and NVFP4-quantized form, with day-0 inference support in transformers, SGLang, and vLLM, and hosted access via Tinker, Together AI, Fireworks, Modal, Databricks, and Baseten; use of the weights is additionally subject to Thinking Machines' acceptable-use policy, which bars surveillance, deceptive, and fully-automated high-stakes decision uses"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "A smaller companion model, Inkling-Small (276-billion total / 12-billion active parameters), was released as a preview; its weights had not yet been published at announcement, pending completion of testing"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Inkling includes a user-adjustable 'controllable thinking effort' setting that trades off answer quality against token cost and latency; vendor benchmarks quoted at the highest effort setting (0.99) include AIME 2026 97.1%, GPQA Diamond 87.2%, SWE-bench Verified 77.6%, HLE-with-tools 46.0%, and VoiceBench 91.4%"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "Thinking Machines Lab itself states Inkling is 'not the strongest overall model available today, open or closed'"
    type: statement
    verdict: confirmed
    evidence: [1]
updated: []
---

## What happened

Thinking Machines Lab — the AI company Mira Murati founded after leaving her
role as OpenAI's chief technology officer — released its first model,
Inkling, on 15 July 2026 [1][2]. Inkling is a sparse mixture-of-experts
model with 975 billion total parameters and 41 billion active per token (a
66-layer transformer routing across 256 experts plus 2 shared ones, 6 active
per token), a context window of up to 1 million tokens, and training on 45
trillion tokens of text, image, audio, and video, producing text output
[1][2]. A smaller preview companion, Inkling-Small (276 billion total / 12
billion active parameters), was announced alongside it, though its weights
were not yet published at announcement time [1][2].

The weights are released under an Apache 2.0 license and are downloadable
from Hugging Face in both BF16 and NVFP4-quantized formats, with same-day
support in the transformers, SGLang, and vLLM inference libraries, plus
hosted access through Tinker, Together AI, Fireworks, Modal, Databricks, and
Baseten [1][2][3]. Use of the weights is additionally governed by Thinking
Machines' own acceptable-use policy, which prohibits surveillance,
deception, and fully automated high-stakes decisions about individuals —
a restriction layered on top of, not replacing, the Apache 2.0 license
[1][2].

Inkling has a "controllable thinking effort" setting a user can adjust to
trade off answer quality against cost and latency. At its highest setting,
Thinking Machines reports benchmark scores of 97.1% on AIME 2026, 87.2% on
GPQA Diamond, 77.6% on SWE-bench Verified, 46.0% on HLE with tools, and
91.4% on VoiceBench [1][2] — figures from the company's own model card, not
yet independently reproduced. The company itself is candid that Inkling is
"not the strongest overall model available today, open or closed" [1].

## Why it matters

This is Thinking Machines Lab's first shipped model since its founding, and
a fully open-weight release (Apache 2.0, full checkpoints public) from a
well-funded lab founded by a former OpenAI CTO — a contrast to labs that
keep frontier-scale weights closed. The benchmark numbers are vendor-supplied
and unverified by an independent evaluator so far; how the model performs
once outside researchers and evaluators test it independently is the open
question.
