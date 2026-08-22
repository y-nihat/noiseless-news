---
title: Slack launches Slack Code, embedding AI coding agents into team channels
date: 2026-08-20
published: 2026-08-22
slug: slack-code-launch
lang: en
tldr: >
  Slack (Salesforce) launched Slack Code on August 20, 2026: dedicated "Code
  Channels" where a team and an AI coding agent write, review and ship
  software together inside Slack, with diffs and a live preview visible to
  the whole channel. Claude Code, GitHub Copilot, Devin and Vercel's agent
  are live at launch; OpenAI's ChatGPT is announced as coming soon.
sources:
  - name: Slack
    url: https://slack.com/blog/news/slack-code-channels-for-agents
  - name: VentureBeat
    url: https://venturebeat.com/orchestration/slack-wants-to-drag-ai-coding-out-of-the-terminal-and-into-the-group-chat
  - name: SiliconANGLE
    url: https://siliconangle.com/2026/08/20/salesforce-introduces-slack-code-to-bring-agentic-team-coding-into-the-open/
claims:
  - text: "Slack launched \"Slack Code\" on August 20, 2026: dedicated \"Code Channels\" where a team works with an AI coding agent together inside Slack, with conversation, plan, code diffs and a live preview in the channel, for review and approval before anything ships."
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Claude Code (Anthropic), GitHub Copilot, Devin (Cognition) and Vercel's agent are live at launch; OpenAI's ChatGPT is announced as a partner but listed as coming soon, not live on day one."
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "At the launch event, Cognition president Jeff Wang cited a Cognition-wide engineering-velocity stat as context, not a measurement of Slack Code itself: the company's internal merged-pull-request count is up \"10x in the last few months,\" against headcount growth of \"about 40 percent.\""
    type: capability
    verdict: vendor-claim
    evidence: [2]
  - text: "Slack Code is available on any Slack plan at launch; customers still need their own separate access/license to each partner AI agent they want to use."
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
updated: []
---

## What happened

Slack, part of Salesforce, launched Slack Code on August 20, 2026: a feature that creates dedicated "Code Channels" where a team and an AI coding agent write, review and ship software together, inside Slack rather than a separate tool [1]. Tagging an agent in any conversation spins up a channel with tabs for the conversation, a plan, code diffs and a live preview, so the whole team can watch and comment before anything ships [1][2].

Claude Code (Anthropic), GitHub Copilot, Devin (Cognition) and Vercel's agent are available at launch; OpenAI's ChatGPT is announced as a partner but listed as coming soon, not live on day one [1][2][3]. Slack Code is available on any Slack plan at no extra charge, though customers still need their own separate access to whichever partner agent they use [2][3].

At the launch event, Cognition president Jeff Wang offered a Cognition-wide engineering-velocity stat as context — not a measurement of Slack Code itself, which launched that same day. He said the company's internal merged-pull-request count is up "10x in the last few months," against headcount growth of "about 40 percent" [2], from its general use of Devin — Cognition's own figure, not independently audited.

## Why it matters

Existing coding agents mostly work solo, in a terminal or IDE, with one developer reviewing the output. Slack Code moves that work into the team's group chat instead, making an agent's output visible to the whole channel by default. It is also a distribution move for Slack: rather than building its own coding agent, it is positioning itself as the shared surface where competing agents — including OpenAI's, once live — work side by side.
