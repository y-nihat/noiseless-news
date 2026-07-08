"""Unit tests for the ingest stage: normalization, identity, dedup (no network)."""

from noiseless.ingest import canonical_url, dedupe, ingest_all, item_id, parse_feed_text
from noiseless.sources import Source

SOURCE = Source(name="Example Blog", tier=0, type="rss", url="https://example.com/feed.xml")

ATOM_FIXTURE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example Blog</title>
  <entry>
    <title>  Model X  released
      today </title>
    <link href="https://example.com/posts/model-x?utm_source=rss&amp;utm_medium=feed#section"/>
    <id>urn:uuid:1</id>
    <updated>2026-07-01T10:00:00Z</updated>
    <summary>Model X is out.</summary>
  </entry>
  <entry>
    <title>Post without a link</title>
    <id>urn:uuid:2</id>
    <updated>2026-07-01T11:00:00Z</updated>
  </entry>
</feed>
"""


class TestCanonicalUrl:
    def test_strips_tracking_params_and_fragment(self):
        url = "https://Example.com/a?utm_source=x&utm_campaign=y&fbclid=z&page=2#frag"
        assert canonical_url(url) == "https://example.com/a?page=2"

    def test_keeps_meaningful_query(self):
        url = "https://example.com/search?q=ai&sort=date"
        assert canonical_url(url) == "https://example.com/search?q=ai&sort=date"

    def test_lowercases_host_not_path(self):
        assert canonical_url("HTTPS://EXAMPLE.com/Path") == "https://example.com/Path"


class TestItemId:
    def test_stable_across_tracking_variants(self):
        a = item_id("https://example.com/a?utm_source=rss")
        b = item_id("https://example.com/a")
        assert a == b

    def test_distinct_urls_differ(self):
        assert item_id("https://example.com/a") != item_id("https://example.com/b")


class TestParseFeedText:
    def test_normalizes_entries(self):
        items = parse_feed_text(SOURCE, ATOM_FIXTURE, fetched_at="2026-07-08T00:00:00+00:00")
        assert len(items) == 1  # the entry without a link is dropped
        item = items[0]
        assert item["title"] == "Model X released today"  # whitespace collapsed
        assert item["url"] == "https://example.com/posts/model-x"  # utm + fragment gone
        assert item["source"] == "Example Blog"
        assert item["tier"] == 0
        assert item["published"] == "2026-07-01T10:00:00+00:00"
        assert item["summary"] == "Model X is out."
        assert item["id"] == item_id("https://example.com/posts/model-x")


class TestIngestAll:
    def test_skips_non_active_sources(self, tmp_path):
        """candidate/retired sources are never fetched (no network call happens)."""
        sources = [
            Source(name="C", tier=2, type="rss", url="https://c.example.com/f", status="candidate"),
            Source(name="R", tier=2, type="rss", url="https://r.example.com/f", status="retired"),
        ]
        summary = ingest_all(sources, tmp_path)
        assert summary == {}


class TestDedupe:
    def test_filters_seen_and_in_run_duplicates(self):
        items = [
            {"id": "aaa", "title": "one"},
            {"id": "bbb", "title": "two"},
            {"id": "aaa", "title": "one again"},
        ]
        seen = {"bbb"}
        new_items = dedupe(items, seen)
        assert [item["id"] for item in new_items] == ["aaa"]
        assert seen == {"aaa", "bbb"}
