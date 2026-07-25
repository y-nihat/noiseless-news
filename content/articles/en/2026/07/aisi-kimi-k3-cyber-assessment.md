---
title: UK and US AI safety institutes find Moonshot AI's Kimi K3 significantly trails frontier closed models on cyber capability
date: 2026-07-23
slug: aisi-kimi-k3-cyber-assessment
lang: en
tldr: >
  The UK AI Security Institute (AISI) and the US Center for AI Standards and
  Innovation (CAISI) jointly published a preliminary assessment on 23 July
  2026 finding Moonshot AI's Kimi K3 performs significantly below frontier
  closed US models on cyber-offense tasks, though it edges out fellow
  open-weight model GLM-5.2 on one exploit-development benchmark. Its
  safeguards did not stop it from attempting the tasks. This follows AISI's
  17 July finding that the open-weight/closed-model cyber gap had been
  narrowing overall.
sources:
  - name: UK AI Security Institute / US CAISI — joint blog post
    url: https://www.aisi.gov.uk/blog/preliminary-assessment-of-kimi-k3s-cyber-capabilities
  - name: South China Morning Post — independent write-up
    url: https://www.scmp.com/tech/tech-war/article/3361711/chinas-kimi-k3-significantly-below-us-rivals-hacking-power-uk-us-study-shows
claims:
  - text: "UK AISI and the US Center for AI Standards and Innovation (CAISI) jointly published a preliminary assessment on 23 July 2026 finding Kimi K3 performs significantly below the most recent frontier cyber-capable closed models"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "On ExploitBench, an exploit-development benchmark, Kimi K3 scored 32% versus open-weight rival GLM-5.2's 24%, but achieved arbitrary code execution on none of 41 test samples, while leading US frontier models averaged arbitrary code execution on 20 of 41"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "On 'The Last Ones,' a 32-step simulated corporate-network attack, Kimi K3 reached step 17 of the path on average versus 28.5 for leading US frontier models, and completed the full attack path in 1 of 10 attempts"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "Kimi K3's safeguards allowed the model to assist with agentic cyber exploit development during the evaluation rather than refusing, unlike more restricted alternatives"
    type: research
    verdict: confirmed
    evidence: [1]
updated: []
follows: aisi-open-weight-cyber-gap
---

## What happened

The UK AI Security Institute (AISI) and its US counterpart, the Center for
AI Standards and Innovation (CAISI), jointly published a preliminary
assessment on 23 July 2026 of the cyber-offense capability of Kimi K3, the
open-weight model from Chinese lab Moonshot AI [1][2]. The two institutes'
top-line finding: Kimi K3 performs significantly below the most recent
frontier cyber-capable closed US models [1].

On ExploitBench, a benchmark for exploit development, Kimi K3 scored 32%,
ahead of fellow open-weight model GLM-5.2's 24% — but it failed to achieve
arbitrary code execution on any of 41 test samples, while leading US
frontier models achieved that on an average of 20 of 41 [1]. On "The Last
Ones," a 32-step simulated attack against a corporate network, Kimi K3
reached step 17 of the path on average, against 28.5 for leading US models,
and completed the full attack path in only 1 of 10 attempts [1][2]. AISI and
CAISI note Kimi K3's overall cyber-capability estimate carries a wider
confidence interval than other models because it draws on a single
benchmark (ExploitBench) rather than the fuller evaluation suite run on
other models [1].

The assessment also found Kimi K3's built-in safeguards allowed it to assist
with agentic cyber exploit development during testing rather than refusing,
unlike more restricted alternatives [1]. The institutes describe this as a
preliminary evaluation on a limited set of public and private benchmarks,
not a final capability determination [1].

This is a follow-up to AISI's 17 July finding that the general gap between
open-weight and closed frontier models on cyber tasks had narrowed to 4-7
months, down from 6-10 months, based on GLM-5.2 and DeepSeek V4-Pro. Kimi
K3, evaluated separately here, falls further behind frontier closed models
than that narrower overall trend on the specific benchmarks used in this
assessment.

## Why it matters

A government-run, joint UK/US assessment finding a widely-downloaded
open-weight model still lags meaningfully on cyber-offense tasks — while
also flagging that its safeguards don't block attempts at those tasks —
matters for the same defenders' planning question AISI raised on 17 July:
how much time remains before freely downloadable models catch up to what
closed frontier systems can already do. Kimi K3's result complicates a
simple narrowing-gap narrative — it trails both frontier closed models and,
on the cyber-range task, does not clearly outperform the earlier open-weight
figures already published.
