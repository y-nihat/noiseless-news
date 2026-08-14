---
title: Alibaba releases open-weight Qwen3.8 models, sets $50 million revenue threshold for commercial license
date: 2026-08-14
slug: alibaba-qwen-revenue-share-plan
lang: en
tldr: >
  Alibaba's Qwen team released open weights for two Qwen3.8 models in mid-August
  2026: Qwen3.8-27B under the permissive Apache 2.0 license, and Qwen3.8-2.4T-A95B
  (the open-weight version of flagship Qwen3.8-Max) under a new custom license
  that requires a paid commercial license only from businesses whose "model as a
  service" or "AI work assistant" revenue exceeds $50 million over any trailing
  12 months. That resolves an earlier Reuters report, based on unnamed sources,
  describing the plan as a percentage-based revenue share — the terms Alibaba
  actually published are a fixed revenue-threshold gate, not a revenue cut.
sources:
  - name: Hugging Face — Qwen/Qwen3.8-2.4T-A95B model card
    url: https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B
  - name: Hugging Face — Qwen/Qwen3.8-27B model card
    url: https://huggingface.co/Qwen/Qwen3.8-27B
  - name: South China Morning Post
    url: https://www.scmp.com/tech/tech-trends/article/3363927/alibaba-adds-commercial-restrictions-open-weight-qwen38-max-ai-model
  - name: Investing.com (Reuters)
    url: https://www.investing.com/news/stock-market-news/alibaba-plans-revenuesharing-for-commercial-users-of-next-qwen-ai-model--reuters-4845019
claims:
  - text: "Alibaba's Qwen team released open weights for Qwen3.8-27B under the Apache 2.0 license and Qwen3.8-2.4T-A95B, the open-weight version of Qwen3.8-Max, in mid-August 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Qwen3.8-2.4T-A95B ships under a custom \"Qwen3.8-Max License\": free to download, use, and modify, including for internal commercial use, but businesses (and affiliates) whose aggregate \"model as a service\" or \"AI work assistant\" revenue exceeds $50 million over any trailing 12-month period must obtain a separate paid commercial license"
    type: business
    verdict: confirmed
    evidence: [1, 3]
  - text: "This is a fixed revenue-threshold gate, not the percentage-based revenue-share arrangement described in earlier Reuters reporting from unnamed sources on 7 August 2026"
    type: business
    verdict: confirmed
    evidence: [3, 4]
updated: []
---

## What happened

Alibaba's Qwen team released open weights for two new Qwen3.8 models in
mid-August 2026 [1][2]. Qwen3.8-27B, a smaller vision-language model, ships
under the permissive Apache 2.0 license [2]. Qwen3.8-2.4T-A95B — the
open-weight release of Alibaba's flagship Qwen3.8-Max — ships under a new,
custom "Qwen3.8-Max License" instead [1][3].

That license is free to download, use, and modify, including for internal
commercial use, as long as outputs and model capabilities are not made
available to third parties [1][3]. A separate paid commercial license is
required only for businesses — including affiliates — running a "model as a
service" or "AI work assistant" product whose aggregate revenue from that
business exceeds $50 million over any trailing 12-month period [1][3].
Alibaba prices its own hosted API for the model separately, at roughly 40% of
Claude Opus 5's international input-token rate [3].

The terms resolve a question this site has tracked since 7 August 2026, when
Reuters, citing unnamed sources, reported Alibaba was planning a
percentage-based revenue-share arrangement for large commercial users of its
next Qwen model [4]. The license Alibaba actually published is a fixed
revenue-threshold gate, not a percentage cut of revenue [3][4].

## Why it matters

Chinese AI labs have driven much of this year's open-weight momentum by
giving away frontier-class models for free. Qwen3.8-Max's license is one of
the first concrete examples of a lab trying to keep that momentum while still
capturing revenue from the largest commercial users — hobbyists, startups,
and internal deployments stay free, but any company that builds a sizeable AI
model or AI-assistant business on top of the weights eventually has to pay
Alibaba directly.
