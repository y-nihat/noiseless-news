---
title: OpenAI says it paused frontier RL training for two weeks, plans to rewrite Preparedness Framework
date: 2026-08-18
slug: openai-preparedness-framework-rewrite
lang: en
tldr: >
  OpenAI says it paused reinforcement-learning (RL) training on its newest
  models for two weeks after July's Hugging Face agent-security breach and
  preliminary evidence that its unreleased Astra model may have crossed its
  highest cyber-risk threshold, then hardened its research environments and
  expanded monitoring. The two-week pause has ended and smaller-scale
  training has resumed, but OpenAI says its largest frontier training runs
  remain on hold, and it plans to rewrite its Preparedness Framework — the
  document defining thresholds like "Critical" — with outside input, though
  no timeline exists yet.
sources:
  - name: OpenAI
    url: https://x.com/OpenAI/status/2089777845187031262
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/18/openai-institutes-new-safeguards-after-hugging-face-breach/
  - name: Axios
    url: https://www.axios.com/2026/08/18/openai-pause-astra-preparedness-framework
  - name: Time
    url: https://time.com/article/2026/08/18/openai-slowing-training/
claims:
  - text: "OpenAI paused reinforcement-learning (RL) training on its newest models intended for deployment for two weeks, citing July's Hugging Face agent-security breach and preliminary evidence that its unreleased Astra model may have reached the 'Critical' cyber-capability threshold in its Preparedness Framework"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "The two-week pause has ended; OpenAI has restarted many less-risky training workloads, but says its largest, most advanced frontier RL runs remain on hold pending new safeguards"
    type: announcement
    verdict: confirmed
    evidence: [2, 4]
  - text: "During the pause, OpenAI isolated its research environments, restricted network and tool access so a single compromised workload cannot reach the internet or internal networks, and expanded monitoring of models' tool actions and reasoning traces, targeting roughly a 30-minute response time to anomalies"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "OpenAI plans to evolve and rewrite its Preparedness Framework, the document defining risk thresholds such as 'Critical', and intends to involve outside organizations in revising it, though it has not set a timeline or published a draft"
    type: statement
    verdict: confirmed
    evidence: [3, 4]
updated: []
follows: openai-astra-critical-cyber-capabilities
---

## What happened

OpenAI said on 18 August 2026 that it temporarily paused reinforcement-learning
(RL) training on its newest models intended for deployment, for two weeks,
"while we hardened and red-teamed our research environments" and expanded
monitoring [1]. It tied the pause to July's Hugging Face agent-security breach
and to preliminary evidence that its unreleased Astra model may have reached
the "Critical" cybersecurity threshold in OpenAI's Preparedness Framework — a
threshold OpenAI first disclosed on 7 August 2026 [1][2][3].

The two-week window has since ended. OpenAI says it has restarted many
less-risky training workloads, but its largest, most advanced frontier RL
runs remain on hold while it builds out new safeguards [2][4].

During the pause, OpenAI isolated its research environments and restricted
network and tool access so that, in the company's words, a single
compromised workload cannot by itself reach the internet or other internal
networks; it also expanded monitoring of models' tool actions and reasoning
traces, targeting roughly a 30-minute response time to anomalies [1][2].
OpenAI VP of Research Amelia Glaese said the company has "put in place
requirements and expectations for safe development" that scale with the
level of risk it sees in a given model [2].

OpenAI also says it plans to evolve and rewrite its Preparedness Framework —
the document defining risk thresholds such as "Critical" — and intends to
involve outside organizations in revising it, though it has not set a
timeline or published a draft [3][4]. Chief Scientist Jakub Pachocki told
Time OpenAI will "definitely" need to evolve the framework; CEO Sam Altman
said "it is a good time to slow down" and that "getting AI safety right is
more important than any company's momentum" [4].

This is a distinct development from a separate, still-unconfirmed report
that OpenAI dissolved its Preparedness team, the group evaluating
catastrophic-risk models — a staffing claim OpenAI has denied on the record.
Today's changes concern the Preparedness Framework, the policy document, and
general safety practice, not that team's structure.

## Why it matters

This is OpenAI's most concrete response yet to the Critical-threshold
questions it raised about Astra on 7 August: rather than restrict one model,
it is changing how it trains and monitors frontier systems generally, and
revisiting the document that defines when a model is too risky to release.
Independent confirmation that the changes are effective — and the eventual
release decision for Astra — is still pending.
