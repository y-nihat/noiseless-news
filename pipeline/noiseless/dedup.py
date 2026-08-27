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
from urllib.parse import urlsplit

from noiseless.ingest import canonical_url
from noiseless.publish import safe_frontmatter

# Minimal English stopwords — enough to stop "the/of/in" from inflating overlap.
_STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are",
    "as", "at", "by", "with", "its", "it", "new", "after", "over", "amid",
    "from", "into", "up", "out", "his", "her", "their",
}

STRONG_THRESHOLD = 0.6
MODERATE_THRESHOLD = 0.34

# Ledger keys the night agent actually writes, in precedence order. The schema
# is defined in policy/article-template.md; these lists are the code's half of
# that contract, and test_dedup_repo_data.py asserts the real files satisfy it.
LEDGER_DATE_KEYS = ("date", "published_at", "first_seen", "updated_at")
LEDGER_URL_KEYS = ("source_urls", "urls")


def _first_present(data: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = data.get(key)
        if value:
            return str(value)
    return ""


def identity_urls(urls) -> set[str]:
    """Canonical URLs usable as story identity.

    Bare origins are dropped. A citation of `https://www.reuters.com/` says only
    that Reuters was involved, so treating it as identity makes every future
    Reuters story a duplicate of the first one that cited the homepage.
    """
    identities = set()
    for url in urls:
        if not isinstance(url, str) or not url.strip():
            continue
        canonical = canonical_url(url)
        path = urlsplit(canonical).path
        if path in ("", "/"):
            continue
        identities.add(canonical)
    return identities


@dataclass
class IndexEntry:
    slug: str
    title: str
    date: str
    state: str
    urls: set[str] = field(default_factory=set)
    # §8's saga link. Two members of one thread are *meant* to look alike, so
    # anything reasoning about "these two stories match" has to be able to see
    # the relationship the policy already blessed.
    follows: str = ""


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
        parsed = safe_frontmatter(path)
        if parsed is None:
            continue  # a broken article must not disable the duplicate gate
        meta, _body = parsed
        slug = meta.get("slug") or path.stem
        urls = identity_urls(
            src["url"]
            for src in (meta.get("sources") or [])
            if isinstance(src, dict) and src.get("url")
        )
        entries[slug] = IndexEntry(
            slug=slug,
            title=str(meta.get("title", "")),
            date=str(meta.get("date", "")),
            state="published",
            urls=urls,
            follows=str(meta.get("follows") or ""),
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
            urls: set[str] = set()
            for key in LEDGER_URL_KEYS:
                value = data.get(key)
                if isinstance(value, list) and value:
                    urls = identity_urls(value)
                    break
            entries[slug] = IndexEntry(
                slug=slug,
                # An entry with no title still has a slug, and a slug is a
                # hyphenated headline. Falling back to it keeps a watching story
                # matchable instead of silently scoring 0.0 against everything.
                title=str(data.get("title") or "") or slug.replace("-", " "),
                date=_first_present(data, LEDGER_DATE_KEYS),
                state=str(data.get("state", data.get("status", "unknown"))),
                urls=urls,
                follows=str(data.get("follows") or ""),
            )

    return list(entries.values())


def check(
    title: str, urls: list[str], index: list[IndexEntry]
) -> list[dict]:
    """Score every archive entry against a candidate story.

    Returns matches at or above MODERATE_THRESHOLD, strongest first.

    A shared canonical source URL is strong evidence of the same story but not
    proof: the archive already contains two genuinely different stories citing
    the same OpenAI announcement page. So one shared URL on its own only
    surfaces the match for the agent to read; it takes a second shared URL, or
    title agreement as well, to reach `strong` — which the cycle prompt treats
    as forbidding a standalone article.
    """
    candidate_tokens = tokens(title)
    candidate_urls = identity_urls(urls)
    matches = []
    for entry in index:
        score = similarity(candidate_tokens, tokens(entry.title))
        shared = candidate_urls & entry.urls
        if shared and (len(shared) >= 2 or score >= MODERATE_THRESHOLD):
            score = 1.0
        elif shared:
            score = max(score, MODERATE_THRESHOLD)
        if score >= MODERATE_THRESHOLD:
            matches.append(
                {
                    "slug": entry.slug,
                    "title": entry.title,
                    "date": entry.date,
                    "state": entry.state,
                    "score": round(score, 3),
                    "shared_source_url": bool(shared),
                    "shared_url_count": len(shared),
                    "strength": "strong" if score >= STRONG_THRESHOLD else "moderate",
                }
            )
    matches.sort(key=lambda m: m["score"], reverse=True)
    return matches


def dedup_note(repo_root: Path | str, slug: str) -> str:
    """The dedup decision recorded in a story's evidence log, or "".

    §0a ends with "the dedup-check result (matches found, decision taken) is
    recorded in the story's evidence log". This reads that record back.
    """
    path = Path(repo_root) / "data" / "verified" / f"{slug}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return ""
    if not isinstance(data, dict):
        return ""
    note = data.get("dedup_check")
    return note if isinstance(note, str) else ""


def _names_slug(note: str, slug: str) -> bool:
    """Does this note refer to `slug` itself, and not merely contain its letters?

    Slug characters are [a-z0-9-], so a slug flanked by another one is a
    different slug: a note about `gpt-5-6-launch-delay` must not excuse a match
    against `gpt-5-6-launch`. Plain substring matching also lets a short slug
    hide inside an ordinary word.
    """
    return re.search(rf"(?<![a-z0-9-]){re.escape(slug)}(?![a-z0-9-])", note) is not None


def policy_exempt_pair(
    repo_root: Path | str, first: IndexEntry, second: IndexEntry
) -> str:
    """Why §8 permits these two published stories to match strongly, or "".

    A strong match is not by itself a defect. §8 gives three outcomes and two of
    them leave two published stories matching on purpose:

      * a follow-up article, which shares the saga and usually the sources; and
      * "unrelated despite surface similarity" — a standalone, whose only
        requirement is that the dedup decision is written down.

    The note has to NAME the other slug. That is what keeps this from being a
    blanket amnesty: a story carrying a dedup_check about some *different* match
    does not get to excuse this one, and a standalone published with no recorded
    reasoning at all still fails loudly.
    """
    if first.follows == second.slug or second.follows == first.slug:
        return "follows"
    if _names_slug(dedup_note(repo_root, first.slug), second.slug):
        return f"recorded standalone in data/verified/{first.slug}.json"
    if _names_slug(dedup_note(repo_root, second.slug), first.slug):
        return f"recorded standalone in data/verified/{second.slug}.json"
    return ""


def unlinked_duplicates(repo_root: Path | str, slugs) -> list[dict]:
    """Strong matches among published stories that §8 has not accounted for.

    The same question `test_dedup_repo_data.py` asks of the whole archive,
    asked of a few slugs — so the hook can refuse exactly what CI would later
    fail on, rather than a near-miss of it.

    This exists because the gate that runs BEFORE a story is written and the
    invariant that runs after it is committed were scoring different things.
    On 2026-08-20 `dedup-check` was run, honestly, against a working title and
    a bare origin URL that `identity_urls` discards; the finished article then
    acquired a citation of the matched story's primary document, and CI went
    red for eight days on a decision the agent had already justified in
    writing. Re-asking with the finished article's real title and real sources
    is what makes that justification land against the right evidence.
    """
    repo_root = Path(repo_root)
    index = load_index(repo_root)
    published = [e for e in index if e.state == "published"]
    by_slug = {e.slug: e for e in published}
    offenders = []
    for slug in sorted(slugs):
        entry = by_slug.get(slug)
        if entry is None:
            continue  # not a published article: nothing for this check to say
        others = [e for e in published if e.slug != slug]
        for match in check(entry.title, sorted(entry.urls), others):
            if match["strength"] != "strong":
                continue
            other = by_slug[match["slug"]]
            if policy_exempt_pair(repo_root, entry, other):
                continue
            offenders.append(
                {
                    "slug": slug,
                    "matches": other.slug,
                    "score": match["score"],
                    "shared_url_count": match["shared_url_count"],
                }
            )
    return offenders
