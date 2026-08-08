---
title: Anthropic adds cross-session messaging to Claude Code
date: 2026-08-07
slug: claude-code-cross-session-messaging
lang: en
tldr: >
  Anthropic shipped a Claude Code feature, as of version 2.1.224, that lets
  separate Claude Code sessions send each other short text messages -- to
  hand off a finding, answer a blocking question, or warn about a change
  that affects another session's work. It runs on macOS and Linux, sessions
  discover each other with a new `ListAgents` tool, and delivery is subject
  to per-session inbound controls the user configures.
sources:
  - name: Claude Code documentation (Anthropic)
    url: https://code.claude.com/docs/en/cross-session-messaging
  - name: Claude Code changelog (Anthropic)
    url: https://code.claude.com/docs/en/changelog
  - name: ClaudeDevs on X
    url: https://x.com/ClaudeDevs/status/2085817074816070014
  - name: 9to5Mac
    url: https://9to5mac.com/2026/08/07/claude-code-now-lets-sessions-talk-to-each-other-on-macos/
claims:
  - text: "Anthropic released cross-session messaging in Claude Code version 2.1.224, dated 7 August 2026, letting one Claude Code session send a text message to another using a new SendMessage tool, with ListAgents used to discover reachable sessions"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "The feature is available on macOS and Linux (including Linux inside WSL 2); it is not available on native Windows, and is not available on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry"
    type: capability
    verdict: confirmed
    evidence: [1]
  - text: "A message is plain text only, never the sender's conversation history or files; delivery to same-machine sessions goes over a local per-session socket, while delivery to a session on another of the user's machines or on Claude Code on the web goes through Anthropic's servers via Remote Control, and in that cross-machine case the receiving session can only reply, not start a new exchange"
    type: capability
    verdict: confirmed
    evidence: [1]
  - text: "Whether an incoming message is delivered, held for approval, or refused is controlled per-session by the crossSessionInbound setting and the sessions' permission modes; held messages default to expiring after five minutes (the dialogExpiry setting) if not approved"
    type: capability
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic's own account, ClaudeDevs, publicly announced the feature the same day, describing it as sending 'a summary (not your history or files)' so another session can pick up work mid-task"
    type: statement
    verdict: confirmed
    evidence: [3]
updated: []
---

## What happened

Anthropic added cross-session messaging to Claude Code, its terminal-based
coding agent, in version 2.1.224, dated 7 August 2026 [1][2]. The feature
lets one running Claude Code session send a short text message to another
session, using a new `SendMessage` tool; a companion `ListAgents` tool lets
a session discover which other sessions it can reach [1]. Anthropic's own
account, ClaudeDevs, announced the feature the same day, describing it as a
way to avoid re-explaining context across terminals: Claude sends "a
summary (not your history or files)," and the receiving session "picks it
up mid-task" [3].

According to Anthropic's documentation, a message carries only plain text,
never the sender's full conversation history or files [1]. Sessions running
on the same machine exchange messages over a local per-session socket;
messaging a session on a different machine, or a Claude Code on the web
session, routes through Anthropic's own servers via the separate Remote
Control feature, and in that cross-machine case the receiving side can only
reply to a message, not start a new one [1]. Whether an incoming message is
delivered automatically, held for the user's approval, or refused outright
is controlled per session through a `crossSessionInbound` setting and the
sessions' permission modes; a held message expires after five minutes by
default unless approved [1].

The feature is available on macOS and Linux, including Linux under WSL 2,
but not on native Windows, and it is not available when Claude Code runs
through Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent
Platform, or Microsoft Foundry [1].

## Why it matters

Developers running several Claude Code sessions in parallel -- for example,
across separate git worktrees of the same repository -- have had no way for
one session to tell another about a relevant change without the user
manually relaying it. Cross-session messaging automates that hand-off, at
the cost of a new inter-agent communication channel whose delivery
Anthropic gates through explicit, user-configurable permission controls
rather than allowing by default in every configuration [1].
