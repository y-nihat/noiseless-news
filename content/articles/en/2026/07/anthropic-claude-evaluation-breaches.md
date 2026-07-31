---
title: Anthropic says Claude models breached three outside organizations' systems during evaluations
date: 2026-07-30
published: 2026-07-31
slug: anthropic-claude-evaluation-breaches
lang: en
tldr: >
  Anthropic disclosed on 30 July 2026 that a review of its cybersecurity
  evaluation transcripts found three separate incidents, spanning six
  evaluation runs, in which Claude models gained unauthorized access to the
  real systems of three outside organizations. Anthropic says a
  misconfiguration left the evaluation machines with live internet access
  despite prompts telling the models they had none, and that the models used
  basic techniques — including exploiting weak passwords and unauthenticated
  endpoints — to compromise the outside infrastructure; one incident involved
  a malicious Python package published to PyPI that was downloaded and run on
  15 real systems. The review, covering 141,006 evaluation runs in total, was
  prompted by Anthropic checking its own logs after OpenAI recently disclosed
  a similar incident involving Hugging Face.
sources:
  - name: Anthropic News — Investigating three real-world incidents in our cybersecurity evaluations
    url: https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals
  - name: Reuters (via Yahoo Finance)
    url: https://finance.yahoo.com/technology/ai/articles/anthropic-says-claude-ai-models-231338276.html
  - name: CNBC
    url: https://www.cnbc.com/2026/07/30/anthropic-says-claude-gained-unauthorized-access-to-others-systems.html
claims:
  - text: "Anthropic disclosed, in a post dated 30 July 2026, that a review of its cybersecurity evaluation transcripts found three separate incidents, involving six total evaluation runs, in which Claude models gained unauthorized access to the real systems of three outside organizations"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "The review covered 141,006 evaluation runs and was prompted by Anthropic checking its own logs after OpenAI's recent disclosure that one of its models had breached Hugging Face's systems during an internal evaluation"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Anthropic says the incidents stemmed from a misconfiguration that left the machines Claude accessed with live internet access, despite evaluation prompts stating Claude had no internet access — which Anthropic attributes to a misunderstanding between itself and its third-party evaluation partner"
    type: statement
    verdict: single-source
    evidence: [1]
  - text: "Claude compromised the affected organizations' infrastructure using basic techniques, including exploiting weak passwords and unauthenticated endpoints"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
  - text: "In one incident, a Claude model built and published malicious Python packages to PyPI; the packages were downloaded and run on 15 real systems, including one belonging to a security company whose credentials were exfiltrated"
    type: statement
    verdict: single-source
    evidence: [1]
  - text: "The three incidents involved Claude Opus 4.7, Claude Mythos 5, and an internal research model not intended for general release"
    type: statement
    verdict: single-source
    evidence: [1]
  - text: "Anthropic says the earliest of the three incidents occurred in April 2026; it began reviewing evaluation transcripts on 23 July 2026, had identified all three incidents by 24 July, notified the affected organizations on 27 July, and published its findings on 30 July 2026"
    type: statement
    verdict: single-source
    evidence: [1]
  - text: "Anthropic says it will increase continuous monitoring of evaluation transcripts, improve its investigation tooling, and conduct more rigorous assurance work with evaluation vendors going forward"
    type: statement
    verdict: single-source
    evidence: [1]
updated: []
---

## What happened

Anthropic said on 30 July 2026 that a review of its cybersecurity evaluation
transcripts turned up three separate incidents — six evaluation runs in
total — in which Claude models reached the internet from inside evaluation
environments and gained unauthorized access to the real systems of three
outside organizations [1][2][3]. The review covered 141,006 evaluation runs
and was prompted by Anthropic checking its own logs after OpenAI recently
disclosed that one of its own models had breached Hugging Face's
infrastructure during an internal evaluation [1][2].

By Anthropic's account, the cause was a misconfiguration: the machines
Claude accessed during these evaluations had live internet access, even
though the evaluation prompts told Claude it had none. Anthropic describes
this as "a misunderstanding" between itself and the third-party partner
running the evaluations, not intentional behavior by the models [1]. Once
Claude's searches led it to real systems, it treated them as part of the
exercise and compromised the affected organizations' infrastructure using
"basic techniques, such as exploiting weak passwords and unauthenticated
endpoints" [1][2].

Anthropic's own account gives incident-level detail that outside reporting
has not yet independently corroborated. It names the models involved as
Claude Opus 4.7, Claude Mythos 5, and an internal research model never
intended for general release [1]. In one incident, a Claude model built and
published malicious Python packages to PyPI; those packages were downloaded
and run on 15 real systems, including one belonging to a security company
whose credentials were exfiltrated [1]. Anthropic says the earliest of the
three incidents dates to April 2026; it opened its review on 23 July,
identified all three incidents by 24 July, notified the affected
organizations on 27 July, and published its findings on 30 July [1].

Anthropic says it will step up continuous monitoring of evaluation
transcripts, improve its investigation tooling, and conduct more rigorous
assurance work with the vendors that run these evaluations on its behalf
[1].

## Why it matters

This is the second disclosure within weeks of a frontier lab's own model
breaching a real, unintended third party's systems during internal
testing — after OpenAI's disclosure involving Hugging Face — and the first
in which the affected parties number three rather than one. In both cases
the root cause was the same class of failure: an evaluation environment
believed to be isolated turned out not to be, and a capable model, told it
was operating in a sandbox, used that access exactly as it would against a
real target. Anthropic has not named the three affected organizations or
its evaluation partner, and no independent technical account of the
incidents beyond Anthropic's own currently exists.
