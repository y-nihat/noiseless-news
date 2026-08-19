"""Making the verification reachable from the article it justifies.

`data/verified/<slug>.json` holds the per-claim reasoning, the independence
analysis and the adversarial falsifier's findings for all 57 stories, and
`publish.py` never opened the directory. A reader got a coloured badge and a
plain-text `[1] [2]` next to a source list with no anchors — visually
indistinguishable from any site that lists sources.
"""

from __future__ import annotations

import json

import pytest
from conftest import write_twins

from noiseless.publish import build_site, claim_reasoning, load_evidence

ARTICLE = """---
title: A verified story
date: 2026-07-20
slug: verified-story
lang: {lang}
tldr: A summary.
sources:
  - name: Primary Source
    url: https://example.com/primary
  - name: Second Outlet
    url: https://example.org/report
claims:
  - text: "{claim_one}"
    type: business
    verdict: confirmed
    evidence: [1, 2]
  - text: "{claim_two}"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

Body.
"""

EVIDENCE = {
    "slug": "verified-story",
    "checked_at": "2026-07-20T23:41:00+00:00",
    "method": "Fresh verifier sub-agent and independent adversarial falsifier.",
    "claims": [
        {
            "text": "The company raised $300 million",
            "verdict": "confirmed",
            "reasoning": "Two independent sources: the company's own release and "
            "an independently reported story with an on-record quote. Eight other "
            "outlets relayed the same press release verbatim and were not counted.",
        },
        {
            "text": "It outperforms the incumbent chip",
            "verdict": "vendor-claim",
            "reasoning": "Benchmark supplied by the vendor; no independent "
            "reproduction found.",
        },
    ],
}


def make(tmp_path, *, evidence=EVIDENCE, tr_claims=None):
    for lang in ("en", "tr"):
        d = tmp_path / "content" / "articles" / lang / "2026" / "07"
        d.mkdir(parents=True, exist_ok=True)
        claims = tr_claims if (lang == "tr" and tr_claims) else (
            "The company raised $300 million",
            "It outperforms the incumbent chip",
        )
        (d / "verified-story.md").write_text(
            ARTICLE.format(lang=lang, claim_one=claims[0], claim_two=claims[1]),
            encoding="utf-8",
        )
    write_twins(tmp_path, "verified-story", claims=2)
    verified = tmp_path / "data" / "verified"
    if evidence is not None:
        (verified / "verified-story.json").write_text(
            json.dumps(evidence), encoding="utf-8"
        )
    else:
        (verified / "verified-story.json").unlink()
    build_site(tmp_path, tmp_path / "site")
    return tmp_path / "site" / "articles" / "verified-story.html"


class TestLoadEvidence:
    def test_missing_file_is_not_an_error(self, tmp_path):
        assert load_evidence(tmp_path, "absent") == {}

    def test_malformed_file_is_not_an_error(self, tmp_path):
        (tmp_path / "verified").mkdir()
        (tmp_path / "verified" / "broken.json").write_text("{truncated", encoding="utf-8")
        assert load_evidence(tmp_path, "broken") == {}

    def test_non_object_is_rejected(self, tmp_path):
        (tmp_path / "verified").mkdir()
        (tmp_path / "verified" / "list.json").write_text("[1,2]", encoding="utf-8")
        assert load_evidence(tmp_path, "list") == {}


class TestClaimMatching:
    def test_matches_on_claim_text(self):
        claims = [
            {"text": "It outperforms the incumbent chip"},
            {"text": "The company raised $300 million"},
        ]
        reasons = claim_reasoning(EVIDENCE, claims)
        assert "no independent reproduction" in reasons[0]
        assert "Eight other outlets" in reasons[1]

    def test_falls_back_to_position_for_translated_claims(self):
        """Turkish claims are translations and never match by text."""
        claims = [{"text": "Şirket 300 milyon dolar topladı"}, {"text": "Rakibini geçiyor"}]
        reasons = claim_reasoning(EVIDENCE, claims)
        assert reasons[0].startswith("Two independent sources")
        assert reasons[1].startswith("Benchmark supplied")

    def test_no_positional_guessing_when_counts_disagree(self):
        """Mismatched counts mean we cannot know which reasoning belongs where."""
        assert claim_reasoning(EVIDENCE, [{"text": "only one claim"}]) == {}

    def test_empty_evidence_yields_nothing(self):
        assert claim_reasoning({}, [{"text": "a"}]) == {}
        assert claim_reasoning({"claims": []}, [{"text": "a"}]) == {}

    def test_entries_without_reasoning_are_skipped(self):
        evidence = {"claims": [{"text": "a", "verdict": "confirmed"}]}
        assert claim_reasoning(evidence, [{"text": "a"}]) == {}


class TestRendering:
    def test_reasoning_is_rendered_per_claim(self, tmp_path):
        page = make(tmp_path).read_text(encoding="utf-8")
        assert "Why this verdict" in page
        assert "Eight other outlets relayed the same press release" in page

    def test_evidence_log_is_linked(self, tmp_path):
        page = make(tmp_path).read_text(encoding="utf-8")
        assert "data/verified/verified-story.json" in page

    def test_checked_at_is_shown_as_a_date(self, tmp_path):
        page = make(tmp_path).read_text(encoding="utf-8")
        assert "Verified 2026-07-20" in page
        assert "23:41" not in page

    def test_reference_markers_link_to_their_source(self, tmp_path):
        page = make(tmp_path).read_text(encoding="utf-8")
        assert "<a href='#s1'>[1]</a>" in page
        assert "<a href='#s2'>[2]</a>" in page
        assert "<li id='s1'>" in page and "<li id='s2'>" in page

    def test_an_article_without_an_evidence_log_is_held_from_the_site(self, tmp_path):
        """It used to render normally, minus the reasoning. It no longer renders.

        On 2026-08-18 two articles were committed without their logs; the site
        must not carry an article whose verdicts cannot be audited, and a stub
        at the URL is what keeps a shared link from 404ing while asserting
        nothing.
        """
        page = make(tmp_path, evidence=None).read_text(encoding="utf-8")
        assert "A verified story" not in page, "the headline of a held story leaked"
        assert "Temporarily withheld" in page
        assert 'name="robots" content="noindex"' in page
        assert "Why this verdict" not in page
        index = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
        assert "verified-story" not in index
        feed = (tmp_path / "site" / "feed.xml").read_text(encoding="utf-8")
        assert "verified-story" not in feed
        sitemap = (tmp_path / "site" / "sitemap.xml").read_text(encoding="utf-8")
        assert "verified-story" not in sitemap

    def test_turkish_page_shows_the_reasoning_with_a_language_note(self, tmp_path):
        make(tmp_path, tr_claims=("Şirket 300 milyon dolar topladı", "Rakibini geçiyor"))
        page = (
            tmp_path / "site" / "tr" / "articles" / "verified-story.html"
        ).read_text(encoding="utf-8")
        assert "Bu hüküm neden verildi" in page
        assert "Eight other outlets" in page
        assert "kanıt notları İngilizcedir" in page

    def test_reasoning_is_escaped(self, tmp_path):
        evidence = {
            "claims": [
                {"text": "The company raised $300 million", "reasoning": "<script>x</script>"},
                {"text": "It outperforms the incumbent chip", "reasoning": "fine"},
            ]
        }
        page = make(tmp_path, evidence=evidence).read_text(encoding="utf-8")
        assert "<script>x</script>" not in page
        assert "&lt;script&gt;" in page


class TestRealArchive:
    def test_every_article_the_site_renders_has_a_reachable_evidence_log(self, tmp_path):
        """The invariant the site makes, checked on the site rather than the tree.

        Until 2026-08-19 this asserted the *archive* had no gaps, which is a
        different and weaker guarantee than the reader's: what matters is that
        no rendered article page lacks its log. The build holds such stories,
        and the held set must be exactly the validator's ERROR set — the two
        halves of the same guarantee, checked against each other.
        """
        from pathlib import Path

        from noiseless.publish import build_site, load_articles, withheld_stories
        from noiseless.validate_content import MAX_HELD_DEFAULT

        repo = Path(__file__).resolve().parents[2]
        held = withheld_stories(repo)
        counts = build_site(repo, tmp_path / "site")
        rendered = [
            a.slug for a in load_articles(repo / "content", "en") if a.slug not in held
        ]
        missing = [slug for slug in rendered if not load_evidence(repo / "data", slug)]
        assert not missing, f"rendered articles with no readable evidence log: {missing}"
        assert counts["held"] == len(held)
        for slug in held:
            page = (tmp_path / "site" / "articles" / f"{slug}.html").read_text("utf-8")
            assert "Temporarily withheld" in page
        assert len(held) <= MAX_HELD_DEFAULT, (
            f"the archive is past the deploy ceiling: {sorted(held)}"
        )

    def test_reasoning_resolves_for_most_of_the_archive(self):
        """Matching must not silently fail — the feature would render nothing.

        Measured on the archive at the time of writing: 194 of 261 claims (74%)
        resolve, and 4 of 57 articles resolve none. Those four all gained claims
        through in-place updates after their evidence log was written, so the
        claim counts no longer agree and the positional fallback is correctly
        refused rather than guessing. The thresholds here are deliberately loose:
        they exist to catch matching breaking entirely, not to freeze a ratio.
        """
        from pathlib import Path

        from noiseless.publish import load_articles

        repo = Path(__file__).resolve().parents[2]
        articles = [a for a in load_articles(repo / "content", "en") if a.meta.get("claims")]
        resolved = total = 0
        without = []
        for article in articles:
            reasons = claim_reasoning(
                load_evidence(repo / "data", article.slug), article.meta["claims"]
            )
            total += len(article.meta["claims"])
            resolved += len(reasons)
            if not reasons:
                without.append(article.slug)

        assert resolved / total > 0.5, f"only {resolved}/{total} claims resolved"
        assert len(without) <= len(articles) * 0.2, (
            f"reasoning did not resolve for {len(without)} articles: {without}"
        )
