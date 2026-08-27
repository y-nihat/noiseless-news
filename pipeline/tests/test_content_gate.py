"""The nightly agent's commits are checked before anything is published.

`tests.yml` triggers `on: push`, but every push the night loop and the daytime
ingest make is authenticated with the workflow's own `GITHUB_TOKEN`, and GitHub
raises no workflow event for those. The consequence was measured on 2026-08-17:
of the 192 commits made since PR #27 merged — 34 of them new English articles —
the test suite had run on exactly none, while `Deploy site` published every one
of them. PR #27's stated purpose, testing the agent's commits like everything
else, was never once carried out.

So the gate runs inside the loop, where its result can still stop the deploy,
and these tests drive the real shell functions against a scratch repository
rather than grepping the script for its own source code.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from night_harness import REPORT, SCRIPT, drive, make_scratch, state

REPO_ROOT = Path(__file__).resolve().parents[2]
INGEST_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ingest.yml"


@pytest.fixture
def scratch(tmp_path: Path) -> dict[str, Path]:
    return make_scratch(tmp_path)


HELD_REPORT = (
    'echo "STATE gate_ok=$content_gate_ok trips=$gate_trips'
    ' guard_trips=$guard_trips push_failed=$push_failed push_blocked=$push_blocked'
    ' held=$held_now suite_ok=$suite_ok"'
)


class TestTheGateItself:
    """One predicate, three outcomes: clean, held, blocked.

    On 2026-08-18 the gate was all-or-nothing, and two articles without their
    evidence logs cost the whole night's seven stories their deploy while four
    later cycles ran without being told what to fix. Now a story with a
    per-story defect is held from the site by the build; the deploy proceeds
    without it; only more than MAX_HELD, or a validator that cannot run,
    withholds the deploy.
    """

    def test_a_clean_run_leaves_the_gate_open(self, scratch):
        result = drive(scratch, f"content_gate; {HELD_REPORT}")
        assert state(result)["gate_ok"] == "1"
        assert state(result)["held"] == "0"
        # Both counters are initialised before the source hook, so without this
        # the test passes with content_gate deleted from the script.
        assert "content: stub python" in result.stdout, "the gate never ran"

    def test_a_held_story_keeps_the_gate_open_and_names_the_slug(self, scratch):
        """The night of 2026-08-18, as it should have gone."""
        result = drive(scratch, f"STUB_HELD=harvey-tenet-launch content_gate; {HELD_REPORT}")
        assert state(result)["gate_ok"] == "1", "a held story withheld the deploy"
        assert state(result)["held"] == "1"
        assert "held from the site — harvey-tenet-launch" in result.stdout
        assert "deploy proceeds without them" in result.stdout
        assert "repair queued" in result.stdout

    def test_more_than_the_ceiling_blocks(self, scratch):
        """`validate-content --strict --max-held N` exits 2 past the ceiling."""
        result = drive(scratch, f"STUB_PYTHON_EXIT=2 content_gate; {HELD_REPORT}")
        assert state(result)["gate_ok"] == "0"
        assert "GATE BLOCKED — more than 3 stories held" in result.stdout

    def test_a_validator_that_cannot_run_blocks(self, scratch):
        """Fail closed: a build that cannot tell what is safe must not publish."""
        result = drive(scratch, f"STUB_PYTHON_EXIT=1 content_gate; {HELD_REPORT}")
        assert state(result)["gate_ok"] == "0"
        assert "validate-content itself failed" in result.stdout

    def test_a_validator_that_exits_zero_without_findings_is_not_trusted(self, scratch):
        """Exit 0 and no findings file means the command was not what we think."""
        result = drive(
            scratch,
            'cat > "$(dirname "$(command -v python)")/python" <<\'EOF\'\n'
            '#!/bin/sh\necho "stub python $*"\nexit 0\nEOF\n'
            f"content_gate; {HELD_REPORT}",
        )
        assert state(result)["gate_ok"] == "0"

    def test_a_read_back_that_prints_nothing_blocks(self, scratch):
        """The fail-open the `?` sentinel could not see.

        The reader prints `? -` when it catches an exception, and the guard
        tested for that literal `?`. An interpreter that dies before printing
        anything leaves $held_now empty instead: `[ "" -gt 0 ]` errors to
        stderr, and the gate used to fall through to content_gate_ok=1 — the
        exact opposite of "treat an unreadable file as held = unknown, which is
        blocked, not clean". CI run #62 recorded it live, as `gate_ok=1 held=`.
        """
        result = drive(
            scratch, f"STUB_READBACK_SILENT=1 content_gate; {HELD_REPORT}"
        )
        assert state(result)["gate_ok"] == "0", "an unreadable held set opened the gate"
        assert state(result)["trips"] == "1"
        assert "refusing to guess" in result.stdout

    def test_a_read_back_that_prints_nonsense_blocks_too(self, scratch):
        """Whatever is not a number is "held = unknown", not "held = none"."""
        result = drive(
            scratch,
            'cat > "$(dirname "$(command -v python)")/python" <<\'EOF\'\n'
            '#!/bin/sh\n'
            'if [ "$1" = "-" ]; then echo "banana -"; exit 0; fi\n'
            'json=""\n'
            'while [ $# -gt 0 ]; do [ "$1" = "--json" ] && json="$2"; shift; done\n'
            '[ -n "$json" ] && echo \'{"held": {}}\' > "$json"\n'
            'exit 0\nEOF\n'
            f"content_gate; {HELD_REPORT}",
        )
        assert state(result)["gate_ok"] == "0"
        assert "refusing to guess" in result.stdout

    def test_a_later_cycle_within_the_ceiling_reopens_it(self, scratch):
        """A cycle can repair what an earlier one broke; the site should catch up."""
        result = drive(
            scratch,
            f"STUB_PYTHON_EXIT=2 content_gate\ncontent_gate\n{HELD_REPORT}",
        )
        assert state(result)["gate_ok"] == "1", "the gate never reopens"
        assert "deploys resume" in result.stdout

    def test_the_test_suite_is_reported_and_never_a_deploy_predicate(self, scratch):
        """deploy.yml made this call first; the night was stricter than the deploy."""
        result = drive(scratch, f"export STUB_PYTEST_EXIT=1; content_gate; suite_check; {HELD_REPORT}")
        assert state(result)["gate_ok"] == "1", "a red unit test withheld the deploy"
        assert state(result)["suite_ok"] == "0"
        assert "reported only" in result.stdout


class TestWhatATrippedGateDoesToTheWork:
    """A failing gate must not cost the night its work — only its deploy.

    The loop's own comment says it plainly: a night whose work never reached
    origin is the worst outcome it can produce, because the runner is destroyed
    at the end of the job. The repository is the audit trail whether the night
    went well or badly, so the commit and the push still happen.
    """

    def test_the_work_is_still_committed_and_pushed(self, scratch):
        drive(
            scratch,
            'echo hi > content/new.md\n'
            'STUB_PYTHON_EXIT=2 commit_push "gated commit"\n'
            f"{HELD_REPORT}",
        )
        pushed = subprocess.run(
            ["git", "log", "--oneline", "-1", "--name-only", "origin/main"],
            cwd=scratch["work"], capture_output=True, text=True, check=True,
        ).stdout
        assert "gated commit" in pushed, "a tripped gate swallowed the night's work"
        assert "content/new.md" in pushed

    def test_the_push_is_not_reported_as_failed(self, scratch):
        """A blocked archive is a deploy problem, not a push problem."""
        result = drive(
            scratch,
            'echo hi > content/new.md\n'
            'STUB_PYTHON_EXIT=2 commit_push "gated commit"\n'
            f"{HELD_REPORT}",
        )
        assert state(result)["push_failed"] == "0"
        assert state(result)["gate_ok"] == "0"

    def test_the_gate_runs_on_every_commit_not_just_the_last(self, scratch):
        """Each cycle's commit is checked, so a bad one is caught when it lands.

        The content check echoes its findings into the cycle log — that echo is
        the observable proof the gate ran, since pytest's own output is
        redirected to a file.
        """
        result = drive(
            scratch,
            'echo a > content/a.md\ncommit_push "one"\n'
            'echo b > content/b.md\ncommit_push "two"\n'
            f"{REPORT}",
        )
        assert result.stdout.count("content: stub python") == 2


class TestTheGateIsWiredIntoTheLoop:
    @pytest.fixture(scope="class")
    def script(self) -> str:
        return SCRIPT.read_text(encoding="utf-8")

    def test_commit_push_calls_it_before_pushing(self, script):
        body = script.split("commit_push() {")[1].split("\n}")[0]
        assert body.index("content_gate") < body.index("git push"), (
            "the gate must run before the push, not after"
        )

    def test_it_is_strict_with_the_deploy_ceiling(self, script):
        """It used to run non-strict with its exit code discarded."""
        gate = script.split("content_gate() {")[1].split("\n}")[0]
        assert "validate-content --strict" in gate
        assert '--max-held "$MAX_HELD"' in gate

    def test_pytest_lives_in_suite_check_not_in_the_gate(self, script):
        gate = script.split("content_gate() {")[1].split("\n}")[0]
        suite = script.split("suite_check() {")[1].split("\n}")[0]
        assert "pytest" not in gate, "the unit tests are back inside the deploy predicate"
        assert "pytest -q" in suite

    def test_a_tripped_gate_withholds_the_deploy(self, script):
        dispatch = script.split('gh workflow run "Deploy site"')[0]
        guard = dispatch[dispatch.rindex("Per-cycle site deploy"):]
        assert 'content_gate_ok" -eq 1' in guard, (
            "the per-cycle deploy is dispatched regardless of the gate"
        )

    def test_a_tripped_gate_fails_the_job(self, script):
        tail = script.split("Loop supervisor footer")[1]
        assert 'if [ "$content_gate_ok" -eq 0 ]; then' in tail
        assert "exit 1" in tail.split('if [ "$content_gate_ok" -eq 0 ]; then')[1]

    def test_the_footer_records_the_gate(self, script):
        footer = script.split("Loop supervisor footer")[1].split("commit_push")[0]
        assert "Content gate:" in footer


class TestTheVisibleSignalOnMain:
    """The local gate is the real check; the dispatch is what the operator sees.

    Until this landed, `Tests` had produced no verdict on main since
    2026-08-07T09:12:48Z, and its silence was indistinguishable from success.
    """

    def test_the_night_dispatches_tests_after_its_final_push(self):
        script = SCRIPT.read_text(encoding="utf-8")
        assert 'gh workflow run "Tests" --ref main' in script
        footer_push = script.rindex('commit_push "Night loop footer')
        assert script.index('gh workflow run "Tests"') > footer_push, (
            "Tests must be dispatched after the last commit, or it tests stale main"
        )

    def test_the_daytime_ingest_dispatches_tests_too(self):
        workflow = INGEST_WORKFLOW.read_text(encoding="utf-8")
        assert 'gh workflow run "Tests" --ref main' in workflow
        assert workflow.index('gh workflow run "Tests"') > workflow.rindex("git push")


class TestTheSuiteReachesTheRepairQueue:
    """`suite_check` wrote its failures to a file nothing read again.

    From 2026-08-20 the repair queue printed "REPAIR QUEUE: empty — the archive
    is clean" on eight consecutive nights, in the same container where pytest
    was failing on two published articles. The archive tests' subject is
    content/ and data/ledger/ — the agent's own OWNED_PATHS — so that was the
    one class of failure the self-repair loop could have closed and did not.
    """

    def _brief(self, scratch, failures: str, existing: str = "REPAIR QUEUE: empty\n"):
        (scratch["state"] / "gate-pytest.txt").write_text(failures, encoding="utf-8")
        brief = scratch["state"] / "repair-1.md"
        brief.write_text(existing, encoding="utf-8")
        drive(scratch, f'append_suite_repairs "{brief}"')
        return brief.read_text(encoding="utf-8")

    def test_the_failures_are_appended_to_the_brief(self, scratch):
        text = self._brief(
            scratch,
            "FAILED pipeline/tests/test_dedup_repo_data.py::test_no_two_published"
            "_stories_strong_match_each_other - AssertionError\n"
            "1 failed, 447 passed\n",
        )
        assert "REPAIR QUEUE: empty" in text, "the archive's own queue was overwritten"
        assert "test_dedup_repo_data" in text
        assert "Unit suite" in text

    def test_it_says_which_failures_are_the_agent_s_to_fix(self, scratch):
        """A red pipeline test is the operator's; a red archive test is not."""
        text = self._brief(scratch, "FAILED pipeline/tests/test_x.py::test_y - boom\n")
        assert "content/ or data/" in text
        assert "operator" in text

    def test_a_green_suite_appends_nothing(self, scratch):
        text = self._brief(scratch, "447 passed in 20.1s\n")
        assert text.strip() == "REPAIR QUEUE: empty"

    def test_no_suite_output_at_all_appends_nothing(self, scratch):
        """Cycle 1 of a night has no previous cycle to have written one."""
        brief = scratch["state"] / "repair-1.md"
        brief.write_text("REPAIR QUEUE: empty\n", encoding="utf-8")
        drive(scratch, f'append_suite_repairs "{brief}"')
        assert brief.read_text(encoding="utf-8").strip() == "REPAIR QUEUE: empty"

    def test_it_does_not_decide_whether_a_cycle_runs(self):
        """Advisory only. Promoting a red suite to a run predicate would spend a
        cycle every night on pipeline tests the agent may not touch."""
        text = SCRIPT.read_text(encoding="utf-8")
        splice = text.split("append_suite_repairs \"$NIGHT_STATE_DIR")[0]
        assert "repairs_pending=$((" in splice, (
            "the suite is spliced in before repairs_pending is computed, so it "
            "now decides whether the agent runs at the story cap"
        )
