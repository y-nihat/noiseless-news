"""Live validation of the source registry: does every URL resolve and parse?

Feed-like sources (rss, arxiv_api, youtube_channel) must return entries; html
sources must return a substantive page. Rate limits mirror the ingest stage.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import feedparser
import httpx

from noiseless.ingest import _delay_for, polite_get
from noiseless.sources import Source

FEED_TYPES = {"rss", "arxiv_api", "youtube_channel"}
MIN_HTML_BYTES = 2048


@dataclass(frozen=True)
class CheckResult:
    source: Source
    ok: bool
    detail: str


def check_source(source: Source, client: httpx.Client) -> CheckResult:
    try:
        response = polite_get(client, source.url)
    except Exception as exc:
        return CheckResult(source, False, f"request failed: {exc}")

    if response.status_code != 200:
        return CheckResult(source, False, f"HTTP {response.status_code}")

    if source.type in FEED_TYPES:
        parsed = feedparser.parse(response.text)
        if not parsed.entries:
            return CheckResult(source, False, "feed parsed but contains no entries")
        return CheckResult(source, True, f"{len(parsed.entries)} entries")

    if len(response.content) < MIN_HTML_BYTES:
        return CheckResult(source, False, f"page too small ({len(response.content)} bytes)")
    return CheckResult(source, True, f"page OK ({len(response.content)} bytes)")


def check_all(sources: list[Source]) -> list[CheckResult]:
    results = []
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for source in sources:
            # candidates/retired are out of rotation; the periodic source-review
            # pass re-checks candidates (policy/source-lifecycle.md §3)
            if source.status != "active":
                continue
            results.append(check_source(source, client))
            time.sleep(_delay_for(source))
    return results
