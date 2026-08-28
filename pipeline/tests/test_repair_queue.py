"""Close the loop: detection becomes a repair instruction the next cycle acts on.

The night of 2026-08-18: the gate tripped in cycle 2 on two articles committed
without their evidence logs, and cycles 3, 4, 5 and 6 each ran a fresh agent
session that was never told. The finding lived only in the supervisor's stdout,
which the agent does not read.

Three mechanisms here, each tested against the real code rather than by string:
the repair brief the next cycle's prompt opens with (recomputed from the tree,
so it needs no state file and carries across nights); the pre-commit hook that
refuses an article whose twins are not in the index, scoped to the agent's
process through git's documented GIT_CONFIG_COUNT runtime config; and the
supervisor splicing the brief into the prompt and running a cycle for it even
at the story cap.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import write_twins
from night_harness import SCRIPT, drive, make_scratch

from noiseless.validate_content import check_staged, repair_brief

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / ".github" / "hooks" / "pre-commit"
CYCLE_PROMPT = REPO_ROOT / ".github" / "cycle-prompt.md"

ARTICLE = """---
title: Story {slug}
slug: {slug}
date: 2026-08-18
lang: {lang}
tldr: A short summary.
sources:
  - url: https://example.com/{slug}
    name: Example
    tier: 0
claims:
  - text: A claim.
    type: fact
    verdict: confirmed
    evidence: [1]
---

Body of {slug}.
"""


def _git(*args, cwd, env=None, check=True):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                          check=check, env=env)


def write_story(repo: Path, slug: str, *, evidence_log=True, ledger=True, turkish=True):
    for lang in ("en", "tr") if turkish else ("en",):
        d = repo / "content" / "articles" / lang / "2026" / "08"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(ARTICLE.format(slug=slug, lang=lang), encoding="utf-8")
    write_twins(repo, slug)
    if not evidence_log:
        (repo / "data" / "verified" / f"{slug}.json").unlink()
    if not ledger:
        (repo / "data" / "ledger" / f"{slug}.json").unlink()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A git repo with the pipeline importable and one clean published story."""
    _git("init", "-q", "-b", "main", ".", cwd=tmp_path)
    _git("config", "user.email", "t@example.invalid", cwd=tmp_path)
    _git("config", "user.name", "t", cwd=tmp_path)
    write_story(tmp_path, "seed-story")
    _git("add", "-A", cwd=tmp_path)
    _git("commit", "-q", "-m", "seed", cwd=tmp_path)
    return tmp_path


class TestTheRepairBrief:
    def test_a_clean_archive_yields_a_one_line_reminder(self, repo):
        text, count = repair_brief(repo)
        assert count == 0
        assert text.startswith("REPAIR QUEUE: empty")
        assert "validate-content --strict" in text

    def test_a_held_story_is_listed_with_its_check_and_its_fix(self, repo):
        write_story(repo, "held-one", evidence_log=False)
        text, count = repair_brief(repo, today="2026-08-19")
        assert count == 1
        assert "`held-one` (evidence-log)" in text
        assert "FIX (evidence-log): write data/verified/held-one.json" in text
        assert "verification actually performed" in text
        assert "commit as `Repair: held-one`" in text

    def test_it_says_when_the_story_was_first_published(self, repo):
        write_story(repo, "held-one", evidence_log=False)
        _git("add", "-A", cwd=repo)
        _git("commit", "-q", "-m", "publish held-one", cwd=repo,
             env={"GIT_AUTHOR_DATE": "2026-08-18T22:56:00Z",
                  "GIT_COMMITTER_DATE": "2026-08-18T22:56:00Z",
                  "PATH": "/usr/bin:/bin", "HOME": str(repo)})
        text, _ = repair_brief(repo, today="2026-08-19")
        assert "first published 2026-08-18" in text
        assert "SECOND-NIGHT RULE" not in text

    def test_the_second_night_rule_appears_after_two_nights(self, repo):
        write_story(repo, "held-one", evidence_log=False)
        _git("add", "-A", cwd=repo)
        _git("commit", "-q", "-m", "publish held-one", cwd=repo,
             env={"GIT_AUTHOR_DATE": "2026-08-16T22:56:00Z",
                  "GIT_COMMITTER_DATE": "2026-08-16T22:56:00Z",
                  "PATH": "/usr/bin:/bin", "HOME": str(repo)})
        text, _ = repair_brief(repo, today="2026-08-19")
        assert "SECOND-NIGHT RULE applies" in text

    def test_it_forbids_fabricating_the_log(self, repo):
        write_story(repo, "held-one", evidence_log=False)
        text, _ = repair_brief(repo)
        assert "Never write an evidence log from the article text" in text
        assert "never a stub" in text
        assert "do not withdraw for lack of time" in text

    def test_the_cli_exits_two_when_non_empty(self, repo):
        from noiseless.validate_content import main

        write_story(repo, "held-one", evidence_log=False)
        assert main(repo, strict=False, warn_as_error=False, brief=True) == 2
        (repo / "data" / "verified" / "held-one.json").write_text(
            (repo / "data" / "verified" / "seed-story.json").read_text("utf-8"), "utf-8"
        )
        assert main(repo, strict=False, warn_as_error=False, brief=True) == 0


class TestTheStagedCheck:
    """`validate-content --staged`: the index, not the tree."""

    def test_an_article_whose_log_is_on_disk_but_not_staged_is_refused(self, repo):
        write_story(repo, "new-one")
        _git("add", "content", "data/ledger", cwd=repo)      # NOT data/verified
        found = check_staged(repo)
        assert [f.check for f in found] == ["evidence-log"]
        assert found[0].slug == "new-one"

    def test_the_full_bundle_passes(self, repo):
        write_story(repo, "new-one")
        _git("add", "-A", cwd=repo)
        assert check_staged(repo) == []

    def test_another_slugs_defect_does_not_block_this_commit(self, repo):
        """No incentive to un-publish someone else's story to land your own."""
        write_story(repo, "already-broken", evidence_log=False)
        _git("add", "-A", cwd=repo)
        _git("commit", "-q", "-m", "broken lands", cwd=repo)
        write_story(repo, "new-one")
        _git("add", "-A", cwd=repo)
        assert check_staged(repo) == []

    def test_a_report_only_commit_is_never_refused(self, repo):
        write_story(repo, "already-broken", evidence_log=False)
        _git("add", "-A", cwd=repo)
        _git("commit", "-q", "-m", "broken lands", cwd=repo)
        (repo / "data" / "ledger" / "run-report-2026-08-19.md").write_text("r", "utf-8")
        _git("add", "data/ledger/run-report-2026-08-19.md", cwd=repo)
        assert check_staged(repo) == []

    def test_a_turkish_twin_without_its_english_original_is_refused(self, repo):
        d = repo / "content" / "articles" / "tr" / "2026" / "08"
        d.mkdir(parents=True, exist_ok=True)
        (d / "orphan.md").write_text(ARTICLE.format(slug="orphan", lang="tr"), "utf-8")
        _git("add", "-A", cwd=repo)
        assert [f.check for f in check_staged(repo)] == ["bilingual-parity"]

    def test_a_missing_turkish_twin_is_refused(self, repo):
        write_story(repo, "solo", turkish=False)
        _git("add", "-A", cwd=repo)
        assert "bilingual-parity" in [f.check for f in check_staged(repo)]


def commit_with_hook(repo, msg):
    """A real `git commit` with the real hook wired in, as the agent runs it."""
    # The hook calls plain `python`; put the interpreter running this suite
    # first on PATH so CI's tool-cache python (with the pipeline's deps) is
    # what the hook finds, as it is on the runner where PATH already has it.
    env = {
        "PATH": f"{Path(sys.executable).parent}:{os.environ.get('PATH', '/usr/bin:/bin')}",
        "HOME": str(repo),
        "PYTHONPATH": str(REPO_ROOT / "pipeline"),
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.hooksPath",
        "GIT_CONFIG_VALUE_0": str(REPO_ROOT / ".github" / "hooks"),
    }
    return _git("commit", "-q", "-m", msg, cwd=repo, env=env, check=False)


class TestTheHook:
    """The real hook script, invoked by a real `git commit`."""

    def _commit_with_hook(self, repo, msg):
        return commit_with_hook(repo, msg)

    def test_it_is_executable(self):
        assert HOOK.exists()
        assert HOOK.stat().st_mode & 0o111, "the hook is not executable — git will skip it"

    def test_it_refuses_an_article_without_its_log_and_says_how_to_fix_it(self, repo):
        write_story(repo, "new-one", evidence_log=False)
        _git("add", "-A", cwd=repo)
        result = self._commit_with_hook(repo, "publish new-one")
        assert result.returncode != 0, "the commit went through"
        assert "commit refused" in result.stderr
        assert "write data/verified/new-one.json" in result.stderr
        assert _git("log", "--oneline", cwd=repo).stdout.count("\n") == 1, "it committed anyway"

    def test_it_accepts_the_bundle(self, repo):
        write_story(repo, "new-one")
        _git("add", "-A", cwd=repo)
        result = self._commit_with_hook(repo, "publish new-one")
        assert result.returncode == 0, result.stderr

    def test_it_does_not_run_without_the_process_scoped_config(self, repo):
        """The supervisor's own sweep commit must always land."""
        write_story(repo, "new-one", evidence_log=False)
        _git("add", "-A", cwd=repo)
        result = _git("commit", "-q", "-m", "sweep", cwd=repo, check=False)
        assert result.returncode == 0


class TestTheHookReAsksTheDuplicateGate:
    """§0a's gate necessarily runs before the story exists.

    It scores a working title against a primary URL. By the time the article is
    staged both have moved: on 2026-08-20 a citation of the matched story's own
    primary document was added during drafting — correctly, as the Tier-0 source
    behind a comparative claim — and turned a justified standalone into a pair
    the archive test rejects. CI stayed red for eight days over a decision that
    had already been made correctly and written down against different evidence.

    Asked again here, with the finished article's real title and real sources,
    the same decision can be recorded against what it will be judged on. Only
    the outcome the archive test would also reject refuses the commit.
    """

    TWIN = ARTICLE.replace("title: Story {slug}", "title: Story seed-story indeed")

    def _stage_twin(self, repo, *, follows=""):
        for lang in ("en", "tr"):
            body = self.TWIN.format(slug="twin-story", lang=lang)
            if follows:
                body = body.replace("lang: ", f"follows: {follows}\nlang: ", 1)
            (repo / "content" / "articles" / lang / "2026" / "08" / "twin-story.md")\
                .write_text(body, encoding="utf-8")
        write_twins(repo, "twin-story")
        _git("add", "-A", cwd=repo)

    def test_an_unlinked_duplicate_is_refused_with_the_three_outcomes(self, repo):
        self._stage_twin(repo)
        result = commit_with_hook(repo, "publish twin-story")
        assert result.returncode != 0, "the commit went through"
        combined = result.stdout + result.stderr
        assert "strongly matches seed-story" in combined, combined
        assert "same saga" in combined and "coincidental" in combined
        assert _git("log", "--oneline", cwd=repo).stdout.count("\n") == 1

    def _declare(self, repo, slug, *others):
        log = repo / "data" / "verified" / f"{slug}.json"
        data = json.loads(log.read_text(encoding="utf-8"))
        data["dedup_standalone"] = list(others)
        data["dedup_check"] = f"strong match against {others[0]}; coincidental"
        log.write_text(json.dumps(data), encoding="utf-8")

    def test_a_declared_standalone_lets_it_through(self, repo):
        self._stage_twin(repo)
        self._declare(repo, "twin-story", "seed-story")
        _git("add", "-A", cwd=repo)
        result = commit_with_hook(repo, "publish twin-story")
        assert result.returncode == 0, result.stdout + result.stderr

    def test_a_declaration_left_unstaged_does_not_count(self, repo):
        """The hook judges the index. A log edited on disk but never `git add`ed
        is exactly what `check_staged` was built to refuse, and this half has to
        agree with it or the two give different verdicts on the same commit."""
        self._stage_twin(repo)
        self._declare(repo, "twin-story", "seed-story")   # written, NOT staged
        result = commit_with_hook(repo, "publish twin-story")
        assert result.returncode != 0, "an unstaged declaration excused the commit"

    def test_a_ledger_only_commit_is_not_refused_for_someone_else_s_defect(self, repo):
        """No incentive to un-publish another story to land your own."""
        self._stage_twin(repo)
        _git("commit", "-q", "--no-verify", "-m", "twin lands unchecked", cwd=repo)
        (repo / "data" / "ledger" / "run-report-2026-08-28.md").write_text("r", "utf-8")
        _git("add", "data/ledger/run-report-2026-08-28.md", cwd=repo)
        assert commit_with_hook(repo, "report only").returncode == 0

    def test_a_follow_up_is_never_refused_for_sharing_its_saga(self, repo):
        """§8(b) members share sources by design."""
        self._stage_twin(repo, follows="seed-story")
        result = commit_with_hook(repo, "publish twin-story")
        assert result.returncode == 0, result.stdout + result.stderr

    def test_a_clean_unrelated_story_is_untouched(self, repo):
        write_story(repo, "new-one")
        _git("add", "-A", cwd=repo)
        result = commit_with_hook(repo, "publish new-one")
        assert result.returncode == 0, result.stdout + result.stderr


class TestTheSupervisorClosesTheLoop:
    @pytest.fixture
    def scratch(self, tmp_path):
        return make_scratch(tmp_path)

    def test_the_agent_process_is_given_the_hook_and_denied_the_bypasses(self):
        script = SCRIPT.read_text(encoding="utf-8")
        invocation = script.split("timeout \"$CYCLE_TIMEOUT\" claude -p")[0][-900:]
        invocation += script.split("timeout \"$CYCLE_TIMEOUT\" claude -p")[1][:900]
        assert "GIT_CONFIG_KEY_0=core.hooksPath" in invocation
        assert 'GIT_CONFIG_VALUE_0="$PWD/.github/hooks"' in invocation
        assert "--disallowedTools" in invocation
        assert "--no-verify" in invocation
        assert "hooksPath" in invocation.split("--disallowedTools")[1]

    def test_the_prompt_carries_the_repair_queue_as_step_zero(self):
        prompt = CYCLE_PROMPT.read_text(encoding="utf-8")
        assert "0. {{REPAIR_INSTRUCTION}}" in prompt
        assert prompt.index("{{REPAIR_INSTRUCTION}}") < prompt.index("1. WATCHING STORIES")

    def test_the_prompt_defines_finished_and_the_publish_order(self):
        prompt = CYCLE_PROMPT.read_text(encoding="utf-8")
        assert "except the stories in the\nREPAIR QUEUE" in prompt
        assert "PUBLISH CHECKLIST" in prompt
        assert prompt.index("data/verified/<slug>.json FIRST") < prompt.index("the EN article per")
        assert "THE REPOSITORY REFUSES a commit" in prompt

    def test_the_supervisor_splices_the_brief_and_leaves_no_placeholder(self, scratch):
        """Render one cycle's prompt through the real sed pipeline."""
        script = SCRIPT.read_text(encoding="utf-8")
        assert "{{REPAIR_INSTRUCTION}}" in script
        assert "r $NIGHT_STATE_DIR/repair-$cycle.md" in script
        # Drive the sed block for real against a fake brief.
        (scratch["state"] / "repair-1.md").write_text(
            "REPAIR QUEUE — 1 story(ies) are HELD.\n- `held-one` (evidence-log)\n", "utf-8"
        )
        result = drive(
            scratch,
            'cycle=1; MAX_CYCLES=6; CYCLE_DEADLINE=00:00; stories=4; remaining=12; '
            'MAX_SEARCHES=15; REPORT_FILE=r.md; sweep=s; watching=w; final_note=f\n'
            + script[script.index('  sed -e "s/{{CYCLE_NUMBER}}'):script.index('  if grep -q \'{{\' "$NIGHT_STATE_DIR/prompt-$cycle.md"')]
            + '\ngrep -c "{{" "$NIGHT_STATE_DIR/prompt-1.md" | sed "s/^/PLACEHOLDERS=/"\n'
            'grep -n "REPAIR QUEUE" "$NIGHT_STATE_DIR/prompt-1.md" | head -1 | sed "s/^/QUEUE_AT=/"\n'
            'grep -n "1. WATCHING STORIES" "$NIGHT_STATE_DIR/prompt-1.md" | head -1 | sed "s/^/WATCH_AT=/"',
        )
        assert "PLACEHOLDERS=0" in result.stdout, result.stdout[-800:]
        queue_at = int(result.stdout.split("QUEUE_AT=")[1].split(":")[0])
        watch_at = int(result.stdout.split("WATCH_AT=")[1].split(":")[0])
        assert queue_at < watch_at, "the repair queue is not step 0"

    def test_a_pending_repair_runs_a_cycle_even_at_the_story_cap(self):
        script = SCRIPT.read_text(encoding="utf-8")
        cap = script.split('log "night story cap reached')[0][-400:]
        assert '"$repairs_pending" -eq 0' in cap, (
            "the cap-skip does not yield to a non-empty repair queue"
        )
        assert script.index("validate-content --brief") < script.index('log "night story cap reached')

    def test_repairs_are_counted_for_the_footer(self):
        script = SCRIPT.read_text(encoding="utf-8")
        assert "grep -c '^Repair: '" in script
        assert "Repairs completed tonight: $repairs_done" in script
