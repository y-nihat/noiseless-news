---
title: Mistral launches Agentic Search, a multi-step retrieval tool for AI models
date: 2026-08-20
slug: mistral-agentic-search
lang: en
tldr: >
  Mistral AI launched Agentic Search on 20 August 2026, a multi-step retrieval
  capability that gives AI models five tools to search, navigate, read and
  verify information across complex documents, rather than relying on a
  single retrieval pass. Tested with Mistral Medium 3.5 and Z.ai's GLM-5.2,
  Mistral's own benchmarks report accuracy rising from 26.7% to 86% on a
  SEC-filings evaluation and from 6.3% to 51.9% on a Treasury-documents
  evaluation, with lower latency and token use — figures that are Mistral's
  own and have not been independently reproduced.
sources:
  - name: Mistral AI
    url: https://mistral.ai/news/agentic-search/
claims:
  - text: "Mistral launched Agentic Search, a multi-step retrieval capability built into the Mistral Search Toolkit that gives AI models five tools -- search, open, navigate, read and grep -- to find, inspect and verify information across complex documents and data sources"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Agentic Search was tested with Mistral Medium 3.5 and Z.ai's GLM-5.2, and is available now through the Mistral Search Toolkit, built into \"Libraries\" in both Studio and Vibe, with a Search Starter App published on GitHub"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "On Mistral's FinanceBench evaluation (368 SEC filings, 150 questions), Agentic Search raised accuracy from 26.7% to 86%"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "On Mistral's OfficeQA Pro evaluation tested with GLM-5.2 (696 Treasury Bulletins, 133 questions), Agentic Search raised accuracy from 6.3% to 51.9% -- a 45.6-point gain; Mistral separately reports up to a 39.6% reduction in p90 latency and roughly one-third lower token consumption"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

Mistral AI announced Agentic Search on 20 August 2026: a multi-step
retrieval capability, built into the existing Mistral Search Toolkit, that
gives AI models five tools — search, open, navigate, read and grep — to
find, inspect and verify information across complex documents and data
sources, rather than relying on a single retrieval pass [1]. It is
available now through the Mistral Search Toolkit and built into
"Libraries" in both Mistral's Studio and Vibe products, with a Search
Starter App published on GitHub [1]. Mistral tested it with its own
Mistral Medium 3.5 model and with Z.ai's GLM-5.2 [1].

Mistral reports, on its own internal benchmarks, that Agentic Search
raised accuracy on a 150-question evaluation built from 368 SEC filings
("FinanceBench") from 26.7% to 86%, and on a 133-question evaluation built
from 696 Treasury Bulletins ("OfficeQA Pro," tested with GLM-5.2) from
6.3% to 51.9% — a 45.6-point gain. The company also reports up to a 39.6%
reduction in p90 latency and roughly one-third lower token consumption
[1]. These figures are Mistral's own and have not yet been independently
reproduced.

## Why it matters

Agentic Search extends the Search Toolkit — in public preview since 28 May
2026 — from single-pass retrieval toward an agentic loop, aimed at the
kind of long, structured documents (filings, bulletins, contracts) where
standard chunk-based retrieval tends to miss cross-references. The
benchmark gains are large but self-reported and untested against outside
evaluators.
