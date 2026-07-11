"""Archive-wide duplicate prevention for stories.

Before any new article is created, the night agent runs `dedup-check` against a
story index built from every published article AND every ledger entry (watching/
dropped stories included) — regardless of date. A story covered last week is
still a duplicate today. Dates travel with each index entry so the caller can
reason about staleness.

Deterministic layer only: token-set title similarity + canonical source-URL
overlap. Nuanced calls (update vs. skip vs. genuinely new) belong to the agent,
which must read the matched article for any non-trivial match.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from noiseless.ingest import canonical_url
from noiseless.publish import parse_frontmatter

# Minimal English stopwords — enough to stop "the/of/in" from inflating overlap.
_STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are",
    "as", "at", "by", "with", "its", "it", "new", "after", "over", "amid",
    "from", "into", "up", "out", "his", "her", "their",
}

STRONG_THRESHOLD = 0.6
MODERATE_THRESHOLD = 0.34


@dataclass
class IndexEntry:
    slug: str
    title: str
    date: str
    state: str
    urls: set[str] = field(default_factory=set)


def tokens(text: str) -> set[str]:
    words = re.split(r"[^a-z0-9.]+", text.lower())
    return {w for w in words if len(w) > 1 and w not in _STOPWORDS}


def similarity(a: set[str], b: set[str]) -> float:
    """Overlap coefficient: |A∩B| / min(|A|,|B|).

    Deliberately not Jaccard — our titles often carry long subtitle clauses
    ("…; independent benchmarks not yet available") that dilute union-based
    scores and hide true duplicates behind the extra words.
    """
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def load_index(repo_root: Path | str) -> list[IndexEntry]:
    """One entry per story the site has ever opened: articles + ledger states."""
    repo_root = Path(repo_root)
    entries: dict[str, IndexEntry] = {}

    for path in sorted((repo_root / "content" / "articles" / "en").rglob("*.md")):
        meta, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
        slug = meta.get("slug") or path.stem
        urls = {
            canonical_url(src["url"])
            for src in (meta.get("sources") or [])
            if isinstance(src, dict) and src.get("url")
        }
        entries[slug] = IndexEntry(
            slug=slug,
            title=str(meta.get("title", "")),
            date=str(meta.get("date", "")),
            state="published",
            urls=urls,
        )

    ledger_dir = repo_root / "data" / "ledger"
    if ledger_dir.exists():
        for path in sorted(ledger_dir.glob("*.json")):
            if path.name in ("source_candidates.json", "source_rejections.json"):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            if not isinstance(data, dict):
                continue
            slug = data.get("slug") or path.stem
            if slug in entries:  # article entry wins; keep its richer data
                continue
            urls = {
                canonical_url(u)
                for u in (data.get("source_urls") or data.get("urls") or [])
                if isinstance(u, str)
            }
            entries[slug] = IndexEntry(
                slug=slug,
                title=str(data.get("title", "")),
                date=str(data.get("date", data.get("updated_at", ""))),
                state=str(data.get("state", data.get("status", "unknown"))),
                urls=urls,
            )

    return list(entries.values())


def check(
    title: str, urls: list[str], index: list[IndexEntry]
) -> list[dict]:
    """Score every archive entry against a candidate story.

    Returns matches at or above MODERATE_THRESHOLD, strongest first. A shared
    canonical source URL is treated as a strong match on its own — two stories
    citing the same primary announcement are the same story.
    """
    candidate_tokens = tokens(title)
    candidate_urls = {canonical_url(u) for u in urls if u}
    matches = []
    for entry in index:
        score = similarity(candidate_tokens, tokens(entry.title))
        url_hit = bool(candidate_urls & entry.urls)
        if url_hit:
            score = max(score, 1.0)
        if score >= MODERATE_THRESHOLD:
            matches.append(
                {
                    "slug": entry.slug,
                    "title": entry.title,
                    "date": entry.date,
                    "state": entry.state,
                    "score": round(score, 3),
                    "shared_source_url": url_hit,
                    "strength": "strong" if score >= STRONG_THRESHOLD else "moderate",
                }
            )
    matches.sort(key=lambda m: m["score"], reverse=True)
    return matches
