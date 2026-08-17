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


class TestTheGateItself:
    def test_a_clean_run_leaves_the_gate_open(self, scratch):
        result = drive(scratch, f"content_gate; {REPORT}")
        assert state(result)["gate_ok"] == "1"
        assert state(result)["trips"] == "0"
        # Both counters are initialised before the source hook, so without this
        # the test passes with content_gate deleted from the script.
        assert "content: stub python" in result.stdout, "the gate never ran"

    def test_a_failing_test_suite_trips_it(self, scratch):
        result = drive(scratch, f"STUB_PYTEST_EXIT=1 content_gate; {REPORT}")
        assert state(result)["gate_ok"] == "0"
        assert state(result)["trips"] == "1"
        assert "pytest FAILED" in result.stdout

    def test_a_blocking_content_finding_trips_it(self, scratch):
        """`validate-content --strict` exits 2 on a blocking finding."""
        result = drive(scratch, f"STUB_PYTHON_EXIT=2 content_gate; {REPORT}")
        assert state(result)["gate_ok"] == "0"
        assert "validate-content --strict FAILED" in result.stdout

    def test_a_later_clean_cycle_reopens_it(self, scratch):
        """A cycle can repair what an earlier one broke; the site should catch up."""
        result = drive(
            scratch,
            f"STUB_PYTEST_EXIT=1 content_gate\ncontent_gate\n{REPORT}",
        )
        assert state(result)["gate_ok"] == "1", "the gate never reopens"
        assert state(result)["trips"] == "1", "the trip must still be counted"
        assert "deploys resume" in result.stdout


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
            'STUB_PYTEST_EXIT=1 commit_push "gated commit"\n'
            f"{REPORT}",
        )
        pushed = subprocess.run(
            ["git", "log", "--oneline", "-1", "--name-only", "origin/main"],
            cwd=scratch["work"], capture_output=True, text=True, check=True,
        ).stdout
        assert "gated commit" in pushed, "a tripped gate swallowed the night's work"
        assert "content/new.md" in pushed

    def test_the_push_is_not_reported_as_failed(self, scratch):
        result = drive(
            scratch,
            'echo hi > content/new.md\n'
            'STUB_PYTEST_EXIT=1 commit_push "gated commit"\n'
            f"{REPORT}",
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

    def test_it_is_strict(self, script):
        """It used to run non-strict with its exit code discarded."""
        gate = script.split("content_gate() {")[1].split("\n}")[0]
        assert "validate-content --strict" in gate
        assert "pytest -q" in gate

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
