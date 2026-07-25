"""Tests for the deterministic content gate.

The gate exists because every editorial guarantee was self-reported: sixteen days
of style-gate records all read "EN pass / TR pass", and there has never been a
recorded failure — including on the night an article shipped with no `confirmed`
claim at all, and on the two nights bare-origin source URLs were published.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from noiseless.validate_content import Finding, validate

ARTICLE = """---
title: {title}
date: 2026-07-20
{published_line}slug: {slug}
lang: {lang}
tldr: A summary.
sources:
{sources}
claims:
{claims}
updated: []
---

Body.
"""

GOOD_SOURCES = "  - name: Primary\n    url: https://example.com/story\n"
GOOD_CLAIMS = (
    '  - text: "A claim"\n    type: announcement\n'
    "    verdict: confirmed\n    evidence: [1]\n"
)


def write(tmp_path, slug="a-story", *, sources=GOOD_SOURCES, claims=GOOD_CLAIMS,
          tr_claims=None, tr_sources=None, published=None, tr_published=None,
          skip_tr=False, evidence_log=True, ledger=True):
    for lang in ("en", "tr"):
        if lang == "tr" and skip_tr:
            continue
        d = tmp_path / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True, exist_ok=True)
        pub = tr_published if lang == "tr" and tr_published else published
        (d / f"{slug}.md").write_text(
            ARTICLE.format(
                title=f"Story {slug}", slug=slug, lang=lang,
                published_line=f"published: {pub}\n" if pub else "",
                sources=(tr_sources if lang == "tr" and tr_sources else sources),
                claims=(tr_claims if lang == "tr" and tr_claims else claims),
            ),
            encoding="utf-8",
        )
    for kind, wanted in (("verified", evidence_log), ("ledger", ledger)):
        d = tmp_path / "data" / kind
        d.mkdir(parents=True, exist_ok=True)
        if wanted:
            (d / f"{slug}.json").write_text(json.dumps({"slug": slug}), encoding="utf-8")
    return tmp_path


def checks(findings: list[Finding], level=None) -> set[str]:
    return {f.check for f in findings if level is None or f.level == level}


class TestCleanArticle:
    def test_a_well_formed_pair_produces_nothing(self, tmp_path):
        assert validate(write(tmp_path)) == []


class TestErrors:
    def test_out_of_range_evidence_index(self, tmp_path):
        claims = (
            '  - text: "A claim"\n    type: announcement\n'
            "    verdict: confirmed\n    evidence: [1, 4]\n"
        )
        findings = validate(write(tmp_path, claims=claims, tr_claims=claims))
        assert "evidence-index" in checks(findings, "ERROR")

    def test_unknown_verdict(self, tmp_path):
        claims = (
            '  - text: "A claim"\n    type: announcement\n'
            "    verdict: probably-true\n    evidence: [1]\n"
        )
        findings = validate(write(tmp_path, claims=claims, tr_claims=claims))
        assert "verdict-vocabulary" in checks(findings, "ERROR")

    def test_missing_turkish_counterpart(self, tmp_path):
        findings = validate(write(tmp_path, skip_tr=True))
        assert "bilingual-parity" in checks(findings, "ERROR")

    def test_claim_structure_drift_between_languages(self, tmp_path):
        tr_claims = (
            '  - text: "Bir iddia"\n    type: announcement\n'
            "    verdict: single-source\n    evidence: [1]\n"
        )
        findings = validate(write(tmp_path, tr_claims=tr_claims))
        assert "bilingual-parity" in checks(findings, "ERROR")

    def test_source_list_drift_between_languages(self, tmp_path):
        findings = validate(
            write(tmp_path, tr_sources="  - name: Other\n    url: https://other.com/x\n")
        )
        assert "bilingual-parity" in checks(findings, "ERROR")

    def test_date_drift_between_languages(self, tmp_path):
        findings = validate(write(tmp_path, published="2026-07-21", tr_published="2026-07-22"))
        assert "bilingual-parity" in checks(findings, "ERROR")

    def test_publication_before_the_event(self, tmp_path):
        findings = validate(write(tmp_path, published="2026-07-01"))
        assert "publication-date" in checks(findings, "ERROR")

    def test_missing_evidence_log(self, tmp_path):
        findings = validate(write(tmp_path, evidence_log=False))
        assert "evidence-log" in checks(findings, "ERROR")

    def test_missing_ledger_entry(self, tmp_path):
        findings = validate(write(tmp_path, ledger=False))
        assert "ledger-entry" in checks(findings, "ERROR")

    def test_orphan_turkish_article(self, tmp_path):
        write(tmp_path)
        d = tmp_path / "content" / "articles" / "tr" / "2026" / "07"
        (d / "orphan.md").write_text(
            ARTICLE.format(title="Orphan", slug="orphan", lang="tr", published_line="",
                           sources=GOOD_SOURCES, claims=GOOD_CLAIMS),
            encoding="utf-8",
        )
        findings = validate(tmp_path)
        assert any(f.slug == "orphan" for f in findings)


class TestWarnings:
    def test_bare_origin_source_url(self, tmp_path):
        sources = "  - name: Reuters\n    url: https://www.reuters.com/\n"
        findings = validate(write(tmp_path, sources=sources, tr_sources=sources))
        assert "bare-source-url" in checks(findings, "WARN")
        assert "bare-source-url" not in checks(findings, "ERROR")

    def test_headline_with_no_confirmed_claim(self, tmp_path):
        claims = (
            '  - text: "A claim"\n    type: business\n'
            "    verdict: single-source\n    evidence: [1]\n"
        )
        findings = validate(write(tmp_path, claims=claims, tr_claims=claims))
        assert "unconfirmed-headline" in checks(findings, "WARN")

    def test_a_deep_link_is_fine(self, tmp_path):
        assert not [f for f in validate(write(tmp_path)) if f.check == "bare-source-url"]


class TestRealArchive:
    """The gate must be adoptable today, so every ERROR check passes right now."""

    def test_no_errors_in_the_live_archive(self):
        repo = Path(__file__).resolve().parents[2]
        errors = [f for f in validate(repo) if f.level == "ERROR"]
        assert not errors, "\n".join(str(f) for f in errors)

    def test_known_warnings_are_bounded(self):
        """Recorded, not hidden. Tighten this as they are cleared.

        At the time of writing: 5 bare-origin URLs across 3 articles, and 1
        article whose claims are all `single-source`.
        """
        repo = Path(__file__).resolve().parents[2]
        warnings = [f for f in validate(repo) if f.level == "WARN"]
        assert len(warnings) <= 8, "\n".join(str(f) for f in warnings)
