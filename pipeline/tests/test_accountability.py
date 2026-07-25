"""The site must say who publishes it, that no person wrote it, and how to complain.

An unattended pipeline publishes claims about named companies and identifiable
people, in two languages, into an archive that is designed never to be deleted.
Before these pages existed the site disclosed less about its own authorship than
it demanded of its sources, and `policy/verification.md §8` promised readers a
corrections page that was never built.
"""

from __future__ import annotations

import pytest

from noiseless.publish import (
    STRINGS,
    build_site,
    collect_corrections,
    latest_run_date,
    load_articles,
    parse_update_entry,
)

ARTICLE = """---
title: {title}
date: 2026-07-20
slug: {slug}
lang: {lang}
tldr: A summary.
sources:
  - name: Example
    url: https://example.com/story
claims:
  - text: "A claim"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: {updated}
---

## What happened

Body.
"""


def make_site(tmp_path, updated="[]", slug="a-story"):
    for lang in ("en", "tr"):
        d = tmp_path / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True)
        (d / f"{slug}.md").write_text(
            ARTICLE.format(title="A story", slug=slug, lang=lang, updated=updated),
            encoding="utf-8",
        )
    ledger = tmp_path / "data" / "ledger"
    ledger.mkdir(parents=True)
    (ledger / "run-report-2026-07-24-2235Z.md").write_text("report", encoding="utf-8")
    (ledger / "run-report-2026-07-25-2231Z.md").write_text("report", encoding="utf-8")
    build_site(tmp_path, tmp_path / "site")
    return tmp_path / "site"


class TestParseUpdateEntry:
    def test_untyped_entry_is_an_update(self):
        parsed = parse_update_entry("2026-07-14: added independent confirmation")
        assert parsed == {
            "kind": "update",
            "date": "2026-07-14",
            "text": "added independent confirmation",
        }

    @pytest.mark.parametrize(
        "entry",
        [
            "correction: 2026-07-14: the round was $200M",
            "2026-07-14: correction: the round was $200M",
            "Correction — 2026-07-14: the round was $200M",
        ],
    )
    def test_correction_is_recognised_in_either_order(self, entry):
        parsed = parse_update_entry(entry)
        assert parsed["kind"] == "correction"
        assert parsed["date"] == "2026-07-14"
        assert "200M" in parsed["text"]

    def test_turkish_correction_keyword(self):
        assert parse_update_entry("düzeltme: 2026-07-14: yanlıştı")["kind"] == "correction"

    def test_entry_without_a_date_still_parses(self):
        assert parse_update_entry("added a source")["text"] == "added a source"


class TestCorrectionsPage:
    def test_exists_in_both_languages(self, tmp_path):
        site = make_site(tmp_path)
        assert (site / "corrections.html").exists()
        assert (site / "tr" / "corrections.html").exists()

    def test_empty_state_explains_rather_than_looking_broken(self, tmp_path):
        site = make_site(tmp_path)
        page = (site / "corrections.html").read_text(encoding="utf-8")
        assert "No corrections have been issued yet" in page

    def test_only_corrections_are_listed_not_updates(self, tmp_path):
        updated = (
            '["2026-07-21: added a second source", '
            '"correction: 2026-07-22: the figure was wrong"]'
        )
        site = make_site(tmp_path, updated=updated)
        page = (site / "corrections.html").read_text(encoding="utf-8")
        assert "the figure was wrong" in page
        assert "added a second source" not in page

    def test_corrections_link_back_to_the_article(self, tmp_path):
        site = make_site(tmp_path, updated='["correction: 2026-07-22: wrong figure"]')
        page = (site / "corrections.html").read_text(encoding="utf-8")
        assert "articles/a-story.html" in page

    def test_collect_is_newest_first(self, tmp_path):
        make_site(
            tmp_path,
            updated=(
                '["correction: 2026-07-20: older", "correction: 2026-07-24: newer"]'
            ),
        )
        articles = load_articles(tmp_path / "content", "en")
        dates = [c["date"] for c in collect_corrections(articles)]
        assert dates == ["2026-07-24", "2026-07-20"]


class TestAboutPage:
    def test_exists_in_both_languages(self, tmp_path):
        site = make_site(tmp_path)
        assert (site / "about.html").exists()
        assert (site / "tr" / "about.html").exists()

    def test_discloses_machine_authorship_prominently(self, tmp_path):
        site = make_site(tmp_path)
        page = (site / "about.html").read_text(encoding="utf-8")
        assert "No person reviews an article before it goes live" in page

    def test_defines_every_verdict_the_site_renders(self, tmp_path):
        """A badge a reader cannot decode is decoration, not verification."""
        site = make_site(tmp_path)
        page = (site / "about.html").read_text(encoding="utf-8")
        for label in STRINGS["en"]["verdicts"].values():
            assert label in page

    def test_turkish_about_is_localized_not_english(self, tmp_path):
        site = make_site(tmp_path)
        page = (site / "tr" / "about.html").read_text(encoding="utf-8")
        assert "Hiçbir haber yayına girmeden önce" in page
        assert "No person reviews" not in page


class TestFooterAndNav:
    @pytest.mark.parametrize(
        "page", ["index.html", "about.html", "corrections.html", "articles/a-story.html"]
    )
    def test_every_page_carries_disclosure_and_a_contact_route(self, tmp_path, page):
        site = make_site(tmp_path)
        html = (site / page).read_text(encoding="utf-8")
        assert "written and verified by AI agents" in html
        assert "issues/new" in html
        assert "github.com/y-nihat" in html

    @pytest.mark.parametrize(
        "page,prefix",
        [("index.html", ""), ("articles/a-story.html", "../")],
    )
    def test_nav_links_resolve_from_every_depth(self, tmp_path, page, prefix):
        site = make_site(tmp_path)
        html = (site / page).read_text(encoding="utf-8")
        assert f'href="{prefix}about.html"' in html
        assert f'href="{prefix}corrections.html"' in html
        assert (site / page).parent.joinpath(f"{prefix}about.html").resolve().exists()

    def test_footer_states_when_the_pipeline_last_ran(self, tmp_path):
        """A site that has stopped running should say so rather than look current."""
        site = make_site(tmp_path)
        assert "2026-07-25" in (site / "index.html").read_text(encoding="utf-8")

    def test_last_run_date_reads_the_newest_report(self, tmp_path):
        make_site(tmp_path)
        assert latest_run_date(tmp_path / "data") == "2026-07-25"

    def test_last_run_is_omitted_when_there_are_no_reports(self, tmp_path):
        assert latest_run_date(tmp_path / "nothing") == ""
