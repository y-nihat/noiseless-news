#!/usr/bin/env bash
# One durable thread per recurring condition, instead of one issue per run.
#
# source-health.yml called `gh issue create` unconditionally every Monday, with
# no dedup search and no label, so one unchanged fact — the same four HTTP 403s
# — opened #19 (2026-07-27), #20 (2026-08-03) and #31 (2026-08-10): identical
# bodies, no comments, none closed, none actioned in the twenty days since. At
# one a week that is roughly fifty open issues a year saying the same thing, and
# an alarm that repeats itself weekly is an alarm nobody reads.
#
# Commenting instead of creating also keeps the history in one place, which is
# what makes "compare against last week's report before acting" — the sentence
# the old body printed at a human — something you can actually do.
#
# The thread is also assigned to the repository owner, because on GitHub an
# issue reaches a person only through assignment, an @-mention or prior
# participation — a label subscribes nobody, and neither does owning the repo.
# Issue #37 carried a red test suite in its body and all seven of its comments
# for eight days and reached nobody. Assignment is best-effort on purpose: a
# filed alarm that could not be assigned is still a filed alarm.
#
# A closed thread is REOPENED rather than replaced. Closing is how an operator
# says "read"; the condition recurring afterwards is the same condition, and
# the week-on-week comparison these bodies instruct the reader to make only
# works if it stays in one place. Without this, closing #34 on 2026-08-28 would
# have had the next Monday open a fresh thread and restart that record from
# empty — the churn this script was written to stop, arriving by a different
# door. Consistent with the rule below it: losing or scattering the alarm is
# worse than a noisy one, so a `not planned` close does not suppress a
# recurrence either.
#
# Usage: flag_issue.sh <title-prefix> <title> <body-file>
#   Comments on the lowest-numbered OPEN issue whose title starts with
#   <title-prefix>; failing that reopens the most recent CLOSED one; opens one
#   titled <title> if there is neither.
set -uo pipefail

if [ "$#" -ne 3 ]; then
  echo "usage: flag_issue.sh <title-prefix> <title> <body-file>" >&2
  exit 2
fi
prefix=$1
title=$2
body_file=$3

if [ ! -f "$body_file" ]; then
  echo "flag_issue: no body file at $body_file" >&2
  exit 2
fi

# The prefix travels in the environment rather than being pasted into the
# filter: it is ordinary prose and has no business being parsed as code. Also
# means an unreadable or empty listing yields "no match" rather than an error.
find_thread() {  # <state> <first|last>
  gh issue list --state "$1" --limit 100 --json number,title 2>/dev/null \
    | PREFIX="$prefix" PICK="$2" python3 -c '
import json, os, sys
try:
    issues = json.load(sys.stdin)
except Exception:
    sys.exit(0)
matches = sorted(
    i["number"] for i in issues
    if isinstance(i, dict) and str(i.get("title", "")).startswith(os.environ["PREFIX"])
)
if matches:
    print(matches[0] if os.environ["PICK"] == "first" else matches[-1])
'
}

# Open threads: the LOWEST number, so everything keeps landing in the one that
# has the history. Closed threads: the HIGHEST, because the older ones are the
# duplicates from before this script existed — #19, #20 and #31 all still carry
# the source-health prefix, and resurrecting #19 from 2026-07-27 would be worse
# than opening something new.
existing=$(find_thread open first)

if [ -z "${existing:-}" ]; then
  reopened=$(find_thread closed last)
  if [ -n "${reopened:-}" ] && gh issue reopen "$reopened" >/dev/null 2>&1; then
    existing=$reopened
    echo "flag_issue: reopened #$reopened — the condition recurred"
  fi
fi

# owner/repo -> owner. Unset outside Actions, where there is nobody to assign
# — and `set -u` above turns a bare ${GITHUB_REPOSITORY%%/*} into an abort, so
# the default has to come first.
repo=${GITHUB_REPOSITORY-}
owner=${repo%%/*}

assign() {
  [ -n "${owner:-}" ] || return 0
  [ -n "${1:-}" ] || return 0
  gh issue edit "$1" --add-assignee "$owner" >/dev/null 2>&1 \
    || echo "flag_issue: filed, but could not assign #$1 to $owner" >&2
}

if [ -n "${existing:-}" ]; then
  if gh issue comment "$existing" --body-file "$body_file" >/dev/null 2>&1; then
    # Assign on every comment, not only at creation: the thread that needed
    # this most was opened before anyone thought to, and a comment on an
    # unassigned issue notifies nobody either.
    assign "$existing"
    echo "flag_issue: commented on #$existing"
    exit 0
  fi
  echo "flag_issue: could not comment on #$existing — opening a new issue instead" >&2
fi

# Created bare and assigned after, rather than with --assignee: an assignee
# GitHub rejects fails the whole create, and losing the alarm to fix its
# addressing would be the wrong trade.
if created=$(gh issue create --title "$title" --body-file "$body_file" 2>/dev/null); then
  assign "${created##*/}"
  echo "flag_issue: opened a new issue — $title"
  exit 0
fi

# Losing the alarm is worse than a noisy one: say so on the job's own log.
echo "flag_issue: could not file anything — $title" >&2
exit 1
