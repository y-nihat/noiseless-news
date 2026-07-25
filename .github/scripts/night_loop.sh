#!/usr/bin/env bash
# Night-loop supervisor: repeated ingest → agent-cycle → publish rounds across
# the 01:00-05:00 Istanbul window. Fresh agent session per cycle; the ledger is
# the shared state. Ends early on usage-limit errors or the story cap.
set -uo pipefail  # deliberately NOT -e: errors are handled per cycle

log() { echo "[loop $(date -u +%H:%M:%S)] $*"; }

SMOKE="${SMOKE:-false}"
if [ "$SMOKE" = "true" ]; then
  MAX_CYCLES=2; CYCLE_INTERVAL=1500; STORIES_PER_CYCLE=1
  MAX_SEARCHES=3; MAX_TURNS=40; NIGHT_STORY_CAP=2; NIGHT_SECONDS=3300
else
  MAX_CYCLES=6; CYCLE_INTERVAL=2100; STORIES_PER_CYCLE=4
  MAX_SEARCHES=15; MAX_TURNS=120; NIGHT_STORY_CAP=12
  # Night ends 01:20 UTC (04:20 Istanbul). Cron fires 22:00-23:00 UTC, so
  # "tomorrow 01:20" is right; the guard handles a post-midnight late start.
  TARGET=$(date -u -d "tomorrow 01:20" +%s); NOW=$(date -u +%s)
  [ $((TARGET - NOW)) -gt 14400 ] && TARGET=$(date -u -d "today 01:20" +%s)
  NIGHT_SECONDS=$((TARGET - NOW))
fi

# Scheduled runs are cron'd at 21:40 UTC to absorb GitHub's cron delay; hold
# the actual start until the window opens at 22:00 UTC (01:00 Istanbul).
if [ "${EVENT_NAME:-}" = "schedule" ] && [ "$SMOKE" != "true" ]; then
  WINDOW_START=$(date -u -d "today 22:00" +%s); NOW=$(date -u +%s)
  if [ "$NOW" -lt "$WINDOW_START" ]; then
    log "holding $((WINDOW_START - NOW))s until the 22:00 UTC window opens"
    sleep $((WINDOW_START - NOW))
    # recompute the window from the true start
    TARGET=$(date -u -d "tomorrow 01:20" +%s); NOW=$(date -u +%s)
    [ $((TARGET - NOW)) -gt 14400 ] && TARGET=$(date -u -d "today 01:20" +%s)
    NIGHT_SECONDS=$((TARGET - NOW))
  fi
fi

START=$(date -u +%s)
NIGHT_START_ISO=$(date -u -d "@$START" +%FT%H:%M:%SZ)
NIGHT_END=$((START + NIGHT_SECONDS))
# Report is named for the Istanbul morning it will be reviewed on, plus the
# run's start time so same-day runs (smoke tests) never collide.
REPORT_FILE="data/ledger/run-report-$(TZ=Europe/Istanbul date +%F)-$(date -u +%H%M)Z.md"
touch /tmp/night-start-marker
ok_cycles=0; ran_cycles=0; usage_stop=0; guard_trips=0; push_failed=0
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
  # Restore tracked files so the next cycle runs the real scripts, not edited
  # ones. Untracked strays are left on the runner and simply never staged.
  git checkout -- . ':(exclude)content' ':(exclude)data' 2>/dev/null || true
}

commit_push() {
  guard_paths
  git add "${OWNED_PATHS[@]}"
  git diff --cached --quiet || git commit -m "$1"
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

for cycle in $(seq 1 "$MAX_CYCLES"); do
  NOW=$(date -u +%s)
  if [ $((NIGHT_END - NOW)) -lt 600 ]; then
    log "under 10 minutes left in the window — not starting cycle $cycle"
    break
  fi

  log "cycle $cycle: ingest"
  PYTHONPATH=pipeline python -m noiseless.run ingest || log "ingest reported failures (continuing)"
  commit_push "Night ingest $(date -u +%FT%H:%MZ)"

  published=$(find content/articles/en -name '*.md' -newer /tmp/night-start-marker | wc -l)
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
    watching="re-check EVERY ledger entry in watching state (1-3 searches each) for its missing evidence; publish if the gate now passes, else update the entry's notes."
  else
    watching="only re-check a watching-state ledger entry if this cycle's fresh ingest or sweep mentions it — otherwise leave watching stories alone (they were checked in cycle 1 and will be re-checked in the final cycle)."
  fi

  if [ "$stories" -eq 0 ] && [ "$is_final" -eq 0 ]; then
    log "night story cap reached — skipping agent cycle $cycle"
    sleep_secs=$((SLOT_END - $(date -u +%s)))
    [ "$sleep_secs" -gt 0 ] && sleep "$sleep_secs"
    continue
  fi

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
      .github/cycle-prompt.md > "/tmp/prompt-$cycle.md"
  if grep -q '{{' "/tmp/prompt-$cycle.md"; then
    log "ERROR: unrendered placeholder in cycle prompt"; grep -o '{{[A-Z_]*}}' "/tmp/prompt-$cycle.md" | sort -u
    exit 1
  fi

  CYCLE_TIMEOUT=$((SLOT_END - $(date -u +%s) - 60))
  [ "$CYCLE_TIMEOUT" -lt 300 ] && CYCLE_TIMEOUT=300
  log "cycle $cycle: agent starting (deadline $CYCLE_DEADLINE UTC, stories<=$stories, timeout ${CYCLE_TIMEOUT}s)"
  ran_cycles=$((ran_cycles + 1))

  timeout "$CYCLE_TIMEOUT" claude -p "$(cat /tmp/prompt-$cycle.md)" \
    --model claude-sonnet-5 \
    --max-turns "$MAX_TURNS" \
    --allowedTools "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch" \
    --output-format stream-json --verbose \
    | tee "/tmp/claude-stream-$cycle.jsonl" \
    | python3 .github/scripts/stream_summary.py
  claude_exit=${PIPESTATUS[0]}

  python3 .github/scripts/check_result.py "/tmp/claude-stream-$cycle.jsonl" \
    --stats-file "$NIGHT_STATS" --night "$NIGHT_START_ISO" --cycle "$cycle"
  gate=$?
  log "cycle $cycle: claude_exit=$claude_exit gate=$gate"

  # Advisory for now: the report goes into the cycle log and the agent can act
  # on it next cycle, but a finding does not block the commit. Promote to
  # --strict once the style.md gate-1 / §3 litigation conflict is settled.
  PYTHONPATH=pipeline python -m noiseless.run validate-content 2>&1 | while IFS= read -r line
  do
    log "content: $line"
  done

  commit_push "Night cycle $cycle artifacts $(date -u +%FT%H:%MZ)"

  # Per-cycle site deploy so articles appear through the night (best effort).
  gh workflow run "Deploy site" --ref main 2>/dev/null \
    && log "site deploy dispatched" || log "deploy dispatch failed (non-fatal)"

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
  echo "- Cycles run: $ran_cycles (successful: $ok_cycles, max: $MAX_CYCLES)"
  echo "- New articles: $new_articles · updated articles: $updated_articles (night cap: $NIGHT_STORY_CAP new)"
  echo "- Usage-limit stop: $([ "$usage_stop" -eq 1 ] && echo yes || echo no)"
  echo "- Out-of-scope write attempts blocked: $guard_trips"
  echo "- Push to origin: $([ "$push_failed" -eq 1 ] && echo FAILED || echo ok)"
  echo "- Night cost (USD): $night_cost"
  echo "- Window: $NIGHT_START_ISO → $(date -u +%FT%H:%MZ)"
} >> "$REPORT_FILE"
commit_push "Night loop footer $(date -u +%F)"

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
warnings=()
[ "$((new_articles + updated_articles))" -eq 0 ] && warnings+=("published nothing tonight")
[ "$ok_cycles" -lt "$ran_cycles" ] && warnings+=("$((ran_cycles - ok_cycles)) of $ran_cycles cycles did not complete cleanly")
[ "$guard_trips" -gt 0 ] && warnings+=("$guard_trips out-of-scope write attempt(s) blocked")
[ "$usage_stop" -eq 1 ] && warnings+=("night ended early on a usage limit")
if [ "${#warnings[@]}" -gt 0 ]; then
  log "review needed: ${warnings[*]}"
  {
    echo "Automated night review flag. The job itself did not fail."
    echo
    for w in "${warnings[@]}"; do echo "- $w"; done
    echo
    echo "- Cycles: $ran_cycles run, $ok_cycles clean"
    echo "- Articles: $new_articles new, $updated_articles updated"
    echo "- Report: \`$REPORT_FILE\`"
    echo "- Run: ${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-y-nihat/noiseless-news}/actions/runs/${GITHUB_RUN_ID:-unknown}"
  } > /tmp/night-review.md
  gh issue create --title "Night review needed $(TZ=Europe/Istanbul date +%F)" \
    --body-file /tmp/night-review.md >/dev/null 2>&1 \
    && log "review issue opened" || log "could not open review issue (non-fatal)"
fi

if [ "$push_failed" -eq 1 ]; then
  log "work did not reach origin — failing the job"
  exit 1
fi
if [ "$ok_cycles" -lt 1 ]; then
  log "no successful cycles tonight — failing the job"
  exit 1
fi
log "night complete: $published_total stories across $ran_cycles cycles"
