"""§4's dead-feed rule, made runnable.

`policy/source-lifecycle.md` §4 says a feed that keeps failing is flagged for
repair or retirement after fourteen consecutive days, and that every ingest run
appends its per-source counts to `data/ledger/source_stats.jsonl` for exactly
that purpose. Nothing ever read the file. `grep -rn source_stats` outside
`data/` returns three hits: the write path in `run.py`, the rule's own sentence
in the policy, and a design note claiming the rule is now runnable.

So the rule never ran. MIT News AI failed its fetch on every recorded day and
Qwen Blog returned nothing on every recorded day, and neither crossed a
threshold, because no threshold was ever evaluated by anything.

Two conditions matter and only one of them is a fetch failure:

  failing — the fetch itself is broken (`-1`), the case §4 describes.
  silent  — the fetch works and returns nothing, every day, for weeks. A feed
            frozen in place looks perfectly healthy to a checker that only asks
            for HTTP 200, which is how a Tier-0 vendor feed last updated in
            September 2025 kept its `[ok]` in every weekly report.

Streaks are counted in DAYS. The file holds roughly seven runs a day — two
daytime crons plus one per night cycle — so a row-based threshold would trip
after two days and mean nothing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from noiseless.sources import DEFAULT_MAX_AGE_DAYS, Source

# policy/source-lifecycle.md §4, verbatim: fourteen consecutive days of failing
# live validation. This governs FETCH FAILURES only.
STREAK_DAYS = 14

# Silence is judged against the source's own freshness allowance instead, the
# same number the live check uses, so the two never disagree about what "too
# quiet" means. Fourteen days would be wrong here: a university lab blog and a
# weekly newsletter both cross it in the course of behaving normally, and an
# alarm that fires on normal behaviour is one people learn to close.

FAILING = "failing"
SILENT = "silent"
UNTRACKED = "untracked"
BLOCKED = "blocked"
OK = "ok"


@dataclass(frozen=True)
class SourceStatus:
    name: str
    verdict: str
    days_tracked: int
    failing_days: int
    silent_days: int
    last_item_day: str | None
    detail: str

    @property
    def flagged(self) -> bool:
        return self.verdict in (FAILING, SILENT)


def read_runs(stats_path: Path) -> list[tuple[str, dict[str, int]]]:
    """Return [(day, {source: count})] in file order, skipping unreadable lines.

    One malformed line must not hide the other 159: this file is appended to by
    an unattended job and read when something has already gone wrong.
    """
    runs: list[tuple[str, dict[str, int]]] = []
    if not stats_path.exists():
        return runs
    with stats_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            run_at = record.get("run_at")
            counts = record.get("counts")
            if not isinstance(run_at, str) or not isinstance(counts, dict):
                continue
            numeric = {
                name: value
                for name, value in counts.items()
                if isinstance(value, int) and not isinstance(value, bool)
            }
            runs.append((run_at[:10], numeric))
    return runs


def _per_day(runs: list[tuple[str, dict[str, int]]]) -> dict[str, dict[str, list[int]]]:
    days: dict[str, dict[str, list[int]]] = {}
    for day, counts in runs:
        bucket = days.setdefault(day, {})
        for name, value in counts.items():
            bucket.setdefault(name, []).append(value)
    return days


def _streaks(day_values: list[tuple[str, list[int]]]) -> tuple[int, int, str | None]:
    """(failing_days, silent_days, last_item_day) counted back from the newest day.

    A day counts as failing only if every fetch that day failed — one transient
    -1 among six good runs is not a dead feed.
    """
    failing = silent = 0
    last_item_day: str | None = None
    still_failing = still_silent = True
    for day, values in reversed(day_values):
        got_items = max(values) > 0
        if got_items and last_item_day is None:
            last_item_day = day
        if still_failing and values and all(value == -1 for value in values):
            failing += 1
        else:
            still_failing = False
        if still_silent and not got_items:
            silent += 1
        else:
            still_silent = False
    return failing, silent, last_item_day


def summarize(sources: list[Source], stats_path: Path) -> list[SourceStatus]:
    days = _per_day(read_runs(stats_path))
    ordered_days = sorted(days)

    statuses: list[SourceStatus] = []
    for source in sources:
        if source.status != "active":
            continue
        day_values = [
            (day, days[day][source.name]) for day in ordered_days if source.name in days[day]
        ]
        if not day_values:
            # html sources are the night agent's sweep targets, not ingest's, so
            # they never appear here. The weekly live check is what covers them.
            statuses.append(
                SourceStatus(source.name, UNTRACKED, 0, 0, 0, None,
                             f"no ingest record (type {source.type})")
            )
            continue

        failing, silent, last_item_day = _streaks(day_values)
        tracked = len(day_values)
        since = last_item_day or "never in this record"
        if source.runner_blocked:
            # One registry fact, written down with its reason, suppresses both
            # this and the weekly live check — rather than each being silenced
            # separately and neither remembering why.
            verdict, detail = BLOCKED, (
                f"registered as blocked from CI addresses; {failing} failing day(s) "
                "here are that block, not a dead feed"
            )
        elif failing >= STREAK_DAYS:
            verdict, detail = FAILING, (
                f"fetch has failed every day for {failing} days "
                f"(§4 threshold {STREAK_DAYS}) — repair or retire"
            )
        elif silent > (source.max_age_days or DEFAULT_MAX_AGE_DAYS):
            verdict, detail = SILENT, (
                f"fetch works but has returned nothing for {silent} days, past this "
                f"source's {source.max_age_days or DEFAULT_MAX_AGE_DAYS}-day allowance "
                f"(last item: {since}) — frozen in place, not dead"
            )
        elif failing:
            verdict, detail = OK, f"failing for {failing} day(s), under the threshold"
        elif silent:
            verdict, detail = OK, f"quiet for {silent} day(s), last item {since}"
        else:
            verdict, detail = OK, f"last item {since}"
        statuses.append(
            SourceStatus(source.name, verdict, tracked, failing, silent, last_item_day, detail)
        )
    return statuses


def report(sources: list[Source], stats_path: Path) -> tuple[str, int]:
    """Render the §4 verdict. Returns (text, exit code); 2 means something is flagged."""
    statuses = summarize(sources, stats_path)
    runs = read_runs(stats_path)
    days = sorted({day for day, _ in runs})
    span = f"{days[0]} … {days[-1]}" if days else "no ingest runs recorded"

    lines = []
    flagged = [s for s in statuses if s.flagged]
    for status in sorted(statuses, key=lambda s: (not s.flagged, s.name)):
        mark = {FAILING: "FLAG", SILENT: "FLAG", UNTRACKED: "n/a",
                BLOCKED: "BLOCKED", OK: "ok"}[status.verdict]
        lines.append(f"[{mark}] {status.name}: {status.detail}")
    lines.append(
        f"source-status done — {len(flagged)} flagged of {len(statuses)} active "
        f"sources over {len(days)} days ({span})"
    )
    return "\n".join(lines), (2 if flagged else 0)
