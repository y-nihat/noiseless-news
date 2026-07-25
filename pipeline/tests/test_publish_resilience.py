"""What happens when the unattended agent writes something malformed.

Articles, ledger entries and raw feed files are all written at 03:00 with no
human in the loop, and the deploy workflow ships whatever is on main about two
minutes later. Before these paths were hardened, a single bad YAML block took
down the site build and `dedup-check` in the same breath — so the duplicate gate,
which is the agent's own way out of the mess, broke exactly when it was needed.
"""

from __future__ import annotations

import json

import pytest

from noiseless.dedup import load_index
from noiseless.ingest import _load_seen_ids, _save_seen_ids
from noiseless.publish import build_digest, build_site, load_articles

GOOD = """---
title: A good article
date: 2026-07-20
slug: good-article
lang: en
tldr: It parses.
sources:
  - name: Example
    url: https://example.com/story
claims: []
---

## What happened

Body text.
"""

BROKEN_YAML = """---
title: "unterminated quote
date: 2026-07-21
slug: broken
  bad: [indent
---

Body.
"""


def make_content(tmp_path, **extra_files):
    art = tmp_path / "content" / "articles"
    for lang in ("en", "tr"):
        (art / lang / "2026" / "07").mkdir(parents=True)
        (art / lang / "2026" / "07" / "good-article.md").write_text(
            GOOD.replace("lang: en", f"lang: {lang}"), encoding="utf-8"
        )
    for name, text in extra_files.items():
        (art / "en" / "2026" / "07" / name).write_text(text, encoding="utf-8")
    return tmp_path


class TestMalformedArticles:
    def test_broken_article_is_skipped_not_fatal(self, tmp_path, capsys):
        make_content(tmp_path, **{"broken.md": BROKEN_YAML})
        articles = load_articles(tmp_path / "content", "en")
        assert [a.slug for a in articles] == ["good-article"]
        assert "SKIP" in capsys.readouterr().out

    def test_broken_article_does_not_disable_the_duplicate_gate(self, tmp_path):
        """The gate must survive precisely the night that produced the bad file."""
        make_content(tmp_path, **{"broken.md": BROKEN_YAML})
        (tmp_path / "data" / "ledger").mkdir(parents=True)
        index = load_index(tmp_path)
        assert [e.slug for e in index] == ["good-article"]

    def test_site_still_builds_around_a_broken_article(self, tmp_path):
        make_content(tmp_path, **{"broken.md": BROKEN_YAML})
        counts = build_site(tmp_path, tmp_path / "site")
        assert counts["en"] == 1
        assert (tmp_path / "site" / "articles" / "good-article.html").exists()


class TestAtomicBuild:
    def test_previous_site_survives_a_failed_build(self, tmp_path, monkeypatch):
        """`if: always()` deploy steps must never find a half-rendered site."""
        make_content(tmp_path)
        out = tmp_path / "site"
        build_site(tmp_path, out)
        previous = (out / "index.html").read_text(encoding="utf-8")

        import noiseless.publish as publish

        def explode(*_args, **_kwargs):
            raise RuntimeError("render failed halfway")

        monkeypatch.setattr(publish, "_article_html", explode)
        with pytest.raises(RuntimeError):
            build_site(tmp_path, out)

        assert (out / "index.html").read_text(encoding="utf-8") == previous
        assert (out / "articles" / "good-article.html").exists()

    def test_no_staging_directory_is_left_behind_on_success(self, tmp_path):
        make_content(tmp_path)
        build_site(tmp_path, tmp_path / "site")
        assert not (tmp_path / ".site.building").exists()


class TestMalformedRawData:
    def test_unparseable_raw_file_is_skipped(self, tmp_path, capsys):
        day = tmp_path / "raw" / "2026-07-20"
        day.mkdir(parents=True)
        (day / "truncated.json").write_text('[{"tier": 2, "title": "cut off"', encoding="utf-8")
        (day / "fine.json").write_text(
            json.dumps(
                [{"tier": 2, "title": "Fine", "url": "https://e.com/a", "source": "E"}]
            ),
            encoding="utf-8",
        )
        digest = build_digest(tmp_path)
        assert [item["title"] for item in digest["tiers"][2]] == ["Fine"]
        assert "SKIP raw" in capsys.readouterr().out

    def test_items_without_a_tier_are_ignored(self, tmp_path):
        day = tmp_path / "raw" / "2026-07-20"
        day.mkdir(parents=True)
        (day / "mixed.json").write_text(
            json.dumps(
                [
                    {"title": "no tier", "url": "https://e.com/a", "source": "E"},
                    {"tier": 0, "title": "ok", "url": "https://e.com/b", "source": "E"},
                ]
            ),
            encoding="utf-8",
        )
        digest = build_digest(tmp_path)
        assert list(digest["tiers"]) == [0]


class TestSeenIds:
    def test_round_trip(self, tmp_path):
        path = tmp_path / "state" / "seen_ids.json"
        _save_seen_ids(path, {"a", "b"})
        assert _load_seen_ids(path) == {"a", "b"}

    def test_missing_file_starts_empty(self, tmp_path):
        assert _load_seen_ids(tmp_path / "absent.json") == set()

    def test_corrupt_file_refuses_rather_than_re_ingesting_everything(self, tmp_path):
        """A rebase conflict here used to be silent.

        Starting from an empty set would re-ingest the whole 14,000-item history
        into today's raw files, so stopping with an actionable message is the
        safer failure.
        """
        path = tmp_path / "seen_ids.json"
        path.write_text("<<<<<<< HEAD\n[\"a\"]\n=======\n[\"b\"]\n", encoding="utf-8")
        with pytest.raises(RuntimeError, match="git checkout"):
            _load_seen_ids(path)
