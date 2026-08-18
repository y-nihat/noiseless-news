---
title: Zhipu launches GLM-5.3, stages open-weight release two weeks behind for safety review
date: 2026-08-14
published: 2026-08-18
slug: zhipu-glm-5-3-launch
lang: en
tldr: >
  Chinese AI lab Zhipu (Z.ai) launched its GLM-5.3 model on 14 August 2026 via
  its coding plan and API, positioning it for coding and cybersecurity work.
  The model scores 60 on the independent Artificial Analysis Intelligence
  Index, on par with Kimi K3. Zhipu says it is holding back the model's open
  weights, plus some cybersecurity-related features, for about two weeks of
  additional safety testing -- a plan announced at launch, not a delay from an
  earlier promise. Zhipu's own cybersecurity-benchmark claims about the model
  have not yet been independently verified.
sources:
  - name: Zhipu AI (Z.ai)
    url: https://www.zhipuai.cn/zh/research/162
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/models/glm-5-3
claims:
  - text: "Zhipu (Z.ai) released GLM-5.3 on 14 August 2026 via its GLM Coding Plan and API, positioned as 'Built to Code. Ready for Cyber Defense'"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Zhipu is holding back GLM-5.3's open-weight release, and access to some of its more sensitive cybersecurity-related features, for about two weeks after launch to complete additional safety assessment and hardening -- a timeline it announced alongside the launch itself, not a delay from an earlier promised date"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "GLM-5.3 in its maximum-reasoning configuration scores 60 on the Artificial Analysis Intelligence Index, ranking it #8 of 181 tracked models and putting it on par with Kimi K3, below Opus 5 (~63) and Fable 5 (~62)"
    type: capability
    verdict: confirmed
    evidence: [2]
  - text: "Zhipu reports GLM-5.3 leads rival models it compared against on a vulnerability-identification benchmark (CyberGym, 84.5%) but trails well behind on a benchmark measuring completion of full exploit chains (ExploitBench, 54.4%, versus a rival score in the high 70s); these are Zhipu's own self-reported, self-benchmarked figures and have not been independently reproduced"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

Chinese AI lab Zhipu, which operates under the brand Z.ai, launched its
GLM-5.3 model on 14 August 2026 through its coding plan and API, marketing
it as "Built to Code. Ready for Cyber Defense" [1]. Zhipu says it is holding
back the model's open-weight release, along with access to some of its more
sensitive cybersecurity-related capabilities, for roughly two weeks after
launch while it completes additional safety assessment and hardening [1].
That timeline was announced alongside the launch itself, not disclosed
afterward as a delay from an earlier promise.

On the independent Artificial Analysis Intelligence Index, GLM-5.3's
maximum-reasoning configuration scores 60, ranking it eighth of 181 tracked
models -- on par with Kimi K3, and behind Opus 5 (about 63) and Fable 5
(about 62) [2]. Separately, Zhipu reports its own cybersecurity-benchmark
results for the model: GLM-5.3 leads the rival models Zhipu compared it
against on CyberGym, a vulnerability-identification benchmark, scoring
84.5%, but trails well behind on ExploitBench, which measures completing a
full exploit chain rather than just spotting a flaw, scoring 54.4% against
a rival score in the high seventies [1]. Those cybersecurity figures come
entirely from Zhipu's own testing; because the model's weights are not yet
public, no outside lab has been able to reproduce them.

## Why it matters

GLM-5.3 is a live, usable release, not an announcement of something still
to come -- the weights hold is a staged rollout of one component, not a
withheld product. Zhipu frames the two-week gap explicitly as a safety
precaution tied to the model's own vulnerability-discovery capability,
rather than disclosing it only after the fact. Its cybersecurity results are
also more mixed than a single benchmark would suggest: strong at finding
vulnerabilities, weaker at chaining them into a working exploit -- a
distinction worth keeping in view given that every number describing that
capability currently comes from Zhipu itself.
