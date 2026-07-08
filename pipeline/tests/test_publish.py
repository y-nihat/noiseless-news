"""Unit tests for the publish stage (no network)."""

import json

from noiseless.publish import build_digest, build_site, parse_frontmatter

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
