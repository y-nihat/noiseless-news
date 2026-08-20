---
title: OpenAI adds an Apple Messages plugin to ChatGPT's Mac app
date: 2026-08-20
slug: openai-chatgpt-apple-messages-plugin
lang: en
tldr: >
  OpenAI rolled out an Apple Messages plugin for ChatGPT's macOS desktop app
  on 20 August 2026: on Apple Silicon Macs, ChatGPT can now read, search and
  send iMessage, SMS and RCS conversations, with sending gated by a default
  per-message approval step. OpenAI told Bloomberg the feature processes
  messages locally and does not build a full index of a user's messages, but
  how much message content still reaches OpenAI's servers during processing
  remains an open question that no outside reporting has independently
  verified.
sources:
  - name: OpenAI (learn.chatgpt.com plugin docs)
    url: https://learn.chatgpt.com/docs/plugins
  - name: 9to5Mac
    url: https://9to5mac.com/2026/08/20/chatgpt-update-adds-apple-messages-integration-on-mac/
  - name: Bloomberg (via Yahoo Finance)
    url: https://finance.yahoo.com/technology/ai/articles/chatgpt-now-control-imessage-potentially-205633657.html
claims:
  - text: "OpenAI rolled out an Apple Messages plugin for ChatGPT's macOS desktop app, limited to Apple Silicon (arm64) Macs, that can read and search a user's iMessage, SMS and RCS conversations and prepare and send messages on the user's behalf"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Sending is gated by a default per-message approval step (\"Allow once\"), with an optional persistent \"Always allow sending to this chat\" override that users can revoke later in ChatGPT's settings; OpenAI's own documentation separately cautions against enabling persistent approval for chats with untrusted instructions"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "The plugin shipped on 20 August 2026, according to OpenAI's own release notes, and is not available on Intel Macs, the web, mobile, or other ChatGPT surfaces"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "OpenAI told Bloomberg the plugin processes messages locally on the user's Mac and does not build a full index of a user's message history; Bloomberg's reporting frames how much message content reaches OpenAI's servers during processing as an open question its own reporting could not independently verify"
    type: statement
    verdict: single-source
    evidence: [3]
updated: []
---

## What happened

OpenAI shipped an Apple Messages plugin for ChatGPT's macOS desktop app on
20 August 2026, limited to Apple Silicon Macs [1, 2]. Once enabled, ChatGPT
can read and search a user's iMessage, SMS and RCS conversations, and
prepare and send messages on their behalf [1]. Sending is gated by a
default per-message approval step ("Allow once"); users can instead grant
persistent "Always allow sending to this chat" access, which they can
revoke later in ChatGPT's settings — OpenAI's own documentation cautions
against turning on persistent approval for chats containing untrusted
instructions [1]. The plugin is not available on Intel Macs, the web,
mobile, or other ChatGPT surfaces [1, 2].

Asked by Bloomberg about the privacy implications of ChatGPT reading a
user's messages, OpenAI said the plugin processes messages locally on the
Mac and does not build a full index of a user's message history [3]. How
much message content still reaches OpenAI's servers during processing is
not addressed by that statement, and no independent reporting has verified
it either way [3].

## Why it matters

Apple Messages joins a small set of local-data plugins OpenAI has opened
ChatGPT up to on the Mac, trading convenience for access to one of the
most sensitive stores of personal data on a user's device. OpenAI's own
approval-step design and its warning against blanket "always allow" access
for untrusted chats suggest the company is aware of the risk; the unresolved
question, per Bloomberg, is how much of that message content leaves the
device in the first place.
