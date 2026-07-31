---
title: ByteDance launches Seedance 2.5, an update to its AI video-generation model
date: 2026-07-31
slug: bytedance-seedance-2-5-launch
lang: en
tldr: >
  ByteDance publicly launched Seedance 2.5 on 31 July 2026, an update to its AI
  video-generation model that the company says produces single-take clips up
  to 30 seconds long, with a multi-round mode for extending sequences further.
  It accepts up to 50 multimodal reference inputs — up to 30 images, 10 video
  clips and 10 audio clips — with timestamp-level editing, and is rolling out
  through Jimeng AI and Doubao Pro; API access via BytePlus ModelArk was not
  yet live at launch.
sources:
  - name: ByteDance Seed
    url: https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
  - name: TechNode
    url: https://technode.com/2026/07/31/bytedance-launches-seedance-2-5-video-generation-model/
claims:
  - text: "ByteDance publicly launched Seedance 2.5, an update to its AI video-generation model, on 31 July 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Seedance 2.5 generates single-take video clips up to 30 seconds long, with a multi-round mode for extending sequences further (vendor claim; no independent reproduction found)"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "The model accepts up to 50 multimodal reference inputs in one request — up to 30 images, 10 video clips and 10 audio clips — with timestamp-level editing of audio and video content"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Seedance 2.5 is rolling out through Jimeng AI and the Pro tier of Doubao; API access via Volcano Engine's BytePlus ModelArk was described as coming soon and was not yet live at launch"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## What happened

ByteDance publicly launched Seedance 2.5, an update to its AI video-generation
model, on 31 July 2026 [1][2]. The company says the model generates
single-take clips up to 30 seconds long, with a multi-round mode that extends
sequences further — a capability claim from ByteDance itself, with no
independent reproduction found [1]. The model accepts up to 50 multimodal
reference inputs in a single request — up to 30 images, 10 video clips and 10
audio clips — and adds timestamp-level editing that can change part of a clip
without regenerating the whole thing [1]. ByteDance describes general
improvements to visual, audio and motion quality over the prior generation
but published no quantitative benchmarks or third-party comparisons [1]. At
launch, the model is rolling out through Jimeng AI and the Pro tier of
Doubao; API access via Volcano Engine's BytePlus ModelArk platform is
described as "coming soon" and was not yet available [1][2].

Some early aggregator coverage conflated this launch with an enterprise-beta
preview of Seedance 2.5 that ByteDance showed at its Volcano Engine FORCE
conference on 23 June, and one low-credibility outlet claimed the API had
already gone live by 16 July — neither is supported by ByteDance's own 31
July blog post or by TechNode's same-day report, both of which describe the
API as still forthcoming [1][2].

## Why it matters

AI video generation is one of the more competitive fronts in generative AI
right now, with ByteDance, OpenAI, Google and Kuaishou all shipping model
updates within weeks of each other this year. The features ByteDance
highlights for Seedance 2.5 — longer single-take clips, denser multimodal
reference input, and finer, timestamp-level editing — track a broader shift
in the field from short novelty clips toward tools aimed at production-style
editing workflows. None of the capability claims have independent
verification yet, and ByteDance has not said when, or whether, the ModelArk
API will open to outside developers.
