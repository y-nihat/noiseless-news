"""Deterministic ingest stage: registered feeds -> normalized, deduplicated JSON items.

No LLM is involved here. Fetching is rate-limited (arXiv: 1 request / 3 s per its
API terms of use; everything else: 1 s between requests).
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import httpx

from noiseless.sources import Source

USER_AGENT = "noiseless-news/0.1 (autonomous news verification; +https://github.com)"
ARXIV_DELAY_SECONDS = 3.0
DEFAULT_DELAY_SECONDS = 1.0

# Source types that serve feed XML the ingest stage can parse directly.
# (google_news_query and youtube_channel URLs are ordinary RSS/Atom feeds.)
FEED_TYPES = {"rss", "arxiv_api", "google_news_query", "youtube_channel"}

_TRACKING_PARAMS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def canonical_url(url: str) -> str:
    """Normalize a URL for identity: drop fragments and tracking params."""
    scheme, netloc, path, query, _fragment = urlsplit(url.strip())
    query_pairs = [
        (key, value)
        for key, value in parse_qsl(query, keep_blank_values=True)
        if not key.startswith("utm_") and key not in _TRACKING_PARAMS
    ]
    return urlunsplit(
        (scheme.lower(), netloc.lower(), path, urlencode(query_pairs), "")
    )


def item_id(url: str) -> str:
    """Stable identifier derived from the canonical URL."""
    return hashlib.sha256(canonical_url(url).encode("utf-8")).hexdigest()[:16]


def _entry_published(entry) -> str | None:
    for attr in ("published_parsed", "updated_parsed"):
        parsed = entry.get(attr)
        if parsed:
            return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()
    return None


def normalize_entry(source: Source, entry, fetched_at: str) -> dict | None:
    """Map a feedparser entry to our canonical item shape. Returns None if unusable."""
    link = (entry.get("link") or "").strip()
    title = " ".join((entry.get("title") or "").split())
    # feedparser can synthesize a non-HTTP "link" from an Atom <id> (e.g. urn:uuid:...)
    if not link.startswith(("http://", "https://")) or not title:
        return None
    item = {
        "id": item_id(link),
        "source": source.name,
        "tier": source.tier,
        "title": title,
        "url": canonical_url(link),
        "published": _entry_published(entry),
        "summary": (entry.get("summary") or "").strip(),
        "fetched_at": fetched_at,
    }
    # Aggregator feeds (Google News) name the origin outlet in <source> — keep it
    # so triage can apply independence rules without fetching the redirect.
    origin = entry.get("source")
    if origin and origin.get("title"):
        item["via_outlet"] = origin["title"]
    return item


def parse_feed_text(source: Source, text: str, fetched_at: str) -> list[dict]:
    parsed = feedparser.parse(text)
    items = []
    for entry in parsed.entries:
        item = normalize_entry(source, entry, fetched_at)
        if item is not None:
            items.append(item)
    return items


def dedupe(items: list[dict], seen_ids: set[str]) -> list[dict]:
    """Return only items whose id is not in seen_ids (order preserved, in-run dupes removed)."""
    new_items = []
    for item in items:
        if item["id"] in seen_ids:
            continue
        seen_ids.add(item["id"])
        new_items.append(item)
    return new_items


def _delay_for(source: Source) -> float:
    type_default = ARXIV_DELAY_SECONDS if source.type == "arxiv_api" else DEFAULT_DELAY_SECONDS
    if source.delay_seconds is not None:
        return max(source.delay_seconds, type_default)
    return type_default


def polite_get(client: httpx.Client, url: str, retry_delay: float = 30.0) -> httpx.Response:
    """GET with one polite retry on HTTP 429 (rate limit)."""
    response = client.get(url, headers={"User-Agent": USER_AGENT})
    if response.status_code == 429:
        time.sleep(retry_delay)
        response = client.get(url, headers={"User-Agent": USER_AGENT})
    return response


def fetch_source(source: Source, client: httpx.Client, fetched_at: str) -> list[dict]:
    """Fetch one feed-like source. html sources are the night agent's sweep targets,
    not ingest's."""
    if source.type not in FEED_TYPES:
        return []
    response = polite_get(client, source.url)
    response.raise_for_status()
    return parse_feed_text(source, response.text, fetched_at)


def _load_seen_ids(state_path: Path) -> set[str]:
    if state_path.exists():
        return set(json.loads(state_path.read_text(encoding="utf-8")))
    return set()


def _save_seen_ids(state_path: Path, seen_ids: set[str]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(sorted(seen_ids), indent=0) + "\n", encoding="utf-8"
    )


def ingest_all(
    sources: list[Source],
    data_dir: Path | str,
    only_sources: list[str] | None = None,
) -> dict[str, int]:
    """Fetch every feed-like source, write new items to data/raw/<date>/, update state.

    Returns {source_name: new_item_count}; failures are recorded as -1 so one broken
    feed never aborts the run.
    """
    data_dir = Path(data_dir)
    state_path = data_dir / "state" / "seen_ids.json"
    seen_ids = _load_seen_ids(state_path)

    fetched_at = datetime.now(timezone.utc).isoformat()
    day_dir = data_dir / "raw" / fetched_at[:10]
    summary: dict[str, int] = {}

    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for source in sources:
            if only_sources and source.name not in only_sources:
                continue
            if source.status != "active":
                continue
            if source.type not in FEED_TYPES:
                continue
            try:
                items = fetch_source(source, client, fetched_at)
            except Exception as exc:  # a broken feed must not abort the nightly run
                print(f"[ingest] FAIL {source.name}: {exc}")
                summary[source.name] = -1
                continue
            new_items = dedupe(items, seen_ids)
            summary[source.name] = len(new_items)
            if new_items:
                day_dir.mkdir(parents=True, exist_ok=True)
                out_path = day_dir / f"{source.slug}.json"
                existing = (
                    json.loads(out_path.read_text(encoding="utf-8"))
                    if out_path.exists()
                    else []
                )
                out_path.write_text(
                    json.dumps(existing + new_items, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
            print(f"[ingest] {source.name}: {len(new_items)} new / {len(items)} fetched")
            time.sleep(_delay_for(source))

    _save_seen_ids(state_path, seen_ids)
    return summary
