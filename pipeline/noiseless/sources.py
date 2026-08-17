"""Loading and validation of the source registry (policy/sources.yaml)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# How long a feed may go without a new entry before it is called frozen rather
# than quiet. Deliberately generous: this is the line past which silence is a
# symptom, not a slow fortnight. Lives here because two different checks read
# it — the live freshness check and the ingest-record streak — and they must
# not disagree about what "too quiet" means.
DEFAULT_MAX_AGE_DAYS = 45

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
    # How long this feed may go without a new entry before live validation calls
    # it frozen. None means DEFAULT_MAX_AGE_DAYS above. Set it where
    # a quiet month is the source's nature — a peer-reviewed journal — rather
    # than a symptom.
    max_age_days: int | None = None
    # The publisher serves this to ordinary clients but returns 401/403 to the
    # address ranges CI runs from. A known, unactionable condition: recorded so
    # it stops being reported as a new failure every week, and so the difference
    # between "blocked from here" and "dead" stays written down.
    runner_blocked: bool = False

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

    max_age = entry.get("max_age_days")
    if max_age is not None and (
        not isinstance(max_age, int) or isinstance(max_age, bool) or max_age < 1
    ):
        raise SourceRegistryError(
            f"source '{name}': max_age_days must be a positive integer, got {max_age!r}"
        )

    runner_blocked = entry.get("runner_blocked", False)
    if not isinstance(runner_blocked, bool):
        raise SourceRegistryError(
            f"source '{name}': runner_blocked must be true or false, got {runner_blocked!r}"
        )
    # `str(None)` is the truthy string "None", so a bare `notes:` key would have
    # satisfied the guard below while recording no explanation at all.
    raw_notes = entry.get("notes")
    notes = "" if raw_notes is None else str(raw_notes).strip()
    if runner_blocked and not notes:
        # Suppressing an alarm without writing down why is how a source ends up
        # quietly excused from the checks for a year.
        raise SourceRegistryError(
            f"source '{name}': runner_blocked requires notes explaining the block"
        )

    return Source(
        name=name,
        tier=tier,
        type=type_,
        url=url,
        status=status,
        verified=bool(entry.get("verified", False)),
        notes=notes,
        delay_seconds=float(delay) if delay is not None else None,
        max_age_days=max_age,
        runner_blocked=runner_blocked,
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
