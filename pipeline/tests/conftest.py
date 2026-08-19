"""Shared helpers for tests that build a site from a scratch archive.

Since 2026-08-19 the build holds any story that lacks its evidence log, its
ledger entry or its Turkish twin (`publish.withheld_stories`). Most rendering
tests write an article and build; they used to get away with writing only the
markdown, because nothing at build time asked for more. They now write the
twins too — which is the invariant the site makes, applied to the fixtures.
"""

from __future__ import annotations

import json
from pathlib import Path


def write_twins(repo_root: Path, slug: str, *, claims: int = 1) -> None:
    """The evidence log and ledger entry that make an article publishable."""
    verified = repo_root / "data" / "verified"
    ledger = repo_root / "data" / "ledger"
    verified.mkdir(parents=True, exist_ok=True)
    ledger.mkdir(parents=True, exist_ok=True)
    (verified / f"{slug}.json").write_text(
        json.dumps({
            "slug": slug,
            "checked_at": "2026-07-10T00:00:00+00:00",
            "method": "test fixture",
            "claims": [
                {"text": f"claim {i + 1}", "type": "fact", "verdict": "confirmed",
                 "reasoning": "fixture", "evidence": ["https://example.com/"]}
                for i in range(claims)
            ],
        }),
        encoding="utf-8",
    )
    (ledger / f"{slug}.json").write_text(
        json.dumps({
            "slug": slug, "title": f"Story {slug}", "status": "published",
            "first_seen": "2026-07-10", "source_urls": ["https://example.com/x"],
        }),
        encoding="utf-8",
    )
