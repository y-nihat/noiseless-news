---
title: Nvidia's Groq 3 LPX inference rack enters full production, Nebius named first launch partner
date: 2026-08-24
slug: nvidia-groq-3-lpx-full-production
lang: en
tldr: >
  Nvidia announced on August 24, 2026 that its Groq 3 LPX inference rack has
  entered full production, with cloud provider Nebius as its first launch
  partner; Nvidia says broader deployment will begin before the end of 2026.
  The rack builds on IP Nvidia licensed and staff it hired from Groq in a deal
  reported at roughly $20 billion in December 2025 — a deal Nvidia said at the
  time was not an acquisition, and Groq has continued operating as an
  independent company. Nvidia's own cited benchmark claims the rack is about
  4x faster than its nearest alternative, a vendor figure not yet
  independently reproduced.
sources:
  - name: Nvidia Newsroom
    url: https://nvidianews.nvidia.com/news/nvidia-groq-3-lpx-now-in-full-production-with-world-class-speed-for-agentic-ai
  - name: CNBC
    url: https://www.cnbc.com/2026/08/24/nvidia-says-groq-racks-will-be-online-this-year-after-20-billion-deal.html
  - name: The Register
    url: https://www.theregister.com/systems/2026/08/24/what-nvidias-first-groq-3-lpu-benchmarks-do-and-dont-tell-us-about-its-20b-gamble/5291880
  - name: CNBC
    url: https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html
  - name: TrendForce
    url: https://www.trendforce.com/news/2025/12/29/news-nvidia-reportedly-denies-usd-20b-groq-acquisition-rumors
claims:
  - text: "Nvidia's Groq 3 LPX inference rack has entered full production, with Nebius as its first cloud launch partner."
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Nvidia says broader deployment of Groq 3 LPX racks, including through Nebius, will begin before the end of 2026."
    type: announcement
    verdict: confirmed
    evidence: [2]
  - text: "Nvidia's relationship with Groq stems from a deal reported in December 2025 at roughly $20 billion; Nvidia said at the time it was licensing Groq's inference IP and hiring key Groq staff -- including founder Jonathan Ross and president Sunny Madra -- rather than acquiring Groq as a company, and Groq has continued to operate independently."
    type: business
    verdict: confirmed
    evidence: [4, 5]
  - text: "Nvidia says the Groq 3 LPX rack delivers about 3,400 output tokens per second at 100K context on Gemma 4 31B, roughly four times faster than the nearest alternative, per an Artificial Analysis benchmark Nvidia cited in its announcement."
    type: capability
    verdict: vendor-claim
    evidence: [1, 3]
updated: []
---

## What happened

Nvidia said on August 24, 2026 that its Groq 3 LPX inference rack has entered full production, naming cloud provider Nebius as its first launch partner; Nebius's own chief technology officer is quoted directly in Nvidia's announcement [1]. Nvidia says broader availability, including through Nebius's Token Factory platform, will follow before the end of 2026 — though Nvidia's release stops short of committing to a firm date for that wider rollout [1][2].

The rack is a product of Nvidia's move into Groq's LPU-style inference chip design. That relationship began with a deal reported in December 2025 at roughly $20 billion, widely described at the time as an acquisition. Nvidia said the deal was in fact a non-exclusive license to Groq's inference IP plus the hiring of key Groq staff, including founder Jonathan Ross and president Sunny Madra — not a purchase of the company itself — and Groq has continued to operate independently since [4][5].

Nvidia cites an Artificial Analysis benchmark showing the Groq 3 LPX delivering about 3,400 output tokens per second at 100K context on Gemma 4 31B, roughly four times faster than the nearest alternative — a vendor-supplied figure, not yet independently reproduced [1]. Independent trade coverage published the same day noted the test used a comparatively small, dense model, and that Nvidia needs 64 or more chips to reach throughput a rival hits with one or two chips on other workloads, with performance on larger models still untested [3].

## Why it matters

Groq's chip architecture was built specifically for fast inference rather than training, a niche Nvidia's GPUs weren't originally designed for. Folding that technology into Nvidia's own product line — while leaving Groq nominally independent — lets Nvidia compete on dedicated inference hardware without a formal acquisition, and gives cloud providers like Nebius another Nvidia-branded option as inference demand grows.
