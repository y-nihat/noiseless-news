---
title: UK AI Security Institute finds open-weight models now trail frontier cyber capability by 4-7 months, down from 6-10
date: 2026-07-18
slug: aisi-open-weight-cyber-gap
lang: en
tldr: >
  The UK AI Security Institute (AISI) published evaluation results on 17 July
  2026 showing that recent open-weight models — Zhipu's GLM-5.2 and
  DeepSeek's V4-Pro — now match the cyber-offense capability closed frontier
  models had 4 to 7 months earlier, down from a 6-to-10-month gap AISI
  measured through most of 2025. Running the same cyber-range tasks on the
  open models also costs a fraction of what it costs on closed frontier
  models.
sources:
  - name: UK AI Security Institute — blog post
    url: https://www.aisi.gov.uk/blog/how-far-behind-the-frontier-are-leading-open-weight-models-on-cyber
  - name: The Decoder — independent write-up
    url: https://the-decoder.com/open-weight-models-now-match-frontier-cyber-performance-from-just-four-months-ago-at-a-fraction-of-the-cost/
claims:
  - text: "AISI's evaluation found recent open-weight models GLM-5.2 and DeepSeek V4-Pro perform similarly on cyber tasks to frontier closed models released 4 to 7 months before them, narrower than the 6-to-10-month gap AISI measured internally through most of 2025"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "On a 70-task narrow cyber benchmark across four difficulty levels, GLM-5.2 performed comparably to the most cyber-capable models released about 4 months earlier; DeepSeek V4-Pro performed comparably to Opus 4.5, released 5 months earlier"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "On multi-step autonomous cyber-range scenarios, GLM-5.2 reached as far as Opus 4.5 (released under 7 months earlier), while DeepSeek V4-Pro fell below Sonnet 4.5 on the same ranges"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Running a 100-million-token cyber-range task cost roughly $85 on Opus 4.5/4.6, versus about $46 on GLM-5.2 and $1.19 on DeepSeek V4-Pro"
    type: research
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## What happened

The UK AI Security Institute (AISI), the government body that evaluates
frontier AI systems for safety, published findings on 17 July 2026 showing
that two recent open-weight models — Zhipu's GLM-5.2 and DeepSeek's V4-Pro —
now come close to matching the cyber-offense capability of closed frontier
models released just months earlier [1][2]. On a 70-task narrow cyber
benchmark, GLM-5.2 matched models released about 4 months before it, and
DeepSeek V4-Pro matched Opus 4.5, released 5 months earlier [1]. On harder,
multi-step cyber-range scenarios that simulate a longer attack sequence,
GLM-5.2 reached as far as Opus 4.5 (a gap of under 7 months), while DeepSeek
V4-Pro fell below Sonnet 4.5 on the same tasks [1]. AISI says this overall
4-to-7-month lag is narrower than the 6-to-10-month gap it measured
internally through most of 2025 [1][2].

Running the same cyber-range workload is also far cheaper on the open
models: AISI put the cost of a 100-million-token cyber-range run at roughly
$85 on Opus 4.5/4.6, versus about $46 on GLM-5.2 and $1.19 on DeepSeek
V4-Pro [1][2].

AISI notes its own setup likely understates the open models' ceiling — it
did not apply extra elicitation or optimization to GLM-5.2 or DeepSeek
V4-Pro — and the cyber-range comparison draws on a smaller set of scenarios
than the narrow-task benchmark, so it carries less statistical confidence
than the 4-to-5-month narrow-task figure [1]. The published comparison set
does not include Anthropic's more recent Opus 4.7 or Opus 4.8, both released
before GLM-5.2 shipped, so the measured gap is against a specific earlier
Opus generation rather than Anthropic's most recent model at the time of
testing [1]. This is a blog post from AISI's own evaluation team, not a
peer-reviewed paper.

## Why it matters

A shrinking capability gap between freely downloadable models and closed
frontier systems means dangerous-capability access is not solely gated by
who can afford closed-model API pricing — a point sharpened by the cost
data, where the open models are roughly half to seventy times cheaper to
run the same tasks on. AISI frames this as reason for defenders to have
less lead time to prepare as open models catch up to what closed frontier
systems could do months prior.
