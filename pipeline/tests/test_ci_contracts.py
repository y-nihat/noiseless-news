"""Agreements between files that no single file can keep on its own.

Every defect this suite was extended for after the branch review was a contract
between two places: a script writing one path and a workflow reading another, a
gate withholding a deploy that a different cron dispatched anyway, a step output
compared against a word nothing emits. Each half was correct; the pair was not.
Nothing here tests behaviour inside one file — these are the seams.
"""

from __future__ import annotations

import io
import json
import re
from contextlib import redirect_stdout
from pathlib import Path

import pytest
import yaml

from noiseless.run import main as run_main
from noiseless.sources import Source
from noiseless.validate import BLOCKED, FAIL, OK, STALE, CheckResult

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"
NIGHT_LOOP = (REPO_ROOT / ".github" / "scripts" / "night_loop.sh").read_text("utf-8")


def workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOW_DIR / name).read_text("utf-8"))


def step(name: str, job: str, step_name: str) -> dict:
    return next(
        s for s in workflow(name)["jobs"][job]["steps"] if s.get("name") == step_name
    )


class TestDispatchesNameSomethingReal:
    """`gh workflow run "X"` 404s silently if X is not a workflow's `name:`.

    Renaming `Deploy site` would leave the suite green while every deploy in the
    repository stopped happening.
    """

    def test_every_dispatch_target_exists(self):
        declared = {
            yaml.safe_load(p.read_text("utf-8")).get("name")
            for p in WORKFLOW_DIR.glob("*.yml")
        }
        sources = {p.name: p.read_text("utf-8") for p in WORKFLOW_DIR.glob("*.yml")}
        sources["night_loop.sh"] = NIGHT_LOOP
        found = False
        for where, text in sources.items():
            for target in re.findall(r'gh workflow run "([^"]+)"', text):
                found = True
                assert target in declared, (
                    f"{where} dispatches {target!r}, which no workflow is named"
                )
        assert found, "no dispatches found — did the call sites move?"


class TestWorkflowFilesAreValidated:
    """A YAML parser is not enough, and its silence was mistaken for a check.

    nightly.yml carried `runner.temp` in a job-level env block — a context
    GitHub does not allow there. PyYAML parsed it happily and the suite stayed
    green, while GitHub rejected the whole file: no "Nightly scan" workflow, no
    cron, and the only trace a zero-second run named `.github/workflows/
    nightly.yml`. The check that catches this has to know Actions' own rules.
    """

    def test_ci_runs_a_real_workflow_linter(self):
        steps = workflow("tests.yml")["jobs"]["pytest"]["steps"]
        linter = next((s for s in steps if s.get("name") == "Workflows are valid"), None)
        assert linter is not None, "nothing validates the workflow files"
        assert "actionlint" in linter["run"]

    def test_it_runs_before_anything_slower(self):
        """A file GitHub will reject should not wait behind a pip install."""
        names = [s.get("name") or s.get("uses") for s in
                 workflow("tests.yml")["jobs"]["pytest"]["steps"]]
        assert names.index("Workflows are valid") < names.index("Unit tests")

    def test_the_linter_is_pinned(self):
        steps = workflow("tests.yml")["jobs"]["pytest"]["steps"]
        run = next(s for s in steps if s.get("name") == "Workflows are valid")["run"]
        assert re.search(r"actionlint/releases/download/v\d+\.\d+\.\d+/", run), (
            "an unpinned linter changes what CI enforces without a commit"
        )

    def test_no_job_level_env_uses_a_context_that_is_unavailable_there(self):
        """The specific rule that broke nightly.yml, kept close to the incident."""
        allowed = {"github", "inputs", "matrix", "needs", "secrets", "strategy", "vars"}
        for path in WORKFLOW_DIR.glob("*.yml"):
            for job_name, job in yaml.safe_load(path.read_text("utf-8"))["jobs"].items():
                for key, value in (job.get("env") or {}).items():
                    for context in re.findall(r"\$\{\{\s*(\w+)\.", str(value)):
                        assert context in allowed, (
                            f"{path.name}:{job_name}.env.{key} uses the {context!r} "
                            f"context, which GitHub rejects at job level"
                        )


class TestTheGateOutputContract:
    """One word, written by a shell script and compared by a YAML expression."""

    def test_the_workflow_compares_against_a_word_the_script_emits(self):
        emitted = set(
            re.findall(
                r"echo (ok|failed)",
                NIGHT_LOOP.split("content_gate=")[1].split("\n")[0],
            )
        )
        assert emitted == {"ok", "failed"}, f"the script emits {emitted}"
        condition = step("nightly.yml", "scan", "Deploy the night's work")["if"]
        compared = re.search(r"content_gate != '([^']+)'", condition).group(1)
        assert compared in emitted, (
            f"the workflow withholds the deploy on {compared!r}, which the script never writes"
        )

    def test_the_step_that_writes_the_output_is_the_one_the_condition_names(self):
        condition = step("nightly.yml", "scan", "Deploy the night's work")["if"]
        referenced = re.search(r"steps\.(\w+)\.outputs", condition).group(1)
        loop = step("nightly.yml", "scan", "Night loop")
        assert loop.get("id") == referenced


class TestNoFixedScratchPaths:
    """The suite drives this script, and the gate runs the suite on the runner.

    With fixed paths under /tmp the tests wrote the live run's own state: the
    issue sentinel (disarming the failure handler for the night) and the
    night-start marker (unbinding the 12-story cap from cycle 2).
    """

    def test_the_supervisor_writes_nothing_to_a_fixed_tmp_path(self):
        code = "\n".join(
            line for line in NIGHT_LOOP.splitlines()
            if not line.lstrip().startswith("#")
        )
        offenders = [
            m for m in re.findall(r'[">\s](/tmp/[\w.$-]+)', code)
            if "NIGHT_STATE_DIR" not in m and not m.startswith("/tmp/night-$$")
        ]
        assert not offenders, f"fixed scratch paths remain: {offenders}"

    def test_the_workflow_scopes_the_directory_to_the_run(self):
        env = workflow("nightly.yml")["jobs"]["scan"]["env"]
        assert "github.run_id" in env["NIGHT_STATE_DIR"]

    def test_the_handler_reads_the_same_directory(self):
        handler = step("nightly.yml", "scan", "Open failure issue")
        assert "$NIGHT_STATE_DIR/issue-filed" in handler["run"]
        assert 'ISSUE_FILED="$NIGHT_STATE_DIR/issue-filed"' in NIGHT_LOOP


class TestEveryRouteToPublicationIsGated:
    """The night gate withholds its own deploys. Two other routes ignore it.

    `ingest.yml` dispatches Deploy site unconditionally on two daytime crons,
    and the gate deliberately does not block the commit, so main already carries
    the article: without a check at the deploy itself the site published exactly
    what the gate refused, eight to eleven hours later and silently.
    """

    def test_the_deploy_validates_the_archive_before_building_it(self):
        steps = workflow("deploy.yml")["jobs"]["build-deploy"]["steps"]
        runs = [s.get("run", "") for s in steps]
        checked = next(i for i, r in enumerate(runs) if "validate-content --strict" in r)
        published = next(i for i, r in enumerate(runs) if "run publish" in r)
        assert checked < published, "the site is built before the archive is checked"

    def test_it_is_the_content_check_and_not_the_test_suite(self):
        """A flaky unit test has no business freezing the public site."""
        steps = workflow("deploy.yml")["jobs"]["build-deploy"]["steps"]
        assert not any("pytest" in s.get("run", "") for s in steps)


class TestTheHealthReportMarksMatchTheirGrep:
    """`source-health.yml` counts failures by grepping the validator's own lines."""

    @pytest.fixture
    def rendered(self, monkeypatch) -> str:
        import noiseless.validate as validate

        def fake(sources):
            src = lambda n: Source(name=n, tier=2, type="rss", url="https://e.invalid/f")
            return [
                CheckResult(src("Fresh"), OK, "10 entries, newest 2026-08-17 (0d)"),
                CheckResult(src("Frozen"), STALE, "44 entries, newest 2025-09-23"),
                CheckResult(src("Broken"), FAIL, "HTTP 500"),
                CheckResult(src("Refused"), BLOCKED, "HTTP 403 — known block"),
            ]

        monkeypatch.setattr(validate, "check_all", fake)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            run_main(["validate-sources", "--live"])
        return buffer.getvalue()

    def test_the_grep_counts_the_two_that_need_attention(self, rendered):
        pattern = re.search(
            r"grep -cE '(\^\\\[\([A-Z|]+\)\\\])'",
            (WORKFLOW_DIR / "source-health.yml").read_text("utf-8"),
        )
        assert pattern, "the failure count no longer greps for marks"
        counted = [
            line for line in rendered.splitlines()
            if re.match(pattern.group(1).replace("\\[", r"\[").replace("\\]", r"\]"), line)
        ]
        assert len(counted) == 2, f"counted {counted} out of:\n{rendered}"
        assert any("Frozen" in line for line in counted)
        assert any("Broken" in line for line in counted)

    def test_a_known_block_is_reported_but_not_counted(self, rendered):
        assert "[BLOCKED] Refused" in rendered
        assert "0 failures" not in rendered
        assert "1 failures, 1 stale, 1 known blocks" in rendered

    def test_the_sentinel_the_workflow_waits_for_is_still_printed(self, rendered):
        assert any(
            line.startswith("live check done — ") for line in rendered.splitlines()
        )


class TestTheSourceStatusCommandIsWiredUp:
    """Only `report()` was ever called directly; the CLI path was untested."""

    def _stats(self, tmp_path: Path, counts: dict[str, int], days: int) -> Path:
        ledger = tmp_path / "ledger"
        ledger.mkdir()
        (ledger / "source_stats.jsonl").write_text(
            "".join(
                json.dumps({"run_at": f"2026-07-{d + 1:02d}T01:00:00+00:00",
                            "counts": counts}) + "\n"
                for d in range(days)
            ),
            encoding="utf-8",
        )
        return ledger

    def test_a_registered_block_does_not_reach_the_shell_as_a_failure(self, tmp_path, capsys):
        """Import AI carries runner_blocked, so its -1s are a recorded fact."""
        self._stats(tmp_path, {"Import AI": -1}, 20)
        code = run_main(["source-status", "--data-dir", str(tmp_path)])
        out = capsys.readouterr().out
        assert "[BLOCKED] Import AI" in out, out
        assert code == 0, "a known block must not make the weekly job go red"

    def test_the_data_dir_flag_is_honoured(self, tmp_path, capsys):
        self._stats(tmp_path, {"Techmeme": -1}, 20)
        code = run_main(["source-status", "--data-dir", str(tmp_path)])
        out = capsys.readouterr().out
        assert "[FLAG] Techmeme" in out, out
        assert code == 2, "a crossed threshold must reach the shell"

    def test_a_missing_data_dir_is_not_a_crash(self, tmp_path, capsys):
        code = run_main(["source-status", "--data-dir", str(tmp_path / "absent")])
        assert code == 0
        assert "no ingest runs recorded" in capsys.readouterr().out


class TestEveryWorkflowSaysSomethingWhenItFails:
    """A red run that notifies nobody is the same as no check at all.

    `Tests` was the only one of the five with no failure handler. It went red on
    main on 2026-08-20 and stayed red for 23 consecutive runs over 8 days,
    because every run of it is dispatched by github-actions[bot] and GitHub's
    Actions-failure notifications are actor-scoped: a bot-dispatched failure
    reaches no human however the repository is watched.
    """

    def _handlers(self, name: str) -> list[dict]:
        return [
            s
            for job in workflow(name)["jobs"].values()
            for s in job["steps"]
            if "failure()" in str(s.get("if", ""))
        ]

    @pytest.mark.parametrize(
        "name", ["tests.yml", "deploy.yml", "nightly.yml", "source-health.yml", "ingest.yml"]
    )
    def test_it_has_a_failure_handler(self, name):
        assert self._handlers(name), f"{name} goes red without telling anyone"

    @pytest.mark.parametrize(
        "name", ["tests.yml", "deploy.yml", "nightly.yml", "source-health.yml", "ingest.yml"]
    )
    def test_a_workflow_that_files_an_issue_may_write_issues(self, name):
        """The permission the handler needs, asserted where it is granted.

        The repository default is read-only. Without `issues: write` the whole
        handler still runs, `gh issue create` 403s, and flag_issue.sh takes its
        "could not file anything" path — a silent alarm that looks configured.
        """
        source = (WORKFLOW_DIR / name).read_text("utf-8")
        if "flag_issue.sh" not in source:
            pytest.skip(f"{name} does not file issues")
        granted = workflow(name).get("permissions") or {}
        assert granted.get("issues") == "write", (
            f"{name} calls flag_issue.sh but does not grant issues: write"
        )


class TestAFailingSuiteStillReportsTheRest:
    """One defect used to hide every other thing that was true.

    All 23 red runs skipped "Source registry parses", "Published content holds
    its invariants" and "Site builds from the real archive" — the steps that are
    a pull request's only content and build coverage, since deploy.yml does not
    run there.
    """

    LATER = [
        "Source registry parses",
        "Published content holds its invariants",
        "Site builds from the real archive",
    ]

    @pytest.mark.parametrize("step_name", LATER)
    def test_it_runs_even_when_the_suite_failed(self, step_name):
        condition = str(step("tests.yml", "pytest", step_name).get("if", ""))
        assert "cancelled()" in condition, (
            f"{step_name!r} is skipped by a failing suite; it does not depend on one"
        )

    @pytest.mark.parametrize("step_name", LATER)
    def test_it_does_not_run_without_its_dependencies(self, step_name):
        """`always()` would fire these three after a failed pip install too,
        producing three guaranteed import errors on top of the real one."""
        condition = str(step("tests.yml", "pytest", step_name).get("if", ""))
        assert "steps.deps" in condition, (
            f"{step_name!r} runs regardless of whether the install succeeded"
        )

    def test_the_step_it_depends_on_is_the_one_that_installs(self):
        steps = workflow("tests.yml")["jobs"]["pytest"]["steps"]
        deps = next((s for s in steps if s.get("id") == "deps"), None)
        assert deps is not None, "no step is id'd deps; the conditions above name nothing"
        assert "pip install" in deps["run"]

    def test_the_suite_keeps_its_own_output_for_the_handler(self):
        """The issue body quotes the FAILED lines, so they have to survive the
        step. `tee` in a pipeline also hides pytest's exit code without an
        explicit PIPESTATUS."""
        run = step("tests.yml", "pytest", "Unit tests")["run"]
        assert "tee" in run and "/tmp/pytest.txt" in run
        assert "PIPESTATUS" in run, "a piped pytest reports tee's exit code, not its own"
