---
title: SpaceXAI open-sources Grok Build coding agent days after data-upload privacy incident
date: 2026-07-18
slug: xai-grok-build-privacy-incident
lang: en
tldr: >
  SpaceXAI (formerly xAI) published the source code of its Grok Build
  terminal coding agent on GitHub under Apache 2.0 on 15 July 2026, three
  days after independent security researcher cereblab showed the tool had
  been uploading users' full code repositories, including secrets, to
  xAI's cloud regardless of a privacy toggle. xAI says it has disabled the
  upload path and deleted previously collected data; the researcher who
  found the issue says that claim is not independently confirmed.
sources:
  - name: GitHub — xai-org/grok-build repository
    url: https://github.com/xai-org/grok-build
  - name: The Register
    url: https://www.theregister.com/ai-and-ml/2026/07/14/musk-promises-purge-after-grok-build-caught-sending-entire-repos-to-the-cloud/5271123
  - name: The Decoder
    url: https://the-decoder.com/xai-open-sources-grok-build-on-github-after-massive-data-breach/
  - name: cereblab — independent security research writeup
    url: https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547
  - name: OECD.AI Incidents Monitor
    url: https://oecd.ai/en/incidents/2026-07-13-acb3
claims:
  - text: "SpaceXAI (renamed from xAI on 6 July 2026) published the Grok Build coding-agent harness and terminal UI as open source under an Apache 2.0 license on GitHub on 15 July 2026; the underlying grok-build-0.1 model itself remains closed and paid"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "Independent security researcher cereblab published a wire-level analysis on 12 July 2026 showing grok-build v0.2.93 uploaded complete git repository bundles -- including a canary file proving full commit-history capture, and separately, .env secret files -- to an xAI Google Cloud Storage bucket, regardless of whether the tool's 'Improve the model' toggle was on or off"
    type: research
    verdict: confirmed
    evidence: [4, 2]
  - text: "xAI said, via a post from Elon Musk, that previously uploaded user data was deleted, the upload path was disabled server-side, and data retention was set off by default, effective 12 July 2026"
    type: business
    verdict: single-source
    evidence: [2]
  - text: "cereblab disputes xAI's account of the fix, saying xAI publicly pointed to its existing per-session '/privacy' retention toggle rather than the separate, previously undocumented server-side flag that actually stopped uploads, and says independent confirmation that all previously uploaded data was deleted is not yet available"
    type: business
    verdict: disputed
    evidence: [4, 2]
updated: []
---

## What happened

SpaceXAI -- the company formerly named xAI, renamed on 6 July 2026 -- published
the source code of Grok Build, its terminal-based coding agent, on GitHub
under an Apache 2.0 license on 15 July 2026 [1][3]. Only the agent harness
and terminal interface are open source; the model it runs on,
grok-build-0.1, remains closed and available only through a paid API [1].

The release came three days after independent security researcher cereblab
published a wire-level analysis of the tool's network traffic showing that
Grok Build version 0.2.93 was uploading users' complete git repositories --
full commit history included -- to a Google Cloud Storage bucket controlled
by xAI [4]. The upload happened regardless of whether the tool's "Improve
the model" privacy toggle was switched on or off, and separately captured
`.env` files containing secrets such as API keys [4]. cereblab proved the
uploads covered full repository history, not just files the agent had been
asked to read, by planting a canary file the agent was never instructed to
open and later recovering it from an uploaded archive [4]. The Register
independently corroborated the core findings [2].

Following the disclosure, Musk said on X that all previously uploaded data
had been deleted, that the upload path had been disabled server-side, and
that data retention was now off by default [2]. cereblab disputes how xAI
has framed that fix: the toggle xAI has publicly pointed to governs
per-session data retention, not the separate server-side upload flag that
was actually the source of the problem, and cereblab says there is no
independent confirmation that all previously collected data has in fact
been deleted [4][2]. The OECD's AI Incidents Monitor has logged the episode
[5].

## Why it matters

A coding agent with broad filesystem access uploading entire repositories,
including credentials, to the vendor's own cloud -- opt-out toggle or not --
is a serious trust failure for a tool built to run inside developers'
private codebases. Open-sourcing the harness days later increases
transparency into how the tool works going forward, but it does not by
itself verify xAI's central remediation claim, which currently rests on the
company's own statement rather than independent confirmation.
