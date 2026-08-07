"""The night window arithmetic, driven against the real script.

On 2026-08-07 GitHub delivered the 21:40 UTC cron 3h24m late, at 01:04. The
supervisor computed "hold until 22:00 today" against the *actual* start date,
so it pointed twenty-two hours forward instead of twenty minutes, slept 75318
seconds, and was killed at the 235-minute step timeout having run zero cycles
and published nothing (run 31136812347).

These tests shell out to `night_loop.sh` itself with `NIGHT_PLAN_ONLY=1` and an
injected clock, so what is asserted is the code that actually runs at 22:00 —
not a Python reimplementation of it that could drift.
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".github" / "scripts" / "night_loop.sh"

WINDOW_SECONDS = 12000  # 22:00 -> 01:20 UTC
MAX_HOLD = 1200  # cron fires 21:40, twenty minutes before the window opens


def epoch(text: str) -> int:
    return int(
        datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )


def plan(when: str, smoke: str = "false") -> tuple[int, int]:
    """Run the real script in plan-only mode. Returns (hold, night_seconds)."""
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=REPO_ROOT,
        env={
            "PATH": "/usr/bin:/bin",
            "NIGHT_PLAN_ONLY": "1",
            "NIGHT_NOW": str(epoch(when)),
            "SMOKE": smoke,
        },
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"plan mode failed: {result.stderr}"
    fields = dict(part.split("=") for part in result.stdout.split())
    return int(fields["hold"]), int(fields["night_seconds"])


class TestTheIncident:
    def test_the_2026_08_07_start_no_longer_sleeps_the_job_away(self):
        """The exact clock of run 31136812347.

        Old behaviour: hold=75318 (20h55m), killed at the step timeout.
        New behaviour: no hold, and the fifteen minutes of window that genuinely
        remained — which is what the pre-existing guard had already computed
        before the hold block overwrote it.
        """
        hold, night = plan("2026-08-07 01:04:42")
        assert hold == 0
        assert night == 918

    def test_a_hold_can_never_exceed_the_cron_offset(self):
        """The bug was an unbounded sleep. Nothing may hold longer than 21:40->22:00."""
        for hour in range(24):
            for minute in (0, 17, 41, 59):
                hold, _ = plan(f"2026-08-06 {hour:02d}:{minute:02d}:00")
                assert hold <= MAX_HOLD, f"{hour:02d}:{minute:02d} would hold {hold}s"

    def test_no_start_time_can_claim_more_window_than_exists(self):
        for hour in range(24):
            for minute in (0, 30):
                _hold, night = plan(f"2026-08-06 {hour:02d}:{minute:02d}:00")
                assert night <= WINDOW_SECONDS


class TestNormalOperation:
    @pytest.mark.parametrize(
        "when,hold,night",
        [
            ("2026-08-06 21:40:00", 1200, 12000),  # cron on time: hold to 22:00
            ("2026-08-06 21:50:00", 600, 12000),   # half the offset used up
            ("2026-08-06 22:00:00", 0, 12000),     # window opens exactly
            ("2026-08-06 22:39:31", 0, 9629),      # a real 2026-08-05 start
            ("2026-08-06 23:03:12", 0, 8208),      # the worst pre-incident delay
            ("2026-08-06 23:59:59", 0, 4801),      # last second before midnight
        ],
    )
    def test_known_start_times(self, when, hold, night):
        assert plan(when) == (hold, night)

    def test_every_historical_start_still_gets_a_working_night(self):
        """All 29 scheduled runs before the incident started between 22:28 and 23:04."""
        for when in ("2026-08-06 22:28:35", "2026-08-06 22:44:06", "2026-08-06 23:03:12"):
            hold, night = plan(when)
            assert hold == 0
            assert night > 8000, f"{when} would only get {night}s"


class TestLateAndOutOfWindow:
    @pytest.mark.parametrize(
        "when,night",
        [
            ("2026-08-07 00:00:00", 4800),   # just past midnight
            ("2026-08-07 00:30:00", 3000),
            ("2026-08-07 01:04:42", 918),    # the incident
            ("2026-08-07 01:10:00", 600),    # exactly the loop's 10-minute floor
        ],
    )
    def test_a_post_midnight_start_belongs_to_last_nights_window(self, when, night):
        """01:04 is 3h24m late for last night, not 21h early for tonight."""
        hold, actual = plan(when)
        assert hold == 0
        assert actual == night

    @pytest.mark.parametrize(
        "when", ["2026-08-07 01:21:00", "2026-08-07 06:00:00", "2026-08-07 15:30:00"]
    )
    def test_a_closed_window_is_refused_rather_than_waited_out(self, when):
        """Negative runway makes the loop's own guard break before cycle 1.

        The job then writes its footer, raises a review warning and exits red in
        a few minutes — instead of sleeping until a timeout kills it.
        """
        hold, night = plan(when)
        assert hold == 0
        assert night < 0

    def test_the_refusal_boundary_is_exactly_the_window_close(self):
        assert plan("2026-08-07 01:19:59")[1] == 1
        assert plan("2026-08-07 01:20:01")[1] == -1


class TestSmokeMode:
    def test_smoke_is_time_independent(self):
        """A smoke test must work at any hour — it is the documented recovery check."""
        for when in ("2026-08-07 03:00:00", "2026-08-07 12:00:00", "2026-08-06 22:30:00"):
            assert plan(when, smoke="true") == (0, 3300)


class TestScriptShape:
    def test_the_unbounded_hold_cannot_come_back(self):
        script = SCRIPT.read_text(encoding="utf-8")
        assert 'date -u -d "today 22:00"' not in script, (
            "`today 22:00` resolves against the start date — this is the bug"
        )
        assert 'date -u -d "tomorrow 01:20"' not in script
        assert "MAX_HOLD=1200" in script

    def test_feed_capture_happens_before_the_window_is_consulted(self):
        """A missed ingest is the only permanent loss; it must not depend on runway."""
        script = SCRIPT.read_text(encoding="utf-8")
        pre_loop = script.split("for cycle in")[0]
        assert "pre-cycle ingest" in pre_loop
        assert "noiseless.run ingest" in pre_loop
