---
title: Qwen releases open-weight Qwen3.8-27B, ties GPT-5.6 Luna on independent benchmark
date: 2026-08-14
published: 2026-08-18
slug: qwen-3-8-27b-release
lang: en
tldr: >
  Alibaba's Qwen team released Qwen3.8-27B around 14 August, a 27-billion-parameter
  dense open-weight model licensed under Apache 2.0, with native image and video
  understanding and a 262,144-token context window. Independent testing by Artificial
  Analysis scores it 52 on its Intelligence Index — level with OpenAI's GPT-5.6 Luna
  and one point behind GLM-5.2 and DeepSeek V4 Pro 0813, both far larger
  mixture-of-experts models. Qwen's own coding-benchmark figures are vendor-reported
  and have not been independently reproduced.
sources:
  - name: Qwen (Hugging Face model card)
    url: https://huggingface.co/Qwen/Qwen3.8-27B
  - name: Simon Willison's Weblog
    url: https://simonwillison.net/2026/Aug/16/qwen-38-27b/
  - name: VentureBeat AI
    url: https://venturebeat.com/technology/qwen3-8-27b-runs-frontier-class-coding-agents-and-reasoning-locally-no-cloud-api-required
  - name: Artificial Analysis (Qwen3.8-27B)
    url: https://artificialanalysis.ai/models/qwen3-8-27b
  - name: Artificial Analysis (GPT-5.6 Luna)
    url: https://artificialanalysis.ai/models/gpt-5-6-luna
  - name: Artificial Analysis (GLM-5.2)
    url: https://artificialanalysis.ai/models/glm-5-2
  - name: Artificial Analysis (DeepSeek V4 Pro 0813)
    url: https://artificialanalysis.ai/models/deepseek-v4-pro
claims:
  - text: "Alibaba's Qwen team released Qwen3.8-27B, a 27-billion-parameter dense open-weight multimodal model, on Hugging Face under the Apache 2.0 license, around 14 August 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Qwen3.8-27B has a native 262,144-token context window (extensible to 1 million via YaRN) with native image and video understanding, and can run locally at roughly 56GB of GPU memory at 16-bit precision, about 28GB in FP8, or about 17GB when 4-bit quantized"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 2]
  - text: "Independent benchmarking by Artificial Analysis scores Qwen3.8-27B at 52 on its Intelligence Index, level with GPT-5.6 Luna (52) and one point behind GLM-5.2 and DeepSeek V4 Pro 0813 (53 each) — both much larger mixture-of-experts models (753 billion total/40 billion active, and 1.6 trillion total/49 billion active, parameters respectively) versus Qwen3.8-27B's 27 billion dense parameters"
    type: capability
    verdict: confirmed
    evidence: [4, 5, 6, 7]
  - text: "Qwen reports the model scoring 61.7 on SWE-bench Pro and 73.0 on Terminal Bench 2.1"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

Alibaba's Qwen research team released Qwen3.8-27B on Hugging Face around 14
August 2026, a dense 27-billion-parameter model licensed under the permissive
Apache 2.0 terms [1]. It is a native vision-language model that understands
both images and video, with a context window of 262,144 tokens natively,
extendable to 1 million via YaRN [1]. Independent developer Simon Willison,
who ran the model himself, called its default reasoning effort poorly chosen
out of the box and recommended lowering it, though it is user-configurable [2].

The model's hardware footprint is unusually small for its capability class.
VentureBeat reports that running it at full 16-bit precision takes roughly
56GB of GPU memory and that an FP8 version needs about 28GB [3]; a 4-bit
quantized version needs around 17GB, within reach of a single high-end
consumer GPU — a figure independently matched by Willison's own local 4-bit
test run [2].

Independent testing by Artificial Analysis scores Qwen3.8-27B at 52 on its
Intelligence Index, level with OpenAI's proprietary GPT-5.6 Luna, also 52, and
one point behind GLM-5.2 and DeepSeek V4 Pro 0813, both scoring 53 [4][5][6][7].
Both of the higher-scoring models are mixture-of-experts systems that activate
more parameters per token than Qwen3.8-27B's 27 billion dense parameters —
GLM-5.2 activates 40 billion of its 753 billion total, and DeepSeek V4 Pro
0813 activates 49 billion of its 1.6 trillion total — a real but modest
1.5-to-1.8-times gap in active compute, not the far larger gap their total
parameter counts alone would suggest [4][5][6]. Artificial Analysis's own
evaluation data shows Qwen3.8-27B generated roughly 160 million output tokens
during testing against a roughly 43 million median across models, indicating
part of its score comes from generating substantially more reasoning output
per answer, not from matching larger models at equal cost [4]. Qwen's own
reported figures on coding and agentic-task benchmarks, including 61.7 on
SWE-bench Pro and 73.0 on Terminal Bench 2.1, have not been independently
reproduced [1].

## Why it matters

A dense 27-billion-parameter model landing within a point of two much larger
mixture-of-experts models, and exactly level with a proprietary frontier
model, on the same third-party index continues this year's trend of smaller
open-weight models narrowing the capability gap, running on a single
consumer GPU rather than datacenter-scale hardware. That comparison carries a
caveat: part of Qwen3.8-27B's score reflects generating substantially more
output per answer than typical models on the index, and independent testing
found its default reasoning setting poorly tuned out of the box — matching
larger models is not without cost.
