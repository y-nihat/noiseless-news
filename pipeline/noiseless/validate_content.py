"""Deterministic checks on published content.

Every editorial guarantee the site makes is upheld by an unattended agent's
discipline and self-reported in prose: sixteen days of style-gate records all
read "EN pass / TR pass" and there has never been a recorded failure. Nothing
between the agent's commit and the live site inspected what was written.

These checks are the machine half. They are deliberately narrow — structure,
not judgement. Whether a story was worth publishing is the agent's call; whether
its Turkish twin has the same claims, whether its citations resolve, and whether
a reader can click through to the evidence are not judgement calls at all.

Findings are ERROR or WARN. Every ERROR check passes on the whole archive today,
so a new one is a regression and can fail the build. The WARN checks currently
have known failures, recorded in the report rather than hidden; promote them
with --warn-as-error once those are cleared.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from noiseless.publish import STRINGS, load_articles, safe_frontmatter

VALID_VERDICTS = set(STRINGS["en"]["verdicts"])
LANGS = ("en", "tr")


@dataclass(frozen=True)
class Finding:
    level: str  # "ERROR" | "WARN"
    check: str
    slug: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.level}] {self.check}: {self.slug} — {self.detail}"


def _claim_shape(claims: list[dict]) -> list[tuple]:
    return [
        (c.get("type"), c.get("verdict"), tuple(c.get("evidence") or []))
        for c in claims
    ]


def check_article(meta: dict, slug: str, repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    sources = meta.get("sources") or []
    claims = meta.get("claims") or []

    for index, claim in enumerate(claims):
        for ref in claim.get("evidence") or []:
            if not isinstance(ref, int) or not 1 <= ref <= len(sources):
                findings.append(
                    Finding("ERROR", "evidence-index", slug,
                            f"claim {index + 1} cites source [{ref}], "
                            f"but the article lists {len(sources)}")
                )
        verdict = claim.get("verdict")
        if verdict not in VALID_VERDICTS:
            findings.append(
                Finding("ERROR", "verdict-vocabulary", slug,
                        f"claim {index + 1} has verdict {verdict!r}, "
                        f"expected one of {sorted(VALID_VERDICTS)}")
            )

    published = str(meta.get("published") or meta.get("date") or "")
    date = str(meta.get("date") or "")
    if published and date and published < date:
        findings.append(
            Finding("ERROR", "publication-date", slug,
                    f"published {published} precedes the event date {date}")
        )

    if not (repo_root / "data" / "verified" / f"{slug}.json").exists():
        findings.append(
            Finding("ERROR", "evidence-log", slug,
                    "no data/verified entry — the article's verdicts cannot be audited")
        )
    if not (repo_root / "data" / "ledger" / f"{slug}.json").exists():
        findings.append(
            Finding("ERROR", "ledger-entry", slug,
                    "no data/ledger entry — the story is invisible to the duplicate gate")
        )

    for source in sources:
        url = str(source.get("url") or "")
        if urlsplit(url).path in ("", "/"):
            findings.append(
                Finding("WARN", "bare-source-url", slug,
                        f"{url} is an origin, not a page: a reader clicking this "
                        "source cannot verify anything, and dedup treats it as identity")
            )

    if claims and not any(c.get("verdict") == "confirmed" for c in claims):
        findings.append(
            Finding("WARN", "unconfirmed-headline", slug,
                    "no claim is `confirmed`, so the headline rests on none "
                    "(policy/style.md gate 1) — note §3's litigation row may "
                    "legitimately conflict here")
        )
    return findings


def check_parity(en_meta: dict, tr_meta: dict | None, slug: str) -> list[Finding]:
    if tr_meta is None:
        return [Finding("ERROR", "bilingual-parity", slug, "no Turkish counterpart")]

    findings = []
    en_claims, tr_claims = en_meta.get("claims") or [], tr_meta.get("claims") or []
    if _claim_shape(en_claims) != _claim_shape(tr_claims):
        findings.append(
            Finding("ERROR", "bilingual-parity", slug,
                    f"claim structure differs: EN {_claim_shape(en_claims)} "
                    f"vs TR {_claim_shape(tr_claims)}")
        )
    en_urls = [s.get("url") for s in (en_meta.get("sources") or [])]
    tr_urls = [s.get("url") for s in (tr_meta.get("sources") or [])]
    if en_urls != tr_urls:
        findings.append(
            Finding("ERROR", "bilingual-parity", slug, "source list differs")
        )
    for field in ("date", "published", "follows"):
        if str(en_meta.get(field) or "") != str(tr_meta.get(field) or ""):
            findings.append(
                Finding("ERROR", "bilingual-parity", slug,
                        f"{field} differs: EN {en_meta.get(field)!r} "
                        f"vs TR {tr_meta.get(field)!r}")
            )
    return findings


def _load_meta(repo_root: Path, lang: str) -> dict[str, dict]:
    metas = {}
    root = repo_root / "content" / "articles" / lang
    for path in sorted(root.rglob("*.md")):
        parsed = safe_frontmatter(path)
        if parsed is None:
            continue
        meta, _body = parsed
        slug = meta.get("slug") or path.stem
        metas[slug] = meta
    return metas


def validate(repo_root: Path | str) -> list[Finding]:
    repo_root = Path(repo_root)
    en = _load_meta(repo_root, "en")
    tr = _load_meta(repo_root, "tr")

    findings: list[Finding] = []
    for slug, meta in en.items():
        findings.extend(check_article(meta, slug, repo_root))
        findings.extend(check_parity(meta, tr.get(slug), slug))
    for slug in sorted(set(tr) - set(en)):
        findings.append(
            Finding("ERROR", "bilingual-parity", slug, "Turkish article has no English original")
        )
    return findings


def report(findings: list[Finding], article_count: int) -> str:
    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARN"]
    lines = [str(f) for f in errors] + [str(f) for f in warnings]
    lines.append(
        f"content check — {article_count} articles, "
        f"{len(errors)} errors, {len(warnings)} warnings"
    )
    return "\n".join(lines)


def main(repo_root: Path | str, *, strict: bool, warn_as_error: bool) -> int:
    repo_root = Path(repo_root)
    findings = validate(repo_root)
    count = len(load_articles(repo_root / "content", "en"))
    print(report(findings, count))

    blocking = [f for f in findings if f.level == "ERROR"]
    if warn_as_error:
        blocking = findings
    if blocking and strict:
        return 2
    return 0
