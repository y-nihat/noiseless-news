"""Ordering the index by when a reader could first have seen a story.

`date` is the event date, and the index used to sort and byline on it. Because
verification often runs past the news cycle, 22 of 57 articles carried a date
earlier than their own publication day — by up to nine days — so they appeared
below stories the reader had already seen, on their own launch day. In-place
updates never resurfaced at all.
"""

from __future__ import annotations

import pytest

from noiseless.publish import Article, build_site, load_articles

ARTICLE = """---
title: {title}
date: {date}
{published_line}slug: {slug}
lang: {lang}
tldr: A summary.
sources:
  - name: Example
    url: https://example.com/{slug}
claims: []
updated: {updated}
---

Body.
"""


def write(tmp_path, slug, date, published=None, updated="[]", title=None):
    for lang in ("en", "tr"):
        d = tmp_path / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(
            ARTICLE.format(
                title=title or slug.replace("-", " "),
                date=date,
                published_line=f"published: {published}\n" if published else "",
                slug=slug,
                lang=lang,
                updated=updated,
            ),
            encoding="utf-8",
        )
    return tmp_path


def make(meta) -> Article:
    return Article(meta=meta, body_html="", lang="en")


class TestArticleDates:
    def test_published_defaults_to_the_event_date(self):
        assert make({"date": "2026-07-09"}).published == "2026-07-09"

    def test_published_overrides_when_present(self):
        article = make({"date": "2026-07-06", "published": "2026-07-14"})
        assert article.date == "2026-07-06"
        assert article.published == "2026-07-14"

    def test_last_touched_follows_the_newest_update(self):
        article = make(
            {
                "date": "2026-07-10",
                "published": "2026-07-10",
                "updated": ["2026-07-14: added detail", "2026-07-19: added more"],
            }
        )
        assert article.last_touched == "2026-07-19"

    def test_undated_update_entries_do_not_break_ordering(self):
        article = make({"date": "2026-07-10", "updated": ["added a source"]})
        assert article.last_touched == "2026-07-10"


class TestOrdering:
    def test_index_orders_by_publication_not_event_date(self, tmp_path):
        """The nine-day case: an old event verified today belongs at the top."""
        write(tmp_path, "old-event-new-story", "2026-07-02", published="2026-07-11")
        write(tmp_path, "recent-story", "2026-07-09")
        order = [a.slug for a in load_articles(tmp_path / "content", "en")]
        assert order == ["old-event-new-story", "recent-story"]

    def test_an_updated_article_resurfaces(self, tmp_path):
        write(tmp_path, "updated-story", "2026-07-10",
              updated='["2026-07-19: material new reporting"]')
        write(tmp_path, "quiet-story", "2026-07-15")
        order = [a.slug for a in load_articles(tmp_path / "content", "en")]
        assert order == ["updated-story", "quiet-story"]

    def test_same_day_order_is_deterministic_not_filename_luck(self, tmp_path):
        write(tmp_path, "zebra", "2026-07-10")
        write(tmp_path, "alpha", "2026-07-10")
        order = [a.slug for a in load_articles(tmp_path / "content", "en")]
        assert order == ["zebra", "alpha"], "expected reverse-slug tiebreak"


class TestRendering:
    def test_byline_shows_one_date_when_they_agree(self, tmp_path):
        write(tmp_path, "same-day", "2026-07-10")
        build_site(tmp_path, tmp_path / "site")
        page = (tmp_path / "site" / "articles" / "same-day.html").read_text("utf-8")
        assert "<time datetime='2026-07-10'>2026-07-10</time>" in page
        assert "Event" not in page

    def test_byline_shows_both_when_they_differ(self, tmp_path):
        write(tmp_path, "delayed", "2026-07-06", published="2026-07-14")
        build_site(tmp_path, tmp_path / "site")
        page = (tmp_path / "site" / "articles" / "delayed.html").read_text("utf-8")
        assert "Event 2026-07-06" in page
        assert "published 2026-07-14" in page

    def test_index_shows_the_publication_date(self, tmp_path):
        write(tmp_path, "delayed", "2026-07-06", published="2026-07-14")
        build_site(tmp_path, tmp_path / "site")
        index = (tmp_path / "site" / "index.html").read_text("utf-8")
        assert "<time class='date' datetime='2026-07-14'>2026-07-14</time>" in index
        assert "2026-07-06" not in index, "index must not show the event date"

    def test_updated_articles_get_a_chip_in_both_languages(self, tmp_path):
        write(tmp_path, "revised", "2026-07-10", updated='["2026-07-19: new reporting"]')
        build_site(tmp_path, tmp_path / "site")
        assert "updated 2026-07-19" in (tmp_path / "site" / "index.html").read_text("utf-8")
        assert "güncellendi 2026-07-19" in (
            tmp_path / "site" / "tr" / "index.html"
        ).read_text("utf-8")

    def test_no_chip_when_nothing_changed(self, tmp_path):
        write(tmp_path, "untouched", "2026-07-10")
        build_site(tmp_path, tmp_path / "site")
        assert "updated 2026" not in (tmp_path / "site" / "index.html").read_text("utf-8")


class TestRealArchive:
    def test_published_never_precedes_the_event(self):
        """A story cannot be published before the thing it reports happened."""
        from pathlib import Path

        repo = Path(__file__).resolve().parents[2]
        for lang in ("en", "tr"):
            for article in load_articles(repo / "content", lang):
                assert article.published >= article.date, (
                    f"{lang}/{article.slug}: published {article.published} "
                    f"precedes event {article.date}"
                )

    def test_language_pairs_agree_on_dates(self):
        from pathlib import Path

        repo = Path(__file__).resolve().parents[2]
        en = {a.slug: (a.date, a.published) for a in load_articles(repo / "content", "en")}
        tr = {a.slug: (a.date, a.published) for a in load_articles(repo / "content", "tr")}
        assert en == tr, "EN and TR disagree on date/published"
