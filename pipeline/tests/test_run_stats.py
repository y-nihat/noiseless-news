"""Tests for the per-run source track record.

policy/source-lifecycle.md §4 builds demotion and dead-feed rules on a stats
file that never existed, so neither rule could ever run and a Tier-2 source sat
dead for two weeks without a signal. These tests cover the file's shape rather
than its content, because the rules that read it care about exactly two things:
that a run leaves a record, and that a failed fetch is distinguishable from a
source that simply had no new items.
"""

from __future__ import annotations

import json

from noiseless.run import STATS_FILENAME, write_ingest_stats


def read_records(data_dir):
    path = data_dir / "ledger" / STATS_FILENAME
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_writes_one_record_per_run(tmp_path):
    write_ingest_stats(tmp_path, {"Anthropic News": 2, "arXiv cs.AI": 0})
    write_ingest_stats(tmp_path, {"Anthropic News": 1, "arXiv cs.AI": 7})

    records = read_records(tmp_path)
    assert len(records) == 2
    assert records[0]["counts"] == {"Anthropic News": 2, "arXiv cs.AI": 0}
    assert records[1]["counts"]["arXiv cs.AI"] == 7
    assert records[0]["run_at"].endswith("+00:00")


def test_failure_is_distinguishable_from_a_quiet_source(tmp_path):
    """-1 means the fetch raised; 0 means the feed was fine and had nothing new.

    Collapsing these is what made a dead feed invisible for two weeks.
    """
    write_ingest_stats(tmp_path, {"MIT News AI": -1, "Quiet Blog": 0})
    counts = read_records(tmp_path)[0]["counts"]
    assert counts["MIT News AI"] == -1
    assert counts["Quiet Blog"] == 0


def test_creates_the_ledger_directory_when_missing(tmp_path):
    target = tmp_path / "scratch"
    write_ingest_stats(target, {"Some Source": 3})
    assert (target / "ledger" / STATS_FILENAME).exists()


def test_empty_summary_writes_nothing(tmp_path):
    """A --source run that matched nothing should not add a misleading record."""
    assert write_ingest_stats(tmp_path, {}) is None
    assert not (tmp_path / "ledger").exists()
