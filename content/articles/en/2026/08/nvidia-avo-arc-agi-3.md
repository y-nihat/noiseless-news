---
title: Nvidia brings its AVO agent harness, running Claude Opus 5, to the ARC-AGI-3 benchmark
date: 2026-08-21
published: 2026-08-22
slug: nvidia-avo-arc-agi-3
lang: en
tldr: >
  Nvidia says it applied AVO, an agent harness it first built months earlier for
  GPU-kernel optimization, to Anthropic's Claude Opus 5 on the ARC-AGI-3 benchmark
  for the first time. Nvidia reports a self-administered perfect score across all
  183 public levels — a result that does not appear on ARC Prize's own leaderboard
  and has no independent confirmation.
sources:
  - name: NVIDIA Developer Blog
    url: https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/21/nvidia-just-showed-that-the-harness-not-the-ai-model-is-now-the-real-hero/
  - name: arXiv preprint (2603.24517)
    url: https://arxiv.org/abs/2603.24517
  - name: ARC Prize
    url: https://arcprize.org/leaderboard
claims:
  - text: "Nvidia applied its AVO agent harness, running Claude Opus 5, to the ARC-AGI-3 benchmark, publishing results on 21 August 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "AVO was first developed for autonomous GPU-kernel optimization on Nvidia Blackwell B200 hardware, described in a March 2026 preprint, months before this ARC-AGI-3 application"
    type: research
    verdict: confirmed
    evidence: [1, 3]
  - text: "Nvidia reports AVO scored a perfect 100.00 on the RHAE metric across all 25 public ARC-AGI-3 environments (183 of 183 levels)"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "ARC Prize's official ARC-AGI-3 site and leaderboard list no entry for Nvidia or AVO"
    type: statement
    verdict: confirmed
    evidence: [4]
  - text: "Nvidia says AVO needed about 12% fewer actions than a prior system, VISTA, to complete the same levels, though it cautions this is not a controlled comparison"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Citing a separate ARC Prize evaluation, Nvidia's post puts Claude Opus 5's own unaided score at approximately 30% under high reasoning effort"
    type: capability
    verdict: single-source
    evidence: [1]
updated: []
---

## What happened

Nvidia said on 21 August 2026 that it applied AVO (Agentic Variation Operators) — an
agent harness it first used for autonomous GPU-kernel optimization on Blackwell B200
hardware, described in a March 2026 preprint — to a new domain: the ARC-AGI-3
benchmark, running on top of Anthropic's Claude Opus 5 [1, 3]. Nvidia reports AVO
scored a perfect 100.00 on the benchmark's RHAE metric, completing all 25 public
environments, 183 of 183 levels [1]. TechCrunch independently covered the
announcement, quoting an Nvidia vice president, but did not itself re-run or verify
the benchmark [2]. ARC Prize's own ARC-AGI-3 site and leaderboard, checked directly,
list no entry for Nvidia or AVO [4].

Nvidia also says AVO needed about 12% fewer actions — 6,624, versus 7,542 for a prior
system called VISTA — to finish the same levels, though it cautions the two systems
differ enough in design that this isn't a controlled comparison [1]. Citing a separate
ARC Prize evaluation, Nvidia's post puts Claude Opus 5's own unaided score at
approximately 30% under high reasoning effort [1].

## Why it matters

A jump from roughly 30% to 100% on a benchmark designed to resist memorization would,
if independently reproduced, be a notable demonstration that agent-harness design —
not just the underlying model — drives capability gains. But the current result is
Nvidia's own self-administered run, absent from ARC Prize's official leaderboard, so
it stands as a vendor claim rather than a verified benchmark result.
