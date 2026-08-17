"""Live validation of the source registry: does every URL resolve, parse — and
is anyone still writing at the other end?

Feed-like sources (rss, arxiv_api, youtube_channel) must return entries; html
sources must return a substantive page. Rate limits mirror the ingest stage.

The freshness check is the part that was missing. This asked for HTTP 200 and a
non-empty entry list and nothing else, so a feed frozen in place passed as
healthy indefinitely: Qwen Blog's newest post was from September 2025 and it
read `[ok] 44 entries` in every weekly report, while the site had to source a
Qwen licensing story from Hugging Face model cards because the Tier-0 vendor
feed had delivered nothing in 154 consecutive ingest runs. "Still serving" and
"still publishing" are different questions and only the first was ever asked.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import feedparser
import httpx

from noiseless.ingest import FEED_TYPES, _delay_for, polite_get
from noiseless.sources import DEFAULT_MAX_AGE_DAYS, Source

MIN_HTML_BYTES = 2048

OK = "ok"
STALE = "stale"
FAIL = "fail"
BLOCKED = "blocked"


@dataclass(frozen=True)
class CheckResult:
    source: Source
    state: str
    detail: str
    newest_entry: str | None = None

    @property
    def ok(self) -> bool:
        return self.state == OK

    @property
    def needs_attention(self) -> bool:
        """A known runner-address block is not news; the other two are."""
        return self.state in (FAIL, STALE)


# A date element holding nothing but a year. jmlr.org/jmlr.xml publishes all 137
# of its items as `<pubDate>2026</pubDate>`.
_BARE_YEAR = re.compile(r"^\s*\d{4}\s*$")


def newest_entry_date(parsed) -> datetime | None:
    """The most recent genuinely parsable date across a feed's entries, or None."""
    newest: datetime | None = None
    for entry in parsed.entries:
        for raw_field, parsed_field in (
            ("published", "published_parsed"),
            ("updated", "updated_parsed"),
        ):
            stamp = entry.get(parsed_field)
            if not stamp:
                continue
            # feedparser turns a bare year into 1 January of that year, so
            # JMLR's items arrive looking like a real date several months back.
            # Believing it would park the source permanently just past whatever
            # allowance anyone sets, for a reason that has nothing to do with
            # when it last published. "We cannot measure this" is the true
            # finding and the one worth reporting.
            if _BARE_YEAR.match(str(entry.get(raw_field, ""))):
                continue
            when = datetime(*stamp[:6], tzinfo=timezone.utc)
            if newest is None or when > newest:
                newest = when
            break
    return newest


def check_source(
    source: Source, client: httpx.Client, now: datetime | None = None
) -> CheckResult:
    now = now or datetime.now(timezone.utc)
    try:
        response = polite_get(client, source.url)
    except Exception as exc:
        return CheckResult(source, FAIL, f"request failed: {exc}")

    if response.status_code in (401, 403) and source.runner_blocked:
        # Recorded in the registry with a reason, so it stops being reported as
        # a fresh discovery every Monday for a year.
        return CheckResult(
            source, BLOCKED,
            f"HTTP {response.status_code} — known address-range block, see notes",
        )

    if response.status_code != 200:
        return CheckResult(source, FAIL, f"HTTP {response.status_code}")

    if source.type in FEED_TYPES:
        parsed = feedparser.parse(response.text)
        count = len(parsed.entries)
        if not count:
            return CheckResult(source, FAIL, "feed parsed but contains no entries")

        newest = newest_entry_date(parsed)
        if newest is None:
            # jmlr.org/jmlr.xml carries the bare string "2026" where a date
            # belongs. Unmeasurable is not the same as healthy, and reporting it
            # as healthy is how it stayed unmeasurable.
            return CheckResult(
                source, STALE, f"{count} entries, none carrying a parsable date"
            )

        allowed = source.max_age_days or DEFAULT_MAX_AGE_DAYS
        age = (now - newest).days
        stamp = newest.date().isoformat()
        if age > allowed:
            return CheckResult(
                source, STALE,
                f"{count} entries, newest {stamp} — {age} days old, past the "
                f"{allowed}-day allowance",
                stamp,
            )
        return CheckResult(source, OK, f"{count} entries, newest {stamp} ({age}d)", stamp)

    if len(response.content) < MIN_HTML_BYTES:
        return CheckResult(
            source, FAIL, f"page too small ({len(response.content)} bytes)"
        )
    return CheckResult(source, OK, f"page OK ({len(response.content)} bytes)")


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
