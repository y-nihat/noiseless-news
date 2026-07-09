---
title: Meta releases Muse Spark 1.1, an agentic coding model, undercutting rivals on price
date: 2026-07-09
slug: meta-muse-spark-1-1
lang: en
tldr: >
  Meta released Muse Spark 1.1 on 9 July 2026, a multimodal, agent-focused model
  with a 1-million-token context window, in US-only public preview via the Meta
  Model API. It's priced well below comparable Anthropic and OpenAI offerings.
  Meta calls it ready to compete with rival coding models, but that's Meta's own
  framing; the one independent benchmark we found places it mid-pack, ahead on
  agentic tasks but behind on the hardest coding tests.
sources:
  - name: Meta AI Blog
    url: https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/
  - name: Meta Developer Blog
    url: https://developer.meta.com/ai/resources/blog/build-with-muse-spark/
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/09/meta-enters-the-crowded-ai-coding-battle-with-muse-spark-1-1/
  - name: The Verge
    url: https://www.theverge.com/ai-artificial-intelligence/963193/meta-muse-spark-model-api
  - name: Vals AI
    url: https://www.vals.ai/models/meta_muse_spark_1_1
claims:
  - text: "Meta released Muse Spark 1.1 on 9 July 2026, a multimodal agentic model with a 1-million-token context window, in US-only public preview via the Meta Model API, and in 'Thinking' mode on the Meta AI app and meta.ai"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 4]
  - text: "Muse Spark 1.1 API pricing is $1.25 per million input tokens and $4.25 per million output tokens, with $20 in free credits per new account, undercutting comparable Anthropic and OpenAI offerings"
    type: business
    verdict: confirmed
    evidence: [2, 3]
  - text: "Meta says Muse Spark 1.1 is 'ready to compete' with rival frontier coding models and cites its own benchmark charts (Meta Internal Coding Bench, Terminal-Bench 2.1, SWE-Bench Pro) showing it close to, but trailing, Claude Opus 4.8 and GPT-5.5 on pure coding tasks"
    type: capability
    verdict: vendor-claim
    evidence: [1, 3, 4]
  - text: "On the independent Vals AI benchmark (35 models tested, as of 9 July 2026), Muse Spark 1.1 ranks 5th overall, leading 3 of 27 sub-benchmarks — MedScribe, TaxEval v2, and Harvey's Legal Agent Benchmark, none of them coding-specific — while trailing Claude Opus 4.8 and GPT-5.5 on the hardest coding tasks"
    type: capability
    verdict: confirmed
    evidence: [5]
  - text: "Mark Zuckerberg posted about the launch on X, reportedly his first post on that platform in about three years"
    type: business
    verdict: confirmed
    evidence: [3]
updated: []
---

## What happened

Meta released Muse Spark 1.1 on 9 July 2026: a multimodal, agent-focused model with a 1-million-token context window, available as a US-only public preview through the Meta Model API — compatible with both the OpenAI SDK and Anthropic's Messages API formats — and in "Thinking" mode on the Meta AI app and meta.ai [1][3][4]. Pricing is $1.25 per million input tokens and $4.25 per million output tokens, with $20 in free credits for new accounts, undercutting comparable Anthropic and OpenAI offerings [2][3].

Meta describes the model as delivering substantial gains in tool and computer use, coding, and multimodal understanding, and says it's "ready to compete" with rival frontier coding models [1]. That framing rests on Meta's own evaluation report and benchmark charts (Meta's Internal Coding Bench, Terminal-Bench 2.1, SWE-Bench Pro), which show Muse Spark 1.1 scoring close to, but behind, Claude Opus 4.8 and GPT-5.5 on pure coding tasks [1]. Neither TechCrunch nor The Verge ran independent tests of the model; both largely relayed Meta's own messaging and early-partner testimonials [3][4].

We found one genuinely independent data point: Vals AI, a third-party evaluator, ranks Muse Spark 1.1 5th overall among 35 models it has tested (as of 9 July 2026), leading on 3 of 27 sub-benchmarks — MedScribe, TaxEval v2, and Harvey's Legal Agent Benchmark, none of which are coding-specific — while trailing Opus 4.8 and GPT-5.5 on the hardest coding tasks [5]. Vals AI's leaderboard updates continuously, so these figures reflect a snapshot at verification time rather than a fixed result.

Separately, Meta CEO Mark Zuckerberg posted about the launch on X — reportedly his first post on the platform in about three years [3].

## Why it matters

Meta is entering the paid AI coding/agent API market for the first time with aggressive, below-market pricing, directly targeting Anthropic's and OpenAI's developer customers. Its "ready to compete" framing is Meta's own and rests on its own benchmark selections; the one independent evaluation available shows a more mixed picture — strong on cost and on agentic/tool-use tasks, but still behind the coding-specialist frontier models on the hardest coding benchmarks.
