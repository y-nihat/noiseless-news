---
title: Meta's SAM 3 and DINOv3 vision models deployed in DOE's Genesis Mission science initiative
date: 2026-07-21
slug: meta-synaps-genesis-mission
lang: en
tldr: >
  Meta said on 21 July 2026 that its open-source computer-vision models, SAM
  3 and DINOv3, have been fine-tuned and deployed on Department of Energy
  supercomputers to speed up analysis of X-ray and neutron science data, as
  part of SYNAPS-I, a Berkeley Lab-led project under the White House's
  Genesis Mission. The claimed processing speedup and hardware details come
  from Meta's own account and are not yet independently confirmed by DOE or
  the national labs involved.
sources:
  - name: Meta AI Blog
    url: https://ai.meta.com/blog/genesis-mission-lawrence-berkeley-national-laboratory-segment-anything-dino/
  - name: US Department of Energy — Genesis Mission announcement
    url: https://www.energy.gov/articles/energy-department-launches-genesis-mission-transform-american-science-and-innovation
  - name: Lawrence Berkeley National Laboratory — Elements
    url: https://elements.lbl.gov/news/supporting-does-genesis-mission/
claims:
  - text: "The Genesis Mission is a US Department of Energy-led national initiative to accelerate scientific discovery using AI, launched by a White House executive order on 24 November 2025, with DOE Under Secretary for Science Darío Gil as mission director"
    type: announcement
    verdict: confirmed
    evidence: [2]
  - text: "SYNAPS-I is a Berkeley Lab-led multi-laboratory initiative, with partner labs including Argonne, Brookhaven, Oak Ridge and SLAC, aimed at turning X-ray and neutron science data analysis into real-time discovery systems across DOE user facilities"
    type: announcement
    verdict: confirmed
    evidence: [3]
  - text: "Meta says it fine-tuned its SAM 3 and DINOv3 vision models on scientific imaging data and deployed them across 300 A100 GPUs at national supercomputing facilities including NERSC, as part of SYNAPS-I's segmentation pipeline"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Meta says that for one example application — micro-CT scans of grapevine stems used to study drought response — what previously required a month of expert annotation per time step now takes 15 minutes"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Meta's post attributes a supportive quote about SYNAPS-I, given by Darío Gil at the Trillion Parameter Consortium, describing the project's approach of analyzing data as it is produced; the quote addresses SYNAPS-I generally rather than endorsing Meta's specific tools"
    type: statement
    verdict: confirmed
    evidence: [1]
  - text: "Meta says roughly 60 researchers across five national labs are involved in SYNAPS-I, and that DOE's light and neutron source facilities produce data at rates that have grown from one image every six seconds to as many as 100,000 images per second"
    type: research
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

Meta said on 21 July 2026 that its open-source computer-vision models —
SAM 3 (Segment Anything Model 3) and DINOv3 — have been fine-tuned on
scientific imaging data and deployed on Department of Energy
supercomputers, including NERSC, to speed up analysis for SYNAPS-I, a
Lawrence Berkeley National Laboratory-led research initiative [1]. SYNAPS-I
sits under the Genesis Mission, a DOE-led national program to accelerate
scientific discovery with AI that the White House launched by executive
order on 24 November 2025, with DOE Under Secretary for Science Darío Gil
as mission director [2]. SYNAPS-I itself is independently documented by
Berkeley Lab as a multi-laboratory effort with Argonne, Brookhaven, Oak
Ridge and SLAC as partners, working across seven DOE light- and
neutron-source user facilities [3].

The specific role Meta describes for its own models — SAM 3 and DINOv3
fine-tuned and run across 300 A100 GPUs — comes from Meta's post alone;
neither DOE's nor Berkeley Lab's own materials name Meta, SAM, or DINOv3 in
describing SYNAPS-I [1][2][3]. The same is true of Meta's headline
performance claim: for one example, micro-CT scans of grapevine stems used
to study drought response, Meta says analysis that previously took a month
of expert annotation per time step now takes 15 minutes [1] — a
capability claim from Meta's own account, not yet independently verified.
Meta's post also quotes Gil on SYNAPS-I's approach of analyzing data as
it's produced; that quote, given at the Trillion Parameter Consortium,
addresses the SYNAPS-I project generally rather than specifically endorsing
Meta's tools [1]. Meta additionally states that about 60 researchers across
five national labs are involved, and cites DOE facility data-generation
rates rising from one image every six seconds to as many as 100,000 images
per second — figures that also appear only in Meta's own account [1];
Berkeley Lab's public materials confirm the facilities produce data at
petabyte scale without giving Meta's specific annual figure or rate [3].

## Why it matters

Genesis Mission is a significant federal push to embed AI across US
national-lab science, and this is Meta's first detailed public account of
its role in it — but the concrete technical claims (GPU count, the speedup
figure, researcher count) currently rest on Meta's telling alone, with DOE
and Berkeley Lab's own materials confirming the project and its stated
goals without corroborating Meta's specific contribution.
