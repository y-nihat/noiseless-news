---
title: Meta releases Muse Code, a terminal coding agent, alongside Muse Spark 1.2
date: 2026-08-05
slug: meta-muse-code-muse-spark-1-2
lang: en
tldr: >
  Meta released Muse Code on 5 August 2026, its first coding agent, running
  entirely from the terminal on macOS and Linux in public beta, powered by a
  new Muse Spark 1.2 model. Pricing matches the July Muse Spark 1.1 API rates,
  undercutting Anthropic and OpenAI, with a further-discounted tier for
  developers who opt in to share usage data. Meta's own benchmark charts claim
  competitive standing against rival coding agents; no independent evaluation
  is available yet.
sources:
  - name: Meta AI Research
    url: https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2
  - name: CNBC Technology
    url: https://www.cnbc.com/2026/08/05/meta-debuts-muse-code-to-take-on-anthropic-and-openai-.html
  - name: VentureBeat AI
    url: https://venturebeat.com/orchestration/meta-enters-the-ai-coding-wars-with-muse-spark-1-2-and-muse-code-with-persistent-async-background-agents
claims:
  - text: "Meta released Muse Code, a terminal coding agent powered by a new Muse Spark 1.2 model, in public beta for macOS and Linux on 5 August 2026, installed via a command-line installer and also available through the Meta Model API with expanded global access"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Muse Code's pay-as-you-go API pricing is $1.25 per million input tokens and $4.25 per million output tokens — the same rate as the July Muse Spark 1.1 release, and below comparable Anthropic and OpenAI offerings — with a separate, further-discounted 'contributor' tier for developers who opt in to share usage data to help improve the model"
    type: business
    verdict: confirmed
    evidence: [2, 3]
  - text: "Meta says Muse Spark 1.2 was co-trained with Muse Code and shows improvements over 1.1 in code generation, complex debugging, codebase understanding and end-to-end developer workflows, citing its own benchmark charts (Terminal-Bench 2.1, DeepSWE 1.1, Meta Internal Coding Bench) against rival coding agents"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
follows: meta-muse-spark-1-1
---

## What happened

Meta released Muse Code on 5 August 2026 — its first AI coding agent, and the company's first product entry in the terminal-based coding-agent category alongside Anthropic's Claude Code and OpenAI's Codex [1][2]. It runs entirely from the command line, installs with a single command, and is available in public beta for macOS and Linux, with persistent background agents and a local event log meant to make sessions replay-exact and restart-safe [1]. It is also available through the Meta Model API, which Meta says now has expanded global access [1].

Muse Code is powered by a new model, Muse Spark 1.2, which Meta describes as a coding-focused update to July's Muse Spark 1.1, co-trained alongside the agent itself [1]. Pay-as-you-go API pricing is unchanged from 1.1: $1.25 per million input tokens and $4.25 per million output tokens, still undercutting comparable Anthropic and OpenAI offerings [2][3]. A separate "contributor" tier offers a further discount to developers who opt in to share usage data to help improve the model [2].

Meta's own benchmark charts — Terminal-Bench 2.1, DeepSWE 1.1, and its Meta Internal Coding Bench — are presented as showing Muse Spark 1.2 competitive with rival coding agents [1]. Neither CNBC nor VentureBeat reported running independent tests; both largely relayed Meta's own release materials and benchmark charts [2][3]. No independent third-party evaluation (of the kind Vals AI published for Muse Spark 1.1) is available yet for this release.

## Why it matters

This is Meta's second move into the paid AI-coding market within a month, following July's Muse Spark 1.1 API launch, and its first dedicated coding-agent product — directly targeting the terminal-agent category Anthropic and OpenAI already compete in. The pricing continuity suggests Meta is committing to undercutting rivals on cost as its main lever rather than a claimed capability lead, which for now rests entirely on Meta's own benchmark selection.
