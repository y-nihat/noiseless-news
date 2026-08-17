""""Still serving" and "still publishing" are different questions.

Live validation asked only the first: HTTP 200 plus a non-empty entry list. So
Qwen Blog — a Tier-0 vendor primary whose newest post was from September 2025 —
read `[ok] 44 entries` in every weekly report while delivering nothing across
154 consecutive ingest runs, and the site sourced a Qwen licensing story from
Hugging Face model cards instead (content/articles/en/2026/08/
alibaba-qwen-revenue-share-plan.md, 2026-08-14). VentureBeat AI, JMLR and the
Yannic Kilcher channel were in the same state, all four invisible.

Meanwhile §4's fourteen-day dead-feed rule had a data file written for it and
no reader: `grep -rn source_stats` outside data/ returns the write path, the
rule's own sentence, and a note claiming the rule is runnable.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from noiseless.source_status import (
    BLOCKED as STATUS_BLOCKED,
    FAILING,
    OK as STATUS_OK,
    SILENT,
    STREAK_DAYS,
    UNTRACKED,
    report,
    summarize,
)
from noiseless.sources import DEFAULT_MAX_AGE_DAYS, Source, SourceRegistryError, load_sources
from noiseless.validate import BLOCKED, FAIL, OK, STALE, check_source

REPO_ROOT = Path(__file__).resolve().parents[2]
NOW = datetime(2026, 8, 17, 12, 0, tzinfo=timezone.utc)


def feed(*dates: str, undated: bool = False) -> str:
    items = "".join(
        f"<item><title>t</title><link>https://e.invalid/{i}</link>"
        + ("" if undated else f"<pubDate>{d}</pubDate>")
        + "</item>"
        for i, d in enumerate(dates)
    )
    return f"<?xml version='1.0'?><rss version='2.0'><channel>{items}</channel></rss>"


def rfc822(days_ago: int) -> str:
    return (NOW - timedelta(days=days_ago)).strftime("%a, %d %b %Y %H:%M:%S +0000")


class FakeResponse:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text
        self.content = text.encode("utf-8")


class FakeClient:
    def __init__(self, response: FakeResponse):
        self._response = response

    def get(self, url, headers=None):
        return self._response


def rss(name="Feed", **kwargs) -> Source:
    return Source(name=name, tier=2, type="rss", url="https://e.invalid/f.xml", **kwargs)


class TestFreshness:
    def test_a_live_feed_passes_and_reports_its_newest_entry(self):
        result = check_source(
            rss(), FakeClient(FakeResponse(200, feed(rfc822(1), rfc822(9)))), now=NOW
        )
        assert result.state == OK
        assert result.newest_entry == "2026-08-16"

    def test_a_feed_frozen_since_last_september_is_no_longer_healthy(self):
        """Qwen Blog: HTTP 200, 44 entries, newest 2025-09-23, `[ok]` every week."""
        result = check_source(
            rss("Qwen Blog"),
            FakeClient(FakeResponse(200, feed(rfc822(328), rfc822(400)))),
            now=NOW,
        )
        assert result.state == STALE
        assert "328 days old" in result.detail
        assert result.newest_entry == "2025-09-23"

    def test_the_boundary_is_the_allowance_not_a_day_either_side(self):
        at = check_source(
            rss(), FakeClient(FakeResponse(200, feed(rfc822(DEFAULT_MAX_AGE_DAYS)))), now=NOW
        )
        past = check_source(
            rss(), FakeClient(FakeResponse(200, feed(rfc822(DEFAULT_MAX_AGE_DAYS + 1)))), now=NOW
        )
        assert at.state == OK
        assert past.state == STALE

    def test_a_source_may_declare_a_slower_cadence(self):
        """A peer-reviewed journal's quiet month is its nature, not a symptom."""
        result = check_source(
            rss("JMLR", max_age_days=180),
            FakeClient(FakeResponse(200, feed(rfc822(120)))),
            now=NOW,
        )
        assert result.state == OK

    def test_an_unmeasurable_date_is_not_treated_as_a_fresh_one(self):
        result = check_source(
            rss("JMLR"),
            FakeClient(FakeResponse(200, feed("x", "y", undated=True))),
            now=NOW,
        )
        assert result.state == STALE
        assert "parsable date" in result.detail

    def test_a_bare_year_is_reported_as_unmeasurable_not_as_an_age(self):
        """All 137 of jmlr.org/jmlr.xml's items carry `<pubDate>2026</pubDate>`.

        feedparser turns that into 1 January, which reads as a real date several
        months in the past — so an age check would report the source stale
        forever, at a distance that grows through the year, for a reason that has
        nothing to do with when JMLR last published a paper.
        """
        result = check_source(
            rss("JMLR"), FakeClient(FakeResponse(200, feed("2026", "2026"))), now=NOW
        )
        assert result.state == STALE
        assert "parsable date" in result.detail, (
            f"reported as an age instead of as unmeasurable: {result.detail}"
        )
        assert result.newest_entry is None

    def test_a_real_date_alongside_a_bare_year_still_counts(self):
        result = check_source(
            rss(), FakeClient(FakeResponse(200, feed("2026", rfc822(2)))), now=NOW
        )
        assert result.state == OK
        assert result.newest_entry == "2026-08-15"

    def test_an_empty_feed_is_still_a_failure_not_a_staleness(self):
        result = check_source(rss(), FakeClient(FakeResponse(200, feed())), now=NOW)
        assert result.state == FAIL

    def test_html_sources_are_judged_on_size_as_before(self):
        page = Source(name="P", tier=0, type="html", url="https://e.invalid/")
        assert check_source(page, FakeClient(FakeResponse(200, "x" * 5000)), now=NOW).state == OK
        assert check_source(page, FakeClient(FakeResponse(200, "tiny")), now=NOW).state == FAIL


class TestKnownBlocks:
    def test_a_403_on_a_registered_block_is_not_reported_as_a_new_failure(self):
        """Three identical weekly issues came from treating this as news."""
        source = rss("MIT News AI", runner_blocked=True, notes="403 from CI addresses")
        result = check_source(source, FakeClient(FakeResponse(403, "")), now=NOW)
        assert result.state == BLOCKED
        assert not result.needs_attention

    def test_a_403_on_any_other_source_is_still_a_failure(self):
        result = check_source(rss("xAI News"), FakeClient(FakeResponse(403, "")), now=NOW)
        assert result.state == FAIL
        assert result.needs_attention

    def test_the_flag_does_not_excuse_a_different_fault(self):
        """Registering a 403 must not blanket-forgive a 500 or a frozen feed."""
        source = rss("MIT News AI", runner_blocked=True, notes="403 from CI addresses")
        assert check_source(source, FakeClient(FakeResponse(500, "")), now=NOW).state == FAIL
        stale = check_source(
            source, FakeClient(FakeResponse(200, feed(rfc822(300)))), now=NOW
        )
        assert stale.state == STALE


class TestTheRegistryFields:
    def _entry(self, **kwargs) -> dict:
        return {"name": "S", "tier": 2, "type": "rss",
                "url": "https://e.invalid/f.xml", **kwargs}

    def _load(self, tmp_path: Path, entry: dict):
        path = tmp_path / "sources.yaml"
        path.write_text(json.dumps({"sources": [entry]}), encoding="utf-8")
        return load_sources(path)

    def test_a_cadence_allowance_must_be_a_positive_integer(self, tmp_path):
        for bad in (0, -5, "soon", 1.5, True):
            with pytest.raises(SourceRegistryError, match="max_age_days"):
                self._load(tmp_path, self._entry(max_age_days=bad))

    def test_a_block_must_be_explained(self, tmp_path):
        """Silencing an alarm without writing down why is how it stays silenced."""
        with pytest.raises(SourceRegistryError, match="requires notes"):
            self._load(tmp_path, self._entry(runner_blocked=True))
        loaded = self._load(
            tmp_path, self._entry(runner_blocked=True, notes="403 from CI addresses")
        )
        assert loaded[0].runner_blocked is True

    def test_the_defaults_leave_existing_entries_alone(self, tmp_path):
        source = self._load(tmp_path, self._entry())[0]
        assert source.max_age_days is None
        assert source.runner_blocked is False

    def test_the_real_registry_still_parses(self):
        sources = load_sources(REPO_ROOT / "policy" / "sources.yaml")
        assert len(sources) > 50


def stats_file(tmp_path: Path, rows: list[tuple[str, dict[str, int]]]) -> Path:
    path = tmp_path / "source_stats.jsonl"
    path.write_text(
        "".join(
            json.dumps({"run_at": f"{day}T0{i % 9}:00:00+00:00", "counts": counts}) + "\n"
            for i, (day, counts) in enumerate(rows)
        ),
        encoding="utf-8",
    )
    return path


def days_back(n: int) -> list[str]:
    return [(NOW - timedelta(days=n - 1 - i)).date().isoformat() for i in range(n)]


class TestTheFourteenDayRule:
    """§4, finally evaluated by something."""

    def test_a_fortnight_of_failed_fetches_is_flagged(self, tmp_path):
        rows = [(day, {"Import AI": -1}) for day in days_back(STREAK_DAYS)]
        statuses = summarize([rss("Import AI")], stats_file(tmp_path, rows))
        assert statuses[0].verdict == FAILING
        assert statuses[0].failing_days == STREAK_DAYS

    def test_a_day_short_of_the_threshold_is_not(self, tmp_path):
        rows = [(day, {"Import AI": -1}) for day in days_back(STREAK_DAYS - 1)]
        statuses = summarize([rss("Import AI")], stats_file(tmp_path, rows))
        assert statuses[0].verdict == STATUS_OK

    def test_one_good_fetch_in_a_day_breaks_the_streak(self, tmp_path):
        """Six runs a day means a transient -1 must not read as a dead feed."""
        rows = [(day, {"S": -1}) for day in days_back(30)]
        recovered = days_back(30)[-3]
        rows.append((recovered, {"S": 4}))
        statuses = summarize([rss("S")], stats_file(tmp_path, rows))
        assert statuses[0].verdict == STATUS_OK
        assert statuses[0].failing_days < STREAK_DAYS

    def test_the_streak_is_counted_in_days_not_rows(self, tmp_path):
        """The file holds about seven rows a day; a row threshold means nothing."""
        rows = [(day, {"S": -1}) for day in days_back(3) for _ in range(8)]
        statuses = summarize([rss("S")], stats_file(tmp_path, rows))
        assert statuses[0].failing_days == 3, "24 rows over 3 days is a 3-day streak"


class TestSilenceAsOpposedToFailure:
    def test_a_feed_silent_past_its_allowance_is_flagged(self, tmp_path):
        rows = [(day, {"S": 0}) for day in days_back(DEFAULT_MAX_AGE_DAYS + 2)]
        statuses = summarize([rss("S")], stats_file(tmp_path, rows))
        assert statuses[0].verdict == SILENT

    def test_a_slow_source_is_judged_against_its_own_cadence(self, tmp_path):
        """A weekly newsletter and a lab blog both cross fourteen days normally."""
        rows = [(day, {"S": 0}) for day in days_back(20)]
        path = stats_file(tmp_path, rows)
        assert summarize([rss("S")], path)[0].verdict == STATUS_OK
        assert summarize([rss("S", max_age_days=14)], path)[0].verdict == SILENT


class TestWhatTheReportDoesNotShoutAbout:
    def test_a_registered_block_is_reported_but_not_flagged(self, tmp_path):
        rows = [(day, {"MIT News AI": -1}) for day in days_back(30)]
        source = rss("MIT News AI", runner_blocked=True, notes="403 from CI addresses")
        status = summarize([source], stats_file(tmp_path, rows))[0]
        assert status.verdict == STATUS_BLOCKED
        assert not status.flagged

    def test_html_sources_are_marked_untracked_rather_than_dead(self, tmp_path):
        page = Source(name="xAI News", tier=0, type="html", url="https://e.invalid/")
        status = summarize([page], stats_file(tmp_path, []))[0]
        assert status.verdict == UNTRACKED
        assert not status.flagged

    def test_candidates_are_out_of_scope(self, tmp_path):
        source = rss("Reuters AI", status="candidate")
        assert summarize([source], stats_file(tmp_path, [])) == []

    def test_one_corrupt_line_does_not_hide_the_rest(self, tmp_path):
        path = stats_file(tmp_path, [(day, {"S": -1}) for day in days_back(STREAK_DAYS)])
        path.write_text("{not json\n" + path.read_text(encoding="utf-8"), encoding="utf-8")
        assert summarize([rss("S")], path)[0].verdict == FAILING


class TestTheReportItself:
    def test_a_flagged_source_makes_it_exit_two(self, tmp_path):
        rows = [(day, {"S": -1}) for day in days_back(STREAK_DAYS)]
        text, code = report([rss("S")], stats_file(tmp_path, rows))
        assert code == 2
        assert "[FLAG] S" in text
        assert "source-status done — 1 flagged" in text

    def test_a_clean_registry_exits_zero(self, tmp_path):
        rows = [(day, {"S": 3}) for day in days_back(5)]
        text, code = report([rss("S")], stats_file(tmp_path, rows))
        assert code == 0
        assert "0 flagged" in text

    def test_a_missing_stats_file_is_not_a_crash(self, tmp_path):
        text, code = report([rss("S")], tmp_path / "absent.jsonl")
        assert code == 0
        assert "no ingest runs recorded" in text
