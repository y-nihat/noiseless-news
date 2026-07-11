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

    validate_parser = subparsers.add_parser(
        "validate-sources", help="validate policy/sources.yaml"
    )
    validate_parser.add_argument(
        "--live",
        action="store_true",
        help="also fetch every non-retired URL and check that it resolves and parses",
    )

    ingest_parser = subparsers.add_parser("ingest", help="fetch registered feeds")
    ingest_parser.add_argument(
        "--source",
        action="append",
        help="ingest only the named source(s); repeatable",
    )
    ingest_parser.add_argument("--data-dir", default="data")

    publish_parser = subparsers.add_parser(
        "publish", help="build the static site from content/ and data/"
    )
    publish_parser.add_argument("--out", default="site/dist")

    dedup_parser = subparsers.add_parser(
        "dedup-check",
        help="check a candidate story against the whole archive (exit 2 = strong match)",
    )
    dedup_parser.add_argument("--title", required=True)
    dedup_parser.add_argument(
        "--url", action="append", default=[], help="candidate source URL(s); repeatable"
    )

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
        if args.live:
            from noiseless.validate import check_all

            failures = 0
            for result in check_all(sources):
                mark = "ok  " if result.ok else "FAIL"
                print(f"[{mark}] {result.source.name}: {result.detail}")
                failures += 0 if result.ok else 1
            print(f"live check done — {failures} failures")
            return 0 if failures == 0 else 2
        return 0

    if args.command == "ingest":
        summary = ingest_all(sources, args.data_dir, only_sources=args.source)
        failures = [name for name, count in summary.items() if count < 0]
        total_new = sum(count for count in summary.values() if count > 0)
        print(f"done — {total_new} new items, {len(failures)} failed sources")
        return 0

    if args.command == "publish":
        from noiseless.publish import build_site

        counts = build_site(Path("."), args.out)
        print(f"site built at {args.out} — articles: en={counts['en']}, tr={counts['tr']}")
        return 0

    if args.command == "dedup-check":
        import json as _json

        from noiseless.dedup import check, load_index

        matches = check(args.title, args.url, load_index(Path(".")))
        print(_json.dumps({"matches": matches}, ensure_ascii=False, indent=2))
        if any(m["strength"] == "strong" for m in matches):
            return 2
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
