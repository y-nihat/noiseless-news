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
ok_cycles=0; ran_cycles=0; usage_stop=0

git config user.name "y-nihat"
git config user.email "nihat@yinovasyon.com"

commit_push() {
  git add -A
  git diff --cached --quiet || git commit -m "$1"
  if ! git push; then
    git pull --rebase || true
    git push || true
  fi
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

  python3 .github/scripts/check_result.py "/tmp/claude-stream-$cycle.jsonl"
  gate=$?
  log "cycle $cycle: claude_exit=$claude_exit gate=$gate"

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
{
  echo ""
  echo "## Loop supervisor footer"
  echo ""
  echo "- Cycles run: $ran_cycles (successful: $ok_cycles, max: $MAX_CYCLES)"
  echo "- New articles: $new_articles · updated articles: $updated_articles (night cap: $NIGHT_STORY_CAP new)"
  echo "- Usage-limit stop: $([ "$usage_stop" -eq 1 ] && echo yes || echo no)"
  echo "- Window: $NIGHT_START_ISO → $(date -u +%FT%H:%MZ)"
} >> "$REPORT_FILE"
commit_push "Night loop footer $(date -u +%F)"

{
  echo "### Night loop"
  echo ""
  echo "cycles=$ran_cycles ok=$ok_cycles published=$published_total usage_stop=$usage_stop"
} >> "${GITHUB_STEP_SUMMARY:-/dev/null}"

if [ "$ok_cycles" -lt 1 ]; then
  log "no successful cycles tonight — failing the job"
  exit 1
fi
log "night complete: $published_total stories across $ran_cycles cycles"
