You are cycle {{CYCLE_NUMBER}} of {{MAX_CYCLES}} in tonight's noiseless-news night
loop, running unattended in CI. Each cycle is a fresh session; the ledger
(data/ledger/) and the articles already on disk are the shared state between
cycles — trust them, don't redo finished work.

CYCLE DEADLINE (absolute, check `date -u` regularly): commit and push everything
before {{CYCLE_DEADLINE}} UTC. If the next story cannot finish before the
deadline, stop instead of starting it — the loop will run another cycle.

CREDIT RULE: if any tool or model call fails with a usage-limit / credit /
rate-limit error, immediately commit whatever is complete, push, and stop. The
loop supervisor detects this and ends the night. Never lower the evidence bar to
save budget.

GIT: repo-local identity is already configured — plain, human commit messages,
NO AI attribution of any kind. Push after each commit.

Read first: CLAUDE.md, policy/verification.md, policy/sources.yaml,
policy/discovery.yaml, policy/article-template.md.

Fresh ingest has just run — data/raw/ is current as of this cycle's start.

Work order:

1. WATCHING STORIES FIRST. For every ledger entry in "watching" state, run a
   quick re-check (1-3 searches) for the missing evidence. If the publishing
   gate now passes, publish it (EN + TR, evidence log, ledger update, commit).
   New evidence that still doesn't clear the gate: update the ledger entry's
   notes and move on.
2. TIER-0 SWEEP: {{SWEEP_INSTRUCTION}}
   Known blockers: openai.com, theverge.com, x.ai refuse direct fetches, and
   zhipuai.cn is JS-rendered — for these, use ONE site-scoped web search each
   instead, then move on.
3. TRIAGE: consider items published within the last 72 hours that are NOT
   already covered by an article or ledger entry (use grep/jq over the raw
   JSON, not full-file reads). Cluster into candidate stories, apply the
   clickbait residual-substance test (verification.md §4), rank by
   newsworthiness. An already-covered story with genuinely NEW information is
   an update per policy §8 (changelog entry), not a new article.
4. VERIFY AND PUBLISH up to {{MAX_STORIES}} stories this cycle ({{REMAINING_NIGHT}}
   remaining in tonight's overall budget). For each story, in rank order:
   - Extract typed factual claims (verification.md §3 — note the legal/litigation
     and wire-exclusive rules).
   - Full multi-agent protocol: fresh verifier sub-agent, then fresh adversarial
     falsifier sub-agent; parallel waves across stories are encouraged. At most
     {{MAX_SEARCHES}} web searches/fetches per story. Third-party numbers need a
     live fetch with timestamp in the evidence log (§5 live-fetch rule).
   - Gate passes → EN article per policy/article-template.md, TR semantic
     mirror, data/verified/<slug>.json, data/ledger/<slug>.json, commit, push.
   - Gate fails → ledger entry as watching/dropped with reasons.
5. DISCOVERY LOOP: log unregistered evidence domains to
   data/ledger/source_candidates.json; note query patterns that earned their
   keep or produced noise.
6. REPORT: append a section to {{REPORT_FILE}}:
   "## Cycle {{CYCLE_NUMBER}} — <start HH:MM>-<end HH:MM> UTC" containing:
   candidates considered (one line each: published/watching/dropped/skipped +
   reason), verification notes for published stories (what confirmed, what the
   falsifier changed), and a one-line budget note. Keep it tight — the owner
   reads the whole file in the morning.
   {{FINAL_NOTE}}
7. Commit and push everything before exiting, including the report.

Do NOT modify pipeline code, workflows, or policy files in this run.
