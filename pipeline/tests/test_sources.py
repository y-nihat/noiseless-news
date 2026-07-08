"""Unit tests for the source registry loader (no network)."""

from pathlib import Path

import pytest

from noiseless.sources import Source, SourceRegistryError, load_sources

REPO_ROOT = Path(__file__).resolve().parents[2]


def write_registry(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "sources.yaml"
    path.write_text(body, encoding="utf-8")
    return path


VALID = """
sources:
  - name: Example Blog
    tier: 0
    type: rss
    url: https://example.com/feed.xml
    verified: true
    notes: hello
  - name: Example Forum
    tier: 3
    type: html
    url: https://forum.example.com/
"""


def test_loads_valid_registry(tmp_path):
    sources = load_sources(write_registry(tmp_path, VALID))
    assert len(sources) == 2
    blog = sources[0]
    assert blog == Source(
        name="Example Blog",
        tier=0,
        type="rss",
        url="https://example.com/feed.xml",
        verified=True,
        notes="hello",
    )
    assert blog.slug == "example-blog"


def test_tier_3_cannot_confirm(tmp_path):
    sources = load_sources(write_registry(tmp_path, VALID))
    assert sources[0].can_confirm is True
    assert sources[1].can_confirm is False


def test_status_defaults_to_active_and_accepts_lifecycle_values(tmp_path):
    body = """
sources:
  - name: Default Status
    tier: 2
    type: rss
    url: https://a.example.com/feed
  - name: Candidate Source
    tier: 2
    type: rss
    url: https://b.example.com/feed
    status: candidate
  - name: Retired Source
    tier: 2
    type: rss
    url: https://c.example.com/feed
    status: retired
"""
    sources = load_sources(write_registry(tmp_path, body))
    assert [source.status for source in sources] == ["active", "candidate", "retired"]


def test_delay_seconds_optional_and_validated(tmp_path):
    body = """
sources:
  - name: Slow Source
    tier: 3
    type: rss
    url: https://slow.example.com/feed
    delay_seconds: 10
  - name: Normal Source
    tier: 3
    type: rss
    url: https://normal.example.com/feed
"""
    sources = load_sources(write_registry(tmp_path, body))
    assert sources[0].delay_seconds == 10.0
    assert sources[1].delay_seconds is None

    bad = body.replace("delay_seconds: 10", "delay_seconds: -1")
    with pytest.raises(SourceRegistryError, match="delay_seconds"):
        load_sources(write_registry(tmp_path, bad))


def test_rejects_invalid_status(tmp_path):
    body = """
sources:
  - name: X
    tier: 1
    type: rss
    url: https://x.example.com/feed
    status: paused
"""
    with pytest.raises(SourceRegistryError, match="status"):
        load_sources(write_registry(tmp_path, body))


@pytest.mark.parametrize(
    "body, message_fragment",
    [
        ("sources:\n  - name: X\n    tier: 9\n    type: rss\n    url: https://x.com/f\n", "tier"),
        ("sources:\n  - name: X\n    tier: 1\n    type: telegraph\n    url: https://x.com/f\n", "type"),
        ("sources:\n  - name: X\n    tier: 1\n    type: rss\n    url: ftp://x.com/f\n", "url"),
        ("sources:\n  - tier: 1\n    type: rss\n    url: https://x.com/f\n", "name"),
        ("not-a-registry: true\n", "sources"),
    ],
)
def test_rejects_invalid_entries(tmp_path, body, message_fragment):
    with pytest.raises(SourceRegistryError, match=message_fragment):
        load_sources(write_registry(tmp_path, body))


def test_rejects_duplicate_names(tmp_path):
    body = """
sources:
  - name: Same Name
    tier: 0
    type: rss
    url: https://a.example.com/feed
  - name: Same Name
    tier: 2
    type: rss
    url: https://b.example.com/feed
"""
    with pytest.raises(SourceRegistryError, match="duplicate"):
        load_sources(write_registry(tmp_path, body))


def test_repo_registry_is_valid():
    """The actual policy/sources.yaml must always validate."""
    sources = load_sources(REPO_ROOT / "policy" / "sources.yaml")
    assert len(sources) >= 10
    names = [source.name for source in sources]
    assert len(names) == len(set(names))
