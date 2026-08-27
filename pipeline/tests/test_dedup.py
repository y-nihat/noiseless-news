"""Unit tests for archive-wide duplicate prevention (no network).

The ledger fixtures below deliberately mirror the shape the night agent really
writes — `status`/`first_seen`/`published_at`, sometimes with no `title` and no
`source_urls` at all. The previous fixture encoded the shape the cycle prompt
*asks* for, which is why thirteen days of schema drift kept the suite green
while two watching stories were invisible to the live duplicate gate.
"""

import json

from noiseless.dedup import (
    IndexEntry,
    check,
    dedup_note,
    identity_urls,
    load_index,
    policy_exempt_pair,
    similarity,
    tokens,
)

ARTICLE = """---
title: OpenAI releases GPT-5.6 model family
date: 2026-07-09
slug: gpt-5-6-launch
lang: en
tldr: OpenAI launched the GPT-5.6 family.
sources:
  - name: OpenAI News
    url: https://openai.com/index/gpt-5-6?utm_source=rss
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/09/openai-gpt-5-6/
---

Body.
"""

# Real production shape: status (not state), published_at/first_seen (not date).
FULL_LEDGER_ENTRY = {
    "slug": "meta-chip",
    "title": "Meta plans in-house AI chip production",
    "status": "watching",
    "first_seen": "2026-07-09",
    "published_at": None,
    "source_urls": ["https://www.reuters.com/technology/meta-chip-2026-07-09/"],
}

# Also real: two of the four live watching entries carry neither title nor URLs.
SPARSE_LEDGER_ENTRY = {
    "slug": "anthropic-meta-compute-deal",
    "status": "watching",
    "first_seen": "2026-07-20",
    "reason": "single origin; wire-exclusive rule still blocks it",
}


def make_repo(tmp_path, *ledger_entries):
    art_dir = tmp_path / "content/articles/en/2026/07"
    art_dir.mkdir(parents=True)
    (art_dir / "gpt-5-6-launch.md").write_text(ARTICLE, encoding="utf-8")

    ledger = tmp_path / "data/ledger"
    ledger.mkdir(parents=True)
    for entry in ledger_entries or (FULL_LEDGER_ENTRY,):
        (ledger / f"{entry['slug']}.json").write_text(
            json.dumps(entry), encoding="utf-8"
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


def test_ledger_dates_come_from_the_keys_the_agent_writes(tmp_path):
    """`date` is rarely present; `first_seen` always is."""
    index = load_index(make_repo(tmp_path))
    entry = next(e for e in index if e.slug == "meta-chip")
    assert entry.date == "2026-07-09"


def test_entry_without_a_title_is_still_matchable(tmp_path):
    """A slug is a hyphenated headline; using it beats scoring 0.0 forever."""
    index = load_index(make_repo(tmp_path, SPARSE_LEDGER_ENTRY))
    entry = next(e for e in index if e.slug == "anthropic-meta-compute-deal")
    assert entry.title == "anthropic meta compute deal"

    matches = check("Anthropic and Meta in talks over a compute deal", [], index)
    assert matches and matches[0]["slug"] == "anthropic-meta-compute-deal"


def test_reworded_title_is_strong_match(tmp_path):
    index = load_index(make_repo(tmp_path))
    matches = check("GPT-5.6 model family released by OpenAI", [], index)
    assert matches and matches[0]["slug"] == "gpt-5-6-launch"
    assert matches[0]["strength"] == "strong"


def test_one_shared_url_alone_surfaces_but_does_not_block(tmp_path):
    """Two different stories can cite the same announcement page.

    The live archive already contains such a pair (gpt-5-6-launch and
    openai-atlas-shutdown share one OpenAI URL and are not a thread), so a
    single shared URL raises the match for the agent to read rather than
    triggering exit 2, which the cycle prompt treats as forbidding a standalone.
    """
    index = load_index(make_repo(tmp_path))
    matches = check(
        "Sam Altman comments on enterprise pricing strategy",
        ["https://openai.com/index/gpt-5-6"],
        index,
    )
    assert matches and matches[0]["slug"] == "gpt-5-6-launch"
    assert matches[0]["shared_source_url"] is True
    assert matches[0]["strength"] == "moderate"


def test_two_shared_urls_are_strong(tmp_path):
    index = load_index(make_repo(tmp_path))
    matches = check(
        "Sam Altman comments on enterprise pricing strategy",
        [
            "https://openai.com/index/gpt-5-6",
            "https://techcrunch.com/2026/07/09/openai-gpt-5-6/",
        ],
        index,
    )
    assert matches[0]["strength"] == "strong"
    assert matches[0]["shared_url_count"] == 2


def test_shared_url_plus_title_agreement_is_strong(tmp_path):
    index = load_index(make_repo(tmp_path))
    matches = check(
        "OpenAI ships the GPT-5.6 family", ["https://openai.com/index/gpt-5-6"], index
    )
    assert matches[0]["strength"] == "strong"


def test_bare_domain_urls_are_never_identity(tmp_path):
    """Citing https://www.reuters.com/ says Reuters was involved, nothing more.

    Four such citations exist in the live archive; treating them as identity
    made every future story citing those domains a duplicate of the first one.
    """
    assert identity_urls(["https://www.reuters.com/", "https://techcrunch.com"]) == set()
    assert identity_urls(["https://www.reuters.com/technology/x-2026/"]) == {
        "https://www.reuters.com/technology/x-2026/"
    }

    index = load_index(make_repo(tmp_path))
    assert check("An unrelated chip supply story", ["https://techcrunch.com/"], index) == []


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


# --- §8: the outcomes that leave two published stories matching on purpose ---
#
# A strong match is not by itself a defect. §8 gives it three outcomes and two
# of them are supposed to produce exactly the state the archive invariant used
# to fail on. These fix the shape of the exemption, so widening it later takes a
# deliberate edit rather than an accident.

FOLLOW_UP = """---
title: OpenAI ships GPT-5.6 to the enterprise tier
date: 2026-07-20
slug: gpt-5-6-enterprise
lang: en
follows: gpt-5-6-launch
tldr: The enterprise rollout of the GPT-5.6 family.
sources:
  - name: OpenAI News
    url: https://openai.com/index/gpt-5-6-enterprise
---

Body.
"""


def write_verified(repo, slug, note):
    verified = repo / "data/verified"
    verified.mkdir(parents=True, exist_ok=True)
    (verified / f"{slug}.json").write_text(
        json.dumps({"slug": slug, "dedup_check": note}), encoding="utf-8"
    )


def test_follows_is_indexed_from_the_article(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "content/articles/en/2026/07/gpt-5-6-enterprise.md").write_text(
        FOLLOW_UP, encoding="utf-8"
    )
    by_slug = {e.slug: e for e in load_index(repo)}
    assert by_slug["gpt-5-6-enterprise"].follows == "gpt-5-6-launch"
    assert by_slug["gpt-5-6-launch"].follows == ""


def test_follows_is_indexed_from_the_ledger(tmp_path):
    """§8 requires the ledger entry to mirror the field; a `null` is not a link."""
    repo = make_repo(
        tmp_path,
        {"slug": "meta-chip-2", "status": "watching", "first_seen": "2026-07-10",
         "follows": "meta-chip"},
        {"slug": "meta-chip", "status": "watching", "first_seen": "2026-07-09",
         "follows": None},
    )
    by_slug = {e.slug: e for e in load_index(repo)}
    assert by_slug["meta-chip-2"].follows == "meta-chip"
    assert by_slug["meta-chip"].follows == ""


def test_a_saga_link_excuses_the_pair_in_either_direction(tmp_path):
    repo = make_repo(tmp_path)
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published", follows="a")
    assert policy_exempt_pair(repo, first, second) == "follows"
    assert policy_exempt_pair(repo, second, first) == "follows"


def test_a_recorded_standalone_excuses_the_pair(tmp_path):
    repo = make_repo(tmp_path)
    write_verified(repo, "b", "strong match against a -- different event, coincidental")
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert "data/verified/b.json" in policy_exempt_pair(repo, first, second)


def test_a_note_about_a_different_match_excuses_nothing(tmp_path):
    """The precision that keeps the exemption from being a blanket amnesty.

    A story may legitimately carry a dedup_check about some other candidate it
    was compared against. That note says nothing about *this* pair, so it must
    not excuse it.
    """
    repo = make_repo(tmp_path)
    write_verified(repo, "b", "strong match against some-other-story -- coincidental")
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(repo, first, second) == ""


def test_a_neighbouring_slug_does_not_excuse_the_pair(tmp_path):
    """Substring matching would let the wrong decision excuse this pair.

    `gpt-5-6-launch` is a substring of `gpt-5-6-launch-delay`; a short slug is
    also a substring of ordinary prose. Both were true of the first cut of this
    exemption, and both are how an unlinked duplicate would slip through it.
    """
    repo = make_repo(tmp_path)
    write_verified(repo, "b", "coincidental match against gpt-5-6-launch-delay")
    launch = IndexEntry("gpt-5-6-launch", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(repo, launch, second) == ""

    write_verified(repo, "b", "no dedup match was found against anything")
    short = IndexEntry("a", "A", "2026-07-01", "published")
    assert policy_exempt_pair(repo, short, second) == ""

    write_verified(repo, "b", "coincidental match against gpt-5-6-launch, five weeks apart")
    assert "data/verified/b.json" in policy_exempt_pair(repo, launch, second)


def test_an_unrecorded_standalone_is_not_excused(tmp_path):
    """No evidence log at all is the unlinked duplicate the gate exists to catch."""
    repo = make_repo(tmp_path)
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(repo, first, second) == ""


def test_an_unreadable_evidence_log_excuses_nothing(tmp_path):
    """Fail closed: a log we cannot parse is not a justification we can trust."""
    repo = make_repo(tmp_path)
    verified = repo / "data/verified"
    verified.mkdir(parents=True, exist_ok=True)
    (verified / "b.json").write_text("{not json", encoding="utf-8")
    assert dedup_note(repo, "b") == ""
    assert dedup_note(repo, "never-written") == ""
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(repo, first, second) == ""
