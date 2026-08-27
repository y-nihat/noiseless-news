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

from noiseless.dedup import check, load_index, policy_exempt_pair, tokens

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


def _strong_pairs(published):
    """Every published pair the live gate would score `strong`, each once.

    Scored by `check()` — the same function `dedup-check` runs — rather than by
    a copy of its arithmetic. The copy this replaces had drifted: it inlined
    MODERATE_THRESHOLD as a literal `0.34` and omitted the `elif shared` branch
    added to `check()` later, so the invariant guarding the archive and the gate
    guarding a new story no longer agreed on what a duplicate is.
    """
    by_slug = {e.slug: e for e in published}
    seen = set()
    for first in published:
        others = [e for e in published if e.slug != first.slug]
        for match in check(first.title, sorted(first.urls), others):
            if match["strength"] != "strong":
                continue
            pair = frozenset((first.slug, match["slug"]))
            if pair in seen:
                continue
            seen.add(pair)
            yield first, by_slug[match["slug"]], match["score"]


def test_no_two_published_stories_strong_match_each_other(index):
    """A strong match means "do not publish this" — unless §8 says otherwise.

    §8 gives a strong match three outcomes, and two of them deliberately leave
    two published stories matching: a follow-up shares its predecessor's saga
    and usually its sources, and "unrelated despite surface similarity" is an
    explicit licence to publish standalone. Asserting that no two published
    stories may match asserted something stricter than the policy it exists to
    mechanise, and on 2026-08-20 it started failing on a pair the policy allows:
    the Pennsylvania executive-order story cites New York's Executive Order 62 —
    as evidence for its own claim that Pennsylvania is the third such state —
    and one shared citation plus four generic title words ("governor", "signs",
    "data", "centers") scored 1.0. That is the site doing its job.

    What still fails, and must: an *unrecorded* standalone. The exemption
    requires the evidence log to name the other slug, so a genuine unlinked
    duplicate has nowhere to hide.
    """
    published = [e for e in index if e.state == "published"]
    collisions = [
        (first.slug, second.slug, score)
        for first, second, score in _strong_pairs(published)
        if not policy_exempt_pair(REPO_ROOT, first, second)
    ]
    assert not collisions, (
        f"published stories that would block each other: {collisions}\n"
        "policy/verification.md §8 gives three outcomes for a strong match — pick one:\n"
        "  * same event      -> fold the newer story into the older one (in-place update)\n"
        "  * same saga       -> `follows: <slug>` in the article frontmatter AND the ledger\n"
        "  * coincidental    -> record why in the newer story's data/verified/<slug>.json\n"
        "                       `dedup_check` field, naming the other slug"
    )


def test_every_follows_link_points_at_a_real_story(index):
    """A saga link into nothing is a thread the site cannot render.

    Also the half of the exemption above that has no other guard: a typo'd
    `follows` would silently stop excusing the pair it was written for.
    """
    known = {e.slug for e in index}
    broken = [(e.slug, e.follows) for e in index if e.follows and e.follows not in known]
    assert not broken, f"follows: pointing at no known story: {broken}"
