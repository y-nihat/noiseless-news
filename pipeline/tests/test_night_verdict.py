"""What the morning is told, and whether the badge agrees with it.

On 2026-08-07 GitHub delivered the 21:40 UTC cron at 01:04. No cycle could
start, and the night produced two issues ten seconds apart that contradicted
each other: #28 "Night review needed", whose first line read "The job itself did
not fail", and #29 "Nightly run failed", whose entire body was "no agent output
captured" — because the workflow's handler tails a stream file that no cycle had
written. The same shape appeared for a deliberate daytime dispatch, which
RUNBOOK.md described as red by design.

Three outcomes, and they are now distinguishable: a lost scheduled night is red
with one report, an operator dispatch outside the window is green with none, and
a night that ran is judged on how it ran.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from night_harness import (
    ISSUE_SENTINEL,
    SCRIPT,
    gh_calls,
    make_scratch,
    run_night,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
NIGHTLY = REPO_ROOT / ".github" / "workflows" / "nightly.yml"

# 07:00 UTC: the window closed at 01:20 and the next does not open until 22:00,
# so the loop computes negative runway and starts no cycle. This is the clock of
# the 08:55 dispatch on 2026-08-07 (run 31163752065).
OUT_OF_WINDOW = "1786604400"


@pytest.fixture
def scratch(tmp_path: Path) -> dict[str, Path]:
    return make_scratch(tmp_path)


def issues_filed(scratch) -> list[str]:
    return [c for c in gh_calls(scratch) if c.startswith(("issue create", "issue comment"))]


class TestAnOperatorDispatchOutsideTheWindow:
    """Documented behaviour. It should not look like a fault."""

    def test_the_job_succeeds(self, scratch):
        result = run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW,
                           EVENT_NAME="workflow_dispatch")
        assert result.returncode == 0, (
            f"a dispatch outside the window still fails the job:\n{result.stdout[-2000:]}"
        )

    def test_it_files_nothing(self, scratch):
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="workflow_dispatch")
        assert issues_filed(scratch) == []

    def test_it_says_what_to_do_instead(self, scratch):
        result = run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW,
                           EVENT_NAME="workflow_dispatch")
        assert "smoke=true" in result.stdout, (
            "the log leaves the operator to work out why nothing happened"
        )

    def test_the_feeds_are_still_captured(self, scratch):
        """A missed ingest is the only permanent loss; runway must not gate it."""
        result = run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW,
                           EVENT_NAME="workflow_dispatch")
        assert "pre-cycle ingest" in result.stdout


class TestALostScheduledNight:
    """The cron was delivered too late to be usable. That is worth knowing."""

    def test_the_job_fails(self, scratch):
        result = run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        assert result.returncode == 1

    def test_exactly_one_report_is_filed(self, scratch):
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        assert len(issues_filed(scratch)) == 1, (
            f"the night filed {issues_filed(scratch)}"
        )

    def test_it_is_titled_as_a_failure_not_as_a_review_flag(self, scratch):
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        assert "Nightly run failed" in issues_filed(scratch)[0]

    def test_the_report_does_not_claim_the_job_survived(self, scratch, tmp_path):
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        body = Path("/tmp/night-review.md").read_text(encoding="utf-8")
        assert "The job itself did not fail" not in body, (
            "the report contradicts the exit code, which is what #28 did"
        )
        assert "cron arrived" in body

    def test_the_workflow_handler_is_told_to_stand_down(self, scratch):
        """Otherwise nightly.yml files its "no agent output captured" issue too."""
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        assert ISSUE_SENTINEL.exists()

    def test_the_handler_actually_checks_for_it(self):
        import yaml

        steps = yaml.safe_load(NIGHTLY.read_text("utf-8"))["jobs"]["scan"]["steps"]
        handler = next(s for s in steps if s.get("name") == "Open failure issue")
        assert "/tmp/night-issue-filed" in handler["run"]
        assert "exit 0" in handler["run"]


class TestTheReportIsHonestAboutTheWindow:
    def test_the_footer_says_how_many_cycles_the_window_allowed(self, scratch):
        """"Cycles run: 5 … max: 6" read as though a sixth had been possible."""
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        reports = list((scratch["work"] / "data" / "ledger").glob("run-report-*.md"))
        assert reports, "no run report was written"
        footer = reports[0].read_text(encoding="utf-8")
        assert "Cycles run: 0 of 6" in footer
        assert "did not fit the rest" in footer

    def test_the_footer_records_what_the_agent_was_run_with(self, scratch):
        """Two documents mandate max effort; nothing recorded whether it was used."""
        run_night(scratch, NIGHT_NOW=OUT_OF_WINDOW, EVENT_NAME="schedule")
        reports = list((scratch["work"] / "data" / "ledger").glob("run-report-*.md"))
        footer = reports[0].read_text(encoding="utf-8")
        assert "effort max" in footer
        assert "claude-sonnet-5" in footer

    def test_a_routine_five_of_six_night_does_not_raise_a_flag(self):
        """It happens on 31 nights in 36, and the sixth slot has never published."""
        script = SCRIPT.read_text(encoding="utf-8")
        clause = next(
            line for line in script.splitlines()
            if "cycles fitted in the window" in line or "ran_cycles * 2" in line
        )
        assert "ran_cycles * 2" in clause, (
            "the shortfall warning fires on every ordinary night"
        )


class TestTheMandatedFlags:
    def test_the_agent_is_run_at_max_effort(self):
        """CLAUDE.md and policy/verification.md §5 both require it."""
        script = SCRIPT.read_text(encoding="utf-8")
        invocation = script.split("claude -p ")[1].split("claude_exit")[0]
        assert "--effort max" in invocation
        assert "--model claude-sonnet-5" in invocation

    def test_the_cli_is_pinned_like_every_other_dependency(self):
        workflow = NIGHTLY.read_text(encoding="utf-8")
        install = next(
            line for line in workflow.splitlines() if "npm install -g" in line
        )
        assert "@anthropic-ai/claude-code@" in install, (
            f"unpinned agent CLI: {install.strip()}"
        )
        version = install.split("@anthropic-ai/claude-code@")[1].strip()
        assert version[0].isdigit(), f"not an exact version: {version!r}"
