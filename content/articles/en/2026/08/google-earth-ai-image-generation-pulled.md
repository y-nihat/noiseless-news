---
title: Google pulls AI image-generation tool from Google Earth a day after launch
date: 2026-07-31
published: 2026-08-02
slug: google-earth-ai-image-generation-pulled
lang: en
tldr: >
  Google added an AI image-generation tool to the web version of Google Earth
  on 30 July 2026, letting users generate photorealistic images layered onto
  real satellite, aerial and 3D data at any location. Within a day, users
  showed the tool could fabricate convincing fake scenes at real coordinates —
  including a nonexistent nuclear facility in Iran and refugee scenes near
  the US-Mexico border — and that its SynthID watermark could be defeated
  simply by photographing the output. Google rolled the feature back on 31
  July, saying it was implementing "stronger guardrails."
sources:
  - name: Google — Nano Banana in Google Earth
    url: https://blog.google/products-and-platforms/products/earth/nano-banana-google-earth-image-generation/
  - name: Futurism
    url: https://futurism.com/artificial-intelligence/google-pulls-down-google-earth-ai-feature
  - name: Forbes
    url: https://www.forbes.com/sites/paulmonckton/2026/08/01/google-earth-ai-feature-removed/
claims:
  - text: "Google added an AI image-generation feature, powered by its Nano Banana 2 model, to the web version of Google Earth on 30 July 2026, letting users tap 'create image' after zooming to a location and type a prompt to generate imagery layered onto Google Earth's real satellite, aerial and 3D data"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Google said generated images did not appear in the main Google Earth experience for other users to see and were watermarked as AI-generated using SynthID"
    type: statement
    verdict: confirmed
    evidence: [1]
  - text: "Within a day of launch, users demonstrated the tool could generate convincing fake imagery tied to real coordinates: OSINT researcher Henk van Ess fabricated scenes of a nuclear facility in Iran and of refugees near the US-Mexico border, and other circulating examples included a bombed hospital superimposed on Gaza imagery and a 'warzone' rendering of the White House; Futurism independently reproduced the capability with its own generated images depicting a Pennsylvania town hit by drought and wildfire"
    type: capability
    verdict: confirmed
    evidence: [2, 3]
  - text: "Forbes reported that Google's SynthID watermark could be defeated simply by photographing or screen-recording a generated image; a screen recording of the tool's output tested with Hive AI's detector was rated only 1% likely to be AI-generated"
    type: statement
    verdict: single-source
    evidence: [3]
  - text: "Google rolled back the image-generation feature on 31 July 2026, about a day after launch, saying it had seen 'people sharing screenshots of generated imagery that appear to violate our policies' and that it was 'rolling back this feature in Google Earth while we work on implementing stronger guardrails'"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## What happened

Google added an AI image-generation tool to the web version of Google Earth
on 30 July 2026, powered by its Nano Banana 2 model. After zooming to any
location, users could tap "create image" and type a prompt to generate a
photorealistic image layered onto Google Earth's real satellite, aerial and
3D-mapping data for that spot. Google said the generated images did not
appear in the main Google Earth experience for other users to see, and were
watermarked as AI-generated using its SynthID system [1].

Within about a day, users showed the tool could be used to fabricate
convincing fake scenes tied to real, identifiable coordinates. OSINT
researcher Henk van Ess generated fabricated imagery of a nuclear facility in
Iran and of refugees near the US-Mexico border; other examples that
circulated included a bombed hospital superimposed on real Gaza imagery and a
"warzone" rendering of the White House. Futurism's own reporters
independently reproduced the capability, generating separate images that
depicted a real Pennsylvania town suffering drought and wildfire damage
[2][3].

Forbes reported that the SynthID watermark meant to mark the images as
AI-generated could be defeated simply by photographing or screen-recording
the output: a screen recording of the tool's generated imagery, tested with
Hive AI's detection service, was rated only 1% likely to be AI-generated
[3].

Google rolled back the feature on 31 July 2026, about a day after launch.
In a statement, the company said: "We know that people uniquely trust Google
Earth for a reliable view of the world... we've also seen people sharing
screenshots of generated imagery that appear to violate our policies. So
we're rolling back this feature in Google Earth while we work on
implementing stronger guardrails" [1].

## Why it matters

Google Earth is widely trusted as an accurate, real-world reference —
unlike a general-purpose image generator, content made with this tool was
grounded in real coordinates and layered onto genuine satellite imagery,
making fabricated scenes of specific real places easier to pass off as
authentic. The watermark Google pointed to as its safeguard did not survive
a screenshot, the simplest way people already share images online, which is
the detail that turned a novelty feature into a same-week rollback.
