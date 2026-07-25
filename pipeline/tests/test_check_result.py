"""Tests for the night-cycle result gate.

check_result.py decides whether a cycle counts as successful, whether the whole
night must stop, and — since it is the only thing that reads the agent's result
event — what a night cost. It is the highest-consequence branch in the system
and had no coverage: a regression here either lets a dead agent look green or
ends a healthy night early.

Loaded by path because .github/scripts/ is not an importable package.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".github" / "scripts" / "check_result.py"

_spec = importlib.util.spec_from_file_location("check_result", SCRIPT)
check_result = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_result)


def stream(tmp_path: Path, *events: dict) -> str:
    path = tmp_path / "stream.jsonl"
    path.write_text(
        "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
    )
    return str(path)


OK_RESULT = {
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "num_turns": 41,
    "duration_ms": 1_200_000,
    "total_cost_usd": 1.23,
    "usage": {"input_tokens": 900, "output_tokens": 120},
}


class TestClassify:
    def test_clean_result_is_success(self):
        assert check_result.classify(OK_RESULT) == (0, "cycle completed OK")

    def test_missing_result_event_is_failure(self):
        """A crashed or timed-out agent must never be scored as a clean cycle."""
        code, reason = check_result.classify(None)
        assert code == 1
        assert "died mid-cycle" in reason

    def test_generic_error_is_failure_not_usage_stop(self):
        code, _ = check_result.classify(
            {"is_error": True, "subtype": "error", "result": "tool call failed"}
        )
        assert code == 1

    @pytest.mark.parametrize(
        "text",
        [
            "Claude AI usage limit reached",
            "rate limit exceeded",
            "your credit balance is too low",
            "quota exceeded for this organization",
        ],
    )
    def test_usage_limit_ends_the_night(self, text):
        code, _ = check_result.classify({"is_error": True, "result": text})
        assert code == 3

    def test_article_text_cannot_trigger_a_usage_stop(self):
        """A story *about* rate limits must not end the night.

        The classifier only reads the result event's own fields, and only when
        is_error is set — an assistant message quoting "usage limit" is ignored.
        """
        assert check_result.classify(
            {"is_error": False, "result": "EU fines X over API rate limit policy"}
        ) == (0, "cycle completed OK")


class TestReadResult:
    def test_last_result_event_wins(self, tmp_path):
        path = stream(
            tmp_path,
            {"type": "system", "subtype": "init"},
            {"type": "result", "subtype": "first", "is_error": True},
            {"type": "result", "subtype": "second", "is_error": False},
        )
        assert check_result.read_result(path)["subtype"] == "second"

    def test_malformed_lines_are_skipped(self, tmp_path):
        path = tmp_path / "stream.jsonl"
        path.write_text(
            'not json\n{"type": "result", "subtype": "success"}\n\n', encoding="utf-8"
        )
        assert check_result.read_result(str(path))["subtype"] == "success"

    def test_missing_file_reports_never_started(self, tmp_path):
        code = check_result.main([str(tmp_path / "absent.jsonl")])
        assert code == 1


class TestTelemetry:
    def test_numeric_fields_are_recorded(self, tmp_path):
        stats = tmp_path / "night-stats.jsonl"
        code = check_result.main(
            [
                stream(tmp_path, OK_RESULT),
                "--stats-file",
                str(stats),
                "--night",
                "2026-07-25T22:00:00Z",
                "--cycle",
                "3",
            ]
        )
        assert code == 0
        record = json.loads(stats.read_text(encoding="utf-8").strip())
        assert record["night"] == "2026-07-25T22:00:00Z"
        assert record["cycle"] == "3"
        assert record["gate"] == 0
        assert record["cost_usd"] == 1.23
        assert record["num_turns"] == 41
        assert record["tokens"] == {"input_tokens": 900, "output_tokens": 120}

    def test_agent_free_text_is_never_committed(self, tmp_path):
        """The stats file is public. Only numbers may reach it."""
        secret = "DRAFT ARTICLE TEXT the agent happened to be holding"
        stats = tmp_path / "night-stats.jsonl"
        check_result.main(
            [
                stream(tmp_path, {**OK_RESULT, "result": secret, "message": secret}),
                "--stats-file",
                str(stats),
            ]
        )
        written = stats.read_text(encoding="utf-8")
        assert secret not in written
        assert "result" not in json.loads(written)
        assert "message" not in json.loads(written)

    def test_records_append_across_cycles(self, tmp_path):
        stats = tmp_path / "night-stats.jsonl"
        for cycle in ("1", "2"):
            check_result.main(
                [stream(tmp_path, OK_RESULT), "--stats-file", str(stats), "--cycle", cycle]
            )
        lines = stats.read_text(encoding="utf-8").strip().splitlines()
        assert [json.loads(line)["cycle"] for line in lines] == ["1", "2"]

    def test_a_dead_cycle_still_leaves_a_record(self, tmp_path):
        stats = tmp_path / "night-stats.jsonl"
        code = check_result.main(
            [
                stream(tmp_path, {"type": "system", "subtype": "init"}),
                "--stats-file",
                str(stats),
            ]
        )
        assert code == 1
        assert json.loads(stats.read_text(encoding="utf-8"))["subtype"] == "no-result-event"

    def test_stats_file_is_optional(self, tmp_path):
        assert check_result.main([stream(tmp_path, OK_RESULT)]) == 0
