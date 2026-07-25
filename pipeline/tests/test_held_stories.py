"""The public record of what was NOT published.

This is the project's most distinctive artifact and it was entirely invisible:
four held stories with written reasons, one of them re-checked for fifteen
consecutive nights, none of it rendered anywhere.

It is also the page with the sharpest failure mode. A held story is by
definition one whose claims did not stand up, so rendering the ledger's internal
`reason` — which restates the claim in full so the next cycle has context —
would turn the page into an outlet for exactly the material the site declined to
print. These tests pin that boundary.
"""

from __future__ import annotations

import json

import pytest

from noiseless.publish import build_site, load_held_stories

INTERNAL_REASON = (
    "Failed publishing gate: every load-bearing claim (production timeline, "
    "Broadcom/TSMC partnership, 7GW->14GW capacity target) traces to a single "
    "origin -- a Reuters exclusive citing an internal memo (policy/verification.md §2)."
)

HELD = {
    "slug": "held-story",
    "title": "Reports of an in-house chip timeline",
    "status": "watching",
    "first_seen": "2026-07-09",
    "reason": INTERNAL_REASON,
    "public_note": "Widely relayed, but every account traces to one report.",
    "watch": ["A statement from the company", "A second independent account"],
}

ARTICLE = """---
title: A published story
date: 2026-07-20
slug: published-story
lang: {lang}
tldr: A summary.
sources:
  - name: Example
    url: https://example.com/a
claims: []
updated: []
---

Body.
"""


def make(tmp_path, *entries):
    for lang in ("en", "tr"):
        d = tmp_path / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True, exist_ok=True)
        (d / "published-story.md").write_text(ARTICLE.format(lang=lang), encoding="utf-8")
    ledger = tmp_path / "data" / "ledger"
    ledger.mkdir(parents=True)
    for entry in entries or (HELD,):
        (ledger / f"{entry['slug']}.json").write_text(json.dumps(entry), encoding="utf-8")
    build_site(tmp_path, tmp_path / "site")
    return tmp_path / "site"


class TestLoading:
    def test_only_watching_entries_are_held(self, tmp_path):
        published = {"slug": "done", "status": "published", "first_seen": "2026-07-01"}
        make(tmp_path, HELD, published)
        held = load_held_stories(tmp_path / "data")
        assert [h["slug"] for h in held] == ["held-story"]

    def test_public_false_opts_an_entry_out_entirely(self, tmp_path):
        """Required by §10 whenever a private individual is involved."""
        private = {**HELD, "slug": "sensitive", "public": False, "first_seen": "2026-07-22"}
        make(tmp_path, HELD, private)
        held = load_held_stories(tmp_path / "data")
        assert [h["slug"] for h in held] == ["held-story"]

    def test_registry_files_are_ignored(self, tmp_path):
        make(tmp_path, HELD)
        (tmp_path / "data" / "ledger" / "source_candidates.json").write_text(
            "[]", encoding="utf-8"
        )
        assert len(load_held_stories(tmp_path / "data")) == 1

    def test_malformed_entry_is_skipped(self, tmp_path):
        make(tmp_path, HELD)
        (tmp_path / "data" / "ledger" / "broken.json").write_text("{", encoding="utf-8")
        assert len(load_held_stories(tmp_path / "data")) == 1

    def test_rule_references_are_extracted_from_the_internal_reason(self, tmp_path):
        make(tmp_path, HELD)
        assert load_held_stories(tmp_path / "data")[0]["rules"] == ["2"]

    def test_subject_falls_back_to_the_slug(self, tmp_path):
        untitled = {"slug": "no-title-here", "status": "watching", "first_seen": "2026-07-01"}
        make(tmp_path, untitled)
        assert load_held_stories(tmp_path / "data")[0]["subject"] == "no title here"


class TestRendering:
    def test_page_exists_in_both_languages(self, tmp_path):
        site = make(tmp_path)
        assert (site / "held.html").exists()
        assert (site / "tr" / "held.html").exists()

    def test_internal_reason_is_never_published(self, tmp_path):
        """The single most important assertion in this module.

        The internal reason restates the unverified claim in full. Rendering it
        would publish the specifics the site decided it could not stand behind.
        """
        page = (make(tmp_path) / "held.html").read_text(encoding="utf-8")
        for fragment in ("Broadcom", "7GW", "production timeline", "Reuters exclusive"):
            assert fragment not in page, f"internal reason leaked: {fragment!r}"

    def test_the_hold_and_its_rule_are_published(self, tmp_path):
        page = (make(tmp_path) / "held.html").read_text(encoding="utf-8")
        assert "Reports of an in-house chip timeline" in page
        assert "held since 2026-07-09" in page
        assert "Independence — every account traces to a single origin" in page

    def test_the_missing_evidence_is_published(self, tmp_path):
        page = (make(tmp_path) / "held.html").read_text(encoding="utf-8")
        assert "A statement from the company" in page
        assert "A second independent account" in page

    def test_page_states_plainly_that_nothing_here_is_fact(self, tmp_path):
        page = (make(tmp_path) / "held.html").read_text(encoding="utf-8")
        assert "Nothing on this page is reported as fact" in page

    def test_entry_without_a_rule_reference_gets_the_generic_label(self, tmp_path):
        vague = {**HELD, "reason": "did not clear the bar"}
        page = (make(tmp_path, vague) / "held.html").read_text(encoding="utf-8")
        assert "Did not meet the publishing gate" in page

    def test_empty_state(self, tmp_path):
        make(tmp_path, {"slug": "done", "status": "published", "first_seen": "2026-07-01"})
        page = (tmp_path / "site" / "held.html").read_text(encoding="utf-8")
        assert "Nothing is on hold right now" in page

    def test_turkish_page_is_localized(self, tmp_path):
        page = (make(tmp_path) / "tr" / "held.html").read_text(encoding="utf-8")
        assert "Yayımlanmayanlar" in page
        assert "olgu olarak aktarılmamaktadır" in page
        assert "Nothing on this page" not in page

    def test_linked_from_the_nav_at_every_depth(self, tmp_path):
        site = make(tmp_path)
        assert 'href="held.html"' in (site / "index.html").read_text(encoding="utf-8")
        assert 'href="../held.html"' in (
            site / "articles" / "published-story.html"
        ).read_text(encoding="utf-8")


class TestRealLedger:
    def test_no_held_subject_asserts_the_claim_it_failed_to_verify(self):
        """§11a: a held title is the subject under review, not the claim.

        Guards the specific defect found in the audit: one entry's title stated
        that a named individual was departing — the exact claim the pipeline had
        decided it could not verify.
        """
        from pathlib import Path

        repo = Path(__file__).resolve().parents[2]
        for entry in load_held_stories(repo / "data"):
            subject = entry["subject"].lower()
            assert not any(
                subject.startswith(w) for w in ("openai's", "meta will", "anthropic will")
            ), f"{entry['slug']}: subject reads as an assertion — {entry['subject']!r}"
            assert entry["since"], f"{entry['slug']}: no first_seen date"
