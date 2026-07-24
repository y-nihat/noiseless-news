---
title: Anthropic releases Claude Opus 5, keeping pricing flat at $5/$25 per million tokens
date: 2026-07-24
slug: anthropic-claude-opus-5-launch
lang: en
tldr: >
  Anthropic released Claude Opus 5 on 24 July 2026, rolling it out day one
  across the Claude API, claude.ai, Claude Code, Bedrock, Google Cloud, and
  Microsoft Foundry (GitHub Copilot access is arriving gradually). Standard
  pricing is unchanged from Opus 4.8 at $5 per million input tokens and $25
  per million output tokens. Independent tracker Artificial Analysis places
  it at the top of its Intelligence Index; Anthropic's own comparative
  benchmark claims against rival models are not yet independently reproduced.
sources:
  - name: Anthropic News
    url: https://www.anthropic.com/news/claude-opus-5
  - name: GitHub Changelog
    url: https://github.blog/changelog/2026-07-24-claude-opus-5-is-now-available-in-github-copilot/
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/models/claude-opus-5
  - name: CodeRabbit
    url: https://www.coderabbit.ai/blog
  - name: VentureBeat
    url: https://venturebeat.com/
claims:
  - text: "Anthropic released Claude Opus 5 on 24 July 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 5]
  - text: "Opus 5 rolled out day one on the Claude API, claude.ai, Claude Code, Claude Cowork, Pro and Max plans, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry; GitHub Copilot access is rolling out gradually to Pro+, Max, Business, and Enterprise users"
    type: business
    verdict: confirmed
    evidence: [1, 2]
  - text: "Standard pricing is $5 per million input tokens and $25 per million output tokens, unchanged from Opus 4.8; a faster inference mode costs roughly double"
    type: business
    verdict: confirmed
    evidence: [1, 5]
  - text: "Anthropic claims Opus 5 approaches Fable 5's intelligence at roughly half the price, citing its own Frontier-Bench v0.1 (43.3% vs Fable 5's 33.7%) and ARC-AGI-3 (30.2% vs the next-best model's 7.8%) results"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "On Artificial Analysis's independent Intelligence Index, Claude Opus 5 (max-effort setting) scores 61, ranking first among tracked models as of the 24 July 2026 live leaderboard fetch"
    type: capability
    verdict: confirmed
    evidence: [3]
  - text: "Independent testing by code-review vendor CodeRabbit found Opus 5 more precise than its baseline reviewer on flagged issues (39.3% vs 35.2%) but with lower recall of known issues (55.2% vs 61.1%) and produced roughly four times more nitpick comments; CodeRabbit says its results do not support using Opus 5 as a sole reviewer"
    type: capability
    verdict: confirmed
    evidence: [4]
updated: []
---

## What happened

Anthropic released Claude Opus 5 on 24 July 2026, making it available the same day across the Claude API, claude.ai, Claude Code, Claude Cowork, and Pro/Max subscription plans, plus Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry [1]. GitHub confirmed Copilot access separately, noting the rollout there is gradual across Pro+, Max, Business, and Enterprise tiers rather than available to everyone immediately [2]. Standard API pricing holds at $5 per million input tokens and $25 per million output tokens — the same rate as Opus 4.8 — with a faster inference mode priced at roughly double [1].

Anthropic's own marketing centers on a comparison to Fable 5, saying Opus 5 approaches that model's intelligence at about half the cost, backed by the company's internally run Frontier-Bench v0.1 (43.3% vs Fable 5's 33.7%) and ARC-AGI-3 (30.2%, more than triple the next-best model's 7.8%) [1]. Neither benchmark has been independently reproduced, so both figures are presented here as Anthropic's own claims rather than confirmed results.

Independent evidence is more limited but does exist. Artificial Analysis's Intelligence Index — a third-party leaderboard — placed Opus 5 at the top of its rankings with a score of 61 at the model's maximum-effort setting, based on a live fetch of the leaderboard on 24 July 2026 [3]. Separately, code-review company CodeRabbit ran its own comparison and found a mixed picture: Opus 5 was more precise than CodeRabbit's baseline reviewer on the issues it flagged (39.3% vs 35.2%) but caught fewer of the known issues in CodeRabbit's test set (55.2% vs 61.1%) and generated about four times as many low-value "nitpick" comments. CodeRabbit's own conclusion was that its data does not support using Opus 5 as a standalone reviewer [4].

## Why it matters

Flat pricing against the previous flagship, combined with day-one availability across every major cloud and coding surface Anthropic sells into, signals the company is treating Opus 5 as a direct swap-in upgrade rather than a premium new tier. The gap between Anthropic's internal benchmark claims and the thinner independent evidence available so far — one favorable third-party leaderboard, one mixed third-party evaluation — is typical for a same-day launch; further independent testing will fill that in over the coming weeks.
