---
title: Anthropic study finds Claude's expressed values shift by model and by language
date: 2026-07-14
slug: anthropic-claude-values-models-languages
lang: en
tldr: >
  Anthropic published research on 13 July 2026 analyzing 309,815 Claude.ai
  conversations and found that Claude's expressed values systematically vary
  by both model version and conversation language — for example, expressing
  the most warmth in Hindi and the most rigor in Russian. The study, a
  follow-up to Anthropic's "Values in the Wild" work, compresses thousands of
  identified values into four measurable axes.
sources:
  - name: Anthropic News
    url: https://www.anthropic.com/research/claude-values-models-languages
claims:
  - text: "Anthropic published a study on 13 July 2026 analyzing 309,815 Claude.ai conversations to measure how Claude's expressed values vary across models and languages"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "The dataset was sampled evenly across three models — Sonnet 4.6, Opus 4.6, and Opus 4.7 — and the top 20 languages used on Claude.ai, yielding roughly 5,000 conversations per model-language pair, collected over a two-week period in May 2026"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic compressed the values it identified into four axes — Deference vs. Caution, Warmth vs. Rigor, Depth vs. Brevity, and Candor vs. Execution — which together capture about 15% of the variation in Claude's expressed values"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "By model, Sonnet 4.6 leaned toward deference, warmth, and brevity; Opus 4.6 leaned toward rigor, deference, and brevity; Opus 4.7 leaned toward caution, rigor, depth, and candor"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "By language, Claude expressed the most warmth in Hindi and the most rigor in Russian, and showed the most deference in Arabic and the most caution in English"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic itself frames the language variation as an open question: some of it may reflect Claude appropriately adapting to cultural conversational norms, and some may reflect uneven alignment investment across languages, without the study resolving which"
    type: research
    verdict: confirmed
    evidence: [1]
updated: []
---

## What happened

Anthropic published a study on 13 July 2026 measuring how Claude's expressed values vary by model version and by the language a conversation is conducted in [1]. It is a follow-up to the company's earlier "Values in the Wild" work, and analyzes 309,815 Claude.ai conversations in which users gave Claude a subjective task, sampled evenly across three models — Sonnet 4.6, Opus 4.6, and Opus 4.7 — and the 20 most common languages on the platform, roughly 5,000 conversations per model-language pair, collected over two weeks in May 2026 [1].

Anthropic compressed the values identified in those conversations into four measurable axes — Deference vs. Caution, Warmth vs. Rigor, Depth vs. Brevity, and Candor vs. Execution — which together account for about 15% of the variation in Claude's expressed values [1]. By model, Sonnet 4.6 leaned toward deference, warmth, and brevity; Opus 4.6 toward rigor, deference, and brevity; Opus 4.7 toward caution, rigor, depth, and candor [1]. By language, Claude expressed the most warmth in Hindi and the most rigor in Russian, and showed the most deference in Arabic and the most caution in English [1].

## Why it matters

The finding has a practical edge: two users asking Claude to review the same plan, one in Hindi and one in Russian, are statistically likely to get differently calibrated responses — one softer, one blunter — purely as a function of language. Anthropic raises, without resolving, whether this reflects Claude appropriately reading cultural context or a gap in how well the model is aligned and character-trained in languages that have received less investment [1]. The underlying conversation data is from May 2026, so the specific model behaviors described are a snapshot of that period rather than a claim about Anthropic's current lineup.
