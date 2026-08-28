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

WINDOW_SECONDS = 7200  # 02:00 -> 04:00 UTC (05:00-07:00 Istanbul)
MAX_HOLD = 1200  # cron fires 01:40, twenty minutes before the window opens


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
        """The exact clock of run 31136812347, kept after the window moved.

        Then: hold=75318 (20h55m), killed at the 235-minute step timeout having
        run nothing. Under the 02:00-04:00 window that clock is twenty minutes
        BEFORE the cron can fire rather than three hours after it, so it is
        refused instead of held — but the property under test is the same one,
        and it is the property that broke: no start time may sleep the job away.
        """
        hold, night = plan("2026-08-07 01:04:42")
        assert hold == 0
        assert night < 0

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
            ("2026-08-06 01:40:00", 1200, 7200),  # cron on time: hold to 02:00
            ("2026-08-06 01:50:00", 600, 7200),   # half the offset used up
            ("2026-08-06 02:00:00", 0, 7200),     # window opens exactly
            ("2026-08-06 02:19:00", 0, 6060),     # the typical +19min delivery
            ("2026-08-06 03:00:00", 0, 3600),     # an hour late: half a night
            ("2026-08-06 03:59:59", 0, 1),        # last second of the window
        ],
    )
    def test_known_start_times(self, when, hold, night):
        assert plan(when) == (hold, night)

    def test_a_typical_delivery_delay_still_gets_a_usable_night(self):
        """Median delivery drift was +18min over the fortnight before the move.

        A 2h window has less to lose to a delay than a 3h20m one had, so this
        is the number that decides whether moving the window was worth it.
        """
        for when in ("2026-08-06 02:15:00", "2026-08-06 02:19:00", "2026-08-06 02:30:00"):
            hold, night = plan(when)
            assert hold == 0
            assert night >= 5400, f"{when} would only get {night}s"


class TestLateAndOutOfWindow:
    @pytest.mark.parametrize(
        "when,night",
        [
            ("2026-08-07 03:50:00", 600),   # exactly the loop's 10-minute floor
            ("2026-08-07 03:55:00", 300),   # under it: the guard breaks first
        ],
    )
    def test_a_late_start_gets_the_window_that_is_left(self, when, night):
        hold, actual = plan(when)
        assert hold == 0
        assert actual == night

    @pytest.mark.parametrize(
        "when",
        [
            "2026-08-07 04:00:01",   # one second after the close
            "2026-08-07 06:00:00",   # a two-hour-late cron
            "2026-08-07 15:30:00",   # an afternoon dispatch
            "2026-08-07 23:30:00",   # the evening before the next window
            "2026-08-07 00:00:00",   # midnight: earlier than the cron can fire
            "2026-08-07 01:39:59",   # one second before the hold window opens
        ],
    )
    def test_a_closed_window_is_refused_rather_than_waited_out(self, when):
        """Negative runway makes the loop's own guard break before cycle 1.

        The job then writes its footer, raises a review warning and exits red in
        a few minutes — instead of sleeping until a timeout kills it. The two
        pre-cron cases matter as much as the late ones: with the window inside a
        single UTC day, 00:00-01:39 is no longer "tonight, in a while" but
        "yesterday's window, twenty hours shut", and holding for it would be the
        unbounded sleep all over again.
        """
        hold, night = plan(when)
        assert hold == 0
        assert night < 0

    def test_the_refusal_boundary_is_exactly_the_window_close(self):
        assert plan("2026-08-07 03:59:59")[1] == 1
        assert plan("2026-08-07 04:00:01")[1] == -1

    def test_the_hold_boundary_is_exactly_the_cron_offset(self):
        assert plan("2026-08-07 01:40:00")[0] == MAX_HOLD
        assert plan("2026-08-07 01:39:59")[0] == 0


class TestSmokeMode:
    def test_smoke_is_time_independent(self):
        """A smoke test must work at any hour — it is the documented recovery check."""
        for when in ("2026-08-07 03:00:00", "2026-08-07 12:00:00", "2026-08-06 22:30:00"):
            assert plan(when, smoke="true") == (0, 3300)


class TestScriptShape:
    def test_the_unbounded_hold_cannot_come_back(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for banned in ("today 22:00", "today 02:00", "tomorrow 01:20", "tomorrow 04:00"):
            assert f'date -u -d "{banned}"' not in script, (
                f"`{banned}` resolves against the start date — this is the bug"
            )
        assert "MAX_HOLD=1200" in script

    def test_feed_capture_happens_before_the_window_is_consulted(self):
        """A missed ingest is the only permanent loss; it must not depend on runway."""
        script = SCRIPT.read_text(encoding="utf-8")
        pre_loop = script.split("for cycle in")[0]
        assert "pre-cycle ingest" in pre_loop
        assert "noiseless.run ingest" in pre_loop


class TestTheWindowAndTheCronAgree:
    """Three files state this schedule; a disagreement is a lost night."""

    WORKFLOW = (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
    SCRIPT_TEXT = SCRIPT.read_text(encoding="utf-8")

    def test_the_cron_fires_exactly_max_hold_before_the_window_opens(self):
        import re

        cron = re.search(r'cron:\s*"(\d+) (\d+) \* \* \*"', self.WORKFLOW)
        assert cron, "no daily cron in nightly.yml"
        fires = int(cron.group(2)) * 3600 + int(cron.group(1)) * 60
        opens = 7200  # 02:00 UTC, the OPEN constant below
        assert opens - fires == MAX_HOLD, (
            f"cron fires {opens - fires}s before the window; the supervisor will "
            f"only hold {MAX_HOLD}s, so the rest is lost every night"
        )

    def test_the_script_opens_the_window_where_the_cron_expects(self):
        assert "OPEN=$((DAY + 7200))" in self.SCRIPT_TEXT

    def test_the_job_timeout_covers_the_hold_and_the_whole_window(self):
        """A timeout shorter than the window kills the final cycle mid-verify."""
        import re

        job = int(re.search(r"timeout-minutes: (\d+)", self.WORKFLOW).group(1))
        needed = (MAX_HOLD + WINDOW_SECONDS) / 60
        assert job >= needed, f"job timeout {job}min cannot cover {needed}min"
        assert job <= needed + 45, (
            f"job timeout {job}min is far longer than the {needed}min it can use; "
            "a hung run should be killed, not billed"
        )

    def test_four_cycles_is_what_the_window_actually_fits(self):
        """MAX_CYCLES is also what the prompt promises the agent it will get."""
        assert "MAX_CYCLES=4" in self.SCRIPT_TEXT
        interval, floor = 2100, 900
        end, cycles = WINDOW_SECONDS, 0
        now = 0
        while now < end:
            cycles += 1
            slot_end = min(now + interval, end)
            if end - slot_end < floor:
                break
            now = slot_end
        assert cycles == 4, f"the window fits {cycles} cycles, not 4"
