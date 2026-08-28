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
    declarations,
    identity_urls,
    load_index,
    policy_exempt_pair,
    similarity,
    tokens,
    unlinked_duplicates,
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


def write_verified(repo, slug, *, declares=None, note="prose about the check"):
    verified = repo / "data/verified"
    verified.mkdir(parents=True, exist_ok=True)
    body = {"slug": slug, "dedup_check": note}
    if declares is not None:
        body["dedup_standalone"] = declares
    (verified / f"{slug}.json").write_text(json.dumps(body), encoding="utf-8")


def declared_for(repo, *slugs):
    return declarations(repo, slugs)


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
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published", follows="a")
    assert policy_exempt_pair({}, first, second) == "follows"
    assert policy_exempt_pair({}, second, first) == "follows"


def test_a_declaration_on_the_newer_story_excuses_the_pair(tmp_path):
    repo = make_repo(tmp_path)
    write_verified(repo, "b", declares=["a"])
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    declared = declared_for(repo, "a", "b")
    assert "data/verified/b.json" in policy_exempt_pair(declared, first, second)


def test_prose_that_merely_names_the_slug_excuses_nothing(tmp_path):
    """The hole the declaration replaced.

    Reading the prose `dedup_check` for the other slug's name granted amnesty
    for merely mentioning it: a note reading "clean, no matches against the
    archive" excused the very pair it denied, and so did a slug cited as a
    styling precedent, a slug inside a URL, and a note confessing to being an
    unlinked duplicate. Twenty-eight published pairs carried such a standing
    exemption on 2026-08-28 without anyone having declared one.
    """
    repo = make_repo(tmp_path)
    for note in (
        "dedup-check clean, no matches against the archive; a is a styling precedent",
        "This is the same event as a. I could not be bothered to fold it in.",
        "see https://example.com/x/a/y for background",
    ):
        write_verified(repo, "b", note=note)
        first = IndexEntry("a", "A", "2026-07-01", "published")
        second = IndexEntry("b", "B", "2026-07-02", "published")
        assert policy_exempt_pair(declared_for(repo, "a", "b"), first, second) == "", note


def test_an_older_story_cannot_excuse_a_newer_duplicate(tmp_path):
    """§8 puts the decision on the story being opened, not the one it matched."""
    repo = make_repo(tmp_path)
    write_verified(repo, "a", declares=["b"])
    older = IndexEntry("a", "A", "2026-07-01", "published")
    newer = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(declared_for(repo, "a", "b"), older, newer) == ""


def test_either_side_counts_when_the_dates_cannot_order_them(tmp_path):
    """Same-day stories have no newer one; refusing both would be arbitrary."""
    repo = make_repo(tmp_path)
    write_verified(repo, "a", declares=["b"])
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-01", "published")
    assert policy_exempt_pair(declared_for(repo, "a", "b"), first, second)
    undated = IndexEntry("b", "B", "", "published")
    assert policy_exempt_pair(declared_for(repo, "a", "b"), first, undated)


def test_a_declaration_naming_a_different_story_excuses_nothing(tmp_path):
    repo = make_repo(tmp_path)
    write_verified(repo, "b", declares=["some-other-story"])
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(declared_for(repo, "a", "b"), first, second) == ""


def test_an_undeclared_standalone_is_not_excused(tmp_path):
    repo = make_repo(tmp_path)
    write_verified(repo, "b")
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(declared_for(repo, "a", "b"), first, second) == ""


def test_an_unreadable_or_missing_evidence_log_excuses_nothing(tmp_path):
    """Fail closed: a log we cannot parse is not a declaration we can trust."""
    repo = make_repo(tmp_path)
    verified = repo / "data/verified"
    verified.mkdir(parents=True, exist_ok=True)
    (verified / "b.json").write_text("{not json", encoding="utf-8")
    assert declarations(repo, ["b", "never-written"]) == {}
    first = IndexEntry("a", "A", "2026-07-01", "published")
    second = IndexEntry("b", "B", "2026-07-02", "published")
    assert policy_exempt_pair(declared_for(repo, "a", "b"), first, second) == ""


def test_a_declaration_may_be_written_as_a_bare_string(tmp_path):
    """One slug is the common case; a list of one is easy to get wrong."""
    repo = make_repo(tmp_path)
    write_verified(repo, "b", declares="a")
    assert declarations(repo, ["b"]) == {"b": {"a"}}


def test_a_malformed_declaration_is_ignored_rather_than_trusted(tmp_path):
    repo = make_repo(tmp_path)
    for bad in (5, {"a": 1}, [None, 7, ""], []):
        write_verified(repo, "b", declares=bad)
        assert declarations(repo, ["b"]) == {}, bad


# A second article whose title agrees with gpt-5-6-launch and which cites one of
# its sources — the exact shape of the pair that reddened CI for eight days.
TWIN = """---
title: OpenAI releases GPT-5.6 model family to enterprise
date: 2026-07-19
slug: gpt-5-6-twin
lang: en
tldr: A second story on the same launch.
sources:
  - name: OpenAI News
    url: https://openai.com/index/gpt-5-6
---

Body.
"""


def with_twin(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "content/articles/en/2026/07/gpt-5-6-twin.md").write_text(TWIN, encoding="utf-8")
    return repo


def test_an_unlinked_duplicate_is_reported(tmp_path):
    repo = with_twin(tmp_path)
    offenders = unlinked_duplicates(repo, ["gpt-5-6-twin"])
    assert [o["matches"] for o in offenders] == ["gpt-5-6-launch"]
    assert offenders[0]["score"] == 1.0


def test_a_declared_standalone_clears_it(tmp_path):
    """The same record the archive test reads, asked before the commit lands."""
    repo = with_twin(tmp_path)
    write_verified(repo, "gpt-5-6-twin", declares=["gpt-5-6-launch"])
    assert unlinked_duplicates(repo, ["gpt-5-6-twin"]) == []


def test_prose_alone_does_not_clear_it(tmp_path):
    repo = with_twin(tmp_path)
    write_verified(repo, "gpt-5-6-twin", note="coincidental against gpt-5-6-launch")
    assert len(unlinked_duplicates(repo, ["gpt-5-6-twin"])) == 1


def test_a_pair_staged_together_is_one_refusal(tmp_path):
    repo = with_twin(tmp_path)
    offenders = unlinked_duplicates(repo, ["gpt-5-6-twin", "gpt-5-6-launch"])
    assert len(offenders) == 1, offenders


def test_a_follow_up_clears_it(tmp_path):
    repo = with_twin(tmp_path)
    path = repo / "content/articles/en/2026/07/gpt-5-6-twin.md"
    path.write_text(
        TWIN.replace("lang: en", "lang: en\nfollows: gpt-5-6-launch"), encoding="utf-8"
    )
    assert unlinked_duplicates(repo, ["gpt-5-6-twin"]) == []


def test_a_story_never_matches_itself(tmp_path):
    """`load_index` reads the working tree, so the staged article is in it."""
    assert unlinked_duplicates(make_repo(tmp_path), ["gpt-5-6-launch"]) == []


def test_a_moderate_match_is_not_refused(tmp_path):
    """Only what the archive test would reject may refuse a commit."""
    repo = make_repo(tmp_path)
    (repo / "content/articles/en/2026/07/mild.md").write_text(
        TWIN.replace("slug: gpt-5-6-twin", "slug: mild")
            .replace("title: OpenAI releases GPT-5.6 model family to enterprise",
                     "title: OpenAI hires a chief revenue officer")
            .replace("url: https://openai.com/index/gpt-5-6",
                     "url: https://openai.com/index/hiring"),
        encoding="utf-8",
    )
    assert unlinked_duplicates(repo, ["mild"]) == []


def test_a_slug_that_is_not_a_published_article_says_nothing(tmp_path):
    """Ledger-only and report-only commits pass untouched."""
    assert unlinked_duplicates(make_repo(tmp_path), ["meta-chip", "nonexistent"]) == []
