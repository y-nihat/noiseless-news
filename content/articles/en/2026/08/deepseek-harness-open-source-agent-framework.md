---
title: DeepSeek open-sources Harness, a plugin-based coding-agent framework
date: 2026-08-13
published: 2026-08-14
slug: deepseek-harness-open-source-agent-framework
lang: en
tldr: >
  DeepSeek released Harness, an MIT-licensed open-source framework for
  building and running coding agents, in developer preview on 13 August
  2026. Every part of the system -- models, tools, sessions, sandboxes and
  the agent loop itself -- is built as a swappable plugin. DeepSeek's own
  materials make no competitor comparison; some outlets have framed it as
  rivaling Anthropic's coding tools, but that framing is press commentary,
  not a DeepSeek claim.
sources:
  - name: DeepSeek Harness (GitHub repository)
    url: https://github.com/deepseek-ai/deepseek-harness
  - name: DeepSeek Harness (LICENSE file)
    url: https://github.com/deepseek-ai/deepseek-harness/blob/master/LICENSE
  - name: DeepSeek AI (official announcement, X)
    url: https://x.com/deepseek_ai/status/2087887408440164663
  - name: The New Stack
    url: https://thenewstack.io/deepseek-harness-open-source-plugins/
  - name: VentureBeat
    url: https://venturebeat.com/technology/deepseek-harness-launches-as-open-source-rival-to-claude-code-alongside-v4-pro-on-api-with-higher-prices
claims:
  - text: "DeepSeek released Harness (CLI alias `dsh`), an open-source agent-runtime framework for building and running coding agents, on GitHub on 13 August 2026, in developer preview"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 4]
  - text: "The Harness codebase is released under the MIT license"
    type: announcement
    verdict: confirmed
    evidence: [2]
  - text: "Harness's architecture implements models, tools, skills, sessions, sandboxes, filesystems, the agent loop, orchestration and the UI as swappable plugins -- DeepSeek's own description, used independently in both the GitHub README and DeepSeek's announcement post"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "DeepSeek's own release materials make no comparison to any competitor; some press coverage has framed Harness as a rival to Anthropic's coding tools, with outlets disagreeing on which product (Claude Code vs. Claude Cowork) it supposedly rivals"
    type: announcement
    verdict: single-source
    evidence: [5]
updated: []
---

## What happened

DeepSeek released Harness, an open-source framework for building and running
coding agents, on GitHub on 13 August 2026, under the MIT license and
labeled a developer preview [1][2]. The repository and DeepSeek's own
announcement describe an architecture where every part of the system --
models, tools, skills, sessions, sandboxes, filesystems, the agent loop,
orchestration and the user interface -- is implemented as a plugin that can
be swapped or replaced [1][3]. The command-line tool ships under the alias
`dsh` and can be started with `npx @deepseek-ai/dsh web`; DeepSeek warns the
preview will have compatibility-breaking changes as it iterates [1].

The release was independently reported the same week by The New Stack,
beyond DeepSeek's own GitHub repository and announcement [4]. DeepSeek's own
materials contain no mention of any competing product. Some press coverage
has nonetheless framed Harness as a challenger to Anthropic's coding tools --
VentureBeat's headline calls it a "rival to Claude Code," while another
outlet framed it against "Claude Cowork," a different Anthropic product --
an inconsistency across outlets that indicates the comparison is each
publication's own framing rather than something DeepSeek stated [5].

## Why it matters

The release itself -- an MIT-licensed, plugin-architected agent framework
from DeepSeek -- is confirmed directly from the company's own GitHub
repository and announcement, plus independent press coverage. Any framing of
it as targeting a specific Anthropic product is press commentary, not a
DeepSeek claim, and outlets do not agree on which product that would be.
