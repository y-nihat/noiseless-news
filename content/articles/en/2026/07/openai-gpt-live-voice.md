---
title: OpenAI replaces ChatGPT's voice mode with GPT-Live, a model family that listens while it speaks
date: 2026-07-09
slug: openai-gpt-live-voice
lang: en
tldr: >
  OpenAI has released GPT-Live, a new family of full-duplex voice models, and made
  it the engine behind ChatGPT Voice on iOS, Android and the web. Paid tiers get
  GPT-Live-1; free users get GPT-Live-1-mini. The full-duplex claims are OpenAI's
  own — independent testing is not yet available.
sources:
  - name: OpenAI — Introducing GPT-Live
    url: https://openai.com/index/introducing-gpt-live/
  - name: The Verge
    url: https://www.theverge.com/ai-artificial-intelligence/962856/chatgpt-upgraded-voice-mode-gpt-live
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/08/openai-releases-new-voice-models-for-more-natural-live-conversations/
  - name: 9to5Mac
    url: https://9to5mac.com/2026/07/08/openai-upgrading-chatgpt-with-all-new-voice-mode-experience-watch-here/
claims:
  - text: "OpenAI released GPT-Live on 8 July 2026 and it now powers ChatGPT Voice"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Two models ship at launch: GPT-Live-1 for paid tiers, GPT-Live-1-mini for free users, on iOS, Android and the web"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 4]
  - text: "GPT-Live is full-duplex — it listens and speaks simultaneously and handles interruptions without restarting"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "OpenAI says complex queries are handed off to a frontier model in the background, currently GPT-5.5"
    type: statement
    verdict: confirmed
    evidence: [1, 3]
updated: []
---

## What happened

OpenAI released GPT-Live on 8 July, a new family of voice models that replaces the
engine behind ChatGPT's voice mode across iOS, Android and the web [1]. Two models
ship at launch: paid subscribers get GPT-Live-1, while free users get the smaller
GPT-Live-1-mini [1][3].

The headline change is the architecture. OpenAI describes GPT-Live as *full-duplex*:
the model listens and speaks at the same time, so a user can talk over it mid-answer
and it adjusts without the stop-and-restart turn-taking of the previous voice mode
[1][2]. For questions that need search or deeper reasoning, OpenAI says the voice
model hands the work to a frontier model in the background — currently GPT-5.5 [1][3].

## Why it matters

Turn-taking friction is the main reason voice assistants still feel like walkie-talkies
rather than conversation. If the full-duplex design works as described, it removes
that constraint at the interface level rather than papering over it with faster
responses. Note the limit of what is verified here: the simultaneous-listening
behavior is OpenAI's own description, echoed in early hands-on coverage but not yet
independently tested — which is why it carries a *vendor claim* label below.
