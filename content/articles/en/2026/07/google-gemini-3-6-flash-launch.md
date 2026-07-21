---
title: Google launches Gemini 3.6 Flash and 3.5 Flash-Lite, holds back its 3.5 Pro flagship
date: 2026-07-21
slug: google-gemini-3-6-flash-launch
lang: en
tldr: >
  Google released two new Gemini models — 3.6 Flash and 3.5 Flash-Lite — on 21
  July 2026, plus a cybersecurity-focused variant, 3.5 Flash Cyber, restricted
  to a government/partner pilot. Google's own figures claim faster, cheaper
  inference than the prior Flash generation; an independent benchmark tracker
  confirms the efficiency gains but found intelligence scores flat rather than
  improved. Multiple outlets report the anticipated Gemini 3.5 Pro flagship
  was held back after Google fell short of its internal performance targets.
sources:
  - name: Google — Gemini models blog
    url: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/
  - name: Artificial Analysis — independent benchmark
    url: https://artificialanalysis.ai/articles/gemini-3-6-flash-3-5-flash-lite-halving-time
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/21/google-releases-three-new-gemini-models-but-no-3-5-pro/
claims:
  - text: "Google introduced three new Gemini models on 21 July 2026: Gemini 3.6 Flash, Gemini 3.5 Flash-Lite, and Gemini 3.5 Flash Cyber"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "3.6 Flash and 3.5 Flash-Lite are available immediately across the Gemini API, Google AI Studio, Android Studio and the Gemini app; 3.5 Flash Cyber is restricted to a limited-access pilot for governments and trusted partners"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "3.6 Flash is priced at $1.50 per million input tokens and $7.50 per million output tokens; 3.5 Flash-Lite at $0.30 and $2.50 respectively; Flash Cyber pricing is not disclosed"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Google's own benchmarks show 3.6 Flash beating 3.5 Flash on MLE-Bench (63.9% vs 49.7%) and OSWorld-Verified (83.0% vs 78.4%), with roughly 17% lower output-token usage"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Independent measurement by Artificial Analysis found 3.6 Flash's Intelligence Index score flat versus 3.5 Flash, but confirmed real efficiency gains: over 50% less time per task (2.7 to 1.3 minutes) and about 18% lower cost per task"
    type: capability
    verdict: confirmed
    evidence: [2]
  - text: "Multiple outlets, citing a Bloomberg report, say Google held back its anticipated Gemini 3.5 Pro flagship update because it fell short of internal performance targets, with Google saying the model is being tested with partners and coming soon"
    type: business
    verdict: single-source
    evidence: [3]
updated: []
---

## What happened

Google released two new members of its Gemini 3 family on 21 July 2026 —
Gemini 3.6 Flash and Gemini 3.5 Flash-Lite — alongside a third, narrower
model, Gemini 3.5 Flash Cyber, built for finding and patching security
vulnerabilities and restricted to a limited pilot for governments and
trusted partners [1]. The two general-availability models are live now
across the Gemini API, Google AI Studio, Android Studio and the Gemini app;
3.6 Flash is priced at $1.50/$7.50 per million input/output tokens, and 3.5
Flash-Lite at $0.30/$2.50 [1]. Google has not disclosed pricing for Flash
Cyber.

Google's own benchmark figures show 3.6 Flash ahead of 3.5 Flash on tasks
like MLE-Bench (63.9% vs 49.7%) and OSWorld-Verified (83.0% vs 78.4%), with
roughly 17% lower output-token usage [1] — vendor-reported numbers not yet
independently reproduced task-by-task. Independent tracker Artificial
Analysis did measure the release directly and confirmed real efficiency
gains — task time cut by more than half (2.7 to 1.3 minutes) and cost per
task down about 18% — but found the model's overall Intelligence Index
score unchanged from 3.5 Flash, meaning this is a speed-and-cost update
rather than a capability jump [2].

Absent from the release is the Gemini 3.5 Pro flagship many expected.
Citing a Bloomberg report, TechCrunch and other outlets say Google held it
back after falling short of internal performance goals; Google has said
only that the model is being tested with partners and is coming soon [3].
That account traces to a single Bloomberg report relayed by other outlets,
not independent confirmation.

## Why it matters

The release reads as an efficiency-focused refresh rather than a capability
leap — useful for cost-sensitive deployment at scale — while the more
consequential flagship update remains unreleased. Gating Flash Cyber to
governments and vetted partners reflects the same dual-use caution Google
has applied to other vulnerability-discovery tools, restricting access to a
model explicitly built to find security flaws.
