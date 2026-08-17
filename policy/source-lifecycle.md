# Source Lifecycle & Discovery

The source registry (`sources.yaml`) is not static. It improves itself through a
feedback loop: agents discover new sources while verifying claims, candidates are
evaluated against fixed criteria, and every source's track record decides whether it
stays, rises, falls, or retires. All changes are commits — the registry's history is
public.

## 1. Statuses

| Status | Meaning |
|---|---|
| `active` | Ingested every run; usable as evidence per its tier |
| `candidate` | Discovered, not yet evaluated. **Not ingested**, not usable as evidence |
| `retired` | Removed from rotation; entry kept with the reason in `notes` |

## 2. Discovery (how candidates appear)

- During verification, agents run keyword web searches (`discovery.yaml`) in addition
  to registered feeds.
- Any unregistered domain that (a) is used as evidence for a claim, or (b) appears in
  search results across ≥3 distinct stories, is appended to
  `data/ledger/source_candidates.json` with: domain, first_seen, occurrence count,
  sample URLs, and the context it appeared in.
- Agents may also directly propose a candidate with a rationale (e.g. a lab launches
  an official blog).

## 3. Evaluation (candidate → active)

A periodic source-review pass (weekly, or when candidates accumulate) evaluates each
candidate against these criteria:

1. **Originality** — does it produce original reporting/research, or aggregate others?
   Aggregators are rejected (we already trace to origins).
2. **Accountability** — named authors, editorial standards, a corrections practice.
3. **Primary-source proximity** — how close is it to the events it covers?
4. **Track record in our own logs** — did its past items survive our falsification pass?

Outcome is a commit: either registration with a tier and a written rationale in
`notes`, or rejection recorded in `data/ledger/source_rejections.json` (so the same
domain is not re-evaluated every cycle).

## 4. Track record and demotion (active → demoted/retired)

- Every ingest run appends one line to `data/ledger/source_stats.jsonl`:
  `{run_at, counts: {source_name: new_items}}`, where `-1` means the fetch failed
  (as distinct from `0`, a healthy feed with nothing new). Written by
  `noiseless.run.write_ingest_stats`.
- A source whose claims are repeatedly falsified (guideline: ≥3 contradicted claims in
  a rolling 90 days) is demoted one tier, or retired if already Tier 3.
- Dead feeds (fail live validation for 14 consecutive days) are flagged for repair or
  retirement. Run the rule:
  `docker compose run --rm pipeline python -m noiseless.run source-status`
  — it reads `source_stats.jsonl`, counts streaks in **days** (the file holds about
  seven runs a day), and exits 2 when a source crosses a threshold. The weekly
  Source health job includes its output in the issue thread.
- **Frozen is not the same as dead.** A feed that still returns HTTP 200 and a full
  entry list, but whose newest entry is months old, contributes exactly as much as one
  returning 403 — and used to be reported as healthy. Live validation now reads the
  newest entry's date and reports `[STALE]` past the source's `max_age_days`
  (default 45). Qwen Blog sat at `[ok] 44 entries` for eleven months this way.
- **Blocked is not the same as dead either.** A publisher that serves a feed to
  ordinary clients but refuses CI address ranges gets `runner_blocked: true` and a note
  saying so. That records the fact once instead of rediscovering it every Monday, and
  keeps the source registered rather than retiring something that is not broken.
- Demotions and retirements are commits with the rationale in `notes` — never silent.

## 5. Keyword pool maintenance

- `discovery.yaml` holds the recurring search queries. Agents append run-specific
  queries (new model names, ongoing story keywords) at run time without editing the file.
- When a topic keeps recurring across runs (e.g. a new model family, a new regulation),
  the agent proposes adding a recurring query; stale queries (zero useful results for
  ~30 days) are proposed for removal. Both are commits.

## 6. Hard rules

- Tier assignment always follows `verification.md` §1; discovery can never place a
  source above Tier 2 — Tier 0/1 registrations require the source to be an official
  or literature venue by its nature.
- YouTube/community sources enter at Tier 3 regardless of channel quality: transcripts
  are leads, never confirmation. Exception: a direct, verbatim interview statement may
  serve as primary evidence *that the person said it* — cited as such, with timestamp.
- The registry never shrinks silently: retired entries stay in the file.
