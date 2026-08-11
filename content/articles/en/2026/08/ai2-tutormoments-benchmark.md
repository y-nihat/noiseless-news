---
title: Ai2 releases TutorMoments, a benchmark for when AI tutors should scaffold or push students
date: 2026-08-07
slug: ai2-tutormoments-benchmark
lang: en
tldr: >
  The Allen Institute for AI (Ai2) published TutorMoments on 7 August 2026,
  a benchmark testing whether language models know when to scaffold a
  struggling student versus push them toward deeper reasoning, built from
  1,500+ teacher-flagged moments in 462 real US math-tutoring transcripts
  covering grades 2-7. Testing seven models, Ai2 found all of them tend to
  over-help and rarely push for rigor compared to a human-tutor baseline,
  with Gemini 2.5 Pro scoring highest on scaffolding and Claude Opus 4.8
  highest on rigor.
sources:
  - name: Allen Institute for AI (Ai2)
    url: https://allenai.org/blog/tutormoments
claims:
  - text: "Ai2 published TutorMoments on 7 August 2026, an evaluation framework built from 1,500+ teacher-identified key learning moments across 462 de-identified transcripts of real US math-tutoring sessions covering grades 2-7"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Ai2 tested seven models (Gemini 2.5 Pro, Gemini 3.5 Flash, Claude Opus 4.8, Claude Sonnet 4.6, GPT 5.5, GPT 5.4 mini, and DeepSeek V4 Pro) as tutors on 520 of these moments, split evenly between moments calling for scaffolding and moments calling for pushing rigor"
    type: research
    verdict: vendor-claim
    evidence: [1]
  - text: "On appropriate scaffolding (0-1 scale), Gemini 2.5 Pro scored highest at 0.896 with an evaluation-aware prompt and GPT 5.4 mini scored lowest at 0.181 with a plain prompt, against a human-tutor baseline of 0.458; on appropriate rigor, Claude Opus 4.8 scored highest at 0.831 and GPT 5.4 mini lowest at 0.023, against a human baseline of 0.182"
    type: research
    verdict: vendor-claim
    evidence: [1]
  - text: "Ai2's overall finding is that models tend to over-help by giving too much support and rarely push students toward deeper thinking, though explicit prompting about the trade-off improved every model's scores while still leaving a gap versus human tutoring"
    type: research
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## What happened

The Allen Institute for AI (Ai2) published TutorMoments on 7 August 2026, a
benchmark for whether language models can judge when to help a struggling
student and when to hold back and let them work through a problem [1]. It
is built from 1,500-plus moments that experienced math teachers flagged in
462 de-identified transcripts of real US tutoring sessions for students in
grades 2 through 7 [1].

Ai2 ran seven models — Gemini 2.5 Pro, Gemini 3.5 Flash, Claude Opus 4.8,
Claude Sonnet 4.6, GPT 5.5, GPT 5.4 mini and DeepSeek V4 Pro — as tutors
across 520 of these teacher-identified moments, split evenly between cases
calling for more scaffolding and cases calling for pushing the student
toward deeper reasoning [1]. On a 0-1 scaffolding score, Gemini 2.5 Pro
scored highest (0.896, with a prompt that made the trade-off explicit) and
GPT 5.4 mini lowest (0.181, with a plain prompt), against a human-tutor
baseline of 0.458. On the rigor score, Claude Opus 4.8 scored highest
(0.831) and GPT 5.4 mini lowest (0.023), against a human baseline of
0.182 [1]. These figures are Ai2's own reported results, fetched directly
from its 7 August post; no independent outlet has yet reproduced or
reported on them.

Ai2's headline finding: every model tested tends to over-help — giving too
much support rather than pushing students to reason for themselves.
Prompting the models explicitly about the scaffolding-versus-rigor
trade-off raised every model's scores, but a gap versus human tutors'
adaptive judgment remained [1].

## Why it matters

As AI tutoring tools spread in classrooms, this is a concrete, data-backed
signal that today's leading models skew toward being unhelpfully helpful —
propping students up rather than letting them struggle productively, a
trade-off central to how learning works. The results are Ai2's own,
unreplicated by an outside evaluator; the framework itself, releasing real
scored transcripts, gives outside researchers a way to check the numbers.
