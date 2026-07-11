"""Unit tests for the publish stage (no network)."""

import json

from noiseless.publish import (
    Article,
    build_digest,
    build_site,
    parse_frontmatter,
    resolve_threads,
)

ARTICLE_EN = """---
title: Example Lab releases Model X
date: 2026-07-08
slug: example-model-x
lang: en
tldr: Example Lab released Model X. Independent benchmarks are not yet available.
sources:
  - name: Example Lab Blog
    url: https://example.com/blog/model-x
  - name: Quality Press
    url: https://press.example.com/model-x
claims:
  - text: "Example Lab released Model X on 8 July"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Model X outperforms rivals on benchmark B"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
---

## What happened

Example Lab released Model X.
"""

ARTICLE_TR = ARTICLE_EN.replace(
    "title: Example Lab releases Model X", "title: Example Lab, Model X'i yayımladı"
).replace("lang: en", "lang: tr")

FOLLOWUP_EN = """---
title: Model X pulled after benchmark dispute
date: 2026-07-10
slug: model-x-pulled
lang: en
tldr: Example Lab withdrew Model X.
follows: example-model-x
sources:
  - name: Example Lab Blog
    url: https://example.com/blog/model-x-pulled
---

## What happened

It was pulled.
"""

FOLLOWUP_TR = FOLLOWUP_EN.replace(
    "title: Model X pulled after benchmark dispute",
    "title: Model X, benchmark tartışması sonrası geri çekildi",
).replace("lang: en", "lang: tr")


def make_repo(tmp_path):
    (tmp_path / "content/articles/en/2026/07").mkdir(parents=True)
    (tmp_path / "content/articles/tr/2026/07").mkdir(parents=True)
    (tmp_path / "content/articles/en/2026/07/example-model-x.md").write_text(
        ARTICLE_EN, encoding="utf-8"
    )
    (tmp_path / "content/articles/tr/2026/07/example-model-x.md").write_text(
        ARTICLE_TR, encoding="utf-8"
    )

    day = tmp_path / "data/raw/2026-07-08"
    day.mkdir(parents=True)
    items = [
        {"id": "a1", "source": "Example Lab Blog", "tier": 0,
         "title": "Model X is here", "url": "https://example.com/blog/model-x",
         "published": "2026-07-08T10:00:00+00:00", "summary": "", "fetched_at": ""},
        {"id": "a2", "source": "Example Forum", "tier": 3,
         "title": "Discussion thread", "url": "https://forum.example.com/1",
         "published": "2026-07-08T11:00:00+00:00", "summary": "", "fetched_at": ""},
    ]
    (day / "example.json").write_text(json.dumps(items), encoding="utf-8")
    # an older day that must NOT be picked
    old = tmp_path / "data/raw/2026-07-01"
    old.mkdir(parents=True)
    (old / "example.json").write_text(json.dumps([items[0] | {"id": "old"}]), encoding="utf-8")
    return tmp_path


def test_parse_frontmatter():
    meta, body = parse_frontmatter(ARTICLE_EN)
    assert meta["slug"] == "example-model-x"
    assert meta["claims"][1]["verdict"] == "vendor-claim"
    assert body.startswith("## What happened")


def test_build_digest_uses_latest_day_and_groups_tiers(tmp_path):
    make_repo(tmp_path)
    digest = build_digest(tmp_path / "data")
    assert digest["date"] == "2026-07-08"
    assert {tier for tier in digest["tiers"]} == {0, 3}
    assert digest["tiers"][0][0]["title"] == "Model X is here"


def _article(slug, date, follows=None, title=None):
    meta = {"slug": slug, "date": date, "title": title or slug}
    if follows:
        meta["follows"] = follows
    return Article(meta=meta, body_html="", lang="en")


class TestResolveThreads:
    def test_chain_groups_and_orders(self):
        a = _article("root", "2026-07-01")
        b = _article("mid", "2026-07-05", follows="root")
        c = _article("tip", "2026-07-10", follows="mid")
        lone = _article("unrelated", "2026-07-04")
        threads = resolve_threads([c, lone, a, b])
        assert "unrelated" not in threads
        assert [m.slug for m in threads["root"]] == ["root", "mid", "tip"]
        assert threads["root"] is threads["tip"]  # every member maps to the thread

    def test_broken_pointer_and_cycle_degrade_gracefully(self):
        orphan = _article("orphan", "2026-07-01", follows="missing-slug")
        x = _article("x", "2026-07-01", follows="y")
        y = _article("y", "2026-07-02", follows="x")
        threads = resolve_threads([orphan, x, y])
        assert "orphan" not in threads  # broken pointer → standalone, no crash
        # a malformed 2-cycle collapses to no thread rather than looping forever
        assert threads == {} or all(len(t) >= 2 for t in threads.values())


def test_thread_box_rendered_on_both_members_and_languages(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "content/articles/en/2026/07/model-x-pulled.md").write_text(
        FOLLOWUP_EN, encoding="utf-8"
    )
    (tmp_path / "content/articles/tr/2026/07/model-x-pulled.md").write_text(
        FOLLOWUP_TR, encoding="utf-8"
    )
    out = tmp_path / "dist"
    build_site(tmp_path, out)

    followup = (out / "articles/model-x-pulled.html").read_text(encoding="utf-8")
    assert "Story thread" in followup
    assert "example-model-x.html" in followup          # links back to the original
    assert "this article" in followup                  # current member marked

    original = (out / "articles/example-model-x.html").read_text(encoding="utf-8")
    assert "Story thread" in original
    assert "model-x-pulled.html" in original           # original links forward

    tr_followup = (out / "tr/articles/model-x-pulled.html").read_text(encoding="utf-8")
    assert "Haberin seyri" in tr_followup              # Turkish thread box

    index = (out / "index.html").read_text(encoding="utf-8")
    assert "follow-up" in index                        # thread chip on the list


def test_build_site_renders_bilingual_pages(tmp_path):
    make_repo(tmp_path)
    out = tmp_path / "dist"
    counts = build_site(tmp_path, out)
    assert counts == {"en": 1, "tr": 1}

    index = (out / "index.html").read_text(encoding="utf-8")
    assert "Example Lab releases Model X" in index
    assert "Model X is here" in index  # digest item present

    tr_index = (out / "tr/index.html").read_text(encoding="utf-8")
    assert "Example Lab, Model X&#x27;i yayımladı" in tr_index or "Model X'i" in tr_index

    article = (out / "articles/example-model-x.html").read_text(encoding="utf-8")
    assert "Vendor claim" in article           # verdict label rendered
    assert "https://press.example.com/model-x" in article  # sources listed

    tr_article = (out / "tr/articles/example-model-x.html").read_text(encoding="utf-8")
    assert "Üretici beyanı" in tr_article      # Turkish verdict label

    assert (out / ".nojekyll").exists()
