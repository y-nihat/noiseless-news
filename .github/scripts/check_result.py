"""Gate a night cycle on the agent's actual outcome, and record what it cost.

Reads the stream-json file from one cycle and classifies it:
  exit 0 — cycle completed successfully
  exit 1 — cycle failed (crash, timeout, generic error)
  exit 3 — usage/credit/rate limit: the supervisor must end the night

A dead agent must never look green, and a credit exhaustion must be
distinguishable from an ordinary error so the loop stops instead of retrying.

With --stats-file, one record per cycle is appended as JSON Lines so cost, turns
and duration become measurable instead of being estimated in prose. Only the
numeric and enum fields in STAT_FIELDS are written: the result event also carries
the agent's own free text, and that must never be copied into a committed file.
"""

import argparse
import json
import os
import re

USAGE_LIMIT = re.compile(
    r"usage limit|rate.?limit|credit balance|out of credits?|quota exceeded"
    r"|limit reached|insufficient credit",
    re.IGNORECASE,
)

# Numeric fields only — never `result`, `error` or `message`, which carry
# agent-authored text and would leak article drafts or fetched page content into
# the public audit trail.
STAT_FIELDS = ("num_turns", "duration_ms", "duration_api_ms", "total_cost_usd")


def read_stream(path: str) -> tuple[dict | None, dict[str, int]]:
    """Return the last `result` event and a per-tool call count.

    The tool counts are the only committed evidence that policy §5's multi-agent
    protocol actually ran. 52 of 54 evidence logs assert a fresh verifier and an
    adversarial falsifier — in prose, written by the same session that drafted
    the article. Nothing else survived the night: the stream file lives on the
    runner and is destroyed with it.

    Counting tool *names* is safe to commit; the tool inputs are not, since they
    carry search queries, fetched URLs and article drafts.
    """
    result = None
    tools: dict[str, int] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                result = event
            elif event.get("type") == "assistant":
                content = event.get("message", {}).get("content")
                for block in content if isinstance(content, list) else []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = str(block.get("name", "unknown"))
                        tools[name] = tools.get(name, 0) + 1
    return result, tools


def read_result(path: str) -> dict | None:
    """Back-compatible accessor for the result event alone."""
    return read_stream(path)[0]


def classify(result: dict | None) -> tuple[int, str]:
    """Map a result event to (exit code, human-readable reason)."""
    if result is None:
        return 1, "FAIL: no result event — the agent died mid-cycle (crash or timeout)"

    if result.get("is_error"):
        # Only the result event's own fields — not article content — decide this.
        result_text = json.dumps(
            {k: result.get(k) for k in ("subtype", "result", "error", "message")}
        )
        if USAGE_LIMIT.search(result_text):
            return 3, "USAGE LIMIT: ending the night"
        return 1, "FAIL: agent reported an error"

    return 0, "cycle completed OK"


def stat_record(result: dict | None, night: str, cycle: str, gate: int,
                tools: dict[str, int] | None = None) -> dict:
    """Build the committed telemetry record. Numeric fields only, by design."""
    record: dict = {"night": night, "cycle": cycle, "gate": gate}
    if tools:
        record["tools"] = dict(sorted(tools.items()))
        # Searches and fetches are what a verification pass is made of, so this
        # is the number to look at when asking whether one actually happened.
        record["research_calls"] = sum(
            count for name, count in tools.items()
            if name in ("WebSearch", "WebFetch")
        )
    if result is None:
        record["subtype"] = "no-result-event"
        return record
    record["subtype"] = result.get("subtype")
    record["is_error"] = bool(result.get("is_error"))
    for field in STAT_FIELDS:
        value = result.get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            record["cost_usd" if field == "total_cost_usd" else field] = value
    usage = result.get("usage")
    if isinstance(usage, dict):
        tokens = {k: v for k, v in usage.items() if isinstance(v, int)}
        if tokens:
            record["tokens"] = tokens
    return record


def append_stats(path: str, record: dict) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_result")
    parser.add_argument("stream_file")
    parser.add_argument("--stats-file", help="append one JSONL telemetry record here")
    parser.add_argument("--night", default="", help="night start ISO timestamp")
    parser.add_argument("--cycle", default="", help="cycle number")
    args = parser.parse_args(argv)

    try:
        result, tools = read_stream(args.stream_file)
    except FileNotFoundError:
        print("FAIL: no agent output file — the agent never started")
        if args.stats_file:
            append_stats(
                args.stats_file,
                {
                    "night": args.night,
                    "cycle": args.cycle,
                    "gate": 1,
                    "subtype": "no-output-file",
                },
            )
        return 1

    code, reason = classify(result)

    if result is not None:
        cost = result.get("total_cost_usd")
        summary = (
            f"subtype={result.get('subtype')} is_error={result.get('is_error')} "
            f"turns={result.get('num_turns')} "
            f"duration_min={round((result.get('duration_ms') or 0) / 60000, 1)}"
            + (f" cost_usd={cost}" if isinstance(cost, (int, float)) else "")
        )
        print(summary)
        step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if step_summary:
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write(f"- cycle result: `{summary}`\n")

    if args.stats_file:
        append_stats(
            args.stats_file, stat_record(result, args.night, args.cycle, code, tools)
        )

    print(reason)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
