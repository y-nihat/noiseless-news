---
title: OpenAI launches GPT-5.6-Cyber, a more permissive model for authorized offensive-security work
date: 2026-08-10
slug: openai-gpt-5-6-cyber-daybreak-red
lang: en
tldr: >
  OpenAI announced GPT-5.6-Cyber on 10 August 2026, a cybersecurity-specialized
  model built on GPT-5.6 Sol that answers offensive-security requests other
  OpenAI models refuse, available only to vetted "trusted customer partners"
  through a new "Daybreak Red" access tier. OpenAI says the model found a since-
  patched Chrome vulnerability (CVE-2026-15903) and completed 95% of advanced
  security-research requests in its own internal test, against 57.3% for its
  predecessor — figures that have not been independently reproduced. The
  release comes three days after OpenAI said a separate, unreleased model,
  Astra, may have crossed its highest cyber-risk threshold; OpenAI attributes
  the difference to its own two-tier capability classification.
sources:
  - name: OpenAI
    url: https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/10/as-ai-led-attacks-multiply-openai-launches-a-new-cyber-model/
  - name: Axios
    url: https://www.axios.com/2026/08/10/openai-gpt-astra-restrictions-safety-hacking-defenders
  - name: The Decoder
    url: https://the-decoder.com/openai-launches-gpt-5-6-cyber-to-help-defenders-find-vulnerabilities-before-attackers-do/
  - name: NVD (CVE-2026-15903)
    url: https://nvd.nist.gov/vuln/detail/CVE-2026-15903
claims:
  - text: "On 10 August 2026, OpenAI announced GPT-5.6-Cyber, a model built on GPT-5.6 Sol and released through a new 'Daybreak Red' access tier for authorized offensive-security work (vulnerability research, exploit validation, security testing), alongside a 'Daybreak Blue' tier for defensive work"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3, 4]
  - text: "OpenAI says GPT-5.6-Cyber completed 95% of requests in its own internal 'Advanced Cybersecurity Completion Rate' evaluation, versus 57.3% for its predecessor GPT-5.5-Cyber and 1.5-2% for GPT-5.6 Sol under normal safeguards; the metric measures whether the model responds to a sensitive request, not whether the response is correct or effective, and no independent lab has reproduced these figures"
    type: capability
    verdict: vendor-claim
    evidence: [1, 3, 4]
  - text: "A high-severity out-of-bounds read/write vulnerability in Chrome's V8 engine, tracked as CVE-2026-15903, was fixed by Google; OpenAI says GPT-5.6-Cyber found this flaw and a second, chainable one during its testing, but Google has not itself credited OpenAI or the model by name"
    type: capability
    verdict: vendor-claim
    evidence: [1, 4, 5]
  - text: "Access to GPT-5.6-Cyber is currently limited to vetted 'trusted customer partners'; OpenAI's own materials, relayed by press, name partners including Accenture, IBM, CrowdStrike and Cloudflare, but none of those companies has independently confirmed access"
    type: business
    verdict: vendor-claim
    evidence: [1, 2, 3]
  - text: "The release follows OpenAI's 7 August 2026 statement that it could not rule out a separate, unreleased model, Astra, having crossed the 'Critical' cyber-capability threshold in its Preparedness Framework; OpenAI says GPT-5.6-Cyber and GPT-5.6 Sol are both self-classified at the lower 'High' tier, which is why one was paused and the other shipped"
    type: statement
    verdict: vendor-claim
    evidence: [1, 3]
updated: []
---

## What happened

OpenAI announced GPT-5.6-Cyber on 10 August 2026, a cybersecurity-specialized
model built on GPT-5.6 Sol [1]. It is released through a new "Daybreak Red"
access tier of OpenAI's existing Daybreak program, alongside a "Daybreak Blue"
tier for defensive work; Daybreak Red is intended for authorized offensive-
security research — vulnerability discovery, exploit-chain development,
authentication-bypass and privilege-escalation testing — that OpenAI's
general-purpose models refuse to answer [1][2][3][4]. Access is limited to
vetted "trusted customer partners"; OpenAI's own materials, relayed by press
coverage, name partners including Accenture, IBM, CrowdStrike and Cloudflare,
though none of those companies has independently confirmed the relationship
[1][2][3].

OpenAI says the model completed 95% of requests in its own internal "Advanced
Cybersecurity Completion Rate" evaluation, compared with 57.3% for its
predecessor GPT-5.5-Cyber and 1.5-2% for GPT-5.6 Sol operating under normal
safeguards [1][3][4]. That metric measures whether the model responds to a
sensitive request at all, not whether the response is a correct or working
exploit — and no independent lab has reproduced the figures [3][4].

As a real-world example, OpenAI says it used GPT-5.6-Cyber to find a
previously unknown, chainable pair of vulnerabilities in Chrome's V8 engine.
One is tracked as CVE-2026-15903, an out-of-bounds read/write flaw that Google
has since fixed [1][4][5]. The vulnerability and Google's patch are
independently verifiable in the public CVE record; OpenAI's claim that
GPT-5.6-Cyber specifically found it is not independently confirmed — Google
has not credited OpenAI or the model by name [4][5].

The release comes three days after OpenAI said it could not rule out that a
separate, unreleased model, Astra, had crossed the "Critical" cyber-capability
threshold in its Preparedness Framework, and paused unsafeguarded internal use
of it. OpenAI's explanation for shipping a more permissive cyber model days
later is that its framework has two relevant tiers, "High" and "Critical," and
both GPT-5.6 Sol and GPT-5.6-Cyber are self-classified at the lower "High"
tier — only Astra crossed into "Critical" [1][3]. That classification is
OpenAI's own and has not been independently audited.

## Why it matters

OpenAI is now selling deliberately less-restricted access to AI-assisted
offensive security research at the same time it says a different model may
have crossed its own highest cyber-risk line. The company's explanation rests
entirely on its own self-reported capability classification, with no outside
verification of where GPT-5.6-Cyber actually sits — the same limitation that
applies to its 95% benchmark claim and its account of finding the Chrome
vulnerability.
