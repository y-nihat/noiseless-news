"""Gate a night cycle on the agent's actual outcome.

Reads the stream-json file from one cycle and classifies it:
  exit 0 — cycle completed successfully
  exit 1 — cycle failed (crash, timeout, generic error)
  exit 3 — usage/credit/rate limit: the supervisor must end the night

A dead agent must never look green, and a credit exhaustion must be
distinguishable from an ordinary error so the loop stops instead of retrying.
"""

import json
import os
import re
import sys

USAGE_LIMIT = re.compile(
    r"usage limit|rate.?limit|credit balance|out of credits?|quota exceeded"
    r"|limit reached|insufficient credit",
    re.IGNORECASE,
)


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
        print("FAIL: no result event — the agent died mid-cycle (crash or timeout)")
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
            f.write(f"- cycle result: `{summary}`\n")

    if result.get("is_error"):
        # Only the result event's own fields — not article content — decide this.
        result_text = json.dumps(
            {k: result.get(k) for k in ("subtype", "result", "error", "message")}
        )
        if USAGE_LIMIT.search(result_text):
            print("USAGE LIMIT: ending the night")
            return 3
        print("FAIL: agent reported an error")
        return 1

    print("cycle completed OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
