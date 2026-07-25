"""Operational controls the owner needs and the repository did not have.

Continuity rested on one consumer token, one person, and no written procedure:
no documented way to pause publishing, take an article down, rotate the token,
or work out what a bad night meant. These tests pin the mechanisms; RUNBOOK.md
carries the prose.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from noiseless.ingest import USER_AGENT

REPO_ROOT = Path(__file__).resolve().parents[2]
NIGHT_LOOP = (REPO_ROOT / ".github" / "scripts" / "night_loop.sh").read_text("utf-8")
RUNBOOK = (REPO_ROOT / "RUNBOOK.md").read_text("utf-8")


class TestPauseSwitch:
    def test_night_loop_checks_for_the_sentinel(self):
        assert "-f .paused" in NIGHT_LOOP

    def test_the_check_runs_before_any_work(self):
        """A pause that only takes effect after the first cycle is not a pause."""
        pause_at = NIGHT_LOOP.index(".paused")
        for later in ("claude -p", "commit_push", "run ingest"):
            assert NIGHT_LOOP.index(later) > pause_at, f"{later} runs before the pause check"

    def test_pausing_exits_cleanly(self):
        """Exiting non-zero would open a failure issue every night while paused."""
        block = NIGHT_LOOP[NIGHT_LOOP.index(".paused"):]
        assert "exit 0" in block[: block.index("SMOKE=")]

    def test_the_sentinel_is_not_gitignored(self):
        """The pause must be visible in the repository, not just on a runner."""
        gitignore = (REPO_ROOT / ".gitignore").read_text("utf-8")
        assert ".paused" not in gitignore


class TestCrawlerIdentity:
    def test_user_agent_points_at_something_contactable(self):
        """A publisher who wants us to stop needs a route that is not a lawsuit."""
        match = re.search(r"\+(\S+?)\)", USER_AGENT)
        assert match, f"no +URL in {USER_AGENT!r}"
        url = match.group(1)
        assert url != "https://github.com", "the +URL must identify this project"
        assert "y-nihat/noiseless-news" in url

    def test_user_agent_still_names_the_tool_and_purpose(self):
        assert USER_AGENT.startswith("noiseless-news/")
        assert "verification" in USER_AGENT


class TestSourceHealthWorkflow:
    @pytest.fixture(scope="class")
    def workflow(self):
        return (REPO_ROOT / ".github" / "workflows" / "source-health.yml").read_text("utf-8")

    def test_runs_the_validator_that_nothing_ever_called(self, workflow):
        assert "validate-sources --live" in workflow

    def test_shares_the_nightly_concurrency_group(self, workflow):
        """It commits to main, so it must never race the night loop."""
        assert "group: nightly" in workflow
        assert "cancel-in-progress: false" in workflow

    def test_commits_only_data(self, workflow):
        assert "git add data/" in workflow
        assert "git add -A" not in workflow

    def test_is_scheduled_weekly(self, workflow):
        assert re.search(r"cron:\s*[\"']0 9 \* \* 1[\"']", workflow)


class TestRunbook:
    @pytest.mark.parametrize(
        "topic",
        ["Pause publishing", "Take an article down", "token stopped working",
         "A night went wrong", "Roll back a bad deploy", "If you are away"],
    )
    def test_covers_the_situations_that_need_a_procedure(self, topic):
        assert topic in RUNBOOK

    def test_pause_instructions_match_what_the_script_checks(self):
        """A runbook that drifts from the code is worse than no runbook."""
        assert "touch .paused" in RUNBOOK
        assert "-f .paused" in NIGHT_LOOP

    def test_names_the_secret_the_workflow_actually_reads(self):
        nightly = (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
        assert "CLAUDE_CODE_OAUTH_TOKEN" in RUNBOOK
        assert "CLAUDE_CODE_OAUTH_TOKEN" in nightly

    def test_points_at_files_that_exist(self):
        for referenced in ("data/ledger/night-stats.jsonl", "policy/verification.md",
                           "docker compose run --rm pipeline pytest"):
            assert referenced in RUNBOOK
