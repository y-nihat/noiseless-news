---
title: Sakana AI releases Fugu-Cyber, a cyber-defense orchestration model
date: 2026-07-21
published: 2026-07-27
slug: sakana-fugu-cyber-release
lang: en
tldr: >
  Sakana AI released Fugu-Cyber on 21 July 2026, a multi-agent system for
  cyber defense — vulnerability verification and generating detection rules
  from threat intelligence — that routes tasks across multiple underlying
  models while presenting itself as one. Sakana's own benchmark figures for
  the release, 86.9% on CyberGym and 72.1% on CTI-REALM, are self-reported:
  Fugu-Cyber does not appear on CyberGym's independent leaderboard, and
  independent outlets say Sakana hasn't disclosed its evaluation methodology.
sources:
  - name: Sakana AI — Fugu-Cyber release page
    url: https://sakana.ai/fugu-cyber-release/
  - name: MarkTechPost
    url: https://www.marktechpost.com/2026/07/25/sakana-ai-releases-fugu-cyber-orchestration-model-cybergym-cti-realm/
  - name: Tech Times
    url: https://www.techtimes.com/articles/321267/20260722/sakana-ai-fugu-cyber-claims-869-vulnerability-score-benchmark-methodology-not-disclosed.htm
  - name: llm-stats.com — CyberGym leaderboard
    url: https://llm-stats.com/benchmarks/cybergym
  - name: CyberGym benchmark paper (arXiv, ICLR 2026)
    url: https://arxiv.org/abs/2506.02548
claims:
  - text: "Sakana AI released Fugu-Cyber, a multi-agent orchestration model for cyber defense, on 21 July 2026"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Sakana reports Fugu-Cyber scores 86.9% on the CyberGym benchmark and 72.1% on CTI-REALM"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Fugu-Cyber does not appear on CyberGym's independent leaderboard, and independent outlets report that Sakana has not disclosed its evaluation methodology"
    type: statement
    verdict: confirmed
    evidence: [2, 3, 4]
  - text: "Published academic results on CyberGym (ICLR 2026) show top model/scaffold combinations reaching about 18-20%, well below Sakana's self-reported figure for Fugu-Cyber"
    type: research
    verdict: confirmed
    evidence: [5]
updated: []
---

## What happened

Sakana AI released Fugu-Cyber on 21 July 2026 [1], a multi-agent system built for cyber defense — verifying vulnerabilities and generating detection rules from threat intelligence — that Sakana says "behaves like a single model" while routing tasks across multiple underlying models it keeps proprietary; access is gated behind an application form [1]. It is the second release in Sakana's Fugu line, after a base version shipped 22 June 2026 [1].

Sakana's release page states Fugu-Cyber scores 86.9% on the CyberGym benchmark and 72.1% on CTI-REALM [1], without disclosing trial count or evaluation scaffold. As of 27 July, Fugu-Cyber does not appear among CyberGym's ten listed entries on the independent leaderboard at llm-stats.com [4]. Tech Times and MarkTechPost both report the figures as self-reported, and note that CTI-REALM's own metric is a 0–1 trajectory-reward score, not a pass/fail rate — meaning Sakana is presenting a score as a "success rate" the benchmark wasn't designed to produce [2][3]. CyberGym's own academic paper, from ICLR 2026, put the top model/scaffold combinations at roughly 18–20% [5] — well below Sakana's self-reported figure for Fugu-Cyber, though that paper used earlier-generation scaffolding.

## Why it matters

Cyber-defense tools live or die on whether their numbers hold up under independent testing. Fugu-Cyber's release is confirmed, but its headline benchmark figures are not: they are vendor claims, absent from CyberGym's own leaderboard and unreplicated outside Sakana, at a wide enough gap from disclosed academic ceilings that independent scrutiny is warranted before treating them as fact.
