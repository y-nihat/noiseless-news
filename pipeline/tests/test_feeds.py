"""Feeds, sitemap and the metadata that lets anyone find or follow the site.

The pipeline reads 48 feeds a night and published none. A reader who found the
site and liked it had no mechanism to be told about the next article except
remembering a github.io URL, and a shared link unfurled as a bare URL because
there were no Open Graph tags, no canonical and no per-language title.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest

from noiseless.publish import FEED_LIMIT, SITE_URL, build_site

ATOM = "{http://www.w3.org/2005/Atom}"

ARTICLE = """---
title: {title}
date: {date}
{published_line}slug: {slug}
lang: {lang}
tldr: A standalone summary of {slug}.
sources:
  - name: Example
    url: https://example.com/{slug}
claims: []
updated: {updated}
---

Body.
"""


def write(tmp_path, slug, date, published=None, updated="[]"):
    for lang in ("en", "tr"):
        d = tmp_path / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(
            ARTICLE.format(
                title=f"Story {slug}", date=date,
                published_line=f"published: {published}\n" if published else "",
                slug=slug, lang=lang, updated=updated,
            ),
            encoding="utf-8",
        )
    return tmp_path


@pytest.fixture
def site(tmp_path):
    write(tmp_path, "first-story", "2026-07-10")
    write(tmp_path, "second-story", "2026-07-06", published="2026-07-14")
    build_site(tmp_path, tmp_path / "site")
    return tmp_path / "site"


class TestAtomFeed:
    def test_written_for_both_languages(self, site):
        assert (site / "feed.xml").exists()
        assert (site / "tr" / "feed.xml").exists()

    def test_is_valid_atom(self, site):
        feed = ET.parse(site / "feed.xml").getroot()
        assert feed.tag == f"{ATOM}feed"
        assert feed.find(f"{ATOM}id") is not None
        assert feed.find(f"{ATOM}updated") is not None
        assert len(feed.findall(f"{ATOM}entry")) == 2

    def test_entries_are_ordered_by_publication_not_event_date(self, site):
        """A feed built on the event date would be wrong for 22 of 57 articles."""
        feed = ET.parse(site / "feed.xml").getroot()
        titles = [e.find(f"{ATOM}title").text for e in feed.findall(f"{ATOM}entry")]
        assert titles == ["Story second-story", "Story first-story"]

    def test_entry_timestamps_are_rfc3339(self, site):
        entry = ET.parse(site / "feed.xml").getroot().find(f"{ATOM}entry")
        assert entry.find(f"{ATOM}published").text == "2026-07-14T00:00:00Z"
        assert entry.find(f"{ATOM}updated").text == "2026-07-14T00:00:00Z"

    def test_entry_updated_follows_an_in_place_update(self, tmp_path):
        write(tmp_path, "revised", "2026-07-10", updated='["2026-07-19: new reporting"]')
        build_site(tmp_path, tmp_path / "site")
        entry = ET.parse(tmp_path / "site" / "feed.xml").getroot().find(f"{ATOM}entry")
        assert entry.find(f"{ATOM}updated").text == "2026-07-19T00:00:00Z"
        assert entry.find(f"{ATOM}published").text == "2026-07-10T00:00:00Z"

    def test_links_and_ids_are_absolute(self, site):
        entry = ET.parse(site / "feed.xml").getroot().find(f"{ATOM}entry")
        url = entry.find(f"{ATOM}id").text
        assert url.startswith(f"{SITE_URL}/articles/")
        assert entry.find(f"{ATOM}link").get("href") == url

    def test_turkish_feed_points_at_turkish_articles(self, site):
        entry = ET.parse(site / "tr" / "feed.xml").getroot().find(f"{ATOM}entry")
        assert entry.find(f"{ATOM}id").text.startswith(f"{SITE_URL}/tr/articles/")

    def test_summary_reuses_the_tldr_verbatim(self, site):
        entry = ET.parse(site / "feed.xml").getroot().find(f"{ATOM}entry")
        assert "A standalone summary of second-story" in entry.find(f"{ATOM}summary").text

    def test_feed_is_capped(self, tmp_path):
        for i in range(FEED_LIMIT + 5):
            write(tmp_path, f"story-{i:02d}", f"2026-07-{(i % 28) + 1:02d}")
        build_site(tmp_path, tmp_path / "site")
        feed = ET.parse(tmp_path / "site" / "feed.xml").getroot()
        assert len(feed.findall(f"{ATOM}entry")) == FEED_LIMIT


class TestSitemapAndRobots:
    def test_sitemap_is_valid_and_absolute(self, site):
        root = ET.parse(site / "sitemap.xml").getroot()
        locs = [loc.text for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        assert all(loc.startswith(SITE_URL) for loc in locs)
        assert f"{SITE_URL}/" in locs and f"{SITE_URL}/tr/" in locs

    def test_sitemap_lists_every_page_that_was_written(self, site):
        root = ET.parse(site / "sitemap.xml").getroot()
        locs = {
            loc.text.removeprefix(f"{SITE_URL}/")
            for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        }
        written = {
            str(p.relative_to(site)).replace("\\", "/")
            for p in site.rglob("*.html")
        }
        # index pages appear in the sitemap as directories, not as index.html
        written = {"" if w == "index.html" else w for w in written}
        written = {"tr/" if w == "tr/index.html" else w for w in written}
        assert written == locs

    def test_robots_points_at_the_sitemap(self, site):
        assert f"Sitemap: {SITE_URL}/sitemap.xml" in (site / "robots.txt").read_text()


class TestPageMetadata:
    def test_canonical_is_self_referential(self, site):
        page = (site / "articles" / "first-story.html").read_text(encoding="utf-8")
        assert f'<link rel="canonical" href="{SITE_URL}/articles/first-story.html">' in page

    def test_reciprocal_hreflang_on_both_editions(self, site):
        en = (site / "index.html").read_text(encoding="utf-8")
        tr = (site / "tr" / "index.html").read_text(encoding="utf-8")
        assert f'hreflang="tr" href="{SITE_URL}/tr/"' in en
        assert f'hreflang="en" href="{SITE_URL}/"' in tr
        assert f'hreflang="x-default" href="{SITE_URL}/"' in en
        assert f'hreflang="x-default" href="{SITE_URL}/"' in tr

    def test_editions_no_longer_share_a_title(self, site):
        """A bookmark or search result could not tell them apart before."""
        en = (site / "index.html").read_text(encoding="utf-8")
        tr = (site / "tr" / "index.html").read_text(encoding="utf-8")
        assert "<title>noiseless.news — verified AI news</title>" in en
        assert "doğrulanmış yapay zekâ haberleri</title>" in tr

    def test_open_graph_present_and_typed(self, site):
        article = (site / "articles" / "first-story.html").read_text(encoding="utf-8")
        index = (site / "index.html").read_text(encoding="utf-8")
        assert '<meta property="og:type" content="article">' in article
        assert '<meta property="og:type" content="website">' in index
        assert '<meta property="og:locale" content="en_US">' in index
        assert '<meta property="og:locale" content="tr_TR">' in (
            site / "tr" / "index.html"
        ).read_text(encoding="utf-8")

    def test_feed_is_discoverable_from_every_page(self, site):
        for rel in ("index.html", "about.html", "articles/first-story.html"):
            page = (site / rel).read_text(encoding="utf-8")
            assert 'type="application/atom+xml"' in page
        article = (site / "articles" / "first-story.html").read_text(encoding="utf-8")
        assert 'href="../feed.xml"' in article

    def test_index_has_exactly_one_h1(self, site):
        """Both index pages previously emitted no h1 at all."""
        for rel in ("index.html", "tr/index.html"):
            assert (site / rel).read_text(encoding="utf-8").count("<h1") == 1

    def test_language_switcher_declares_the_target_language(self, site):
        assert 'hreflang="tr" lang="tr"' in (site / "index.html").read_text(encoding="utf-8")

    def test_index_dates_are_machine_readable(self, site):
        index = (site / "index.html").read_text(encoding="utf-8")
        assert "<time class='date' datetime='2026-07-14'>" in index
