"""Raw HTML must not reach the page, and feed summaries must stay citations.

The article body is the one field written wholly by an agent that has just read
attacker-reachable text. Python-Markdown has shipped no sanitiser since 3.0
removed safe_mode, so anything the agent wrote became live markup on a public
site — defacement or a redirect under the masthead of a site that advertises
rigour. No article body in the archive has ever contained a tag, so disabling
raw HTML costs nothing.

Separately, some publishers put a whole article body in the feed's `summary`,
which the repository then committed verbatim and permanently.
"""

from __future__ import annotations

import pytest

from noiseless.ingest import SUMMARY_LIMIT, _clip, normalize_entry
from noiseless.publish import body_to_html
from noiseless.sources import Source
from noiseless.validate_content import RAW_TAG


class TestBodyRendering:
    def test_ordinary_markdown_still_works(self):
        rendered = body_to_html("## What happened\n\nA **bold** [link](https://e.com/x).")
        assert "<h2>What happened</h2>" in rendered
        assert "<strong>bold</strong>" in rendered
        assert 'href="https://e.com/x"' in rendered

    @pytest.mark.parametrize(
        "markup",
        [
            "<script>alert(1)</script>",
            "<iframe src='https://evil.example'></iframe>",
            "<img src=x onerror=alert(1)>",
            "<form action='https://evil.example'><input name='p'></form>",
            "<style>body{display:none}</style>",
        ],
    )
    def test_raw_html_is_escaped_not_executed(self, markup):
        rendered = body_to_html(f"Text.\n\n{markup}\n\nMore text.")
        assert markup not in rendered
        assert "&lt;" in rendered

    def test_escaped_markup_is_visible_rather_than_dropped(self):
        """A defaced article should look wrong, not silently disappear."""
        rendered = body_to_html("<script>alert(1)</script>")
        assert "script" in rendered
        assert "alert(1)" in rendered

    def test_less_than_in_prose_is_left_alone(self):
        rendered = body_to_html("The model scored < 40% on the benchmark.")
        assert "&lt; 40%" in rendered or "< 40%" in rendered

    @pytest.mark.parametrize("scheme", ["javascript", "data", "vbscript"])
    def test_dangerous_link_schemes_are_neutralised(self, scheme):
        rendered = body_to_html(f"[click]({scheme}:alert(1))")
        assert f"{scheme}:alert" not in rendered
        assert "#blocked-scheme" in rendered

    def test_http_links_are_untouched(self):
        for url in ("https://e.com/a", "http://e.com/b", "#anchor"):
            assert url in body_to_html(f"[x]({url})")


class TestValidatorFlagsIt:
    def test_the_detector_matches_what_the_renderer_escapes(self):
        for markup in ("<script>", "<iframe ", "<form ", "<object ", "<embed "):
            assert RAW_TAG.search(markup), markup

    def test_prose_is_not_flagged(self):
        for text in ("x < y", "a<b and c>d", "the <em>only</em> emphasis we allow"):
            assert not RAW_TAG.search(text), text


class TestSummaryClipping:
    def test_short_summaries_are_untouched(self):
        assert _clip("A normal lede.") == "A normal lede."

    def test_a_full_article_body_is_clipped(self):
        clipped = _clip("word " * 5000)
        assert len(clipped) <= SUMMARY_LIMIT + 1
        assert clipped.endswith("…")

    def test_the_lede_survives(self):
        """Triage greps over these, so the beginning must be intact."""
        text = "Anthropic announced X today. " + ("filler " * 2000)
        assert _clip(text).startswith("Anthropic announced X today.")

    def test_applied_at_ingest(self):
        class Entry(dict):
            def get(self, key, default=None):
                return dict.get(self, key, default)

        source = Source(name="Test", tier=2, type="rss", url="https://e.com/feed")
        entry = Entry(
            link="https://e.com/story",
            title="A headline",
            summary="x" * 9000,
        )
        item = normalize_entry(source, entry, "2026-07-25T00:00:00Z")
        assert len(item["summary"]) <= SUMMARY_LIMIT + 1


class TestObligationSweep:
    """A published accusation with no published outcome is a defect."""

    def test_the_night_loop_re_checks_open_obligations(self):
        from pathlib import Path

        script = (
            Path(__file__).resolve().parents[2] / ".github" / "scripts" / "night_loop.sh"
        ).read_text(encoding="utf-8")
        assert "open_obligation" in script
        assert "revisit_after" in script

    def test_the_prompt_tells_the_agent_to_record_one(self):
        from pathlib import Path

        prompt = (
            Path(__file__).resolve().parents[2] / ".github" / "cycle-prompt.md"
        ).read_text(encoding="utf-8")
        assert "open_obligation: true" in prompt
        assert "revisit_after" in prompt
