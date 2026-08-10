---
title: Mistral releases Shieldstral, an open-weight AI content-safety classifier
date: 2026-08-04
published: 2026-08-10
slug: mistral-shieldstral-safety-classifier
lang: en
tldr: >
  On 4 August 2026, Mistral AI released Shieldstral, a 3-billion-parameter
  open-weights content-safety classifier under Apache 2.0, which screens
  text and images against plain-language policies specified at query time
  instead of a fixed taxonomy. Mistral says it matches or beats guard
  models up to seven times its size on most of its own benchmarks, though
  it trails a 20-billion-parameter rival on one adaptability test; no
  independent evaluation of these figures exists yet. It is the first
  tool released by the Open Secure AI Alliance, the NVIDIA-led coalition
  Mistral joined as a founding member in July.
sources:
  - name: Mistral AI News
    url: https://mistral.ai/news/shieldstral/
  - name: The Decoder
    url: https://the-decoder.com/mistrals-open-model-shieldstral-matches-much-larger-safety-models/
claims:
  - text: "On 4 August 2026, Mistral AI released Shieldstral, a 3-billion-parameter open-weights AI content-safety classifier under the Apache 2.0 license, runnable on a single 16GB GPU, which evaluates text and image content against plain-language policies specified at inference time rather than a fixed, retrained taxonomy"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Mistral reports Shieldstral matches or outperforms open guard models up to seven times its size across text safety, refusal detection, policy adaptability, and multimodal benchmarks, including an 84.9% F1 score on text safety that ties OpenAI's 20-billion-parameter GPT-OSS-Safeguard-20B; on a separate adaptability benchmark using unseen policies, Mistral's own reported score for Shieldstral (91.3%) trails that same 20B model's (94.1%)"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "Mistral is a founding member of the Open Secure AI Alliance, the NVIDIA-led AI-security coalition formed in late July 2026, and describes Shieldstral as released under that alliance"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
follows: open-secure-ai-alliance-formation
---

## What happened

Mistral AI said on 4 August 2026 that it released Shieldstral, a 3-billion-
parameter, open-weights content-safety classifier under the Apache 2.0
license, small enough to run on a single 16GB GPU [1][2]. Rather than using
a fixed, retrained taxonomy of unsafe categories, Shieldstral takes a
plain-language policy question at inference time — such as "does this
content promote physical violence?" — and returns a calibrated safety
verdict from a single token, across both text and images [1][2].

Mistral's own benchmarks report that Shieldstral matches or outperforms
open guard models up to seven times its size on most measures, including an
84.9% F1 score on text safety that ties OpenAI's 20-billion-parameter
GPT-OSS-Safeguard-20B [1][2]. That comparison is not uniform: on a separate
test of adapting to unseen policies, Mistral's own reported score for
Shieldstral (91.3%) trails the same 20B rival's (94.1%) [2]. All of these
figures come from Mistral's own evaluation; no independent third-party
benchmark of Shieldstral has been published yet [2].

Shieldstral is the first tool released under the Open Secure AI Alliance,
the NVIDIA-led AI-security coalition formed in late July 2026 after a
Hugging Face agent-security breach, which Mistral joined as a founding
member alongside NVIDIA and other companies [1].

## Why it matters

The alliance's founding announcement promised future tool contributions
from its members; Shieldstral is the first of those to actually ship,
rather than a restated commitment. As with any vendor-published benchmark,
the numbers are Mistral's own, on tests Mistral selected — safety
classification is a domain where that matters more than most, since what
counts as "unsafe" is itself policy-dependent and the model under test is
the one interpreting the policy. Independent confirmation is not yet
available.
