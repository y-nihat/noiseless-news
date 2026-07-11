"""Loading and validation of the source registry (policy/sources.yaml)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

VALID_TIERS = {0, 1, 2, 3}
VALID_TYPES = {"rss", "arxiv_api", "html", "youtube_channel", "google_news_query"}
# Lifecycle statuses — see policy/source-lifecycle.md. Only active sources are ingested.
VALID_STATUSES = {"active", "candidate", "retired"}
# Tier 3 is discovery-only and may never confirm a claim (policy/verification.md §1).
CONFIRMATION_TIERS = {0, 1, 2}


@dataclass(frozen=True)
class Source:
    name: str
    tier: int
    type: str
    url: str
    status: str = "active"
    verified: bool = False
    notes: str = ""
    # Optional per-source politeness delay; None means the type default applies.
    delay_seconds: float | None = None

    @property
    def slug(self) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
        return slug

    @property
    def can_confirm(self) -> bool:
        return self.tier in CONFIRMATION_TIERS


class SourceRegistryError(ValueError):
    pass


def _validate_entry(entry: dict, index: int) -> Source:
    name = entry.get("name")
    if not name or not isinstance(name, str):
        raise SourceRegistryError(f"sources[{index}]: missing or invalid 'name'")

    tier = entry.get("tier")
    if tier not in VALID_TIERS:
        raise SourceRegistryError(
            f"source '{name}': tier must be one of {sorted(VALID_TIERS)}, got {tier!r}"
        )

    type_ = entry.get("type")
    if type_ not in VALID_TYPES:
        raise SourceRegistryError(
            f"source '{name}': type must be one of {sorted(VALID_TYPES)}, got {type_!r}"
        )

    url = entry.get("url")
    if not url or not isinstance(url, str) or not url.startswith(("http://", "https://")):
        raise SourceRegistryError(f"source '{name}': missing or invalid 'url'")

    status = entry.get("status", "active")
    if status not in VALID_STATUSES:
        raise SourceRegistryError(
            f"source '{name}': status must be one of {sorted(VALID_STATUSES)}, got {status!r}"
        )

    delay = entry.get("delay_seconds")
    if delay is not None and (not isinstance(delay, (int, float)) or delay < 0):
        raise SourceRegistryError(
            f"source '{name}': delay_seconds must be a non-negative number, got {delay!r}"
        )

    return Source(
        name=name,
        tier=tier,
        type=type_,
        url=url,
        status=status,
        verified=bool(entry.get("verified", False)),
        notes=str(entry.get("notes", "")).strip(),
        delay_seconds=float(delay) if delay is not None else None,
    )


def load_sources(path: Path | str) -> list[Source]:
    """Parse and validate the registry. Raises SourceRegistryError on any problem."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise SourceRegistryError("registry must be a mapping with a 'sources' list")

    sources = [_validate_entry(entry, i) for i, entry in enumerate(raw["sources"])]

    seen_names: set[str] = set()
    for source in sources:
        if source.name in seen_names:
            raise SourceRegistryError(f"duplicate source name: '{source.name}'")
        seen_names.add(source.name)

    return sources
