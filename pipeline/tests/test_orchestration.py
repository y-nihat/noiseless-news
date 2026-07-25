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
