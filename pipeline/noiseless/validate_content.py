"""Deterministic checks on published content.

Every editorial guarantee the site makes is upheld by an unattended agent's
discipline and self-reported in prose: sixteen days of style-gate records all
read "EN pass / TR pass" and there has never been a recorded failure. Nothing
between the agent's commit and the live site inspected what was written.

These checks are the machine half. They are deliberately narrow — structure,
not judgement. Whether a story was worth publishing is the agent's call; whether
its Turkish twin has the same claims, whether its citations resolve, and whether
a reader can click through to the evidence are not judgement calls at all.

Findings are ERROR or WARN. An ERROR is a per-story defect: the story that
carries it is HELD from the site at build time (publish.py renders a stub at
its URL and leaves it out of the index, feed and sitemap) while everything else
publishes. `--max-held N` bounds how many stories may be held before the build
is refused outright — a ceiling, in the SRE sense: degrade one item, but alarm
when too many items degrade. Without `--max-held`, --strict fails on any ERROR,
which is what a code-change PR wants. The WARN checks currently have known
failures, recorded in the report rather than hidden; promote them with
--warn-as-error once those are cleared.

The night of 2026-08-18 is why the hold exists. Two articles were committed
without their evidence logs; the gate caught it, and because the gate was
all-or-nothing the whole night's seven stories were withheld from the site over
two missing JSON files, and the job went red. Nothing unauditable reached the
public — but nothing valid did either.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from noiseless.publish import STRINGS, load_articles, safe_frontmatter

VALID_VERDICTS = set(STRINGS["en"]["verdicts"])
LANGS = ("en", "tr")

# How many stories may be held from the site before the build is refused. The
# number is a judgement, not a measurement: one or two is a bad cycle that the
# next cycle repairs; more than three in one archive means the agent's
# publishing step is broken and a human should look before anything ships.
MAX_HELD_DEFAULT = 3

# GitHub caps annotations at ten of each kind per step; past that they are
# silently dropped, so say so instead.
MAX_ANNOTATIONS = 10

# What the agent must do about each ERROR check, in the imperative. Rendered
# into the repair queue the next cycle's prompt opens with, and into the
# annotations. The evidence-log text is the editorial contract the council
# settled on: a log is written only from verification that actually happened.
FIX_TEXT = {
    "evidence-log": (
        "write data/verified/<slug>.json from verification actually performed. "
        "If this session ran the verifier and falsifier for the story, write it "
        "now from their findings. Otherwise re-verify (fresh verifier, fresh "
        "adversarial falsifier, at most 8 searches/fetches) and write it with "
        "checked_at = now and a `method` naming this cycle and saying the "
        "original log was not written at publication. Never write it from the "
        "article text, the run report, the ledger prose or memory; never a stub. "
        "If the load-bearing claims cannot be re-established, withdraw the story "
        "instead: remove both article files, set the ledger entry to `watching` "
        "with a `reason`. If it has been held for two nights, decide now."
    ),
    "ledger-entry": (
        "write data/ledger/<slug>.json per policy/article-template.md — title, "
        "status, first_seen, deep-link source_urls."
    ),
    "bilingual-parity": (
        "make the Turkish twin mirror the English article: same claims in the "
        "same order with the same verdicts and evidence indices, same source "
        "list, same date/published/follows."
    ),
    "evidence-index": (
        "every claim's `evidence` list must index into the article's `sources` "
        "(1-based); fix the indices or add the missing source."
    ),
    "verdict-vocabulary": (
        "use only the verdict vocabulary from policy/article-template.md."
    ),
    "publication-date": (
        "`published` cannot precede the event `date`; correct whichever is wrong."
    ),
    "raw-html-in-body": (
        "remove the raw HTML markup from the body; write plain markdown."
    ),
}


@dataclass(frozen=True)
class Finding:
    level: str  # "ERROR" | "WARN"
    check: str
    slug: str
    detail: str
    # Repo-relative path of the English article, so an annotation can point at
    # the file. Empty for findings that have no single file (a Turkish orphan).
    path: str = ""

    def __str__(self) -> str:
        return f"[{self.level}] {self.check}: {self.slug} — {self.detail}"

    @property
    def fix(self) -> str:
        return FIX_TEXT.get(self.check, "")

    def as_dict(self) -> dict:
        return {"level": self.level, "check": self.check, "slug": self.slug,
                "detail": self.detail, "path": self.path, "fix": self.fix}


def _evidence_log_problem(path: Path) -> str:
    """Why this evidence log cannot be audited, or "" if it can.

    "The file exists" was the whole test until 2026-08-19. A log that is not
    JSON, or is JSON with no claims in it, satisfies that and audits nothing —
    which is exactly the empty file a rushed agent would drop in to get past a
    check. Every one of the archive's 130 logs has a non-empty `claims` list,
    so raising the bar holds nothing that was not already unauditable.
    """
    if not path.exists():
        return "no data/verified entry — the article's verdicts cannot be audited"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        return f"data/verified entry is not readable JSON ({type(exc).__name__})"
    if not isinstance(data, dict):
        return "data/verified entry is not a JSON object"
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        return "data/verified entry has no claims — nothing in it can be audited"
    return ""


def _claim_shape(claims: list[dict]) -> list[tuple]:
    return [
        (c.get("type"), c.get("verdict"), tuple(c.get("evidence") or []))
        for c in claims
    ]


RAW_TAG = re.compile(r"<\s*(script|iframe|object|embed|form|style|link|meta)\b", re.I)


def check_article(meta: dict, slug: str, repo_root: Path, body: str = "") -> list[Finding]:
    findings: list[Finding] = []
    sources = meta.get("sources") or []
    claims = meta.get("claims") or []

    if RAW_TAG.search(body):
        findings.append(
            Finding("ERROR", "raw-html-in-body", slug,
                    "the body contains raw HTML markup; it is escaped at render "
                    "time, but an agent writing tags means something went wrong "
                    "upstream and needs looking at")
        )

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

    evidence_problem = _evidence_log_problem(repo_root / "data" / "verified" / f"{slug}.json")
    if evidence_problem:
        findings.append(Finding("ERROR", "evidence-log", slug, evidence_problem))
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


def _load_meta(repo_root: Path, lang: str) -> dict[str, tuple[dict, str, str]]:
    """slug -> (frontmatter, body, repo-relative path)."""
    metas = {}
    root = repo_root / "content" / "articles" / lang
    for path in sorted(root.rglob("*.md")):
        parsed = safe_frontmatter(path)
        if parsed is None:
            continue
        meta, body = parsed
        slug = meta.get("slug") or path.stem
        metas[slug] = (meta, body, path.relative_to(repo_root).as_posix())
    return metas


def validate(repo_root: Path | str) -> list[Finding]:
    repo_root = Path(repo_root)
    en = _load_meta(repo_root, "en")
    tr = _load_meta(repo_root, "tr")

    findings: list[Finding] = []
    for slug, (meta, body, rel) in en.items():
        found = check_article(meta, slug, repo_root, body)
        tr_entry = tr.get(slug)
        found += check_parity(meta, tr_entry[0] if tr_entry else None, slug)
        if tr_entry and RAW_TAG.search(tr_entry[1]):
            found.append(
                Finding("ERROR", "raw-html-in-body", slug,
                        "the Turkish body contains raw HTML markup")
            )
        # Stamp the English article's path on everything about this story, so
        # an annotation lands on the file the agent has to open.
        findings.extend(
            Finding(f.level, f.check, f.slug, f.detail, rel) for f in found
        )
    for slug in sorted(set(tr) - set(en)):
        findings.append(
            Finding("ERROR", "bilingual-parity", slug,
                    "Turkish article has no English original", tr[slug][2])
        )
    return findings


def held_slugs(findings: list[Finding]) -> dict[str, list[Finding]]:
    """The stories the site must not carry, with why. ERROR findings only."""
    held: dict[str, list[Finding]] = {}
    for finding in findings:
        if finding.level == "ERROR":
            held.setdefault(finding.slug, []).append(finding)
    return held


def report(findings: list[Finding], article_count: int) -> str:
    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARN"]
    lines = [str(f) for f in errors] + [str(f) for f in warnings]
    held = held_slugs(findings)
    if held:
        lines.append(
            "held from the site: "
            + ", ".join(f"{slug} ({', '.join(sorted({f.check for f in fs}))})"
                        for slug, fs in sorted(held.items()))
        )
    lines.append(
        f"content check — {article_count} articles, "
        f"{len(errors)} errors, {len(warnings)} warnings, {len(held)} held"
    )
    return "\n".join(lines)


def github_annotations(findings: list[Finding], blocked: bool) -> list[str]:
    """GitHub workflow commands, one per held story, capped at what GitHub keeps.

    docs.github.com/actions/reference/workflow-commands: `::warning file=…`
    surfaces on the run page and on the PR diff; ten per kind per step, the
    rest dropped without a word — so the eleventh line says how many were.
    """
    held = held_slugs(findings)
    level = "error" if blocked else "warning"
    lines = []
    for slug, fs in sorted(held.items()):
        first = fs[0]
        where = f"file={first.path}," if first.path else ""
        checks = ", ".join(sorted({f.check for f in fs}))
        lines.append(
            f"::{level} {where}title=content gate::{slug} held from the site — "
            f"{checks}: {first.detail}"
        )
    if len(lines) > MAX_ANNOTATIONS:
        overflow = len(lines) - MAX_ANNOTATIONS
        lines = lines[:MAX_ANNOTATIONS] + [
            f"::{level} title=content gate::… and {overflow} more held "
            f"(GitHub shows at most {MAX_ANNOTATIONS} annotations per step)"
        ]
    return lines


def _first_published(repo_root: Path, path: str) -> str:
    """The date the article's file was first committed, or "" outside a repo.

    That is when the story was first *on* main and, until 2026-08-19, on the
    site — the reader-facing "since when" the repair brief needs, and the
    difference between "fix it tonight" and "second night: decide now".
    """
    import subprocess

    try:
        # No --follow: articles are never renamed, and rename detection would
        # match a new article to an older one built from the same template and
        # report the older one's date.
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cs", "--", path],
            cwd=repo_root, capture_output=True, text=True, timeout=30,
        ).stdout.split()
    except (OSError, subprocess.SubprocessError):
        return ""
    return out[-1] if out else ""


def repair_brief(repo_root: Path | str, today: str = "") -> tuple[str, int]:
    """The repair queue the next cycle's prompt opens with. Returns (markdown, held count).

    Recomputed from the archive at every cycle start, so it carries across
    nights with no state file to forge, forget or go stale. This is what closes
    the loop the night of 2026-08-18 lacked: the gate tripped in cycle 2 and
    cycles 3-6 each ran a fresh session that was never told.
    """
    from datetime import date

    repo_root = Path(repo_root)
    held = held_slugs(validate(repo_root))
    if not held:
        return (
            "REPAIR QUEUE: empty — the archive is clean. Before your first commit "
            "tonight, run `PYTHONPATH=pipeline python -m noiseless.run validate-content "
            "--strict` once and keep it clean.",
            0,
        )
    today_d = date.fromisoformat(today) if today else date.today()
    lines = [
        f"REPAIR QUEUE — {len(held)} story(ies) are HELD from the site. Do these "
        "BEFORE step 1, before any new story. A repair does not count against "
        "your story budget. Repaired stories publish on the next deploy; a story "
        "still held tomorrow morning is a review item for the owner.",
        "",
    ]
    for slug, findings in sorted(held.items()):
        checks = sorted({f.check for f in findings})
        since = _first_published(repo_root, findings[0].path) if findings[0].path else ""
        nights = ""
        if since:
            try:
                age = (today_d - date.fromisoformat(since)).days
                nights = f" — first published {since}" + (
                    f", held for {age} night(s): SECOND-NIGHT RULE applies — complete "
                    "the repair now or withdraw" if age >= 2 else ""
                )
            except ValueError:
                nights = f" — first published {since}"
        lines.append(f"- `{slug}` ({', '.join(checks)}){nights}")
        for finding in findings:
            lines.append(f"    - {finding.check}: {finding.detail}")
        for check in checks:
            fix = FIX_TEXT.get(check)
            if fix:
                lines.append(f"    - FIX ({check}): {fix.replace('<slug>', slug)}")
        lines.append(
            "    - THEN: `PYTHONPATH=pipeline python -m noiseless.run validate-content "
            "--strict` must no longer list this slug; commit as `Repair: "
            f"{slug}`; push; add a `Repair:` line to your report section."
        )
    lines.append("")
    lines.append(
        "Never write an evidence log from the article text, the run report, the "
        "ledger prose or memory, and never a stub — a log written by a party that "
        "did not verify is a fabricated audit trail, which is worse than an honest "
        "hold. If your budget runs out mid-repair, leave the story held; do not "
        "withdraw for lack of time."
    )
    return "\n".join(lines), len(held)


def _staged_slugs(repo_root: Path) -> tuple[set[str], list[str]]:
    """Slugs touched by the index, and the staged paths, from `git diff --cached`."""
    import subprocess

    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AMD"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout.split()
    slugs: set[str] = set()
    for path in out:
        parts = Path(path).parts
        if len(parts) >= 3 and parts[0] == "content" and parts[1] == "articles":
            slugs.add(Path(path).stem)
        elif len(parts) == 3 and parts[0] == "data" and parts[1] in ("verified", "ledger"):
            slugs.add(Path(path).stem)
    return slugs, out


def check_staged(repo_root: Path | str) -> list[Finding]:
    """Validate what is about to be COMMITTED — the index, not the tree.

    The pre-commit hook. It exports each touched slug's four twins from the
    index into a temp tree and validates that, so an evidence log that exists
    on disk but was not `git add`ed fails, and another slug's pre-existing
    defect does not block this commit. Report-only and ledger-only commits
    touch no article and pass. Whole-tree checks were rejected for the hook
    because they refuse an agent's unrelated good commit while another slug
    is red, and create an incentive to un-publish someone else's story to land
    your own.
    """
    import shutil
    import subprocess
    import tempfile

    repo_root = Path(repo_root)
    slugs, staged = _staged_slugs(repo_root)
    article_touch = [p for p in staged if p.startswith("content/articles/")]
    if not article_touch:
        return []

    tmp = Path(tempfile.mkdtemp(prefix="staged-"))
    try:
        for slug in slugs:
            for rel in (
                *(f"content/articles/{lang}/{y}/{m}/{slug}.md"
                  for lang in ("en", "tr")
                  for y, m in _year_months(repo_root, staged, slug)),
                f"data/verified/{slug}.json",
                f"data/ledger/{slug}.json",
            ):
                blob = subprocess.run(
                    ["git", "show", f":{rel}"], cwd=repo_root,
                    capture_output=True, text=True,
                )
                if blob.returncode == 0:
                    target = tmp / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(blob.stdout, encoding="utf-8")
        found = [f for f in validate(tmp) if f.level == "ERROR" and f.slug in slugs]
        # Only slugs whose ARTICLE is being committed are this commit's business.
        touched_articles = {Path(p).stem for p in article_touch}
        return [f for f in found if f.slug in touched_articles]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _year_months(repo_root: Path, staged: list[str], slug: str) -> set[tuple[str, str]]:
    """The YYYY/MM directories this slug's article lives in — staged or in HEAD."""
    import subprocess

    found: set[tuple[str, str]] = set()
    for path in staged:
        parts = Path(path).parts
        if len(parts) == 6 and parts[:2] == ("content", "articles") and Path(path).stem == slug:
            found.add((parts[3], parts[4]))
    if not found:
        ls = subprocess.run(
            ["git", "ls-files", f"content/articles/*/*/*/{slug}.md"],
            cwd=repo_root, capture_output=True, text=True,
        ).stdout.split()
        for path in ls:
            parts = Path(path).parts
            if len(parts) == 6:
                found.add((parts[3], parts[4]))
    return found


def main(repo_root: Path | str, *, strict: bool, warn_as_error: bool,
         max_held: int | None = None, github: bool = False,
         json_path: Path | str | None = None, brief: bool = False,
         staged: bool = False) -> int:
    """Exit 0 clean, 0 held-within-ceiling, 2 blocked.

    --strict alone: any ERROR exits 2 (a code PR should not merge with one).
    --strict --max-held N: ERRORs hold their stories; exit 2 only past N.
    """
    repo_root = Path(repo_root)
    if brief:
        text, held_count = repair_brief(repo_root)
        print(text)
        return 2 if held_count else 0
    if staged:
        found = check_staged(repo_root)
        if not found:
            return 0
        import sys

        print("commit refused — the article(s) being committed are not publishable:",
              file=sys.stderr)
        for finding in found:
            print(f"  [{finding.check}] {finding.slug}: {finding.detail}", file=sys.stderr)
            if finding.fix:
                print(f"    FIX: {finding.fix.replace('<slug>', finding.slug)}", file=sys.stderr)
        print("Stage the missing twin (data/verified, data/ledger, the Turkish "
              "article) in the SAME commit and try again. Report-only commits are "
              "never refused.", file=sys.stderr)
        return 1

    findings = validate(repo_root)
    count = len(load_articles(repo_root / "content", "en"))
    print(report(findings, count))

    held = held_slugs(findings)
    if warn_as_error:
        blocked = bool(findings)
    elif max_held is None:
        blocked = bool(held)
    else:
        blocked = len(held) > max_held
    if held and max_held is not None and not blocked:
        print(f"held within the ceiling ({len(held)} of at most {max_held}) — deployable")

    if github:
        for line in github_annotations(findings, blocked and strict):
            print(line)
        if blocked and strict and max_held is not None:
            print(f"::error title=content gate::{len(held)} stories held, ceiling is "
                  f"{max_held} — the build is refused")

    if json_path:
        Path(json_path).write_text(
            json.dumps({
                "articles": count,
                "blocked": bool(blocked and strict),
                "max_held": max_held,
                "held": {slug: [f.as_dict() for f in fs] for slug, fs in sorted(held.items())},
                "findings": [f.as_dict() for f in findings],
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if blocked and strict:
        return 2
    return 0
