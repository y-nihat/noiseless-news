"""The path allowlist, asserted by behaviour rather than by string.

The night agent runs unattended with unrestricted Write/Edit over the whole
checkout and reads thousands of untrusted third-party items a night. Its only
legitimate output is content/ and data/. Everything else — this supervisor, the
result gate, the cycle prompt, the pipeline, the policy documents — is read back
and executed by the *next* cycle, with `CLAUDE_CODE_OAUTH_TOKEN` and a
`contents: write` token in scope.

The guard had one test, and it asserted that the string "guard_paths" appeared
in the script. It did. The guard also recovered with
`git checkout -- . ':(exclude)content' ':(exclude)data'`, which copies the index
into the working tree and never touches the index itself — so an edit the agent
had already staged was written back over the file, left staged, and committed
by the very next line. The guard logged the attempt and shipped it. These tests
run the real functions instead.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from night_harness import (
    ORIGINAL,
    OUT_OF_SCOPE,
    REPORT,
    SCRIPT,
    committed_content,
    drive,
    make_scratch,
    origin_content,
    pushed_files,
    state,
)

POISON = "#!/bin/sh\necho PWNED\n"


@pytest.fixture
def scratch(tmp_path: Path) -> dict[str, Path]:
    return make_scratch(tmp_path)


def _poison(scratch: dict[str, Path]) -> None:
    (scratch["work"] / OUT_OF_SCOPE).write_text(POISON, encoding="utf-8")


class TestAStagedOutOfScopeEdit:
    """The reproduction: the agent edits the supervisor and stages it itself."""

    def test_it_never_reaches_a_commit(self, scratch):
        _poison(scratch)
        drive(scratch, f'git add -A\ncommit_push "cycle artifacts"\n{REPORT}')
        assert committed_content(scratch, OUT_OF_SCOPE) == ORIGINAL, (
            "the guard logged the edit and committed it anyway"
        )

    def test_it_never_reaches_origin(self, scratch):
        """origin is what tomorrow's runner clones and executes."""
        _poison(scratch)
        drive(scratch, f'git add -A\ncommit_push "cycle artifacts"\n{REPORT}')
        assert origin_content(scratch, OUT_OF_SCOPE) == ORIGINAL

    def test_the_working_tree_is_restored_so_the_next_cycle_runs_the_real_script(
        self, scratch
    ):
        _poison(scratch)
        drive(scratch, f'git add -A\ncommit_push "cycle artifacts"\n{REPORT}')
        assert (scratch["work"] / OUT_OF_SCOPE).read_text(encoding="utf-8") == ORIGINAL

    def test_the_index_is_left_clean(self, scratch):
        """A staged stray survives into the *next* commit if it is only checked out.

        Observed between the guard and the commit: after `git commit` the index
        always matches HEAD, so a check placed there can never see this.
        """
        _poison(scratch)
        result = drive(
            scratch,
            'git add -A\nguard_paths\n'
            'echo "STAGED[$(git diff --cached --name-only)]"\n'
            f"{REPORT}",
        )
        assert "STAGED[]" in result.stdout, "the stray is still staged after the guard"

    def test_the_attempt_is_counted_and_reported(self, scratch):
        _poison(scratch)
        result = drive(scratch, f'git add -A\ncommit_push "cycle artifacts"\n{REPORT}')
        assert state(result)["guard_trips"] != "0", "a blocked write left no trace"
        assert "GUARD TRIPPED" in result.stdout

    def test_the_legitimate_work_in_the_same_commit_still_ships(self, scratch):
        """Blocking the stray must not cost the night its articles."""
        _poison(scratch)
        (scratch["work"] / "content" / "story.md").write_text("story\n", encoding="utf-8")
        drive(scratch, f'git add -A\ncommit_push "cycle artifacts"\n{REPORT}')
        pushed = pushed_files(scratch)
        assert "content/story.md" in pushed
        assert OUT_OF_SCOPE not in pushed


class TestAnUnstagedOutOfScopeEdit:
    """The case the old guard did handle. It must keep working."""

    def test_the_file_is_restored_and_nothing_is_committed(self, scratch):
        _poison(scratch)
        drive(scratch, f'commit_push "cycle artifacts"\n{REPORT}')
        assert committed_content(scratch, OUT_OF_SCOPE) == ORIGINAL
        assert (scratch["work"] / OUT_OF_SCOPE).read_text(encoding="utf-8") == ORIGINAL


class TestACommitTheAgentMadeItself:
    """`cycle-prompt.md` tells the agent to commit and push its own work.

    44 "Publish: …" commits on main were made that way, never passing through
    commit_push, so guard_paths never saw them. The push scope check covers
    everything waiting to go to origin, whoever committed it.
    """

    def test_the_push_is_refused(self, scratch):
        _poison(scratch)
        result = drive(
            scratch,
            'git add -A && git commit -q -m "agent self-commit"\n'
            'echo ok > content/story.md\n'
            f'commit_push "cycle artifacts"\n{REPORT}',
        )
        assert state(result)["push_blocked"] == "1"
        assert origin_content(scratch, OUT_OF_SCOPE) == ORIGINAL, (
            "a self-committed supervisor edit reached origin"
        )

    def test_a_stray_the_agent_pushed_itself_is_still_caught(self, scratch):
        """The baseline cannot be the upstream ref, because `git push` moves it.

        cycle-prompt.md tells the agent to push after each commit and it holds
        the same credential, so anchoring on `@{upstream}` meant the agent's own
        push advanced the goalposts and the check that exists for this case
        reported guard_trips=0 with the poisoned file already on origin.
        """
        _poison(scratch)
        result = drive(
            scratch,
            'git add -A && git commit -q -m "agent self-commit" && git push -q\n'
            'echo ok > content/story.md\n'
            f'commit_push "cycle artifacts"\n{REPORT}',
        )
        assert state(result)["push_blocked"] == "1", (
            "the agent pushed its own stray and the guard saw nothing"
        )
        assert state(result)["guard_trips"] != "0"

    def test_the_origin_check_sees_a_stray_that_is_already_pushed(self, scratch):
        """The guard can only refuse the next push; something must look at origin."""
        _poison(scratch)
        result = drive(
            scratch,
            'git add -A && git commit -q -m "agent self-commit" && git push -q\n'
            'git fetch -q origin main\n'
            'assert_push_scope FETCH_HEAD "already on origin" '
            '&& echo "ORIGIN_CLEAN" || echo "ORIGIN_DIRTY"\n'
            f'{REPORT}',
        )
        assert "ORIGIN_DIRTY" in result.stdout

    def test_the_night_then_fails_rather_than_reporting_success(self, scratch):
        script = SCRIPT.read_text(encoding="utf-8")
        tail = script.split("Loop supervisor footer")[1]
        assert 'if [ "$push_blocked" -eq 1 ]; then' in tail
        assert "exit 1" in tail.split('if [ "$push_blocked" -eq 1 ]; then')[1]

    def test_the_footer_says_which_it_was(self, scratch):
        """"Blocked" and "failed" are different mornings; the report must not blur them."""
        footer = SCRIPT.read_text(encoding="utf-8").split("Loop supervisor footer")[1]
        assert "BLOCKED (path allowlist)" in footer
        assert "FAILED" in footer


class TestTheCheckCannotFailOpen:
    def test_no_baseline_means_no_push(self, scratch):
        """An empty diff against nothing is not an all-clear."""
        result = drive(
            scratch,
            'NIGHT_BASE=""\n'
            'echo ok > content/story.md\n'
            f'commit_push "cycle artifacts"\n{REPORT}',
        )
        assert state(result)["push_blocked"] == "1"
        assert "no night baseline" in result.stdout


class TestTheAllowlistStaysInOnePlace:
    def test_the_guard_unstages_before_it_restores(self):
        """Order is the whole bug: checkout reads the index, reset writes it."""
        body = SCRIPT.read_text(encoding="utf-8").split("guard_paths() {")[1].split("\n}")[0]
        # Comments in here quote both commands while explaining the bug.
        code = "\n".join(
            line for line in body.splitlines() if not line.lstrip().startswith("#")
        )
        assert "git reset" in code, "the guard restores from an index it never reset"
        assert code.index("git reset") < code.index("git checkout")

    def test_ordinary_work_is_untouched_by_any_of_this(self, scratch):
        (scratch["work"] / "content" / "story.md").write_text("story\n", encoding="utf-8")
        (scratch["work"] / "data" / "ledger.json").write_text("{}\n", encoding="utf-8")
        result = drive(scratch, f'commit_push "cycle artifacts"\n{REPORT}')
        assert state(result)["guard_trips"] == "0"
        assert state(result)["push_blocked"] == "0"
        pushed = pushed_files(scratch)
        assert "content/story.md" in pushed and "data/ledger.json" in pushed
