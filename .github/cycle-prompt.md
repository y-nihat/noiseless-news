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

Read first: CLAUDE.md, policy/verification.md (note §0 scope and §0a duplicate
prevention), policy/style.md, policy/sources.yaml, policy/discovery.yaml,
policy/article-template.md.

Fresh ingest has just run — data/raw/ is current as of this cycle's start.
Google News feed items are Tier-3 aggregator leads: `via_outlet` names the
origin outlet; always trace to the origin before any use. Never use domains
from discovery.yaml `blocked_evidence_domains` as evidence.

Work order:

1. WATCHING STORIES: {{WATCHING_INSTRUCTION}}
2. TIER-0 SWEEP: {{SWEEP_INSTRUCTION}}
   Known blockers: openai.com, theverge.com, x.ai refuse direct fetches, and
   zhipuai.cn is JS-rendered — for these, use ONE site-scoped web search each
   instead, then move on.
3. DISCOVERY SWEEP: take `recurring_queries` from policy/discovery.yaml and run
   the 3 queries starting at index ((({{CYCLE_NUMBER}} - 1) * 3) mod list
   length) via WebSearch. New candidates found this way join triage. Log each
   query's hit/miss in the report — this is how the query pool gets tuned.
4. TRIAGE: consider items published within the last 72 hours that are NOT
   already covered by an article or ledger entry (grep/jq over the raw JSON,
   not full-file reads). Cluster into candidate stories, apply the clickbait
   residual-substance test (verification.md §4), check scope (§0), rank by
   newsworthiness.
5. DUPLICATE GATE (mandatory, per §0a — the archive spans ALL dates): for each
   candidate BEFORE opening it:
     PYTHONPATH=pipeline python -m noiseless.run dedup-check \
       --title "<working title>" --url "<primary source url>"
   - Any match: pick one of the three §8 outcomes — (a) same event, new details
     → in-place update with changelog; (b) NEW event in the same saga → follow-up
     article with `follows: <matched-slug>` in frontmatter AND ledger entry;
     (c) unrelated → standalone. Exit 2 (strong match) forbids outcome (c)
     unless you can justify in the report why the match is coincidental.
   - Moderate matches: read the matched article first. Record the dedup result
     and the chosen outcome in the story's evidence log and the report.
6. VERIFY AND PUBLISH up to {{MAX_STORIES}} stories this cycle
   ({{REMAINING_NIGHT}} remaining in tonight's overall budget), in rank order:
   - Extract typed factual claims (verification.md §3 — note legal/litigation
     and wire-exclusive rules).
   - Full multi-agent protocol: fresh verifier sub-agent, then fresh adversarial
     falsifier sub-agent; parallel waves across stories are encouraged. At most
     {{MAX_SEARCHES}} web searches/fetches per story. Third-party numbers need a
     live fetch with timestamp in the evidence log (§5 live-fetch rule).
   - EDITOR GATE (policy/style.md): run all four gates on the English AND
     Turkish versions as the last step before committing; record the one-line
     gate note per article in the report.
   - Gate passes → EN article per policy/article-template.md, TR semantic
     mirror, data/verified/<slug>.json, data/ledger/<slug>.json (include title,
     date, state, and source_urls so the dedup index stays sharp), commit, push.
   - Gate fails → ledger entry as watching/dropped with reasons (also with
     title/date/source_urls).
7. DISCOVERY LOGGING: unregistered evidence domains →
   data/ledger/source_candidates.json; query patterns that earned their keep or
   produced noise → note in report.
8. REPORT: append a section to {{REPORT_FILE}}:
   "## Cycle {{CYCLE_NUMBER}} — <start HH:MM>-<end HH:MM> UTC" containing:
   candidates considered (one line each: published/updated/watching/dropped/
   skipped-duplicate + reason), verification notes for published stories,
   style-gate notes, discovery-sweep query outcomes, and a one-line budget
   note. Keep it tight — the owner reads the whole file in the morning.
   {{FINAL_NOTE}}
9. Commit and push everything before exiting, including the report.

Do NOT modify pipeline code, workflows, or policy files in this run.
