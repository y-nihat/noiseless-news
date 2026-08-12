---
title: Nvidia releases Nemotron 3.5 Lightning, an open-weight 30B model built for speed on agent tasks
date: 2026-08-11
published: 2026-08-12
slug: nvidia-nemotron-3-5-lightning
lang: en
tldr: >
  Nvidia released Nemotron 3.5 Lightning on 11 August, an open-weight
  30-billion-parameter mixture-of-experts model with 3 billion active
  parameters, aimed at fast, high-volume agent tasks like tool calls and
  retrieval. Independent testing by Artificial Analysis measured it tying
  gpt-oss-120b on their Intelligence Index; Nvidia's own claim that it beats
  Qwen3.6 35B by 30% on its in-house PinchBench is unverified outside the
  company.
sources:
  - name: NVIDIA Technical Blog
    url: https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/articles/nemotron-3-5-lightning-launch
  - name: The Decoder
    url: https://the-decoder.com/nvidias-open-weight-nemotron-3-5-lightning-prioritizes-speed-over-maximum-intelligence/
claims:
  - text: "Nvidia released Nemotron 3.5 Lightning, a 30-billion-parameter open-weight mixture-of-experts model with 3 billion active parameters, on 11 August 2026"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "The model is released under the permissive OpenMDW-1.1 license, free for commercial use, with weights available on Hugging Face and Nvidia's build.nvidia.com platform"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Independent testing by Artificial Analysis scored the model 24 on its Intelligence Index, tying gpt-oss-120b; a pre-release measurement on a single provider's endpoint put output speed at roughly 670 tokens/second, though Artificial Analysis's own post-launch figure aggregated across providers is lower"
    type: capability
    verdict: confirmed
    evidence: [2, 3]
  - text: "Nvidia says the model completes 86% of PinchBench agentic tasks correctly while finishing 30% faster than Qwen3.6 35B"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

Nvidia released Nemotron 3.5 Lightning on 11 August, an open-weight
mixture-of-experts model with 30 billion total parameters and 3 billion
active per token, built on the hybrid Mamba-Transformer backbone used across
the Nemotron 3 family [1]. It is licensed under the permissive OpenMDW-1.1
terms, free for commercial use, with weights posted to Hugging Face and
Nvidia's build.nvidia.com platform in BF16 and NVFP4 formats [1].

Nvidia positions the model for the high-volume "grunt work" layer of agent
systems — tool calls, validation, retrieval, formatting — rather than
maximum reasoning capability [1]. Independent benchmarking by Artificial
Analysis scored it 24 on the Intelligence Index, matching gpt-oss-120b
despite using about a quarter of the active parameters [2]. A pre-release
measurement on a single hosting provider's endpoint put output speed at
roughly 670 tokens per second, nearly double Google's Gemini 3.5
Flash-Lite; Artificial Analysis's own live tracking page, aggregating
across providers after launch, shows a lower median of about 292
tokens/second, with the fastest available provider at around 594 [2].
Nvidia's own figures, from its PinchBench agentic-task suite, claim 86%
accuracy while finishing tasks 30% faster than Qwen3.6 35B; those numbers
have not been independently reproduced [1].

## Why it matters

Nemotron 3.5 Lightning is Nvidia's first open-weight model release since
CEO Jensen Huang entered the public debate over open-source AI policy in
Washington. The independent Intelligence Index result stands on its own:
a 3-billion-active-parameter model matching a much larger open model on a
third-party benchmark supports Nvidia's speed-over-size pitch for
agent-pipeline workloads, even though its head-to-head throughput and
PinchBench numbers are best-case figures still to be checked in normal use.
