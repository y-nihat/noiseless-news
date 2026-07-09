"""Gate the workflow on the agent's actual outcome.

Reads the stream-json file produced by the agent step, finds the final result
event, and fails (exit 1) when the agent never finished or reported an error —
so a dead agent turns the job red instead of silently passing.
"""

import json
import os
import sys


def main() -> int:
    path = sys.argv[1]
    result = None
    try:
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
    except FileNotFoundError:
        print("FAIL: no agent output file — the agent never started")
        return 1

    if result is None:
        print("FAIL: no result event — the agent died mid-run")
        return 1

    summary = (
        f"subtype={result.get('subtype')} is_error={result.get('is_error')} "
        f"turns={result.get('num_turns')} "
        f"duration_min={round((result.get('duration_ms') or 0) / 60000, 1)}"
    )
    print(summary)

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(f"### Nightly agent result\n\n`{summary}`\n")

    if result.get("is_error"):
        print("FAIL: agent reported an error")
        return 1
    print("agent completed OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
