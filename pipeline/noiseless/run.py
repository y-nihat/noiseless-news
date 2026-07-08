"""Pipeline stage runner.

Usage (inside the pipeline container):
    python -m noiseless.run validate-sources
    python -m noiseless.run ingest [--source NAME] [--data-dir data]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from noiseless.ingest import ingest_all
from noiseless.sources import SourceRegistryError, load_sources

REGISTRY_PATH = Path("policy/sources.yaml")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="noiseless")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-sources", help="validate policy/sources.yaml")

    ingest_parser = subparsers.add_parser("ingest", help="fetch registered feeds")
    ingest_parser.add_argument("--source", help="ingest a single source by name")
    ingest_parser.add_argument("--data-dir", default="data")

    args = parser.parse_args(argv)

    try:
        sources = load_sources(REGISTRY_PATH)
    except SourceRegistryError as exc:
        print(f"source registry invalid: {exc}", file=sys.stderr)
        return 1

    if args.command == "validate-sources":
        by_tier: dict[int, int] = {}
        for source in sources:
            by_tier[source.tier] = by_tier.get(source.tier, 0) + 1
        tiers = ", ".join(f"tier {t}: {n}" for t, n in sorted(by_tier.items()))
        print(f"OK — {len(sources)} sources ({tiers})")
        return 0

    if args.command == "ingest":
        summary = ingest_all(sources, args.data_dir, only_source=args.source)
        failures = [name for name, count in summary.items() if count < 0]
        total_new = sum(count for count in summary.values() if count > 0)
        print(f"done — {total_new} new items, {len(failures)} failed sources")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
