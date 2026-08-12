---
title: Google DeepMind launches SL2T, an AI model that translates sign language into text, debuting on Pixel 11
date: 2026-08-12
slug: deepmind-sl2t-sign-language-model
lang: en
tldr: >
  Google DeepMind released SL2T, an AI model that translates sign language
  directly into text, debuting in Gboard and Live Transcribe on the Pixel 11,
  starting with American Sign Language to English. DeepMind reports a record
  score on the FLEURS-ASL benchmark, a test it co-created, and says the model
  still struggles with rare signs and some grammatical constructions.
sources:
  - name: Google DeepMind Blog
    url: https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
  - name: Engadget
    url: https://www.engadget.com/2234618/deepmind-newest-model-allows-pixel-11-devices-to-transcribe-sign-language-into-text/
claims:
  - text: "Google DeepMind released SL2T, a sign-language-to-text AI model debuting in Gboard and Live Transcribe on Pixel 11, starting with ASL-to-English"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "SL2T was trained on over 100,000 hours of data across more than 50 sign languages"
    type: statement
    verdict: vendor-claim
    evidence: [1]
  - text: "SL2T achieves a zero-shot score of 70 BLEURT on the FLEURS-ASL benchmark, which DeepMind says is higher than any previously reported score; the benchmark was co-created by a Google-affiliated researcher, so this is not an independently-set record"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "DeepMind states the model still makes errors on rare signs, rapid fingerspelling, passive constructions, classifier depictions, and tense without context, and needs further optimization for left-handed and one-handed signing"
    type: statement
    verdict: confirmed
    evidence: [1]
updated: []
---

## What happened

Google DeepMind released SL2T (sign-language-to-text), an AI model that
translates sign language video directly into written text without an
intermediate gloss step. On-device, the model uses MediaPipe Holistic to
extract body and hand coordinates from camera input, and only that
coordinate sequence — not video — is processed by SL2T [1].

DeepMind says it trained the model on more than 100,000 hours of
sign-language data spanning over 50 sign languages, though the initial
consumer release supports only American Sign Language to English, with more
languages planned [1]. The model debuts in Gboard, as a sign-to-text
dictation input, and in Live Transcribe, letting deaf and hard-of-hearing
users sign replies instead of typing during conversations; both ship first
on the Pixel 11 [1]. Independent tech press (Engadget and others) confirms
the same product details, though nearly all of that coverage traces back to
DeepMind's own announcement rather than separate reporting [1, 2].

DeepMind reports SL2T scores 70 BLEURT zero-shot on the FLEURS-ASL
benchmark, which it describes as higher than any previously reported score.
FLEURS-ASL is a legitimate, peer-reviewed public benchmark built with
reference translations from five Certified Deaf Interpreters, but one of
its co-authors is a Google-affiliated researcher — so this is Google
scoring its own model on a benchmark with Google ties, not an
independently-verified record [1]. DeepMind also states the model still
errs on rare signs, rapid fingerspelling, passive constructions, classifier
depictions, and signs whose meaning depends on tense or context, and needs
further work for left-handed and one-handed signing [1].

## Why it matters

Sign-language translation has long lagged behind spoken-language AI, and
DeepMind is pitching SL2T as the first such model shipped inside a
mainstream consumer product rather than a research demo. Deaf and
hard-of-hearing advocates have previously raised concerns about
sign-to-text AI more broadly — including skepticism documented in
recent surveys and research about accuracy, cultural nuance, and
hearing-dominated development pipelines — concerns this launch has not yet
been tested against by independent, outside evaluation.
