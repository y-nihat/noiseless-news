# Style Policy — the Editor Gate

Purpose: this site exists to remove attention-competition from news. Clickbait,
empty phrasing, and padding are not style preferences — they are defects that
void the product. Every article, in BOTH languages, must pass this gate as the
final step before its commit. The gate result is recorded as one line per
article in the night report.

## Gate 1 — Headline falsifiability

The headline must state a fact a reader could in principle prove wrong.
"OpenAI releases GPT-5.6" passes. "OpenAI just changed everything" fails.

- No curiosity gaps ("What X did next…", "The surprising reason…").
- No unsupported superlatives: revolutionary, game-changer, groundbreaking,
  stunning, shocking, massive (unless quantified), first-ever (unless verified).
- No rhetorical questions as headlines.
- The headline must be supported by `confirmed` claims only — never by a
  vendor-claim or single-source claim.

## Gate 2 — TL;DR standalone test

Read ONLY the TL;DR. If it fully answers "what happened, and why does it
matter?", it passes. If it teases ("here's what we found…") or requires the
body, it fails.

## Gate 3 — Padding scan

Delete any sentence that adds no new verified fact. Specifically banned:

- Throat-clearing openers: "In a move that…", "In today's fast-paced AI
  landscape…", "It's no secret that…"
- Empty closers: "It remains to be seen…", "Only time will tell…",
  "…in the ever-evolving world of AI."
- Restating the headline or TL;DR in different words.
- Unattributed vibes: "many experts believe", "some say", "observers note".
- Filler transitions that carry no content ("Moreover, it is worth noting that").

Target stays ≈2-minute reads; if the verified claim set is thin, the article
should be SHORT, not padded.

## Gate 4 — Turkish parity

Run gates 1–3 on the Turkish version independently. Turkish must mirror the
English structure and facts but read as natural Turkish — no calque phrasing,
no anglicisms where a Turkish term exists, same absence of padding. A padded
Turkish version of a clean English article is a gate failure.

## Recording

Per article, append to the cycle report: `style-gate: <slug> EN pass / TR pass`
(or what was cut — one line, e.g. "removed 2 filler closers, tightened headline").
