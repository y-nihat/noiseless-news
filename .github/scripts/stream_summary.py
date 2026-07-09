"""Compact, readable progress log from Claude Code's stream-json output.

Reads the JSONL event stream on stdin (already tee'd to a file by the workflow)
and prints one short line per meaningful event, so the Actions log shows what
the agent is doing without dumping full message payloads.
"""

import json
import sys


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        etype = event.get("type")
        if etype == "system" and event.get("subtype") == "init":
            print(f"[init] model={event.get('model')}", flush=True)
        elif etype == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    text = " ".join(block.get("text", "").split())
                    if text:
                        print(f"[claude] {text[:220]}", flush=True)
                elif block.get("type") == "tool_use":
                    brief = json.dumps(block.get("input", {}), ensure_ascii=False)[:160]
                    print(f"[tool] {block.get('name')} {brief}", flush=True)
        elif etype == "result":
            print(
                f"[result] subtype={event.get('subtype')} "
                f"is_error={event.get('is_error')} turns={event.get('num_turns')} "
                f"duration_min={round((event.get('duration_ms') or 0) / 60000, 1)}",
                flush=True,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
