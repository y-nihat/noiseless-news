"""Unit tests for archive-wide duplicate prevention (no network)."""

import json

from noiseless.dedup import check, load_index, similarity, tokens

ARTICLE = """---
title: OpenAI releases GPT-5.6 model family
date: 2026-07-09
slug: gpt-5-6-launch
lang: en
tldr: OpenAI launched the GPT-5.6 family.
sources:
  - name: OpenAI News
    url: https://openai.com/index/gpt-5-6?utm_source=rss
---

Body.
"""


def make_repo(tmp_path):
    art_dir = tmp_path / "content/articles/en/2026/07"
    art_dir.mkdir(parents=True)
    (art_dir / "gpt-5-6-launch.md").write_text(ARTICLE, encoding="utf-8")

    ledger = tmp_path / "data/ledger"
    ledger.mkdir(parents=True)
    (ledger / "meta-chip.json").write_text(
        json.dumps(
            {
                "slug": "meta-chip",
                "title": "Meta plans in-house AI chip production",
                "state": "watching",
                "date": "2026-07-09",
                "source_urls": ["https://www.reuters.com/technology/meta-chip"],
            }
        ),
        encoding="utf-8",
    )
    # non-story ledger files must be ignored
    (ledger / "source_candidates.json").write_text("[]", encoding="utf-8")
    return tmp_path


def test_index_covers_articles_and_ledger(tmp_path):
    index = load_index(make_repo(tmp_path))
    by_slug = {e.slug: e for e in index}
    assert set(by_slug) == {"gpt-5-6-launch", "meta-chip"}
    assert by_slug["gpt-5-6-launch"].state == "published"
    assert by_slug["gpt-5-6-launch"].date == "2026-07-09"
    assert by_slug["meta-chip"].state == "watching"


def test_reworded_title_is_strong_match(tmp_path):
    index = load_index(make_repo(tmp_path))
    matches = check("GPT-5.6 model family released by OpenAI", [], index)
    assert matches and matches[0]["slug"] == "gpt-5-6-launch"
    assert matches[0]["strength"] == "strong"


def test_shared_source_url_is_strong_even_with_different_title(tmp_path):
    index = load_index(make_repo(tmp_path))
    matches = check(
        "Sam Altman comments on pricing strategy",
        ["https://openai.com/index/gpt-5-6"],  # same canonical primary source
        index,
    )
    assert matches and matches[0]["slug"] == "gpt-5-6-launch"
    assert matches[0]["shared_source_url"] is True
    assert matches[0]["strength"] == "strong"


def test_unrelated_story_has_no_match(tmp_path):
    index = load_index(make_repo(tmp_path))
    assert check("EU parliament passes water directive", [], index) == []


def test_watching_ledger_entry_matches(tmp_path):
    index = load_index(make_repo(tmp_path))
    matches = check("Meta AI chip production timeline", [], index)
    assert matches and matches[0]["slug"] == "meta-chip"


def test_token_similarity_basics():
    assert similarity(tokens("OpenAI releases GPT-5.6"), tokens("the of and")) == 0.0
    assert similarity(set(), set()) == 0.0
