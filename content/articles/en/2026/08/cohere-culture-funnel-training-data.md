---
title: Cohere Labs preprint finds cultural markers largely vanish from LLM training data after pretraining
date: 2026-08-19
published: 2026-08-21
slug: cohere-culture-funnel-training-data
lang: en
tldr: >
  A Cohere Labs preprint analyzing 5.6 million LLM training samples reports
  that explicit cultural signals decline sharply between pretraining and
  post-training, and what remains is geographically skewed toward India,
  China and the US. In fine-tuning experiments, adding cultural markers back
  improved three cultural/bias benchmarks without a reported drop in general
  capability. The finding is described in an arXiv preprint that has not yet
  been peer-reviewed.
sources:
  - name: Cohere Blog
    url: https://cohere.com/blog/the-culture-funnel-you-cant-align-what-isnt-in-the-data
  - name: arXiv cs.AI+cs.LG+cs.CL
    url: https://arxiv.org/abs/2606.13808
claims:
  - text: "Cohere Labs researchers analyzed 5.6 million training samples across pretraining, supervised fine-tuning, alignment and reasoning stages, tagging cultural signals with Cohere's Command A model and manually validating a subset across six languages, and report that explicit cultural signals decline sharply during post-training while the remaining culturally-tagged data is geographically concentrated -- India, China and the USA dominate, with minimal representation from South America and Africa (preprint -- not peer-reviewed)"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "In follow-up fine-tuning experiments, adding explicit cultural markers back into training data improved performance by +8% on NormAd, +6% on BBQ and +2.3% on GMMLU without a reported drop in general-capability scores (preprint -- not peer-reviewed)"
    type: research
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## What happened

A Cohere Labs preprint posted 19 August 2026 argues that large language
models lose most of their explicit cultural context on the way from
pretraining to the finished, post-trained model [1][2]. The team tagged
cultural signals -- domain, task intent, language, geolocation and cultural
characteristics -- across 5.6 million training samples spanning pretraining,
supervised fine-tuning, alignment and reasoning stages, using Cohere's own
Command A model to auto-tag the data and manually validating a subset across
six languages [1][2]. They report that culturally-marked data is
comparatively plentiful during pretraining but shrinks sharply as the
pipeline moves toward post-training, which increasingly prioritizes
technical domains like math and code that carry few cultural signals [1].
Within the culturally-tagged data that does remain, representation follows a
long-tail skew: India, China and the US dominate, while South America and
Africa are barely represented, and adding more languages increases
geographic spread only marginally [1][2].

In a follow-up experiment, the researchers fine-tuned with explicit cultural
markers added back into the training data and report gains on three
third-party cultural and bias benchmarks -- +8% on NormAd, +6% on BBQ and
+2.3% on GMMLU -- without a reported drop in general-capability scores [1][2].
The team also released a 5.6-million-sample tagged dataset publicly. The
work is described in an arXiv preprint (2606.13808, first submitted 11 June
2026) that has not been peer-reviewed or accepted at any venue [2]; no
independent reproduction of the findings currently exists.

## Why it matters

Most efforts to make chatbots culturally aware target the model at
inference time -- prompting or fine-tuning it to "act" culturally informed --
on the assumption the underlying knowledge is already there. This preprint
argues the more basic problem is upstream, in what data survives to the
post-training stage at all. The recovery experiment is a single team's own
preprint result on its own model and task suite, not an independently
reproduced finding, but it offers a concrete lever -- what data goes into
fine-tuning -- rather than only a diagnosis.
