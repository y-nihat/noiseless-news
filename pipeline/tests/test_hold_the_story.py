"""Hold the story, not the night.

On the night of 2026-08-18 the agent published two articles without their
evidence logs. The content gate caught it — and, being all-or-nothing, withheld
the entire night's seven stories from the site and failed the job over two
missing JSON files, while four later cycles ran without ever being told what to
repair. Nothing unauditable reached the public; nothing valid did either.

The design that replaced it: a per-story defect HOLDS that story from the site
at build time (a stub at its URL, absent from index/feed/sitemap), the rest of
the night publishes, a ceiling bounds how many may be held before the build is
refused, and the same predicate runs at all three gates so they cannot
disagree. Per-item quarantine with a bound is how dead-letter queues, test
quarantine and per-item CMS publication states all work; this is that.
"""

from __future__ import annotations

import io
import json
import re
from contextlib import redirect_stdout
from pathlib import Path

import pytest
import yaml
from conftest import write_twins

from noiseless.publish import build_site, withheld_stories
from noiseless.validate_content import (
    MAX_ANNOTATIONS,
    MAX_HELD_DEFAULT,
    Finding,
    github_annotations,
    held_slugs,
    main,
    validate,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

ARTICLE = """---
title: Story {slug}
slug: {slug}
date: 2026-07-10
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


def write_story(repo: Path, slug: str, *, evidence_log: bool = True,
                ledger: bool = True, turkish: bool = True) -> None:
    for lang in ("en", "tr") if turkish else ("en",):
        d = repo / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(ARTICLE.format(slug=slug, lang=lang), encoding="utf-8")
    write_twins(repo, slug)
    if not evidence_log:
        (repo / "data" / "verified" / f"{slug}.json").unlink()
    if not ledger:
        (repo / "data" / "ledger" / f"{slug}.json").unlink()


def run_main(repo: Path, **kwargs) -> tuple[int, str]:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main(repo, **{"strict": True, "warn_as_error": False, **kwargs})
    return code, buffer.getvalue()


class TestTheEvidenceLogBar:
    """"The file exists" was the whole test. It audits nothing."""

    def test_a_missing_log_is_an_error(self, tmp_path):
        write_story(tmp_path, "s", evidence_log=False)
        assert "evidence-log" in {f.check for f in validate(tmp_path) if f.level == "ERROR"}

    def test_an_unreadable_log_is_an_error(self, tmp_path):
        write_story(tmp_path, "s")
        (tmp_path / "data" / "verified" / "s.json").write_text("{truncated", encoding="utf-8")
        found = [f for f in validate(tmp_path) if f.check == "evidence-log"]
        assert found and "not readable" in found[0].detail

    def test_a_log_with_no_claims_is_an_error(self, tmp_path):
        """The empty file a rushed agent would drop in to get past a check."""
        write_story(tmp_path, "s")
        (tmp_path / "data" / "verified" / "s.json").write_text('{"slug": "s"}', encoding="utf-8")
        found = [f for f in validate(tmp_path) if f.check == "evidence-log"]
        assert found and "no claims" in found[0].detail

    def test_a_real_log_passes(self, tmp_path):
        write_story(tmp_path, "s")
        assert not [f for f in validate(tmp_path) if f.level == "ERROR"]

    def test_findings_carry_the_english_articles_path(self, tmp_path):
        write_story(tmp_path, "s", evidence_log=False)
        found = next(f for f in validate(tmp_path) if f.check == "evidence-log")
        assert found.path == "content/articles/en/2026/07/s.md"
        assert found.fix.startswith("write data/verified/<slug>.json")


class TestTheCeiling:
    def test_without_a_ceiling_any_error_blocks(self, tmp_path):
        write_story(tmp_path, "s", evidence_log=False)
        code, _ = run_main(tmp_path)
        assert code == 2

    def test_within_the_ceiling_is_deployable(self, tmp_path):
        for slug in ("a", "b"):
            write_story(tmp_path, slug, evidence_log=False)
        write_story(tmp_path, "good")
        code, out = run_main(tmp_path, max_held=MAX_HELD_DEFAULT)
        assert code == 0
        assert "held from the site: a (evidence-log), b (evidence-log)" in out
        assert "2 held" in out
        assert "deployable" in out

    def test_past_the_ceiling_blocks(self, tmp_path):
        for slug in ("a", "b", "c", "d"):
            write_story(tmp_path, slug, evidence_log=False)
        code, out = run_main(tmp_path, max_held=MAX_HELD_DEFAULT)
        assert code == 2
        assert "4 held" in out

    def test_the_ceiling_is_exactly_the_boundary(self, tmp_path):
        for slug in ("a", "b", "c"):
            write_story(tmp_path, slug, evidence_log=False)
        assert run_main(tmp_path, max_held=3)[0] == 0
        assert run_main(tmp_path, max_held=2)[0] == 2

    def test_a_clean_archive_says_nothing_about_holds(self, tmp_path):
        write_story(tmp_path, "good")
        code, out = run_main(tmp_path, max_held=MAX_HELD_DEFAULT)
        assert code == 0
        assert "held from the site" not in out
        assert "0 held" in out


class TestGitHubAnnotations:
    def test_one_warning_per_held_story_pointing_at_the_file(self, tmp_path):
        write_story(tmp_path, "s", evidence_log=False)
        _, out = run_main(tmp_path, max_held=3, github=True)
        lines = [l for l in out.splitlines() if l.startswith("::")]
        assert lines == [
            "::warning file=content/articles/en/2026/07/s.md,title=content gate::"
            "s held from the site — evidence-log: no data/verified entry — "
            "the article's verdicts cannot be audited"
        ]

    def test_errors_when_blocked(self, tmp_path):
        for slug in ("a", "b", "c", "d"):
            write_story(tmp_path, slug, evidence_log=False)
        _, out = run_main(tmp_path, max_held=3, github=True)
        assert "::error" in out
        assert "the build is refused" in out

    def test_capped_at_what_github_keeps(self):
        findings = [
            Finding("ERROR", "evidence-log", f"s{i:02d}", "x", f"content/articles/en/s{i:02d}.md")
            for i in range(MAX_ANNOTATIONS + 4)
        ]
        lines = github_annotations(findings, blocked=False)
        assert len(lines) == MAX_ANNOTATIONS + 1
        assert "and 4 more held" in lines[-1]


class TestTheJsonHandoff:
    """What the supervisor reads back, and the repair queue is built from."""

    def test_lists_held_slugs_with_their_fix(self, tmp_path):
        write_story(tmp_path, "s", evidence_log=False)
        out = tmp_path / "findings.json"
        run_main(tmp_path, max_held=3, json_path=out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert sorted(data["held"]) == ["s"]
        assert data["held"]["s"][0]["check"] == "evidence-log"
        assert "verification actually performed" in data["held"]["s"][0]["fix"]
        assert data["blocked"] is False
        assert data["max_held"] == 3

    def test_blocked_is_recorded(self, tmp_path):
        for slug in ("a", "b", "c", "d"):
            write_story(tmp_path, slug, evidence_log=False)
        out = tmp_path / "findings.json"
        run_main(tmp_path, max_held=3, json_path=out)
        assert json.loads(out.read_text(encoding="utf-8"))["blocked"] is True


class TestTheBuildHoldsTheStory:
    def test_the_held_story_is_absent_everywhere_but_its_own_url(self, tmp_path):
        write_story(tmp_path, "shipped-story")
        write_story(tmp_path, "held-story", evidence_log=False)
        counts = build_site(tmp_path, tmp_path / "site")
        assert counts == {"en": 1, "tr": 1, "held": 1}
        site = tmp_path / "site"
        for page in ("index.html", "feed.xml", "sitemap.xml", "tr/index.html", "tr/feed.xml"):
            text = (site / page).read_text(encoding="utf-8")
            assert "held-story" not in text, f"{page} still lists the held story"
            assert "shipped-story" in text, f"{page} lost the good story too"
        assert (site / "articles" / "held-story.html").exists(), "a shared link would 404"

    def test_the_stub_asserts_nothing_and_is_noindex(self, tmp_path):
        write_story(tmp_path, "bad", evidence_log=False)
        build_site(tmp_path, tmp_path / "site")
        for lang_dir in ("", "tr/"):
            page = (tmp_path / "site" / lang_dir / "articles" / "bad.html").read_text("utf-8")
            assert 'name="robots" content="noindex"' in page
            assert "Story bad" not in page, "the headline leaked into the stub"
            assert "A claim." not in page
            assert "example.com/bad" not in page
            assert "A short summary" not in page
            assert ("Temporarily withheld" in page) or ("Geçici olarak bekletiliyor" in page)

    def test_a_missing_turkish_twin_holds_the_english_article(self, tmp_path):
        write_story(tmp_path, "solo", turkish=False)
        build_site(tmp_path, tmp_path / "site")
        assert "solo" not in (tmp_path / "site" / "index.html").read_text("utf-8")

    def test_the_held_set_is_the_validators_error_set(self, tmp_path):
        write_story(tmp_path, "a", evidence_log=False)
        write_story(tmp_path, "b", ledger=False)
        write_story(tmp_path, "c")
        held = withheld_stories(tmp_path)
        assert sorted(held) == ["a", "b"]
        assert sorted(held) == sorted(held_slugs(validate(tmp_path)))

    def test_a_validator_crash_aborts_the_build_and_keeps_the_old_site(self, tmp_path, monkeypatch):
        """Fail closed: a build that cannot tell what is safe must not publish."""
        write_story(tmp_path, "good")
        out = tmp_path / "site"
        build_site(tmp_path, out)
        marker = out / "marker.txt"
        marker.write_text("previous build", encoding="utf-8")

        import noiseless.validate_content as vc

        def boom(_):
            raise RuntimeError("validator exploded")

        # publish.withheld_stories imports `validate` lazily by name from this
        # module, so patching the module attribute is what it sees.
        monkeypatch.setattr(vc, "validate", boom)
        with pytest.raises(RuntimeError):
            build_site(tmp_path, out)
        assert marker.exists(), "a failed build replaced the previous site"


class TestOnePredicateAtThreeGates:
    """deploy.yml, tests.yml and the night loop must never disagree."""

    def _flags(self, text: str) -> set[str]:
        # Only command lines: deploy.yml also quotes the command in an issue body.
        return set(re.findall(
            r'^\s*(?:run:\s*|-\s*run:\s*)?PYTHONPATH=pipeline python -m noiseless\.run '
            r'validate-content --strict\s*(?:\\\n\s*)?--max-held (\S+)',
            text, re.MULTILINE,
        ))

    def test_all_three_pass_the_same_ceiling(self):
        deploy = (REPO_ROOT / ".github/workflows/deploy.yml").read_text("utf-8")
        tests = (REPO_ROOT / ".github/workflows/tests.yml").read_text("utf-8")
        loop = (REPO_ROOT / ".github/scripts/night_loop.sh").read_text("utf-8")
        assert self._flags(deploy) == {"3"}
        assert self._flags(tests) == {"3"}
        assert self._flags(loop) == {'"$MAX_HELD"'}
        assert re.search(r"^MAX_HELD=3\b", loop, re.MULTILINE)
        assert MAX_HELD_DEFAULT == 3

    def test_the_deploy_still_checks_before_it_builds(self):
        steps = yaml.safe_load(
            (REPO_ROOT / ".github/workflows/deploy.yml").read_text("utf-8")
        )["jobs"]["build-deploy"]["steps"]
        runs = [s.get("run", "") for s in steps]
        checked = next(i for i, r in enumerate(runs) if "validate-content --strict" in r)
        published = next(i for i, r in enumerate(runs) if "run publish" in r)
        assert checked < published
