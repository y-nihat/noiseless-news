---
title: DeepSeek moves V4-Pro out of preview, raises API peak-hour pricing 4.5x
date: 2026-08-13
published: 2026-08-14
slug: deepseek-v4-pro-0813-quiet-update
lang: en
tldr: >
  DeepSeek's V4-Pro model exited API preview and reached general availability
  across its app, web interface and API on 13 August 2026, a release DeepSeek
  frames around agent capabilities. The company is also raising output-token
  API pricing from a flat rate to a peak/off-peak structure roughly 4.5x
  higher at peak hours, effective 16 August. DeepSeek reports large gains on
  its own benchmark suite for the release, but an independent evaluation
  places the model behind current frontier proprietary rivals overall.
sources:
  - name: DeepSeek API (GA release announcement)
    url: https://api-docs.deepseek.com/news/news260813/
  - name: DeepSeek API (updates log)
    url: https://api-docs.deepseek.com/updates
  - name: DeepSeek API (pricing)
    url: https://api-docs.deepseek.com/quick_start/pricing
  - name: Reuters (via TradingView)
    url: https://www.tradingview.com/news/reuters.com,2026:newsml_FWN44A0IU:0-deepseek-says-launching-deepseek-v4-pro-today/
  - name: Nikkei Asia
    url: https://asia.nikkei.com/business/technology/artificial-intelligence/deepseek-releases-official-v4-pro-model-with-sharply-higher-user-prices
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/models/deepseek-v4-pro
  - name: South China Morning Post
    url: https://www.scmp.com/tech/big-tech/article/3363895/deepseeks-updated-v4-pro-ai-model-struggles-benchmarks-shines-cybersecurity
claims:
  - text: "DeepSeek moved V4-Pro out of API preview to general availability across app, web interface and API on 13 August 2026, with the release centered on agent capabilities and new configurable reasoning-effort levels"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 4, 5]
  - text: "DeepSeek is raising V4-Pro API output-token pricing from a flat $0.87 per million tokens to a peak/off-peak structure -- $3.96 per million at peak hours (01:00-04:00 and 06:00-10:00 UTC) and $1.98 per million off-peak -- effective 16:00 UTC on 16 August 2026"
    type: announcement
    verdict: confirmed
    evidence: [3, 4, 5]
  - text: "DeepSeek reports V4-Pro-0813 scoring 87.9 on Terminal-Bench 2.1 (up from 72.1 for the April preview build), 62.7 on DeepSWE, 83.3 on CyberGym, 61.5 on NL2Repo, and 42.7/60.0 on Humanity's Last Exam without/with tools"
    type: capability
    verdict: vendor-claim
    evidence: [2]
  - text: "An independent Artificial Analysis evaluation, live-checked at publication, scores V4-Pro-0813 at 53 on its Intelligence Index, ranking it third among comparable open-weight models but behind current frontier proprietary systems"
    type: capability
    verdict: confirmed
    evidence: [6]
  - text: "South China Morning Post reported that Vals AI's independent evaluation found V4-Pro-0813 notably weaker than rivals on sandboxed-terminal and complex financial-spreadsheet tasks, despite comparatively strong cybersecurity performance"
    type: capability
    verdict: single-source
    evidence: [7]
updated: []
---

## What happened

DeepSeek moved its V4-Pro model out of API preview and into general
availability across its app, web interface ("Expert Mode") and API on 13
August 2026 [1]. DeepSeek frames the release around agent capabilities --
tool use, code execution and multi-step workflows -- and adds three
configurable reasoning-effort levels (low, high, max) for both V4-Pro and
V4-Flash, plus native support for OpenAI's Responses API format [1]. Reuters
and Nikkei Asia both independently reported the launch the same day [4][5].

Alongside the release, DeepSeek is raising API pricing. Output-token pricing
is currently a flat $0.87 per million tokens; from 16:00 UTC on 16 August
2026 it splits into a peak rate of $3.96 per million during defined
high-demand hours (01:00-04:00 and 06:00-10:00 UTC) and an off-peak rate of
$1.98 per million -- half the peak rate -- the rest of the day [3]. The peak
rate is roughly 4.5 times the current flat price.

DeepSeek reports large benchmark gains for the new release: 87.9 on
Terminal-Bench 2.1, up from 72.1 for the April preview build; 62.7 on
DeepSWE; 83.3 on CyberGym; 61.5 on NL2Repo; and 42.7/60.0 on Humanity's Last
Exam without and with tool use [2]. These are DeepSeek's own reported
figures, not independently reproduced. An Artificial Analysis evaluation,
checked at publication, scores V4-Pro-0813 at 53 on its Intelligence Index,
ranking it third among comparable open-weight models but behind current
frontier proprietary systems [6]. South China Morning Post separately
reported that Vals AI's independent evaluation found the model notably
weaker than rivals on sandboxed-terminal tasks and complex
financial-spreadsheet modeling, while noting researchers were more impressed
by its cybersecurity performance [7].

## Why it matters

The launch and pricing change are confirmed directly from DeepSeek and
independently reported by two outlets, but the capability picture is mixed:
DeepSeek's own figures show a large jump over its April preview, while
independent evaluations cited by press coverage put the model behind current
frontier proprietary rivals overall. The roughly 4.5x peak-hour price
increase also narrows DeepSeek's cost advantage, one of the model family's
main selling points, at least during high-demand hours.
