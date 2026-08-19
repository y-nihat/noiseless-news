---
title: OpenAI previews Private Safety Processing, a zero-retention misuse detector
date: 2026-08-19
slug: openai-private-safety-processing
lang: en
tldr: >
  OpenAI said on 19 August 2026 that it is testing a new system, Private
  Safety Processing, with early enterprise and API customers. It aims to
  detect misuse patterns across a customer's related interactions by sending
  OpenAI only a narrow safety signal rather than the underlying prompts or
  responses, while remaining compatible with OpenAI's existing Zero Data
  Retention terms. OpenAI plans a broader rollout and a technical white paper
  in September 2026; for now the feature applies only to enterprise and API
  customers, not consumer ChatGPT plans.
sources:
  - name: OpenAI News
    url: https://openai.com/index/offering-zero-data-retention-for-frontier-models
  - name: Bloomberg
    url: https://www.bloomberg.com/news/articles/2026-08-19/openai-to-enhance-safety-processes-for-paid-tool-customers
  - name: Axios
    url: https://www.axios.com/2026/08/19/openai-previews-zero-retention-safety-system-as-anthropic-requires-data-logs
  - name: OpenAI News
    url: https://openai.com/index/responding-next-frontier-critical-cyber-capabilities
claims:
  - text: "OpenAI's Zero Data Retention (ZDR) terms mean prompts and responses submitted by eligible API customers are not retained once a request is processed, are not available to OpenAI staff for review, and are not used to train its models unless the customer opts in"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "OpenAI is previewing a new system, Private Safety Processing, that aims to detect misuse patterns across a customer's related interactions by sending OpenAI only a narrowly defined safety signal rather than the underlying prompts or responses; customer data can remain on the customer's infrastructure or be stored by OpenAI encrypted with customer-controlled keys, while remaining compatible with ZDR"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Private Safety Processing is currently being tested with early enterprise and API customers; OpenAI says it plans a broader rollout and a technical white paper in September 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "The new system is scoped to enterprise and API customers and does not currently extend to consumer ChatGPT subscription plans"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "OpenAI has separately said its unreleased Astra model may cross its highest cyber-risk threshold, and paused related reinforcement-learning work pending additional safeguards"
    type: announcement
    verdict: confirmed
    evidence: [4]
updated: []
---

## What happened

Under OpenAI's existing Zero Data Retention (ZDR) terms, prompts and
responses submitted by eligible API customers are not retained once a
request is processed, are not available to OpenAI staff for review, and are
not used to train its models unless the customer opts in [1]. OpenAI said on
19 August 2026 that it is now previewing a new system on top of that
baseline, called Private Safety Processing, with early enterprise and API
customers [1][2][3].

Private Safety Processing is designed to detect misuse patterns across a
customer's related interactions -- something OpenAI says today's
ZDR-compatible safety tools cannot do, since they evaluate each interaction
individually. Instead of seeing the underlying prompts and responses, OpenAI
says it receives only a "narrowly defined safety signal"; customer data can
stay on the customer's own infrastructure, or be stored by OpenAI encrypted
with keys the customer controls [1][2][3]. The system is currently in
testing with early customers; OpenAI says it plans a broader rollout and a
technical white paper in September 2026 [1][3]. For now it is scoped to
enterprise and API customers only, not consumer ChatGPT subscription plans
[1][2].

## Why it matters

The announcement lands in the same week OpenAI separately disclosed that its
unreleased Astra model may cross the company's highest cyber-risk threshold,
and that it paused related reinforcement-learning work pending additional
safeguards [4] -- a reminder that the company's privacy commitments and its
safety concerns about its own most capable models are moving on parallel
tracks. Private Safety Processing itself is still a preview: there has been
no independent technical review yet of whether a safety signal could
indirectly leak content, and the September rollout is a stated plan, not a
shipped product.
