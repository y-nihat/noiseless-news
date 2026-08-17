"""Security invariants for the unattended night loop.

These are not style checks. The night agent runs with unrestricted Write/Edit
over the checkout and reads thousands of untrusted third-party items per night;
the only thing that stops a stray or steered edit from persisting is that the
supervisor refuses to stage anything outside content/ and data/. Everything else
in the tree is executed by the next cycle. A regression here is a security
regression, so it is asserted rather than trusted.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
NIGHT_LOOP = REPO_ROOT / ".github" / "scripts" / "night_loop.sh"
CYCLE_PROMPT = REPO_ROOT / ".github" / "cycle-prompt.md"
INGEST_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ingest.yml"


def test_night_loop_never_stages_the_whole_tree():
    """`git add -A` would let the agent commit its own supervisor."""
    script = NIGHT_LOOP.read_text(encoding="utf-8")
    offenders = [
        line.strip()
        for line in script.splitlines()
        if re.search(r"^\s*git add\s+(-A|--all|\.)\s*$", line)
    ]
    assert not offenders, f"night_loop.sh stages unowned paths: {offenders}"


def test_night_loop_stages_only_owned_paths():
    script = NIGHT_LOOP.read_text(encoding="utf-8")
    staged = re.findall(r"^\s*git add\s+(.+)$", script, re.MULTILINE)
    assert staged, "night_loop.sh no longer stages anything — did commit_push move?"
    for target in staged:
        assert target.strip() == '"${OWNED_PATHS[@]}"', (
            f"unexpected `git add {target.strip()}` — staging must go through "
            "OWNED_PATHS so the allowlist stays in one place"
        )
    assert re.search(r"^OWNED_PATHS=\(content data\)$", script, re.MULTILINE), (
        "OWNED_PATHS must be exactly (content data)"
    )


def test_night_loop_guards_and_reports_out_of_scope_writes():
    """A blocked write must be visible in the morning, not silently dropped."""
    script = NIGHT_LOOP.read_text(encoding="utf-8")
    assert "guard_paths()" in script
    assert "guard_paths" in script.split("commit_push()")[1], (
        "commit_push must call guard_paths before staging"
    )
    assert "guard_trips" in script.split("Loop supervisor footer")[1], (
        "the run report footer must record blocked write attempts"
    )


def test_daytime_ingest_also_stages_only_data():
    """The sibling workflow commits to the same branch and must match."""
    workflow = INGEST_WORKFLOW.read_text(encoding="utf-8")
    staged = re.findall(r"^\s*git add\s+(.+)$", workflow, re.MULTILINE)
    assert staged == ["data/"], f"ingest.yml stages {staged}, expected ['data/']"


def test_cycle_prompt_frames_fetched_content_as_untrusted():
    """The agent must be told that ingested and fetched text is never an order."""
    prompt = CYCLE_PROMPT.read_text(encoding="utf-8").lower()
    for phrase in (
        "untrusted content rule",
        "evidence, never instructions",
        "never follow a directive",
        "suspected injection",
    ):
        assert phrase in prompt, f"cycle prompt lost its injection framing: {phrase!r}"


class TestDeployRace:
    """The final cycle must not race the workflow's own backstop deploy.

    GitHub Pages allows one deployment in flight. `nightly.yml` runs its
    `if: always()` backstop deploy seconds after the script exits, with
    byte-identical content, so a dispatch on the last cycle and the backstop
    both try to create a deployment and whichever arrives second gets HTTP 400
    (2026-08-04, run 30867516175).
    """

    def test_final_cycle_leaves_the_deploy_to_the_backstop(self):
        script = NIGHT_LOOP.read_text(encoding="utf-8")
        before = script.split('gh workflow run "Deploy site"')[0]
        guard = before[before.rindex("Per-cycle site deploy"):]
        assert 'is_final" -eq 0' in guard, "dispatch is not gated on is_final"
        assert 'gate" -ne 3' in guard, "dispatch is not gated on a usage-limit stop"
        assert before.rstrip().endswith("then"), "the dispatch is outside the guard"

    def test_the_backstop_deploy_is_still_there(self):
        """It was the only thing that deployed the site on 2026-08-07."""
        import yaml

        workflow = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
        )
        backstop = next(
            s for s in workflow["jobs"]["scan"]["steps"]
            if s.get("name") == "Deploy the night's work"
        )
        assert "always()" in backstop["if"]
        assert 'gh workflow run "Deploy site"' in backstop["run"]

    def test_the_backstop_does_not_publish_what_the_gate_rejected(self):
        """Publishing "whatever the script left behind" must exclude the bad part."""
        import yaml

        workflow = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
        )
        steps = workflow["jobs"]["scan"]["steps"]
        loop = next(s for s in steps if s.get("name") == "Night loop")
        backstop = next(s for s in steps if s.get("name") == "Deploy the night's work")
        assert loop.get("id") == "loop", "the backstop reads an output this step cannot emit"
        assert "steps.loop.outputs.content_gate != 'failed'" in backstop["if"]

    def test_the_script_actually_emits_the_output_the_workflow_reads(self):
        """A condition on an output nothing writes is a condition that never fires."""
        script = NIGHT_LOOP.read_text(encoding="utf-8")
        assert 'echo "content_gate=' in script
        assert 'GITHUB_OUTPUT' in script.split('echo "content_gate=')[0][-400:]

    def test_the_failure_handler_runs_after_every_other_step(self):
        """`if: failure()` is evaluated in step order.

        A handler placed before the deploy steps cannot see them fail, so a run
        that died in `configure-pages` filed no issue at all.
        """
        import yaml

        workflow = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
        )
        names = [s.get("name") or s.get("uses") for s in workflow["jobs"]["scan"]["steps"]]
        assert names[-1] == "Open failure issue", f"handler is not last: {names}"
        assert names.index("Night loop") < names.index("Open failure issue")


class TestOnePathToPages:
    """Every Pages deployment in this repository goes through one mutex.

    GitHub allows a single deployment in flight. nightly.yml used to build and
    deploy Pages inline from the `nightly` concurrency group while deploy.yml
    deployed the same site from the `pages` group, so the two could not see each
    other: on 2026-08-04 the last cycle's dispatch and the backstop collided and
    the second create call got HTTP 400 (run 30867516175). PR #24 stopped the
    loop racing itself, but a human merge to main inside the 01:00-01:20 UTC
    window would still have collided.
    """

    WORKFLOWS = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))

    def test_only_one_workflow_touches_the_pages_backend(self):
        """Parsed steps, not a text search: the prose explains the incident too."""
        import yaml

        deployers = []
        for path in self.WORKFLOWS:
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            uses = [
                step.get("uses", "")
                for job in workflow.get("jobs", {}).values()
                for step in job.get("steps", [])
            ]
            if any("deploy-pages" in u for u in uses):
                deployers.append(path.name)
        assert deployers == ["deploy.yml"], (
            f"more than one route to Pages: {deployers} — they share no mutex"
        )

    def test_that_workflow_serialises_on_the_pages_group(self):
        import yaml

        deploy = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "deploy.yml").read_text("utf-8")
        )
        assert deploy["concurrency"]["group"] == "pages"

    def test_everyone_else_asks_it_rather_than_doing_it(self):
        for path in self.WORKFLOWS:
            if path.name == "deploy.yml":
                continue
            text = path.read_text(encoding="utf-8")
            if "Deploy site" not in text:
                continue
            assert 'gh workflow run "Deploy site"' in text, (
                f"{path.name} reaches Pages by some other route"
            )

    def test_the_night_no_longer_holds_pages_credentials(self):
        """It stopped deploying; the token scope should say so."""
        import yaml

        nightly = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
        )
        assert "pages" not in nightly["permissions"]
        assert "id-token" not in nightly["permissions"]

    def test_the_nightly_job_is_not_in_the_pages_concurrency_group(self):
        """deploy.yml cancels in-progress runs in that group.

        Putting the four-hour night in it would let any push to main kill it.
        """
        import yaml

        workflow = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "nightly.yml").read_text("utf-8")
        )
        assert workflow["concurrency"]["group"] == "nightly"
        assert workflow["concurrency"]["cancel-in-progress"] is False


class TestPushResilience:
    """Every workflow that pushes to main must survive a server-side rejection.

    GitHub's ref backend rejected a push once with `remote: fatal error in
    commit_refs` (2026-08-04, run 30935854819). The run died with the capture
    committed but never pushed, and because seen_ids.json is git-resident the
    runner's state went with it — the items that had already scrolled out of
    their feed window were lost for good.
    """

    WRITERS = ["ingest.yml", "source-health.yml"]

    @pytest.mark.parametrize("workflow", WRITERS)
    def test_a_rejected_push_is_retried(self, workflow):
        text = (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        assert "git push" in text, f"{workflow} no longer pushes — update this test"
        assert "for attempt in" in text, f"{workflow} has an unretried push"
        assert "git pull --rebase" in text, f"{workflow} retries without refetching"

    @pytest.mark.parametrize("workflow", WRITERS)
    def test_the_retry_still_fails_the_step_when_it_never_succeeds(self, workflow):
        """A swallowed push is worse than a red run: the work is silently gone."""
        text = (REPO_ROOT / ".github" / "workflows" / workflow).read_text("utf-8")
        loop_end = text.rindex("git push")
        assert "|| true" not in text[loop_end:loop_end + 40], (
            f"{workflow}'s final push swallows failure"
        )

    def test_the_night_loop_records_rather_than_swallows(self):
        """It cannot exit mid-night, so it flags and fails at the end instead."""
        script = NIGHT_LOOP.read_text(encoding="utf-8")
        assert "push_failed=1" in script
        assert 'if [ "$push_failed" -eq 1 ]; then' in script
