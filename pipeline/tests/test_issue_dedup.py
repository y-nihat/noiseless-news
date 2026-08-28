"""One thread per recurring condition, and no alarm that can go off silently.

`source-health.yml` opened a fresh issue every Monday with no dedup search. One
unchanged fact — the same four HTTP 403s — produced #19 (2026-07-27), #20
(2026-08-03) and #31 (2026-08-10), byte-identical, uncommented, unlabelled, all
three still open twenty days later. Meanwhile the step that decides whether to
raise the alarm at all ran under `set +e` and derived its verdict from counting
`[FAIL]` lines, so a crash inside the validator — which emits no `[FAIL]` lines
— read as zero failures, opened nothing, and left a green tick.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
FLAG_ISSUE = REPO_ROOT / ".github" / "scripts" / "flag_issue.sh"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "source-health.yml"

# The three open issues this exists to stop a fourth of.
OPEN_ISSUES = """[
  {"number": 31, "title": "Source health: failing feeds 2026-08-10"},
  {"number": 20, "title": "Source health: failing feeds 2026-08-03"},
  {"number": 19, "title": "Source health: failing feeds 2026-07-27"},
  {"number": 7,  "title": "Something else entirely"}
]"""


@pytest.fixture
def gh_stub(tmp_path: Path) -> dict[str, Path]:
    """A `gh` that records its argv and serves a canned issue list."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "gh.log"
    listing = tmp_path / "issues.json"
    listing.write_text(OPEN_ISSUES, encoding="utf-8")
    closed = tmp_path / "closed.json"
    closed.write_text("[]", encoding="utf-8")
    (bindir / "gh").write_text(
        "#!/bin/sh\n"
        f'echo "$@" >> "{log}"\n'
        'if [ "$1" = "issue" ] && [ "$2" = "list" ]; then\n'
        '  case "$*" in\n'
        f'    *"--state closed"*) cat "{closed}" ;;\n'
        f'    *) cat "{listing}" ;;\n'
        "  esac\n"
        "  exit 0\n"
        "fi\n"
        'if [ "$1" = "issue" ] && [ "$2" = "reopen" ]; then\n'
        '  exit "${GH_REOPEN_EXIT:-0}"\n'
        "fi\n"
        'if [ "$1" = "issue" ] && [ "$2" = "create" ]; then\n'
        '  echo "https://github.com/y-nihat/noiseless-news/issues/99"\n'
        "fi\n"
        'if [ "$1" = "issue" ] && [ "$2" = "edit" ]; then\n'
        '  exit "${GH_EDIT_EXIT:-0}"\n'
        "fi\n"
        'exit "${GH_WRITE_EXIT:-0}"\n',
        encoding="utf-8",
    )
    (bindir / "gh").chmod(0o755)
    body = tmp_path / "body.md"
    body.write_text("the same four 403s, again\n", encoding="utf-8")
    return {"bin": bindir, "log": log, "listing": listing, "closed": closed,
            "body": body}


def flag(gh_stub, prefix: str, title: str, env: dict | None = None):
    return subprocess.run(
        ["bash", str(FLAG_ISSUE), prefix, title, str(gh_stub["body"])],
        capture_output=True,
        text=True,
        timeout=60,
        env={"PATH": f"{gh_stub['bin']}:/usr/local/bin:/usr/bin:/bin", **(env or {})},
    )


def calls(gh_stub) -> list[str]:
    if not gh_stub["log"].exists():
        return []
    return gh_stub["log"].read_text(encoding="utf-8").splitlines()


class TestWhenTheThreadAlreadyExists:
    def test_it_comments_instead_of_opening_a_fourth_issue(self, gh_stub):
        result = flag(gh_stub, "Source health: failing feeds",
                      "Source health: failing feeds 2026-08-17")
        assert result.returncode == 0, result.stderr
        assert any(c.startswith("issue comment") for c in calls(gh_stub))
        assert not any(c.startswith("issue create") for c in calls(gh_stub)), (
            "a fourth identical issue was opened"
        )

    def test_it_picks_the_oldest_open_thread_not_the_newest(self, gh_stub):
        """Week-on-week comparison only works if everything lands in one place."""
        flag(gh_stub, "Source health: failing feeds", "irrelevant")
        comment = next(c for c in calls(gh_stub) if c.startswith("issue comment"))
        assert comment.split()[2] == "19", f"commented on the wrong thread: {comment}"

    def test_an_unrelated_open_issue_is_not_mistaken_for_the_thread(self, gh_stub):
        result = flag(gh_stub, "Nightly run failed", "Nightly run failed 2026-08-17")
        assert any(c.startswith("issue create") for c in calls(gh_stub))
        assert result.returncode == 0


class TestWhenThereIsNoThreadYet:
    def test_it_opens_one(self, gh_stub):
        gh_stub["listing"].write_text("[]", encoding="utf-8")
        result = flag(gh_stub, "Source health: failing feeds",
                      "Source health: failing feeds 2026-08-17")
        assert result.returncode == 0
        assert any(c.startswith("issue create") for c in calls(gh_stub))

    def test_an_unreadable_listing_still_files_something(self, gh_stub):
        """Losing the alarm is worse than duplicating it."""
        gh_stub["listing"].write_text("not json at all", encoding="utf-8")
        result = flag(gh_stub, "Source health: failing feeds", "a title")
        assert result.returncode == 0
        assert any(c.startswith("issue create") for c in calls(gh_stub))


class TestAClosedThreadIsReopened:
    """Closing is how an operator says "read", not "never tell me again".

    `flag_issue.sh` searched only OPEN issues, so closing the source-health
    thread on 2026-08-28 would have had the next Monday open a fresh one and
    restart from empty the week-on-week record its own body instructs the
    reader to make — the churn this script exists to stop, by a different door.
    """

    CLOSED = """[
      {"number": 34, "title": "Source health: failing feeds 2026-08-17"},
      {"number": 31, "title": "Source health: failing feeds 2026-08-10"},
      {"number": 20, "title": "Source health: failing feeds 2026-08-03"},
      {"number": 19, "title": "Source health: failing feeds 2026-07-27"}
    ]"""

    def _only_closed(self, gh_stub):
        gh_stub["listing"].write_text("[]", encoding="utf-8")
        gh_stub["closed"].write_text(self.CLOSED, encoding="utf-8")

    def test_it_reopens_instead_of_opening_a_new_one(self, gh_stub):
        self._only_closed(gh_stub)
        result = flag(gh_stub, "Source health: failing feeds", "a title")
        assert result.returncode == 0, result.stderr
        assert any(c.startswith("issue reopen 34") for c in calls(gh_stub)), calls(gh_stub)
        assert any(c.startswith("issue comment 34") for c in calls(gh_stub))
        assert not any(c.startswith("issue create") for c in calls(gh_stub))

    def test_it_reopens_the_most_recent_not_the_oldest(self, gh_stub):
        """#19, #20 and #31 are the duplicates from before this script existed.
        Resurrecting #19 from 2026-07-27 would be worse than opening a new one."""
        self._only_closed(gh_stub)
        flag(gh_stub, "Source health: failing feeds", "a title")
        assert any(c.startswith("issue reopen 34") for c in calls(gh_stub))
        for stale in ("19", "20", "31"):
            assert not any(c.startswith(f"issue reopen {stale}") for c in calls(gh_stub))

    def test_an_open_thread_still_wins_over_a_closed_one(self, gh_stub):
        gh_stub["closed"].write_text(self.CLOSED, encoding="utf-8")
        flag(gh_stub, "Source health: failing feeds", "a title")
        assert any(c.startswith("issue comment 19") for c in calls(gh_stub))
        assert not any(c.startswith("issue reopen") for c in calls(gh_stub))

    def test_a_refused_reopen_still_files_the_alarm(self, gh_stub):
        """Losing the alarm is worse than a noisy one."""
        self._only_closed(gh_stub)
        result = flag(gh_stub, "Source health: failing feeds", "a title",
                      env={"GH_REOPEN_EXIT": "1"})
        assert result.returncode == 0
        assert any(c.startswith("issue create") for c in calls(gh_stub))

    def test_an_unrelated_closed_thread_is_not_reopened(self, gh_stub):
        self._only_closed(gh_stub)
        flag(gh_stub, "Test suite red on main", "Test suite red on main 2026-08-28")
        assert not any(c.startswith("issue reopen") for c in calls(gh_stub))
        assert any(c.startswith("issue create") for c in calls(gh_stub))

    def test_a_reopened_thread_is_assigned_too(self, gh_stub):
        self._only_closed(gh_stub)
        flag(gh_stub, "Source health: failing feeds", "a title",
             env={"GITHUB_REPOSITORY": "y-nihat/noiseless-news"})
        assert any("issue edit 34 --add-assignee y-nihat" in c for c in calls(gh_stub))


class TestTheAlarmIsAddressedToSomebody:
    """A filed alarm that reaches nobody is the failure mode this exists for.

    On GitHub an issue reaches a person through assignment, an @-mention or
    prior participation. A label subscribes nobody, and neither does owning the
    repository: issue #37 carried a red test suite in its body and all seven of
    its comments for eight days, unassigned, and reached nobody.
    """

    OWNER = {"GITHUB_REPOSITORY": "y-nihat/noiseless-news"}

    def test_a_new_thread_is_assigned_to_the_repository_owner(self, gh_stub):
        gh_stub["listing"].write_text("[]", encoding="utf-8")
        result = flag(gh_stub, "Tests red", "Tests red 2026-08-28", env=self.OWNER)
        assert result.returncode == 0
        assert any("--add-assignee y-nihat" in c for c in calls(gh_stub)), calls(gh_stub)

    def test_an_existing_thread_is_assigned_too(self, gh_stub):
        """The thread that needed this most was opened before anyone thought to,
        and a comment on an unassigned issue notifies nobody either."""
        flag(gh_stub, "Source health: failing feeds", "a title", env=self.OWNER)
        assert any("issue edit 19 --add-assignee y-nihat" in c for c in calls(gh_stub))

    def test_a_refused_assignment_still_leaves_the_alarm_filed(self, gh_stub):
        """Losing the alarm to fix its addressing would be the wrong trade."""
        gh_stub["listing"].write_text("[]", encoding="utf-8")
        result = flag(
            gh_stub, "Tests red", "a title", env={**self.OWNER, "GH_EDIT_EXIT": "1"}
        )
        assert result.returncode == 0
        assert any(c.startswith("issue create") for c in calls(gh_stub))

    def test_outside_actions_it_files_without_assigning(self, gh_stub):
        """`set -u` turns a bare ${GITHUB_REPOSITORY%%/*} into an abort, which
        would take every local and test invocation of the script with it."""
        gh_stub["listing"].write_text("[]", encoding="utf-8")
        result = flag(gh_stub, "Tests red", "a title")
        assert result.returncode == 0, result.stderr
        assert any(c.startswith("issue create") for c in calls(gh_stub))
        assert not any("add-assignee" in c for c in calls(gh_stub))


class TestWhenGitHubRefuses:
    def test_a_failed_comment_falls_back_to_creating(self, gh_stub):
        result = flag(gh_stub, "Source health: failing feeds", "a title",
                      env={"GH_WRITE_EXIT": "1"})
        assert any(c.startswith("issue comment") for c in calls(gh_stub))
        assert any(c.startswith("issue create") for c in calls(gh_stub))
        assert result.returncode == 1, "filing nothing must not look like success"

    def test_a_missing_body_file_is_refused_rather_than_filed_empty(self, gh_stub):
        result = subprocess.run(
            ["bash", str(FLAG_ISSUE), "prefix", "title", "/nonexistent/body.md"],
            capture_output=True, text=True, timeout=60,
            env={"PATH": f"{gh_stub['bin']}:/usr/local/bin:/usr/bin:/bin"},
        )
        assert result.returncode == 2
        assert not calls(gh_stub)


class TestTheWeeklyCheckCannotSucceedSilently:
    @pytest.fixture(scope="class")
    def steps(self) -> list[dict]:
        return yaml.safe_load(WORKFLOW_PATH.read_text("utf-8"))["jobs"]["check"]["steps"]

    @pytest.fixture(scope="class")
    def text(self) -> str:
        return WORKFLOW_PATH.read_text("utf-8")

    def test_the_check_step_demands_the_validator_ran_to_the_end(self, steps):
        check = next(s for s in steps if s.get("id") == "check")
        assert "live check done — " in check["run"], (
            "nothing asserts the validator finished; a crash reads as zero failures"
        )
        assert "exit 1" in check["run"]

    def test_a_crashed_check_is_reported_as_its_own_condition(self, steps):
        names = [s.get("name") for s in steps]
        assert "Flag a broken check" in names
        broken = next(s for s in steps if s.get("name") == "Flag a broken check")
        assert broken["if"] == "failure()"

    def test_the_alarm_goes_through_the_deduplicating_script(self, text):
        assert "flag_issue.sh" in text
        assert "gh issue create" not in text, (
            "source-health still opens issues directly, which is how three "
            "identical ones ended up open"
        )

    def test_the_failing_feeds_flag_is_not_raised_on_an_unset_count(self, steps):
        """An unset output is not the same as a count of zero."""
        flagger = next(s for s in steps if s.get("name") == "Flag failing sources")
        assert "steps.check.outputs.failures != ''" in flagger["if"]

    def test_the_evidence_is_committed_even_when_the_check_dies(self, steps):
        commit = next(s for s in steps if s.get("name") == "Commit the health report")
        assert commit.get("if") == "always()"

    def test_the_sentinel_is_a_line_the_validator_really_prints(self, steps):
        """A grep for a string nothing emits would fail every week instead."""
        check = next(s for s in steps if s.get("id") == "check")
        run_py = (REPO_ROOT / "pipeline" / "noiseless" / "run.py").read_text("utf-8")
        assert "live check done — " in check["run"]
        assert "live check done — " in run_py, (
            "the workflow greps for a sentinel run.py no longer prints"
        )


class TestEveryScheduledJobLeavesATrace:
    """A red badge is not a report.

    Of the twelve failures in this repository's history, four were in workflows
    with no failure handler: two daytime ingests (a server-side ref rejection
    that lost the capture, and a run GitHub never allocated a runner for) and
    two Pages deploys. Both deploys were dispatched by github-actions[bot],
    which notifies nobody at all, so they sat red for nine days having produced
    no issue, no comment and no notification.
    """

    HANDLERS = {
        "ingest.yml": ("ingest", "Say so if the capture failed"),
        "deploy.yml": ("build-deploy", "Say so if the deploy failed"),
        "nightly.yml": ("scan", "Open failure issue"),
        "source-health.yml": ("check", "Flag a broken check"),
    }

    @pytest.mark.parametrize("workflow,job_and_step", sorted(HANDLERS.items()))
    def test_it_has_a_failure_handler(self, workflow, job_and_step):
        job, step_name = job_and_step
        steps = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        )["jobs"][job]["steps"]
        handler = next((s for s in steps if s.get("name") == step_name), None)
        assert handler is not None, f"{workflow} has no failure handler"
        assert handler["if"] == "failure()"

    @pytest.mark.parametrize("workflow,job_and_step", sorted(HANDLERS.items()))
    def test_the_handler_is_the_last_step(self, workflow, job_and_step):
        """`if: failure()` is evaluated in step order and cannot see ahead."""
        job, step_name = job_and_step
        steps = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        )["jobs"][job]["steps"]
        assert steps[-1].get("name") == step_name, (
            f"{workflow}'s handler cannot see the steps after it"
        )

    @pytest.mark.parametrize("workflow", sorted(HANDLERS))
    def test_it_can_actually_open_an_issue(self, workflow):
        """A handler without the permission fails silently at the worst moment."""
        parsed = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        )
        assert parsed["permissions"].get("issues") == "write", (
            f"{workflow} files an issue it has no permission to file"
        )

    @pytest.mark.parametrize("workflow", ["ingest.yml", "deploy.yml", "source-health.yml"])
    def test_repeat_failures_land_in_one_thread(self, workflow):
        text = (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        assert "flag_issue.sh" in text, (
            f"{workflow} opens a fresh issue per failure — see #19/#20/#31"
        )


class TestTheHandlersActuallyRun:
    """Execute each handler's shell body against a stub `gh`.

    A failure handler only ever runs on a day that is already going badly, so a
    typo in one is invisible until precisely the moment it matters. These render
    the workflow expressions to placeholders and run the rest for real.
    """

    HANDLERS = [
        ("ingest.yml", "ingest", "Say so if the capture failed", "Daytime ingest failed"),
        ("deploy.yml", "build-deploy", "Say so if the deploy failed", "Site deploy failed"),
    ]

    @pytest.mark.parametrize("workflow,job,step_name,prefix", HANDLERS)
    def test_the_body_runs_and_files_an_issue(
        self, workflow, job, step_name, prefix, tmp_path
    ):
        steps = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        )["jobs"][job]["steps"]
        body = next(s for s in steps if s.get("name") == step_name)["run"]
        # GitHub substitutes these before the shell sees them; bash would read
        # "${{" as a bad substitution.
        body = re.sub(r"\$\{\{[^}]*\}\}", "PLACEHOLDER", body)

        bindir = tmp_path / "bin"
        bindir.mkdir()
        log = tmp_path / "gh.log"
        (bindir / "gh").write_text(
            f'#!/bin/sh\necho "$@" >> "{log}"\n'
            '[ "$1" = "issue" ] && [ "$2" = "list" ] && echo "[]"\nexit 0\n',
            encoding="utf-8",
        )
        (bindir / "gh").chmod(0o755)

        result = subprocess.run(
            ["bash", "-c", body], cwd=REPO_ROOT, capture_output=True, text=True,
            timeout=60,
            env={"PATH": f"{bindir}:/usr/local/bin:/usr/bin:/bin", "HOME": str(tmp_path)},
        )
        assert result.returncode == 0, (
            f"{workflow}'s failure handler is itself broken:\n{result.stderr}"
        )
        calls = log.read_text(encoding="utf-8") if log.exists() else ""
        assert "issue create" in calls, f"{workflow} filed nothing: {calls!r}"
        assert prefix in calls


class TestTheCheckStepAsItWillActuallyRun:
    """The YAML's own shell body, executed against a good and a crashing validator.

    The silent-success path was never hypothetical: it just never happened to
    fire in the three runs the workflow has had.
    """

    @pytest.fixture
    def harness(self, tmp_path: Path):
        bindir = tmp_path / "bin"
        bindir.mkdir()
        body = yaml.safe_load(WORKFLOW_PATH.read_text("utf-8"))["jobs"]["check"]["steps"]
        run = next(s for s in body if s.get("id") == "check")["run"]

        def go(validator_stdout: str, validator_exit: int):
            (bindir / "python").write_text(
                f"#!/bin/sh\ncat <<'EOF'\n{validator_stdout}\nEOF\nexit {validator_exit}\n",
                encoding="utf-8",
            )
            (bindir / "python").chmod(0o755)
            output = tmp_path / "github_output"
            output.write_text("", encoding="utf-8")
            result = subprocess.run(
                ["bash", "-c", run],
                capture_output=True, text=True, timeout=60,
                env={"PATH": f"{bindir}:/usr/bin:/bin",
                     "GITHUB_OUTPUT": str(output)},
            )
            return result, output.read_text(encoding="utf-8")

        return go

    def test_a_clean_run_reports_no_failures_and_succeeds(self, harness):
        result, outputs = harness("[ok  ] OpenAI News: 20 entries\nlive check done — 0 failures", 0)
        assert result.returncode == 0, result.stderr
        assert "failures=0" in outputs

    def test_failing_feeds_are_counted(self, harness):
        result, outputs = harness(
            "[FAIL] xAI News: HTTP 403\n[FAIL] Import AI: HTTP 403\n"
            "live check done — 2 failures",
            2,
        )
        assert result.returncode == 0
        assert "failures=2" in outputs

    def test_a_crash_no_longer_reads_as_a_clean_bill_of_health(self, harness):
        """No [FAIL] lines and no sentinel: the old step called this zero failures."""
        result, outputs = harness("Traceback (most recent call last):\n  boom", 1)
        assert result.returncode != 0, (
            "a crashed validator still produced a green step and no alarm"
        )
        assert "failures=" not in outputs, (
            "an unset count is safer than a fabricated zero"
        )
