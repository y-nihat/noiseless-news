"""Pipeline stage runner.

Usage (inside the pipeline container):
    python -m noiseless.run validate-sources
    python -m noiseless.run ingest [--source NAME] [--data-dir data]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from noiseless.sources import SourceRegistryError, load_sources

REGISTRY_PATH = Path("policy/sources.yaml")
# policy/source-lifecycle.md §4 builds two governance rules on a per-run source
# track record — demote a repeatedly-contradicted source, retire a feed that has
# been dead 14 days. ingest_all has always returned the numbers; nothing ever
# wrote them down, so neither rule could run.
STATS_FILENAME = "source_stats.jsonl"


def write_ingest_stats(data_dir: Path, summary: dict[str, int]) -> Path | None:
    """Append one line per ingest run: {run_at, counts}. -1 means the fetch failed.

    Line-oriented and append-only so the committed diff is one added line per
    run, the same property that keeps seen_ids.json cheap in git.
    """
    if not summary:
        return None
    stats_path = data_dir / "ledger" / STATS_FILENAME
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "counts": dict(sorted(summary.items())),
    }
    with stats_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return stats_path


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

    status_parser = subparsers.add_parser(
        "source-status",
        help="apply policy/source-lifecycle.md §4 to data/ledger/source_stats.jsonl "
             "(exit 2 = a source crossed the 14-day threshold)",
    )
    status_parser.add_argument("--data-dir", default="data")

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

    content_parser = subparsers.add_parser(
        "validate-content",
        help="check published articles against the invariants (exit 2 with --strict)",
    )
    content_parser.add_argument(
        "--strict", action="store_true", help="exit 2 when a blocking finding exists"
    )
    content_parser.add_argument(
        "--warn-as-error",
        action="store_true",
        help="treat warnings as blocking too (once the known ones are cleared)",
    )
    content_parser.add_argument(
        "--max-held",
        type=int,
        default=None,
        metavar="N",
        help="with --strict: hold defective stories from the site instead of failing, "
             "and exit 2 only when more than N are held (the deploy ceiling)",
    )
    content_parser.add_argument(
        "--github",
        action="store_true",
        help="print GitHub workflow-command annotations for held stories",
    )
    content_parser.add_argument(
        "--json",
        default=None,
        metavar="PATH",
        help="also write the findings and the held set as JSON here",
    )
    content_parser.add_argument(
        "--brief",
        action="store_true",
        help="print the repair queue for the next agent cycle (exit 2 if non-empty)",
    )
    content_parser.add_argument(
        "--staged",
        action="store_true",
        help="pre-commit mode: validate only the articles in the git index (exit 1 to refuse)",
    )

    dedup_parser = subparsers.add_parser(
        "dedup-check",
        help="check a candidate story against the whole archive (exit 2 = strong match)",
    )
    dedup_parser.add_argument("--title", required=True)
    dedup_parser.add_argument(
        "--url", action="append", default=[], help="candidate source URL(s); repeatable"
    )

    args = parser.parse_args(argv)

    # Only the commands that read the registry load it. validate-content and
    # publish are about the archive, and validate-content also runs as a
    # pre-commit hook from whatever directory git is in — a content check must
    # not fail because policy/sources.yaml is not under the cwd.
    sources = []
    if args.command in ("validate-sources", "source-status", "ingest"):
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
            from noiseless.validate import BLOCKED, FAIL, OK, STALE, check_all

            marks = {OK: "ok", STALE: "STALE", FAIL: "FAIL", BLOCKED: "BLOCKED"}
            tally = {FAIL: 0, STALE: 0, BLOCKED: 0}
            for result in check_all(sources):
                print(f"[{marks[result.state]}] {result.source.name}: {result.detail}")
                if result.state in tally:
                    tally[result.state] += 1
            # A frozen feed counts alongside a broken one: both mean the source
            # is contributing nothing, and only one of them used to be visible.
            print(
                f"live check done — {tally[FAIL]} failures, {tally[STALE]} stale, "
                f"{tally[BLOCKED]} known blocks"
            )
            return 0 if tally[FAIL] + tally[STALE] == 0 else 2
        return 0

    if args.command == "source-status":
        from noiseless.source_status import report

        text, code = report(sources, Path(args.data_dir) / "ledger" / STATS_FILENAME)
        print(text)
        return code

    if args.command == "ingest":
        # Imported here, not at module load: `validate-content --staged` runs as
        # a pre-commit hook and must not depend on the feed-fetching stack.
        from noiseless.ingest import ingest_all

        summary = ingest_all(sources, args.data_dir, only_sources=args.source)
        failures = [name for name, count in summary.items() if count < 0]
        total_new = sum(count for count in summary.values() if count > 0)
        write_ingest_stats(Path(args.data_dir), summary)
        print(f"done — {total_new} new items, {len(failures)} failed sources")
        if failures:
            # Named, not just counted: "3 failed sources" in a three-hour log is
            # not something anyone finds. The committed stats file is the durable
            # record; this line is for whoever is watching the run.
            print(f"failed sources: {', '.join(sorted(failures))}", file=sys.stderr)
        return 0

    if args.command == "publish":
        from noiseless.publish import build_site

        counts = build_site(Path("."), args.out)
        print(
            f"site built at {args.out} — articles: en={counts['en']}, tr={counts['tr']}"
            f", held={counts.get('held', 0)}"
        )
        return 0

    if args.command == "validate-content":
        from noiseless.validate_content import main as validate_content_main

        return validate_content_main(
            Path("."), strict=args.strict, warn_as_error=args.warn_as_error,
            max_held=args.max_held, github=args.github, json_path=args.json,
            brief=args.brief, staged=args.staged,
        )

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
