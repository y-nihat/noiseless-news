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
    (bindir / "gh").write_text(
        "#!/bin/sh\n"
        f'echo "$@" >> "{log}"\n'
        'if [ "$1" = "issue" ] && [ "$2" = "list" ]; then\n'
        f'  cat "{listing}"\n'
        "  exit 0\n"
        "fi\n"
        'exit "${GH_WRITE_EXIT:-0}"\n',
        encoding="utf-8",
    )
    (bindir / "gh").chmod(0o755)
    body = tmp_path / "body.md"
    body.write_text("the same four 403s, again\n", encoding="utf-8")
    return {"bin": bindir, "log": log, "listing": listing, "body": body}


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
