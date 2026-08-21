---
title: DeepSeek releases experimental multimodal model V4-Flash-Vision-Exp as API-only
date: 2026-08-21
slug: deepseek-v4-flash-vision-exp
lang: en
tldr: >
  DeepSeek released an experimental vision-capable model, DeepSeek-V4-Flash-Vision-Exp,
  through its API on 21 August 2026, adding image understanding to its existing
  V4-Flash-0731 text model. Unlike that July release, the new model is API-only —
  DeepSeek states explicitly that it is not open-weight. DeepSeek says the model's
  agentic performance on benchmarks it ran itself comes close to Claude Opus 4.8,
  though its own figures show mixed results and no independent evaluation has been
  published.
sources:
  - name: DeepSeek News
    url: https://api-docs.deepseek.com/news/news260821
  - name: The Decoder
    url: https://the-decoder.com/deepseek-releases-experimental-flash-vision-model-that-rivals-opus-4-8-on-agent-benchmarks/
  - name: officechai
    url: https://officechai.com/ai/deepseek-releases-v4-flash-vision-exp-matches-opus-4-8-on-some-multimodal-benchmarks/
  - name: The Next Web
    url: https://thenextweb.com/news/deepseek-v4-flash-vision-exp-opus-benchmarks
claims:
  - text: "DeepSeek released DeepSeek-V4-Flash-Vision-Exp, an experimental multimodal model, through its API on 21 August 2026, adding image understanding to its existing V4-Flash-0731 text model while matching that model's text performance"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "V4-Flash-Vision-Exp is available only through DeepSeek's API; DeepSeek's own announcement states it is not open-weight, unlike the July V4-Flash-0731 release it is built on"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "DeepSeek says the model's multimodal agent performance is close to Claude Opus 4.8, based on evaluations run on DeepSeek's own benchmark harness"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "DeepSeek's own per-benchmark figures, as reported by The Decoder and officechai, show the model leading Opus 4.8 on some tasks (e.g. Agents' Last Exam, 27.3 vs 25.7) and trailing by as much as roughly 12 points on others (e.g. NL2Repo); no independent evaluator's results for the model were found"
    type: capability
    verdict: vendor-claim
    evidence: [2, 3]
  - text: "The Next Web reported that DeepSeek's comparison benchmarks against Opus 4.8 rather than the newer Opus 5, and that DeepSeek's own before/after table appears to score its prior non-vision model on tests containing images it could not see"
    type: capability
    verdict: single-source
    evidence: [4]
updated: []
---

## What happened

DeepSeek released an experimental multimodal model, DeepSeek-V4-Flash-Vision-Exp,
through its API on 21 August 2026 [1]. The model adds image understanding to
DeepSeek-V4-Flash-0731, the text-only model DeepSeek open-sourced on 31 July,
and matches that model's text performance [1][2]. Unlike the July release,
V4-Flash-Vision-Exp is available only through DeepSeek's API — DeepSeek's own
announcement states plainly that it is "not open-weight" [1]; no official
DeepSeek repository for the model has appeared on Hugging Face.

DeepSeek says the new model's multimodal agent performance comes "close to"
Claude Opus 4.8, based on evaluations it ran itself on its own benchmark
harness [1]. Per DeepSeek's own per-benchmark figures, as reported by The
Decoder and officechai, the model leads Opus 4.8 on some tasks — including
Agents' Last Exam (27.3 versus 25.7) and ZeroBench Pass@5 (35.0 versus 34.0)
— while trailing by as much as roughly 12 points on others, including a
code-repository task called NL2Repo [2][3]. DeepSeek has not published this
as an independent evaluation, and no independent evaluator's results for the
model were found at publication time.

The Next Web reported two issues with DeepSeek's comparison: it benchmarks
against Claude Opus 4.8 rather than Anthropic's newer Opus 5, and DeepSeek's
own before-and-after table appears to score its prior, non-vision model on
tests that included images it could not see — which may inflate the apparent
gain [4].

## Why it matters

DeepSeek is testing multimodal capability on top of an already-competitive
text model while keeping the release API-only, a departure from the
open-weight approach that built its reputation. The performance comparison to
Opus 4.8 is DeepSeek's own and mixed even by its own numbers; independent
confirmation is not yet available.
