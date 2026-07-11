---
title: ByteDance Seed releases EdgeBench, reports a new scaling law for AI agents learning from real-world environments
date: 2026-07-02
slug: bytedance-edgebench-scaling-law
lang: en
tldr: >
  ByteDance's Seed team released EdgeBench on 2 July 2026, a benchmark of 134
  real-world tasks that each run for 12+ hours, to measure how AI agents improve
  through extended interaction with an environment after training. Analyzing
  roughly 38,000 hours of agent interaction, the team reports a log-sigmoid
  "scaling law" (R² = 0.998) showing agents' post-deployment learning speed has
  roughly doubled every three months across recent model generations. The
  finding is described in an arXiv preprint that has not yet been peer-reviewed.
sources:
  - name: ByteDance Seed
    url: https://seed.bytedance.com/en/blog/edgebench-measuring-real-world-environment-learning-and-discovering-a-new-scaling-law
  - name: arXiv cs.AI+cs.LG+cs.CL
    url: https://arxiv.org/abs/2607.05155
  - name: South China Morning Post
    url: https://www.scmp.com/tech/big-tech/article/3359373/chinas-bytedance-discovers-new-scaling-law-could-sustain-ai-boom
claims:
  - text: "ByteDance Seed released EdgeBench on 2 July 2026, a benchmark of 134 real-world tasks across six domains (scientific discovery, software engineering, combinatorial optimization, knowledge work, formal mathematics, interactive games), each requiring at least 12 hours of continuous agent operation; 51 of the 134 tasks and the evaluation framework were released publicly, the rest held back to prevent contamination"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Analyzing roughly 38,000 hours of agent interaction (402 learning curves), the team reports that overall agent performance in environment learning follows a log-sigmoid curve against interaction time with a mean R² of 0.998, and that agents' learning speed from environment interaction has roughly doubled every three months across successive model generations (preprint — not peer-reviewed)"
    type: research
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## What happened

ByteDance's Seed research team released EdgeBench on 2 July 2026, a benchmark
built to measure a different thing than most existing tests: not what a model
already knows, but how much an AI agent improves the longer it interacts with
a real-world environment after it has already been trained and deployed [1][2].
The suite comprises 134 tasks spanning scientific discovery, software
engineering, combinatorial optimization, professional knowledge work, formal
mathematics, and interactive games, and each task keeps an agent working
continuously for at least 12 hours, with some running past 72 [1]. The team
publicly released 51 of the 134 tasks along with the full evaluation
framework; the remaining tasks are held back specifically to prevent
benchmark contamination [1][2].

Using the benchmark, the team analyzed about 38,000 hours of agent
interaction across 402 learning curves and reports that performance during
this "environment learning" phase follows a log-sigmoid curve against
interaction time, with a mean fit of R² = 0.998 [1]. From that curve, they
report that agents' learning speed from environment interaction has roughly
doubled every three months across recent model generations [1][2]. The
finding is described in a preprint posted to arXiv (2607.05155) that has not
been peer-reviewed or accepted at any venue [2]. South China Morning Post
independently reported the same figures on 4 July but did not verify them or
report independent reproduction [3].

## Why it matters

AI labs have leaned on scaling training data and compute to improve models,
and researchers including Epoch AI have flagged that public text data could
be exhausted within years. ByteDance's result is being framed as evidence of
a second lever — agents getting measurably better from interacting with real
environments after deployment, independent of retraining — but it currently
rests on one team's own preprint and self-selected task suite, with no
independent reproduction yet. The R² fit describes how well the curve matches
ByteDance's own measurements, not whether the underlying trend will hold as
more model generations and outside labs are tested.
