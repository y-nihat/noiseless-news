"""The duplicate gate, asserted against the archive it actually protects.

Unit tests use fixtures, and a fixture can drift away from what the night agent
writes — that is exactly how two watching stories became invisible to the live
gate for thirteen days while the suite stayed green. These tests run against the
real content/ and data/ledger/ instead, so schema drift fails loudly on the next
push rather than silently degrading the one editorial rule the project decided
was worth mechanising.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from noiseless.dedup import STRONG_THRESHOLD, load_index, similarity, tokens

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def index():
    return load_index(REPO_ROOT)


def test_index_is_not_empty(index):
    assert len(index) >= 50, "the archive should be indexed; did load_index break?"


def test_every_entry_is_matchable(index):
    """An entry with no title and no URLs can never match anything.

    similarity() short-circuits to 0.0 on an empty token set, so such an entry
    is silently absent from every future duplicate check.
    """
    unmatchable = [e.slug for e in index if not tokens(e.title) and not e.urls]
    assert not unmatchable, f"invisible to the duplicate gate: {unmatchable}"


def test_every_entry_carries_a_date(index):
    """§0a reasons about staleness, which needs a date on every entry."""
    undated = [e.slug for e in index if not e.date]
    assert not undated, f"no usable date: {undated}"


def test_open_stories_are_visible(index):
    """The unpublished entries are the ones the archive-wide index exists for.

    Published stories are covered twice over by the article scan; a watching
    story that cannot match is how an unlinked duplicate gets published.
    """
    open_entries = [e for e in index if e.state != "published"]
    if not open_entries:
        pytest.skip("no open stories in the ledger right now")
    for entry in open_entries:
        assert tokens(entry.title), f"{entry.slug}: no matchable title"
        assert entry.date, f"{entry.slug}: no date"


# Open entries with no recoverable identity URL. Each was checked against the
# whole committed raw capture and the entry's own notes on 2026-08-07; none is
# present anywhere in the archive, and inventing a plausible link on a site whose
# proposition is that citations can be checked is worse than recording the gap.
# Clear a slug from this list the moment a real URL turns up for it.
NO_RECOVERABLE_URL = {
    "anthropic-meta-compute-deal",   # origin is a paywalled exclusive, never captured
    "bytedance-seed-audio-1-0",      # vendor blog post, never captured
    "cohere-north-automations",      # dropped; nothing in the archive matches the story
}


def test_every_published_story_has_at_least_one_deep_link(index):
    """A published article with no identity URL is invisible to the URL half.

    Replaces an assertion that could never fail: `identity_urls` drops bare
    origins while building the index, so a test looking for them in the built
    index was vacuous.
    """
    offenders = [e.slug for e in index if e.state == "published" and not e.urls]
    assert not offenders, f"published with no identity URL: {offenders}"


def test_open_stories_carry_an_identity_url(index):
    """Watching entries are exactly what the archive-wide index exists for.

    With no URL, only the title half of the gate can match them — and naming
    divergence between a story and its re-reporting is precisely the case the
    URL half was added to catch.
    """
    offenders = [
        e.slug
        for e in index
        if e.state != "published" and not e.urls and e.slug not in NO_RECOVERABLE_URL
    ]
    assert not offenders, (
        f"open stories with no identity URL: {offenders} — "
        "policy/article-template.md requires deep-link source_urls on every entry"
    )


def test_no_two_published_stories_strong_match_each_other(index):
    """A strong match means "do not publish this". Two live articles matching
    each other means the gate would have blocked one of them."""
    published = [e for e in index if e.state == "published"]
    collisions = []
    for i, first in enumerate(published):
        for second in published[i + 1 :]:
            score = similarity(tokens(first.title), tokens(second.title))
            shared = first.urls & second.urls
            if shared and (len(shared) >= 2 or score >= 0.34):
                score = 1.0
            if score >= STRONG_THRESHOLD:
                collisions.append((first.slug, second.slug, round(score, 3)))
    assert not collisions, f"published stories that would block each other: {collisions}"
