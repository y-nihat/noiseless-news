---
title: Anthropic says biological-weapons classifiers were disabled for 11 months on contractor traffic, exposing 133 million exchanges
date: 2026-08-14
published: 2026-08-16
slug: anthropic-bio-classifier-logging-gap
lang: en
tldr: >
  Anthropic disclosed in its Risk Report: August 2026 that classifiers meant to
  block biological-weapons content ran disabled for all human-feedback vendor
  traffic from May 2025 to April 2026 -- an eleven-month gap that a mislabeled
  internal flag also hid from logging and review. Roughly 50,000 outside
  contractors generated about 133 million exchanges during that window.
  Anthropic's after-the-fact review found no clearly concerning misuse,
  though it flagged a handful of dual-use conversations, and says no
  customer data was affected.
sources:
  - name: Anthropic
    url: https://www.anthropic.com/aug-2026-risk-report
  - name: The Decoder
    url: https://the-decoder.com/anthropics-bio-weapons-filter-was-down-for-nearly-a-year-exposing-133-million-requests/
  - name: TheNextWeb
    url: https://thenextweb.com/news/anthropic-risk-report-bio-classifiers-human-feedback-gap
claims:
  - text: "Anthropic disclosed in its Risk Report: August 2026, published 14 August 2026, that classifiers meant to block biological-weapons content ran disabled for all human-feedback vendor traffic from May 2025 to April 2026, an eleven-month gap"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "The gap affected roughly 50,000 external contractors, who generated about 133 million exchanges with Anthropic's models during that period; the contractors were vetted only by outside vendors, not by Anthropic itself"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "The cause was a flag meant only for internal use that disabled both the classifiers' blocking behavior and the logging of their flags, so affected traffic was not recorded or propagated to any review mechanism at the time"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Anthropic's after-the-fact review, using Claude Sonnet 5 to re-scan retained transcripts, flagged 1,197 as high biological-harm risk; manual review of the flags not attributable to internal teams or known red-teaming found no clearly concerning misuse capable of providing meaningful uplift to a threat actor, though it identified a handful of potentially dual-use conversations Anthropic described as academic in level"
    type: research
    verdict: vendor-claim
    evidence: [1]
  - text: "Anthropic says no customer data, internal systems or model weights were accessed or exposed; the gap was confined to its human-feedback data-labeling vendor pipeline"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic corrected the issue in April 2026 and retroactively downgraded its own February 2026 risk assessment for this category from 'very low' to 'low'"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## What happened

Anthropic disclosed in its Risk Report: August 2026, published 14 August
2026, that the classifiers meant to block biological-weapons content in
model outputs ran disabled across all of its human-feedback vendor traffic
from May 2025 -- when it first deployed models with these safeguards --
until April 2026 [1][2][3]. The cause was a flag meant only for internal
use that disabled not just the classifiers' blocking behavior but also the
logging of their flags, so traffic that would otherwise have been flagged
was never recorded or sent to any review mechanism [1][2][3].

The gap covered roughly 50,000 external contractors, who between them
generated about 133 million exchanges with Anthropic's models during the
eleven-month window [1][2][3]. These contractors, who evaluate Anthropic's
models as part of human-feedback data collection, were vetted only by
outside vendors -- some of which, Anthropic says, "did not have screening
processes capable of stopping even CB-1 threat actors" [1].

Because the failure also disabled logging, Anthropic had to reconstruct
what happened after the fact from retained raw transcripts. It used Claude
Sonnet 5 to re-scan that traffic and flag conversations carrying high
biological-harm risk, producing 1,197 flagged transcripts. Of those, 757
came from Anthropic's own internal teams using the same infrastructure;
of the remainder, all but 62 were traced to deliberate internal or external
red-teaming exercises. Anthropic manually reviewed those 62 transcripts
plus a 30-transcript sample of the red-teaming flags, and says it "did not
observe clearly concerning CB misuse which could have provided meaningful
uplift to a threat actor," while noting it "identified a handful of
potentially dual-use conversations, or red-teaming interactions at a
fairly academic level" [1]. Anthropic says no customer data, internal
systems or model weights were exposed -- the gap was confined to the
human-feedback vendor pipeline, not its commercial API or other product
surfaces [1].

Anthropic says it corrected the underlying flag in April 2026 and now runs
blocking classifiers on the vast majority of its vendor traffic, with
exceptions only for vendors with controls it judges sufficient for a
specific project [1]. The disclosure is new: Anthropic's previous Risk
Report, published in February 2026, did not treat its human-feedback
platforms as a risk surface at all. In the August report, Anthropic
retroactively revised that February assessment for this risk category
from "very low" to "low" [1].

## Why it matters

This is Anthropic's own accounting of a gap in a safeguard specifically
built to catch attempts at getting AI-assisted help with biological
weapons -- one of the risk categories the company has repeatedly said it
takes most seriously. The eleven-month duration and the fact that the same
bug silenced the monitoring meant to catch problems like this are the
most significant elements: the company did not know about its own gap
until well after the window had closed. Anthropic's self-review is
transparent about its methodology, but it remains a self-assessment --
sampling only part of the flagged traffic and using Anthropic's own model
as the reviewer -- and the company itself says the discovery "reduced our
confidence that no similar gaps exist" elsewhere in its systems.
