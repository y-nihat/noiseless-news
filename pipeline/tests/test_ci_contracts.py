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
