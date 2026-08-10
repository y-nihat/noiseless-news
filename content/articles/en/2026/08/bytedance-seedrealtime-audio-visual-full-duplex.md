---
title: ByteDance's Seed team releases SeedRealtime, an audio-visual full-duplex model
date: 2026-08-05
published: 2026-08-10
slug: bytedance-seedrealtime-audio-visual-full-duplex
lang: en
tldr: >
  On 5 August 2026, ByteDance's Seed team released SeedRealtime, a native
  audio-visual full-duplex model that processes audio, video and text
  streams together so it can watch, listen and speak in real time, rolling
  out through the Doubao app. It extends Seed's audio-only full-duplex
  model from April 2026 by adding vision. ByteDance says its own human
  evaluation found the model cuts awkward conversational pacing compared
  with older cascaded pipelines, but no independent benchmark of that
  claim exists yet.
sources:
  - name: ByteDance Seed
    url: https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction
claims:
  - text: "On 5 August 2026, ByteDance's Seed team released SeedRealtime, a native audio-visual full-duplex model that natively fuses audio, video and text streams to enable real-time, proactive conversational interaction, deployed through the Doubao app; it extends Seed's audio-only full-duplex model ('Seed Full-Duplex Speech LLM'), released in April 2026, by adding vision"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "ByteDance says SeedRealtime uses visual context to resolve spoken-word ambiguity and, per its own human evaluation, substantially reduces awkward pacing and interruption problems compared with older cascaded (non-end-to-end) voice-assistant pipelines"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

ByteDance's Seed team said on 5 August 2026 that it released SeedRealtime, a
native audio-visual full-duplex model: one system that takes in audio, video
and text streams together and can watch, listen and speak at the same time,
rather than processing a request and replying in turns [1]. It is rolling
out through the Doubao app [1]. The release extends Seed's audio-only
full-duplex model, "Seed Full-Duplex Speech LLM," which the team released in
April 2026 — SeedRealtime adds vision to that same real-time-interaction
approach [1].

ByteDance says the model uses visual context to resolve ambiguity in what a
speaker says, and that its own human evaluation found SeedRealtime
substantially cuts the awkward pacing and interruption problems common to
older, cascaded voice-assistant pipelines that process speech-to-text,
reasoning and text-to-speech as separate stages [1]. These figures come only
from ByteDance's own evaluation; no independent benchmark or third-party
reproduction of the capability claims has been published yet.

## Why it matters

SeedRealtime is a real product shipping to users, not a research preview,
and it marks Seed's move from audio-only full-duplex interaction to a
combined audio-visual version within four months. As with any
vendor-reported human evaluation, the pacing-improvement figures are
ByteDance's own, on a comparison ByteDance selected. Independent
confirmation is not yet available.
