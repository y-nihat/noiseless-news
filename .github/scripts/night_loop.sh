#!/usr/bin/env bash
# Night-loop supervisor: repeated ingest → agent-cycle → publish rounds across
# the 01:00-05:00 Istanbul window. Fresh agent session per cycle; the ledger is
# the shared state. Ends early on usage-limit errors or the story cap.
set -uo pipefail  # deliberately NOT -e: errors are handled per cycle

log() { echo "[loop $(date -u +%H:%M:%S)] $*"; }

# A pause you can see in the repository, rather than a workflow toggled off in a
# settings page nobody will remember. See RUNBOOK.md.
if [ -f .paused ]; then
  log "'.paused' present at the repo root — publishing is paused, exiting cleanly"
  exit 0
fi

SMOKE="${SMOKE:-false}"
# The cron fires 21:40 UTC, twenty minutes before the window opens, so no
# legitimate hold is longer than this. Enforced here, not asserted in a comment.
MAX_HOLD=1200
HOLD=0
if [ "$SMOKE" = "true" ]; then
  MAX_CYCLES=2; CYCLE_INTERVAL=1500; STORIES_PER_CYCLE=1
  MAX_SEARCHES=3; MAX_TURNS=40; NIGHT_STORY_CAP=2; NIGHT_SECONDS=3300
else
  MAX_CYCLES=6; CYCLE_INTERVAL=2100; STORIES_PER_CYCLE=4
  MAX_SEARCHES=15; MAX_TURNS=120; NIGHT_STORY_CAP=12
  # Window is 22:00 -> 01:20 UTC (01:00-04:20 Istanbul; UTC+3, no DST). Plain
  # epoch arithmetic, deliberately: `date -d "today 22:00"` resolves against the
  # ACTUAL start date, so a cron delivered 3h24m late at 01:04 on 2026-08-07
  # pointed 22 hours forward instead of twenty minutes and slept the job away
  # until the step timeout killed it (run 31136812347). Every branch below
  # yields NIGHT_SECONDS <= 12000 by construction, so no start time can ask for
  # more window than the window has.
  # NIGHT_NOW is a test hook. It is never set in production.
  NOW=${NIGHT_NOW:-$(date -u +%s)}
  DAY=$((NOW - NOW % 86400))                      # 00:00 UTC of the start date
  OPEN=$((DAY + 79200))                           # 22:00 UTC that same date
  if [ "$NOW" -ge "$OPEN" ]; then                 # 22:00-23:59 — start now
    CLOSE=$((OPEN + 12000))
  elif [ $((OPEN - NOW)) -le "$MAX_HOLD" ]; then  # 21:40-21:59 — wait for 22:00
    HOLD=$((OPEN - NOW)); CLOSE=$((OPEN + 12000))
  else                                            # 00:00-21:39 — this run belongs
    CLOSE=$((DAY + 4800))                         # to last night's window (01:20)
  fi
  NIGHT_SECONDS=$((CLOSE - NOW - HOLD))
fi

if [ -n "${NIGHT_PLAN_ONLY:-}" ]; then   # test hook: pytest drives the arithmetic
  echo "hold=$HOLD night_seconds=$NIGHT_SECONDS"; exit 0
fi

if [ "$HOLD" -gt 0 ]; then
  log "holding ${HOLD}s until the 22:00 UTC window opens"
  sleep "$HOLD"
fi

START=$(date -u +%s)
NIGHT_START_ISO=$(date -u -d "@$START" +%FT%H:%M:%SZ)
NIGHT_END=$((START + NIGHT_SECONDS))

# Every scratch file this run owns, in one directory scoped to the run.
#
# They used to be fixed paths under /tmp, which was harmless until content_gate
# started running `pytest` on the live runner: the suite drives this very script
# against scratch repositories, so the tests re-created the supervisor's own
# state files underneath it. Two live consequences, both measured — the suite
# left /tmp/night-issue-filed behind, which stands nightly.yml's failure handler
# down for the rest of the night, and it re-touched the night-start marker,
# which reset the published-articles count and unbound the 12-story cap from
# cycle 2 onwards. nightly.yml sets this variable; a run without it gets a
# per-process directory, so a nested run can never write the outer run's state.
NIGHT_STATE_DIR="${NIGHT_STATE_DIR:-/tmp/night-$$}"
mkdir -p "$NIGHT_STATE_DIR"
ISSUE_FILED="$NIGHT_STATE_DIR/issue-filed"

# The tree outside content/ and data/ as it stood before the agent could touch
# anything. assert_push_scope compares against this rather than against the
# upstream ref: `git push` advances the upstream ref, and the agent has the same
# credential and is told by cycle-prompt.md to push after each commit, so a
# self-pushed supervisor edit moved the goalposts and passed the check that
# exists to catch it.
NIGHT_BASE=$(git rev-parse HEAD)
# Report is named for the Istanbul morning it will be reviewed on, plus the
# run's start time so same-day runs (smoke tests) never collide.
REPORT_FILE="data/ledger/run-report-$(TZ=Europe/Istanbul date +%F)-$(date -u +%H%M)Z.md"
# The report is the morning's primary artifact and it is written with `>>`, so a
# missing directory would lose it without a word.
mkdir -p "$(dirname "$REPORT_FILE")"
ok_cycles=0; ran_cycles=0; usage_stop=0; guard_trips=0; push_failed=0
gate_trips=0; content_gate_ok=1; push_blocked=0; origin_polluted=0
held_now=0; held_slugs=""; suite_ok=1; suite_failures=0; repairs_done=0; cycle_label="pre"
MAX_HELD=3   # the deploy ceiling — the same number deploy.yml and tests.yml pass
NIGHT_STATS="data/ledger/night-stats.jsonl"

git config user.name "y-nihat"
git config user.email "nihat@yinovasyon.com"

# The agent session runs unattended with unrestricted Write/Edit over the whole
# checkout, and it reads thousands of third-party feed items and fetched pages
# every night. Its only legitimate output is content/ and data/. Everything else
# — the supervisor script, the result gate, the cycle prompt, the pipeline, the
# policy documents — is read back and EXECUTED by the next cycle, so a stray
# edit that reached main would run tomorrow with both tokens in scope.
# The prompt already forbids this; the allowlist is what enforces it.
OWNED_PATHS=(content data)

guard_paths() {
  local stray
  stray=$(git status --porcelain -- . ':(exclude)content' ':(exclude)data')
  [ -z "$stray" ] && return 0
  guard_trips=$((guard_trips + 1))
  log "GUARD TRIPPED: changes outside content/ and data/ — refusing to commit them:"
  printf '%s\n' "$stray" | while IFS= read -r line; do log "  $line"; done
  # Unstage before restoring. `git checkout -- <paths>` copies the INDEX into
  # the working tree, so if the agent had already run `git add` the index still
  # held its version: the checkout wrote that version back over the file and
  # left it staged, and the `git commit` two lines below carried it to main.
  # The guard logged the attempt and then committed it anyway — reproduced in a
  # scratch repo on 2026-08-17. Reset the index to HEAD first, then restore the
  # tree from it. Untracked strays are left on the runner and never staged.
  git reset -q -- . ':(exclude)content' ':(exclude)data' 2>/dev/null || true
  git checkout -- . ':(exclude)content' ':(exclude)data' 2>/dev/null || true
}

# guard_paths only sees what this script is about to stage. It cannot see a
# commit the agent made on its own — and .github/cycle-prompt.md tells the agent
# to commit and push its own work, which is how 44 "Publish: …" commits reached
# main without passing through commit_push at all. This is the check that covers
# those: whoever wrote it, nothing outside the allowlist may be pushed.
#
# A stray here is not untidiness. It is the supervisor, the result gate, the
# pipeline or the policy being rewritten by a session that spent the night
# reading untrusted third-party text, and main is executed the next night with
# both tokens in scope. One night's articles are worth less than that, so this
# refuses the push and lets the job fail.
assert_push_scope() {
  local target=${1:-HEAD} label=${2:-the commits waiting to be pushed} strays
  if [ -z "${NIGHT_BASE:-}" ]; then
    # Fail closed: with nothing to compare against, "no strays found" is an
    # empty answer dressed up as an all-clear.
    log "GUARD: no night baseline to compare against — refusing to push"
    return 1
  fi
  # Trees, not a commit range. A commit range anchored on the upstream ref is
  # exactly what the agent's own `git push` defeats, and it also disappears the
  # evidence after a rebase. Comparing the tree at the night's baseline against
  # the tree now answers the only question that matters: is anything outside
  # content/ and data/ different from what the operator last reviewed?
  strays=$(git diff --name-only "$NIGHT_BASE" "$target" -- . ':(exclude)content' ':(exclude)data')
  [ -z "$strays" ] && return 0
  guard_trips=$((guard_trips + 1))
  log "GUARD: $label touch paths outside content/ and data/:"
  printf '%s\n' "$strays" | while IFS= read -r line; do log "  $line"; done
  # A legitimate cause exists and is rare: an operator merging to main inside
  # the 22:00-01:20 UTC window, pulled in by commit_push's rebase. One such
  # merge has happened in the repository's history. Failing loudly on it is the
  # right trade for a control whose other case is a supervisor rewritten by a
  # session that spent the night reading untrusted third-party text.
  return 1
}

# The archive's only automated check, moved to where it can still stop
# something.
#
# tests.yml triggers `on: push`, but every push below authenticates with the
# workflow's own GITHUB_TOKEN and GitHub raises no workflow event for such a
# push. So the gate PR #27 added — "test the nightly agent's commits like
# everything else" — ran on none of the 192 commits the agent made between
# 2026-08-07 and 2026-08-17, and 34 articles reached the public site unchecked.
#
# One predicate, three outcomes — the same command deploy.yml and tests.yml run,
# with the same ceiling, so the three gates cannot disagree:
#   clean   — nothing held; deploy as normal.
#   held    — up to MAX_HELD stories carry a per-story defect (no evidence log,
#             broken parity, …). publish.py holds exactly those from the site at
#             build time, so the deploy PROCEEDS without them and the defect is
#             queued for the next cycle's agent to repair. This is the case the
#             night of 2026-08-18 needed: two articles without their evidence
#             logs cost the whole night's seven stories their deploy, and four
#             later cycles ran without ever being told what to fix.
#   blocked — more than MAX_HELD held, or the validator itself failed to run.
#             Fail closed: deploy withheld, red at dawn if still blocked.
# A trip never blocks the commit or the push: the night's work must reach
# origin, and the repository is the audit trail whether the night went well or
# badly. It blocks the *deploy*, which is the only moment at which a bad
# article is still unpublished.
content_gate() {
  local out="$NIGHT_STATE_DIR/gate-content.txt" json="$NIGHT_STATE_DIR/findings.json"
  rm -f "$json"
  PYTHONPATH=pipeline python -m noiseless.run validate-content --strict \
    --max-held "$MAX_HELD" --json "$json" >"$out" 2>&1
  local rc=$?
  # Log every finding either way, but keep the annotation lines out of the
  # cycle log — they are for GitHub, printed once at the end of the night.
  grep -v '^::' "$out" | while IFS= read -r line; do log "content: $line"; done

  if [ "$rc" -eq 0 ] && [ -s "$json" ]; then
    # Read the held set back with the same interpreter that wrote it, and treat
    # an unreadable file as "held = unknown", which is blocked, not clean.
    local summary
    summary=$(PYTHONPATH=pipeline python - "$json" <<'PYEOF'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    held = d.get("held")
    if not isinstance(held, dict):
        raise ValueError("no held map")
    print(len(held), ",".join(sorted(held)) or "-")
except Exception:
    print("? -")
PYEOF
)
    read -r held_now held_slugs <<<"$summary"
    [ "$held_slugs" = "-" ] && held_slugs=""
    # Anything that is not a number is "held = unknown", which is blocked. The
    # guard used to test for the literal `?` this reader prints when it catches
    # an exception, and so missed the case where the reader printed nothing at
    # all: $held_now was empty, `[ "" -gt 0 ]` below errored to stderr, and the
    # function fell through to content_gate_ok=1 — a fail-open, and the exact
    # opposite of the comment above it. Seen for real in CI run #62, whose
    # STATE line read `gate_ok=1 held=`.
    case "${held_now:-}" in
      '' | *[!0-9]*)
        gate_trips=$((gate_trips + 1)); content_gate_ok=0; held_now=0
        log "GATE BLOCKED — the findings file could not be read; refusing to guess"
        return 1
        ;;
    esac
    if [ "$held_now" -gt 0 ]; then
      log "GATE: $held_now held from the site — ${held_slugs//,/, } — deploy proceeds without them; repair queued for the next cycle"
      # First-seen bookkeeping for the footer's lifecycle line.
      for slug in ${held_slugs//,/ }; do
        grep -q "^$slug	" "$NIGHT_STATE_DIR/held.tsv" 2>/dev/null \
          || printf '%s\t%s\n' "$slug" "${cycle_label:-pre}" >> "$NIGHT_STATE_DIR/held.tsv"
      done
    fi
    [ "$content_gate_ok" -eq 0 ] && log "GATE: within the ceiling again — deploys resume"
    content_gate_ok=1
    return 0
  fi

  gate_trips=$((gate_trips + 1))
  content_gate_ok=0
  if [ "$rc" -eq 2 ]; then
    log "GATE BLOCKED — more than $MAX_HELD stories held: holding every deploy until a later cycle comes back within the ceiling"
  else
    log "GATE BLOCKED — validate-content itself failed (exit $rc): a build that cannot tell what is safe to publish must not publish"
  fi
  return 1
}

# The unit tests, reported and never a deploy predicate. deploy.yml already
# made that call — "a flaky unit test has no business freezing the public
# site" — and the agent may not touch pipeline code, so a red suite at 01:00 is
# something for the operator, not a reason to hold the site. It was inside the
# gate until 2026-08-19, which made the night stricter than the deploy it was
# withholding.
suite_check() {
  if pytest -q >"$NIGHT_STATE_DIR/gate-pytest.txt" 2>&1; then
    suite_ok=1
    return 0
  fi
  suite_ok=0
  suite_failures=$((suite_failures + 1))
  log "TESTS: pytest FAILED (reported only — never a deploy predicate)"
  grep -E '^(FAILED|ERROR) ' "$NIGHT_STATE_DIR/gate-pytest.txt" | head -n 10 \
    | while IFS= read -r line; do log "  $line"; done
  return 1
}

# `suite_check` has written the suite's failures to gate-pytest.txt since
# 2026-08-19 and nothing ever read the file again. So on every night from
# 2026-08-20 the repair queue printed "REPAIR QUEUE: empty — the archive is
# clean" in the same container where pytest was failing on two published
# articles, and eight consecutive nights of self-repair never saw it.
#
# The archive tests' subject is content/ and data/ledger/ — the agent's own
# OWNED_PATHS — so a failure there is precisely the class of thing it can fix.
# Advisory, never a gate: a red suite is not a deploy predicate here (deploy.yml
# made that call first), it does not decide whether a cycle runs, and pipeline
# code is not the agent's to touch.
append_suite_repairs() {
  local brief=$1 pytest_out="$NIGHT_STATE_DIR/gate-pytest.txt" failures
  [ -s "$pytest_out" ] || return 0
  failures=$(grep -E '^(FAILED|ERROR) ' "$pytest_out" | head -n 10)
  [ -n "$failures" ] || return 0
  {
    echo
    echo "## Unit suite — advisory, from the previous cycle"
    echo
    echo '```'
    echo "$failures"
    echo '```'
    echo
    echo "A failure naming content/ or data/ is yours to repair in this cycle,"
    echo "the same way a held story is: fix the archive, not the test. A failure"
    echo "in pipeline/ is the operator's — leave it alone, it is already filed."
  } >> "$brief"
}

commit_push() {
  guard_paths
  git add "${OWNED_PATHS[@]}"
  git diff --cached --quiet || git commit -m "$1"
  content_gate || true
  suite_check || true
  if ! assert_push_scope; then
    push_blocked=1
    log "PUSH BLOCKED by the path allowlist — nothing sent to origin"
    return 1
  fi
  if git push; then
    return 0
  fi
  log "push rejected — pulling and retrying once"
  git pull --rebase || log "rebase failed (likely a conflict left in the tree)"
  if git push; then
    return 0
  fi
  # A night whose work never reached origin is the worst outcome the loop can
  # produce and the one the operator is least likely to notice: the runner is
  # destroyed at the end of the job, and the footer's article counts come from
  # the LOCAL branch, so they would still read "New articles: N". Record it and
  # fail the job at the end.
  push_failed=1
  log "PUSH FAILED — work is committed locally but has NOT reached origin"
}

# Test hook: pytest sources this file to drive the functions above against a
# scratch repository with a local bare remote, so the guard and the gate are
# asserted by behaviour rather than by grepping for their own source code. The
# only test that ever covered the path allowlist asserted that the string
# "guard_paths" appeared in the script. Never set in production.
if [ -n "${NIGHT_SOURCE_ONLY:-}" ]; then return 0 2>/dev/null || exit 0; fi

# Feed capture is deterministic, free, and takes about three minutes. A missed
# ingest is the only permanent loss a bad night causes — Techmeme and
# r/LocalLLaMA roll their windows over within hours and nothing ever re-fetches
# them — so this runs unconditionally, before the window is even consulted. A
# night with no runway left still captures the day's feeds.
log "pre-cycle ingest"
PYTHONPATH=pipeline python -m noiseless.run ingest || log "ingest reported failures (continuing)"
commit_push "Night ingest $(date -u +%FT%H:%MZ)"

for cycle in $(seq 1 "$MAX_CYCLES"); do
  NOW=$(date -u +%s)
  if [ $((NIGHT_END - NOW)) -lt 600 ]; then
    log "under 10 minutes left in the window — not starting cycle $cycle"
    break
  fi

  # Cycle 1 uses the pre-cycle capture above; re-ingesting would cost it three
  # minutes of its own agent slot for nothing.
  if [ "$cycle" -gt 1 ]; then
    log "cycle $cycle: ingest"
    PYTHONPATH=pipeline python -m noiseless.run ingest || log "ingest reported failures (continuing)"
    commit_push "Night ingest $(date -u +%FT%H:%MZ)"
  fi

  # `-newermt "@$START"` rather than a marker file: the marker was a fixed path
  # under /tmp, and content_gate's `pytest` run re-created it, which reset this
  # count to zero from cycle 2 onwards and quietly unbound the night story cap.
  published=$(find content/articles/en -name '*.md' -newermt "@$START" | wc -l)
  remaining=$((NIGHT_STORY_CAP - published)); [ "$remaining" -lt 0 ] && remaining=0
  stories=$STORIES_PER_CYCLE; [ "$stories" -gt "$remaining" ] && stories=$remaining

  SLOT_END=$((NOW + CYCLE_INTERVAL)); [ "$SLOT_END" -gt "$NIGHT_END" ] && SLOT_END=$NIGHT_END
  is_final=0
  final_note="This is NOT the final cycle; leave night-wide summaries for a later cycle."
  if [ "$cycle" -eq "$MAX_CYCLES" ] || [ $((NIGHT_END - SLOT_END)) -lt 900 ]; then
    is_final=1
    final_note="THIS IS THE FINAL CYCLE of the night: after your cycle section, append '## Night summary' (stories published tonight across all cycles, coverage gaps) and '## For the owner' (3-5 concrete tuning questions)."
  fi
  if [ "$cycle" -eq 1 ]; then
    sweep="full sweep — WebFetch every active Tier-0 source of type html in sources.yaml."
  else
    sweep="light sweep — re-fetch only Tier-0 html sources that had fresh content earlier tonight or that a candidate story points to."
  fi
  if [ "$cycle" -eq 1 ] || [ "$is_final" -eq 1 ]; then
    watching="re-check EVERY ledger entry in watching state (1-3 searches each) for its missing evidence; publish if the gate now passes, else update the entry's notes. ALSO re-check every PUBLISHED ledger entry whose open_obligation is true and whose revisit_after date has passed (or is absent) — a covered case with a pending outcome is an obligation under verification.md 3, not a finished story."
  else
    watching="only re-check a watching-state ledger entry if this cycle's fresh ingest or sweep mentions it — otherwise leave watching stories alone (they were checked in cycle 1 and will be re-checked in the final cycle)."
  fi

  # The repair queue: what the archive says is held right now, rendered as the
  # cycle's step 0. Recomputed from the tree at every cycle start, so it needs
  # no state file and carries across nights. This is the loop the night of
  # 2026-08-18 lacked — the gate tripped in cycle 2 and cycles 3-6 each ran a
  # fresh session that was never told what to fix.
  PYTHONPATH=pipeline python -m noiseless.run validate-content --brief \
    > "$NIGHT_STATE_DIR/repair-$cycle.md" 2>/dev/null
  repairs_pending=$(( $? == 2 ? 1 : 0 ))
  [ -s "$NIGHT_STATE_DIR/repair-$cycle.md" ] \
    || echo "REPAIR QUEUE: could not be computed — run validate-content --strict before your first commit." \
       > "$NIGHT_STATE_DIR/repair-$cycle.md"
  # Deliberately after `repairs_pending` is set, so a red suite never decides
  # whether a cycle runs — only what it is told once it does.
  append_suite_repairs "$NIGHT_STATE_DIR/repair-$cycle.md"

  if [ "$stories" -eq 0 ] && [ "$is_final" -eq 0 ] && [ "$repairs_pending" -eq 0 ]; then
    log "night story cap reached — skipping agent cycle $cycle"
    sleep_secs=$((SLOT_END - $(date -u +%s)))
    [ "$sleep_secs" -gt 0 ] && sleep "$sleep_secs"
    continue
  fi
  [ "$repairs_pending" -eq 1 ] && log "cycle $cycle: repair queue is non-empty — the agent runs even at the story cap"

  CYCLE_DEADLINE=$(date -u -d "@$((SLOT_END - 120))" +%H:%M)
  sed -e "s/{{CYCLE_NUMBER}}/$cycle/g" \
      -e "s/{{MAX_CYCLES}}/$MAX_CYCLES/g" \
      -e "s/{{CYCLE_DEADLINE}}/$CYCLE_DEADLINE/g" \
      -e "s/{{MAX_STORIES}}/$stories/g" \
      -e "s/{{REMAINING_NIGHT}}/$remaining/g" \
      -e "s/{{MAX_SEARCHES}}/$MAX_SEARCHES/g" \
      -e "s|{{REPORT_FILE}}|$REPORT_FILE|g" \
      -e "s|{{SWEEP_INSTRUCTION}}|$sweep|g" \
      -e "s|{{WATCHING_INSTRUCTION}}|$watching|g" \
      -e "s|{{FINAL_NOTE}}|$final_note|g" \
      -e "/{{REPAIR_INSTRUCTION}}/{
r $NIGHT_STATE_DIR/repair-$cycle.md
d
}" \
      .github/cycle-prompt.md > "$NIGHT_STATE_DIR/prompt-$cycle.md"
  if grep -q '{{' "$NIGHT_STATE_DIR/prompt-$cycle.md"; then
    log "ERROR: unrendered placeholder in cycle prompt"; grep -o '{{[A-Z_]*}}' "$NIGHT_STATE_DIR/prompt-$cycle.md" | sort -u
    exit 1
  fi

  CYCLE_TIMEOUT=$((SLOT_END - $(date -u +%s) - 60))
  [ "$CYCLE_TIMEOUT" -lt 300 ] && CYCLE_TIMEOUT=300
  log "cycle $cycle: agent starting (deadline $CYCLE_DEADLINE UTC, stories<=$stories, timeout ${CYCLE_TIMEOUT}s)"
  ran_cycles=$((ran_cycles + 1))
  cycle_label="c$cycle"

  # CLAUDE.md and policy/verification.md §5 both require max effort for the
  # verification agents. Neither had ever been passed it: `git log -S"--effort"`
  # returns no commit in the repository's history, so every night since the
  # first ran at the CLI default while two documents said otherwise.
  # The agent's own `git commit` runs .github/hooks/pre-commit, which refuses
  # an article whose evidence log, ledger entry or Turkish twin is not in the
  # index and prints the missing file and the fix into the agent's Bash
  # output. That is the structural prevention: the article that started the
  # night of 2026-08-18 could not have been committed. It is scoped to the
  # agent's PROCESS through git's documented GIT_CONFIG_COUNT/KEY/VALUE runtime
  # config, so the supervisor's own commit_push is never refused — its sweep
  # commit must land, since the runner is destroyed at the end of the job and
  # the repository is the audit trail. The bypasses are closed on the agent's
  # Bash: `--no-verify`, and re-pointing or unsetting core.hooksPath.
  GIT_CONFIG_COUNT=1 \
  GIT_CONFIG_KEY_0=core.hooksPath \
  GIT_CONFIG_VALUE_0="$PWD/.github/hooks" \
  timeout "$CYCLE_TIMEOUT" claude -p "$(cat "$NIGHT_STATE_DIR/prompt-$cycle.md")" \
    --model claude-sonnet-5 \
    --effort max \
    --max-turns "$MAX_TURNS" \
    --allowedTools "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch" \
    --disallowedTools "Bash(*--no-verify*),Bash(*hooksPath*),Bash(*GIT_CONFIG_*)" \
    --output-format stream-json --verbose \
    | tee "$NIGHT_STATE_DIR/claude-stream-$cycle.jsonl" \
    | python3 .github/scripts/stream_summary.py
  claude_exit=${PIPESTATUS[0]}

  python3 .github/scripts/check_result.py "$NIGHT_STATE_DIR/claude-stream-$cycle.jsonl" \
    --stats-file "$NIGHT_STATS" --night "$NIGHT_START_ISO" --cycle "$cycle"
  gate=$?
  log "cycle $cycle: claude_exit=$claude_exit gate=$gate"

  # The content check used to live here, non-strict, with its exit code
  # discarded. It now runs inside commit_push as `content_gate`, strict, where
  # tripping it holds the deploy back.
  commit_push "Night cycle $cycle artifacts $(date -u +%FT%H:%MZ)"

  # Per-cycle site deploy so articles appear through the night (best effort).
  # Not on the cycle we are about to break out of: nightly.yml's `if: always()`
  # backstop deploy runs a few seconds after this script exits, with
  # byte-identical content, and GitHub Pages allows one deployment in flight —
  # whichever create call arrives second gets HTTP 400 (2026-08-04, run
  # 30867516175). Every non-final dispatch is followed by the slot sleep below,
  # so it is at least fifteen minutes clear of the backstop.
  if [ "$is_final" -eq 0 ] && [ "$gate" -ne 3 ] && [ "$content_gate_ok" -eq 1 ]; then
    gh workflow run "Deploy site" --ref main 2>/dev/null \
      && log "site deploy dispatched" || log "deploy dispatch failed (non-fatal)"
  elif [ "$content_gate_ok" -eq 0 ]; then
    log "content gate BLOCKED — deploy withheld, the site stays on the last deployable build"
  else
    log "last cycle — leaving the deploy to the workflow's backstop step"
  fi

  if [ "$gate" -eq 3 ]; then
    usage_stop=1
    log "usage limit reached — ending the night"
    break
  fi
  [ "$gate" -eq 0 ] && ok_cycles=$((ok_cycles + 1))
  [ "$is_final" -eq 1 ] && break

  NOW=$(date -u +%s); sleep_secs=$((SLOT_END - NOW))
  if [ "$sleep_secs" -gt 0 ]; then
    log "sleeping ${sleep_secs}s until the next cycle slot"
    sleep "$sleep_secs"
  fi
done

new_articles=$(git log --since="$NIGHT_START_ISO" --diff-filter=A --name-only --pretty=format: -- 'content/articles/en/*' | grep -c '\.md$' || true)
repairs_done=$(git log --since="$NIGHT_START_ISO" --format=%s | grep -c '^Repair: ' || true)
updated_articles=$(git log --since="$NIGHT_START_ISO" --diff-filter=M --name-only --pretty=format: -- 'content/articles/en/*' | grep -c '\.md$' || true)
published_total=$new_articles
# Sum tonight's per-cycle costs. check_result.py writes one record per cycle;
# older nights have no records, so an empty result is reported as "unknown"
# rather than a misleading 0.
night_cost=$(python3 - "$NIGHT_STATS" "$NIGHT_START_ISO" <<'PY' 2>/dev/null || echo unknown
import json, sys
path, night = sys.argv[1], sys.argv[2]
total, seen = 0.0, False
try:
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("night") == night and isinstance(rec.get("cost_usd"), (int, float)):
                total += rec["cost_usd"]
                seen = True
except FileNotFoundError:
    pass
print(f"{total:.2f}" if seen else "unknown")
PY
)
{
  echo ""
  echo "## Loop supervisor footer"
  echo ""
  # "Cycles run: 5 … max: 6" read as though a sixth had been possible. A sixth
  # needs the window to have opened by 22:10 UTC and it opened later than that
  # on 31 of 36 nights, so the shortfall is the cron's arrival time, not the
  # loop giving up. Say which.
  echo "- Cycles run: $ran_cycles of $MAX_CYCLES (successful: $ok_cycles)$(
    [ "$ran_cycles" -lt "$MAX_CYCLES" ] \
      && echo " — the ${NIGHT_SECONDS}s of window left at start did not fit the rest" \
      || echo "")"
  echo "- Agent: claude-sonnet-5, effort max, max-turns $MAX_TURNS, searches/story $MAX_SEARCHES"
  echo "- New articles: $new_articles · updated articles: $updated_articles (night cap: $NIGHT_STORY_CAP new)"
  echo "- Usage-limit stop: $([ "$usage_stop" -eq 1 ] && echo yes || echo no)"
  echo "- Out-of-scope write attempts blocked: $guard_trips$([ "$origin_polluted" -eq 1 ] && echo " · ORIGIN CARRIES A STRAY" || echo "")"
  echo "- Content gate: $([ "$content_gate_ok" -eq 1 ] && echo pass || echo "BLOCKED — the archive is not deployable")"
  # The hold has a lifecycle worth seeing in one line: what is held, since
  # which cycle. Values come from the LAST gate run before this footer, so the
  # count cannot disagree with itself the way a running trip tally did.
  if [ "$held_now" -gt 0 ]; then
    held_line=""
    for slug in ${held_slugs//,/ }; do
      since=$(awk -F'\t' -v s="$slug" '$1==s{print $2; exit}' "$NIGHT_STATE_DIR/held.tsv" 2>/dev/null)
      held_line="$held_line$slug (held since ${since:-before tonight}) · "
    done
    echo "- Held from the site at dawn: $held_now — ${held_line% · } — everything else the night produced is live; tonight's cycle 1 repairs or withdraws"
  else
    echo "- Held from the site at dawn: none"
  fi
  echo "- Repairs completed tonight: $repairs_done"
  echo "- Unit tests: $([ "$suite_ok" -eq 1 ] && echo pass || echo "FAILED — reported only, never a deploy predicate")"
  echo "- Push to origin: $([ "$push_blocked" -eq 1 ] && echo "BLOCKED (path allowlist)" || { [ "$push_failed" -eq 1 ] && echo FAILED || echo ok; })"
  echo "- Night cost (USD): $night_cost"
  echo "- Window: $NIGHT_START_ISO → $(date -u +%FT%H:%MZ)"
} >> "$REPORT_FILE"
commit_push "Night loop footer $(date -u +%F)"

# One set of GitHub annotations for the run page, from the final gate state.
if [ -s "$NIGHT_STATE_DIR/gate-content.txt" ]; then
  grep '^::' "$NIGHT_STATE_DIR/gate-content.txt" || true
fi
[ "$suite_ok" -eq 0 ] && echo "::warning title=unit tests::pytest failed on the runner during the night — reported only, see the job log"

# tests.yml cannot see a single one of tonight's commits — a push made with the
# workflow's own GITHUB_TOKEN raises no workflow event, which is why `Deploy
# site` has to be dispatched by hand too. content_gate has already run the same
# checks locally; this is what puts the result on main where the operator looks.
gh workflow run "Tests" --ref main 2>/dev/null \
  && log "Tests dispatched against main" || log "Tests dispatch failed (non-fatal)"

# Last look. assert_push_scope can only refuse the NEXT push, so it cannot undo
# a stray the agent pushed itself before commit_push ever ran. The only way to
# know what is on the branch tomorrow's runner will clone is to ask origin.
if git fetch -q origin main 2>/dev/null; then
  if ! assert_push_scope FETCH_HEAD "commits that have already reached origin/main"; then
    origin_polluted=1
    log "GUARD: a stray is on origin/main — repair the branch before the next night runs it"
  fi
else
  log "GUARD: could not reach origin to check what landed (not treated as a pass)"
  origin_polluted=1
fi

# nightly.yml's backstop deploy reads this. The backstop exists to publish
# whatever the script left behind, which must not include the one thing the
# script decided should not be published.
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "content_gate=$([ "$content_gate_ok" -eq 1 ] && echo ok || echo failed)" >> "$GITHUB_OUTPUT"
fi

{
  echo "### Night loop"
  echo ""
  echo "cycles=$ran_cycles ok=$ok_cycles new=$new_articles updated=$updated_articles"
  echo "usage_stop=$usage_stop push_failed=$push_failed guard_trips=$guard_trips cost_usd=$night_cost"
} >> "${GITHUB_STEP_SUMMARY:-/dev/null}"

# Warning tier. A green check has meant three different things — "worked, quiet
# news night", "worked, but something upstream is broken" and "flailed for three
# hours" — and the operator could only tell them apart by reading a 40 KB report.
# These conditions do not fail the job; they raise a hand.
# Three different mornings, which the old reporting blurred into two issues ten
# seconds apart that contradicted each other — "Night review needed", whose
# first line read "The job itself did not fail", and "Nightly run failed",
# whose entire body was "no agent output captured" because it tailed a stream
# file no cycle had written (#28 and #29, both 2026-08-07).
#
#   no runway  — the window had already closed when the job started, so nothing
#                was attempted and nothing failed. A SCHEDULED run reaching this
#                means GitHub delivered the cron too late to be usable, which is
#                a lost night and should be red. An operator dispatching outside
#                the window already knows; that is documented behaviour and has
#                no business opening an issue or failing a job.
#   ran badly  — cycles started and none finished cleanly. A failure.
#   ran fine   — with or without things worth a look in the morning.
no_runway=0
[ "$ran_cycles" -eq 0 ] && no_runway=1
scheduled=0
[ "${EVENT_NAME:-schedule}" = "schedule" ] && scheduled=1

warnings=()
[ "$((new_articles + updated_articles))" -eq 0 ] && [ "$no_runway" -eq 0 ] \
  && warnings+=("published nothing tonight")
[ "$no_runway" -eq 1 ] && [ "$scheduled" -eq 1 ] \
  && warnings+=("the cron arrived with only ${NIGHT_SECONDS}s of the 22:00-01:20 UTC window left, so no cycle could start — the night is lost, not broken")
[ "$ok_cycles" -lt "$ran_cycles" ] && warnings+=("$((ran_cycles - ok_cycles)) of $ran_cycles cycles did not complete cleanly")
# Only a badly truncated night, not the routine 5-of-6: a sixth cycle needs the
# window open by 22:10 UTC and it rarely is, and the sixth slot has produced no
# article on any night it ran. The footer records the shortfall either way.
[ "$ran_cycles" -gt 0 ] && [ $((ran_cycles * 2)) -lt "$MAX_CYCLES" ] \
  && warnings+=("only $ran_cycles of $MAX_CYCLES cycles fitted in the window")
[ "$guard_trips" -gt 0 ] && warnings+=("$guard_trips out-of-scope write attempt(s) blocked")
[ "$push_blocked" -eq 1 ] && warnings+=("the path allowlist refused to push — a commit touches files outside content/ and data/")
# The only job_failed condition that used to raise no warning of its own, so a
# night that published and then lost its push depended entirely on the
# workflow's handler to say anything at all.
[ "$push_failed" -eq 1 ] && warnings+=("the night's work is committed on a runner that no longer exists — it never reached origin")
[ "$origin_polluted" -eq 1 ] && warnings+=("origin/main carries a change outside content/ and data/ that was not there at the start of the night — inspect it before the next run executes it")
[ "$held_now" -gt 0 ] && warnings+=("$held_now story(ies) held from the site at dawn — ${held_slugs//,/, } — the site carries everything else; tonight's cycle 1 must repair or withdraw them")
[ "$content_gate_ok" -eq 0 ] && warnings+=("the archive is BLOCKED — more than $MAX_HELD stories held or the validator could not run; no deploy went out")
[ "$suite_ok" -eq 0 ] && warnings+=("the unit test suite is red on the runner ($suite_failures run(s)) — reported only, it never withholds a deploy")
[ "$usage_stop" -eq 1 ] && warnings+=("night ended early on a usage limit")
# Decide the outcome BEFORE writing the report, so the report can say which one
# it is. The old one asserted "The job itself did not fail" unconditionally, and
# was filed ten seconds before the job failed.
job_failed=0
[ "$push_blocked" -eq 1 ] && job_failed=1
[ "$push_failed" -eq 1 ] && job_failed=1
[ "$origin_polluted" -eq 1 ] && job_failed=1
[ "$content_gate_ok" -eq 0 ] && job_failed=1
[ "$no_runway" -eq 0 ] && [ "$ok_cycles" -lt 1 ] && job_failed=1
[ "$no_runway" -eq 1 ] && [ "$scheduled" -eq 1 ] && job_failed=1

if [ "$no_runway" -eq 1 ] && [ "$scheduled" -eq 0 ]; then
  log "dispatched outside the 22:00-01:20 UTC window (${NIGHT_SECONDS}s of runway), so no cycle ran"
  log "that is documented behaviour, not a fault — use -f smoke=true to exercise the loop at any hour"
fi

if [ "${#warnings[@]}" -gt 0 ]; then
  log "review needed: ${warnings[*]}"
  if [ "$job_failed" -eq 1 ]; then
    issue_prefix="Nightly run failed"
    opening="This night failed, and this is the report of it."
  else
    issue_prefix="Night review needed"
    opening="Automated night review flag. The job itself did not fail."
  fi
  {
    echo "### $(TZ=Europe/Istanbul date +%F) — $opening"
    echo
    for w in "${warnings[@]}"; do echo "- $w"; done
    echo
    echo "- Cycles: $ran_cycles run of $MAX_CYCLES, $ok_cycles clean"
    echo "- Articles: $new_articles new, $updated_articles updated"
    echo "- Window at start: ${NIGHT_SECONDS}s · trigger: ${EVENT_NAME:-unknown}"
    echo "- Report: \`$REPORT_FILE\`"
    echo "- Run: ${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-y-nihat/noiseless-news}/actions/runs/${GITHUB_RUN_ID:-unknown}"
  } > "$NIGHT_STATE_DIR/night-review.md"
  if bash .github/scripts/flag_issue.sh "$issue_prefix" \
       "$issue_prefix $(TZ=Europe/Istanbul date +%F)" "$NIGHT_STATE_DIR/night-review.md"; then
    # Tell nightly.yml's own handler to stand down. Two issues ten seconds
    # apart, one saying the job did not fail and one whose whole body is "no
    # agent output captured", is worse than either alone.
    touch "$ISSUE_FILED"
  else
    log "could not file the night report — leaving it to the workflow handler"
  fi
fi

if [ "$push_blocked" -eq 1 ]; then
  log "the path allowlist refused the push — failing the job"
  exit 1
fi
if [ "$origin_polluted" -eq 1 ]; then
  log "origin/main is not what it was at the start of the night — failing the job"
  exit 1
fi
if [ "$push_failed" -eq 1 ]; then
  log "work did not reach origin — failing the job"
  exit 1
fi
if [ "$content_gate_ok" -eq 0 ]; then
  log "the archive is still BLOCKED at the end of the night — failing the job"
  exit 1
fi
if [ "$no_runway" -eq 1 ]; then
  if [ "$scheduled" -eq 1 ]; then
    log "the cron arrived too late for any cycle to start — failing the job so a lost night is visible"
    exit 1
  fi
  # RUNBOOK.md used to call this red "the correct behaviour". It was not: a red
  # badge for doing exactly what was asked is how a red badge stops meaning
  # anything.
  log "nothing to do outside the window — exiting clean"
  exit 0
fi
if [ "$ok_cycles" -lt 1 ]; then
  log "no successful cycles tonight — failing the job"
  exit 1
fi
log "night complete: $published_total stories across $ran_cycles cycles"
