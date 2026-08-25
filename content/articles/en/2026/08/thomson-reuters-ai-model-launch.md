---
title: Thomson Reuters launches an in-house AI model inside its CoCounsel Legal product
date: 2026-08-24
published: 2026-08-25
slug: thomson-reuters-ai-model-launch
lang: en
tldr: >
  Thomson Reuters has built and launched its own AI model, called Thomson,
  moving away from renting models from outside AI labs for at least this
  product line. It first ships inside Tabular Analysis in Thomson Reuters'
  CoCounsel Legal, with a smaller open-weight version released on Hugging
  Face for academic use. Thomson Reuters says the model descends from
  Alibaba's open-weight Qwen and cost about $40 million to build, and that it
  matches or beats frontier models like GPT-5.5 and Claude Opus 4.8 on
  benchmarks — the Qwen lineage, cost figure and benchmark comparisons all
  come solely from the company's own reporting, and independent scrutiny of
  the benchmark methodology found the comparison less clear-cut than the
  headline claim.
sources:
  - name: Thomson Reuters (PR Newswire)
    url: https://www.prnewswire.com/news-releases/thomson-reuters-leverages-its-world-class-data-assets-to-launch-its-own-frontier-model-302857499.html
  - name: Thomson Reuters
    url: https://www.thomsonreuters.com/en-us/posts/innovation/thomson-reuters-built-its-own-ai-model-that-now-ranks-among-the-worlds-best/
  - name: The Decoder
    url: https://the-decoder.com/thomson-reuters-bets-40m-on-owning-its-ai-instead-of-renting-from-openai-or-anthropic/
  - name: LawSites
    url: https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html
claims:
  - text: "Thomson Reuters has built and launched its own proprietary AI model, called Thomson, rather than relying solely on models rented from outside AI labs for at least this part of its product line; it is first deployed in Tabular Analysis within Thomson Reuters' CoCounsel Legal, with a smaller open-weight version released on Hugging Face for academic and non-commercial use."
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Thomson Reuters says the model descends from an intermediate, safety-retrained checkpoint it calls \"Snowdon,\" built on Alibaba's open-weight Qwen3.5-397B, with Imperial College conducting the safety and ethics retraining."
    type: announcement
    verdict: single-source
    evidence: [3]
  - text: "Thomson Reuters says building Thomson cost about $40 million over more than two years, including roughly $450,000 for the final training run."
    type: business
    verdict: single-source
    evidence: [1]
  - text: "Thomson Reuters says Thomson performs on par with or ahead of frontier models, including Claude Opus 4.8, GPT-5.5, Claude Sonnet 5 and Gemini 3.1 Pro, on legal and general benchmarks."
    type: capability
    verdict: vendor-claim
    evidence: [1, 2, 4]
updated: []
---

## What happened

Thomson Reuters says it has built and launched its own proprietary AI model, called Thomson, rather than relying solely on models rented from outside AI labs for at least this part of its product line [1][2]. The model's first deployment is Tabular Analysis, a feature inside Thomson Reuters' CoCounsel Legal product, and the company has also released a smaller, open-weight version on Hugging Face for academic and non-commercial use [1]. Thomson Reuters says Thomson descends from an intermediate, safety-retrained checkpoint it calls "Snowdon," built on Alibaba's open-weight Qwen3.5-397B, with Imperial College conducting the safety and ethics retraining — a detail that appears only in secondary reporting, not in Thomson Reuters' own announcement materials [3].

Thomson Reuters says the project cost about $40 million over more than two years, including roughly $450,000 for the final training run, and that Thomson performs on par with or ahead of frontier models — including Claude Opus 4.8, GPT-5.5, Claude Sonnet 5 and Gemini 3.1 Pro — on legal and general benchmarks [1][2]. Both figures come solely from the company's own release; despite broad same-day pickup across outlets, every account traces back to that single source, with no independent filing or estimate confirming the cost. An independent look at the benchmark methodology, by legal-technology journalist Bob Ambrogi at LawSites, found asymmetries in how the tests were run — including test-time scaling applied to Thomson but not clearly to its rivals, and GPT-5.5 tested in a non-reasoning mode — and concluded the self-reported comparison is "more mixed than the headline suggests" [4].

## Why it matters

A major legal-information vendor building and owning its model, instead of renting from OpenAI or Anthropic, marks a strategy shift other enterprise AI buyers are weighing — but the cost of doing so, and the resulting model's standing against frontier competitors, are so far entirely Thomson Reuters' own telling.
