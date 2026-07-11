"""Publish stage: render content/ and data/ into a static site (site/dist).

Deliberately dependency-light: markdown + hand-rolled templates. The site is
bilingual — English is canonical, Turkish mirrors it (policy/verification.md §7).
Design: minimalist editorial — system sans for UI, serif for article prose,
verdict-colored badges, light/dark via prefers-color-scheme.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown as md
import yaml

REPO_URL = "https://github.com/y-nihat/noiseless-news"

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ccircle cx='50' cy='50' r='34' fill='none' stroke='%230c7d62' stroke-width='14'/%3E"
    "%3Ccircle cx='50' cy='50' r='9' fill='%230c7d62'/%3E%3C/svg%3E"
)

STRINGS = {
    "en": {
        "lang_name": "English",
        "other_lang": "Türkçe",
        "tagline": "AI news that survives verification. Nothing else.",
        "articles": "Latest",
        "no_articles": (
            "No verified articles yet — the verification pipeline is being built. "
            "Below is a live sample of what the scanner currently ingests."
        ),
        "digest": "Scanner feed",
        "digest_note": (
            "Raw headlines exactly as their sources published them — unverified, "
            "listed only to show what the pipeline watches."
        ),
        "methodology": "Methodology",
        "footer": "Built in the open — every verdict's evidence trail is public.",
        "verification": "Verification",
        "sources": "Sources",
        "updated": "Updates",
        "thread": "Story thread",
        "thread_current": "this article",
        "thread_chip": "follow-up",
        "back": "All articles",
        "min_read": "min read",
        "claims_chip": "{n} claims checked",
        "sources_chip": "{n} sources",
        "tiers": {
            0: "Primary / official",
            1: "Literature",
            2: "Press",
            3: "Community — discovery only",
        },
        "verdicts": {
            "confirmed": "Confirmed",
            "vendor-claim": "Vendor claim",
            "single-source": "Single source",
            "disputed": "Disputed",
        },
    },
    "tr": {
        "lang_name": "Türkçe",
        "other_lang": "English",
        "tagline": "Doğrulamadan geçen yapay zekâ haberleri. Fazlası değil.",
        "articles": "Son haberler",
        "no_articles": (
            "Henüz doğrulanmış haber yok — doğrulama hattı inşa ediliyor. Aşağıda "
            "tarayıcının şu anda topladığı içeriklerden canlı bir örnek görüyorsunuz."
        ),
        "digest": "Tarayıcı akışı",
        "digest_note": (
            "Başlıklar kaynakların yayımladığı hâliyle, ham olarak listelenmiştir — "
            "doğrulanmamıştır; yalnızca hattın neyi izlediğini göstermek içindir."
        ),
        "methodology": "Yöntem",
        "footer": "Açık inşa ediliyor — her hükmün kanıt zinciri kamuya açık.",
        "verification": "Doğrulama",
        "sources": "Kaynaklar",
        "updated": "Güncellemeler",
        "thread": "Haberin seyri",
        "thread_current": "bu haber",
        "thread_chip": "devam haberi",
        "back": "Tüm haberler",
        "min_read": "dk okuma",
        "claims_chip": "{n} iddia denetlendi",
        "sources_chip": "{n} kaynak",
        "tiers": {
            0: "Birincil / resmî",
            1: "Literatür",
            2: "Basın",
            3: "Topluluk — yalnızca keşif",
        },
        "verdicts": {
            "confirmed": "Doğrulandı",
            "vendor-claim": "Üretici beyanı",
            "single-source": "Tek kaynak",
            "disputed": "İhtilaflı",
        },
    },
}

VERDICT_CLASS = {
    "confirmed": "v-ok",
    "vendor-claim": "v-vendor",
    "single-source": "v-single",
    "disputed": "v-bad",
}

CSS = """
:root {
  --sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --bg:#fdfdfb; --fg:#1a1b1e; --muted:#6e7480; --rule:#e9e7e1; --box:#f4f3ee;
  --accent:#0c7d62; --accent-soft:rgba(12,125,98,.08);
  --ok:#0b6e57; --ok-bg:rgba(12,125,98,.10);
  --warn:#8f5f00; --warn-bg:rgba(191,135,0,.13);
  --gray:#5c6370; --gray-bg:rgba(100,110,125,.12);
  --bad:#b3271e; --bad-bg:rgba(214,69,56,.10);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#111214; --fg:#e9e7e2; --muted:#9aa0ab; --rule:#26282c; --box:#1a1c20;
    --accent:#57c9a4; --accent-soft:rgba(87,201,164,.10);
    --ok:#57c9a4; --ok-bg:rgba(87,201,164,.12);
    --warn:#e0b04a; --warn-bg:rgba(224,176,74,.13);
    --gray:#a2a9b4; --gray-bg:rgba(160,170,185,.14);
    --bad:#f27b6f; --bad-bg:rgba(242,123,111,.12);
  }
}
* { box-sizing:border-box; }
html { color-scheme: light dark; }
body { margin:0; background:var(--bg); color:var(--fg);
       font:16px/1.6 var(--sans); -webkit-font-smoothing:antialiased; }
.wrap { max-width:42.5rem; margin:0 auto; padding:0 1.35rem; }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; text-underline-offset:3px; }

header.site { padding:2.1rem 0 1.4rem; }
header.site .bar { display:flex; align-items:baseline; justify-content:space-between;
                   gap:1rem; flex-wrap:wrap; }
.wordmark { font-weight:750; font-size:1.22rem; letter-spacing:-.02em; color:var(--fg); }
.wordmark em { font-style:normal; color:var(--accent); }
nav.top { display:flex; gap:1.1rem; font-size:.84rem; }
nav.top a { color:var(--muted); font-weight:500; }
nav.top a:hover { color:var(--accent); text-decoration:none; }
.tagline { margin:.4rem 0 0; color:var(--muted); font-size:.95rem; }
.rule { border:0; border-top:1px solid var(--rule); margin:0; }

main { padding:1.2rem 0 2rem; }
h2.section { font-size:.8rem; font-weight:650; text-transform:uppercase;
             letter-spacing:.09em; color:var(--muted); margin:2.4rem 0 .4rem; }
.note { color:var(--muted); font-size:.85rem; margin:.1rem 0 .9rem; }
.empty { color:var(--muted); font-size:.95rem; }

ul.posts { list-style:none; margin:0; padding:0; }
ul.posts li { padding:1.15rem 0; border-bottom:1px solid var(--rule); }
ul.posts .date { font-size:.78rem; color:var(--muted); letter-spacing:.02em; }
ul.posts h3 { margin:.2rem 0 .35rem; font-size:1.28rem; line-height:1.3;
              letter-spacing:-.015em; font-weight:700; }
ul.posts h3 a { color:var(--fg); }
ul.posts h3 a:hover { color:var(--accent); text-decoration:none; }
ul.posts .tldr { margin:0 0 .55rem; color:var(--muted); font-size:.93rem; line-height:1.55; }
.chips { display:flex; gap:.45rem; flex-wrap:wrap; }
.chip { font-size:.73rem; font-weight:600; color:var(--accent);
        background:var(--accent-soft); padding:.24rem .6rem; border-radius:999px; }

.tier-block { margin:0 0 1.3rem; }
.tier-label { font-size:.72rem; font-weight:650; text-transform:uppercase;
              letter-spacing:.08em; color:var(--muted); margin:1.2rem 0 .3rem; }
ul.feed { list-style:none; margin:0; padding:0; }
ul.feed li { padding:.5rem 0; border-bottom:1px solid var(--rule); font-size:.92rem; }
ul.feed li:last-child { border-bottom:0; }
ul.feed a { color:var(--fg); }
ul.feed a:hover { color:var(--accent); text-decoration:none; }
ul.feed .meta { display:block; font-size:.76rem; color:var(--muted); margin-top:.1rem; }

.crumb { font-size:.84rem; margin:0 0 1.6rem; }
article h1 { font-size:1.85rem; line-height:1.2; letter-spacing:-.022em;
             font-weight:780; margin:.2rem 0 .6rem; }
.byline { color:var(--muted); font-size:.85rem; margin:0 0 1.4rem; }
.byline .dot { margin:0 .45rem; opacity:.5; }
.tldr-box { background:var(--box); border-left:3px solid var(--accent);
            border-radius:0 10px 10px 0; padding:.95rem 1.15rem; margin:0 0 1.7rem;
            font-size:.99rem; line-height:1.6; }
.prose { font-family:var(--serif); font-size:1.07rem; line-height:1.78; }
.prose h2 { font-family:var(--sans); font-size:1.06rem; letter-spacing:-.01em;
            font-weight:700; margin:2rem 0 .6rem; }
.prose p { margin:0 0 1.05rem; }

.verify { background:var(--box); border-radius:12px; padding:1.05rem 1.2rem; margin:2.1rem 0; }
.verify h2 { font-size:.8rem; font-weight:650; text-transform:uppercase;
             letter-spacing:.09em; color:var(--muted); margin:0 0 .7rem; }
.claim { display:flex; gap:.8rem; align-items:flex-start; padding:.55rem 0;
         border-top:1px solid var(--rule); font-size:.9rem; line-height:1.5; }
.claim:first-of-type { border-top:0; }
.claim .refs { margin-left:auto; color:var(--muted); font-size:.78rem; white-space:nowrap; }
.badge { flex:none; font-size:.7rem; font-weight:700; letter-spacing:.02em;
         padding:.26rem .6rem; border-radius:999px; margin-top:.1rem; }
.v-ok { color:var(--ok); background:var(--ok-bg); }
.v-vendor { color:var(--warn); background:var(--warn-bg); }
.v-single { color:var(--gray); background:var(--gray-bg); }
.v-bad { color:var(--bad); background:var(--bad-bg); }

ol.sources { margin:.4rem 0 0; padding-left:1.3rem; font-size:.92rem; }
ol.sources li { padding:.22rem 0; }
ol.sources .domain { color:var(--muted); font-size:.8rem; margin-left:.45rem; }
ul.updates { list-style:none; margin:.4rem 0 0; padding:0; font-size:.88rem; color:var(--muted); }
ul.updates li { padding:.25rem 0; }

.thread { background:var(--accent-soft); border-radius:12px; padding:1rem 1.2rem; margin:0 0 1.7rem; }
.thread h2 { font-size:.8rem; font-weight:650; text-transform:uppercase;
             letter-spacing:.09em; color:var(--muted); margin:0 0 .55rem; }
.thread ol { margin:0; padding-left:1.25rem; font-size:.9rem; }
.thread li { padding:.22rem 0; }
.thread .date { color:var(--muted); font-size:.78rem; margin-right:.5rem; }
.thread .current { font-weight:700; }
.thread .you { color:var(--muted); font-size:.78rem; margin-left:.4rem; }

footer.site { margin:3rem 0 0; padding:1.3rem 0 2.6rem; border-top:1px solid var(--rule);
              font-size:.8rem; color:var(--muted); }
"""


@dataclass
class Article:
    meta: dict
    body_html: str
    lang: str

    @property
    def slug(self) -> str:
        return self.meta["slug"]

    @property
    def title(self) -> str:
        return self.meta["title"]

    @property
    def date(self) -> str:
        return str(self.meta.get("date", ""))


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split '---' frontmatter from body. Returns (meta, body_markdown)."""
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body.strip()
    return {}, text.strip()


def load_articles(content_dir: Path, lang: str) -> list[Article]:
    lang_dir = content_dir / "articles" / lang
    articles = []
    for path in sorted(lang_dir.rglob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta.get("title") or not meta.get("slug"):
            continue
        articles.append(Article(meta=meta, body_html=md.markdown(body), lang=lang))
    articles.sort(key=lambda a: a.date, reverse=True)
    return articles


def resolve_threads(articles: list[Article]) -> dict[str, list[Article]]:
    """Group articles into story threads via `follows` frontmatter pointers.

    Each article may declare `follows: <slug>` pointing at the story it
    continues. A thread is the transitive chain down to its root article.
    Returns {member_slug: chronologically-ordered members} for every article in
    a thread of size ≥ 2. Broken pointers and cycles degrade to "no thread" —
    never an error.
    """
    by_slug = {a.slug: a for a in articles}

    def root_of(article: Article) -> str:
        seen = {article.slug}
        current = article
        while True:
            nxt = current.meta.get("follows")
            if not nxt or nxt not in by_slug or nxt in seen:
                return current.slug
            seen.add(nxt)
            current = by_slug[nxt]

    groups: dict[str, list[Article]] = {}
    for article in articles:
        groups.setdefault(root_of(article), []).append(article)

    threads: dict[str, list[Article]] = {}
    for members in groups.values():
        if len(members) < 2:
            continue
        members.sort(key=lambda a: (a.date, a.slug))
        for member in members:
            threads[member.slug] = members
    return threads


def build_digest(data_dir: Path, max_per_tier: int = 5) -> dict:
    """Latest raw-ingest day grouped by tier: {'date': ..., 'tiers': {0: [...], ...}}."""
    raw_root = data_dir / "raw"
    day_dirs = sorted(
        (d for d in raw_root.iterdir() if d.is_dir()) if raw_root.exists() else []
    )
    if not day_dirs:
        return {"date": None, "tiers": {}}
    latest = day_dirs[-1]

    tiers: dict[int, list[dict]] = {}
    for path in sorted(latest.glob("*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            tiers.setdefault(item["tier"], []).append(item)
    for tier, items in tiers.items():
        items.sort(key=lambda item: item.get("published") or "", reverse=True)
        tiers[tier] = items[:max_per_tier]
    return {"date": latest.name, "tiers": tiers}


def reading_minutes(body_html: str) -> int:
    words = len(re.sub(r"<[^>]+>", " ", body_html).split())
    return max(1, round(words / 200))


def _domain(url: str) -> str:
    return re.sub(r"^www\.", "", url.split("//")[-1].split("/")[0])


def _page(*, lang: str, title: str, body: str, home: str, other_lang_href: str,
          description: str = "") -> str:
    s = STRINGS[lang]
    desc = html.escape(description or s["tagline"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<title>{html.escape(title)}</title>
<link rel="icon" href="{FAVICON}">
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <div class="wrap">
    <div class="bar">
      <a class="wordmark" href="{home}">noiseless<em>.</em>news</a>
      <nav class="top">
        <a href="{other_lang_href}">{s['other_lang']}</a>
        <a href="{REPO_URL}/blob/main/policy/verification.md">{s['methodology']}</a>
        <a href="{REPO_URL}">GitHub</a>
      </nav>
    </div>
    <p class="tagline">{s['tagline']}</p>
  </div>
</header>
<hr class="rule">
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">{s['footer']}</div></footer>
</body>
</html>
"""


def _chips_html(article: Article, lang: str) -> str:
    s = STRINGS[lang]
    chips = []
    sources = article.meta.get("sources") or []
    claims = article.meta.get("claims") or []
    if article.meta.get("follows"):
        chips.append(s["thread_chip"])
    if sources:
        chips.append(s["sources_chip"].format(n=len(sources)))
    if claims:
        chips.append(s["claims_chip"].format(n=len(claims)))
    if not chips:
        return ""
    return "<div class='chips'>" + "".join(
        f"<span class='chip'>{c}</span>" for c in chips
    ) + "</div>"


def _article_list_html(articles: list[Article], lang: str, article_prefix: str) -> str:
    s = STRINGS[lang]
    if not articles:
        return f"<h2 class='section'>{s['articles']}</h2><p class='empty'>{s['no_articles']}</p>"
    parts = [f"<h2 class='section'>{s['articles']}</h2><ul class='posts'>"]
    for article in articles:
        tldr = html.escape(str(article.meta.get("tldr", "")).strip())
        parts.append(
            f"<li><span class='date'>{article.date}</span>"
            f"<h3><a href='{article_prefix}{article.slug}.html'>"
            f"{html.escape(article.title)}</a></h3>"
            f"{f'<p class=tldr>{tldr}</p>' if tldr else ''}"
            f"{_chips_html(article, lang)}</li>"
        )
    parts.append("</ul>")
    return "\n".join(parts)


def _digest_html(digest: dict, lang: str) -> str:
    s = STRINGS[lang]
    if not digest["tiers"]:
        return ""
    parts = [
        f"<h2 class='section'>{s['digest']}</h2>",
        f"<p class='note'>{s['digest_note']}</p>",
    ]
    for tier in sorted(digest["tiers"]):
        parts.append(f"<p class='tier-label'>{s['tiers'][tier]}</p><ul class='feed'>")
        for item in digest["tiers"][tier]:
            published = (item.get("published") or "")[:10]
            parts.append(
                f"<li><a href='{html.escape(item['url'])}'>{html.escape(item['title'])}</a>"
                f"<span class='meta'>{html.escape(item['source'])}"
                f"{' · ' + published if published else ''}</span></li>"
            )
        parts.append("</ul>")
    return "\n".join(parts)


def _thread_html(article: Article, thread: list[Article], lang: str) -> str:
    s = STRINGS[lang]
    items = []
    for member in thread:
        date = f"<span class='date'>{member.date}</span>"
        if member.slug == article.slug:
            items.append(
                f"<li class='current'>{date}{html.escape(member.title)}"
                f"<span class='you'>— {s['thread_current']}</span></li>"
            )
        else:
            items.append(
                f"<li>{date}<a href='{member.slug}.html'>"
                f"{html.escape(member.title)}</a></li>"
            )
    return f"<div class='thread'><h2>{s['thread']}</h2><ol>{''.join(items)}</ol></div>"


def _article_html(
    article: Article, lang: str, home: str, thread: list[Article] | None = None
) -> str:
    s = STRINGS[lang]
    meta = article.meta
    minutes = reading_minutes(article.body_html)
    parts = [
        f"<p class='crumb'><a href='{home}'>← {s['back']}</a></p>",
        "<article>",
        f"<h1>{html.escape(article.title)}</h1>",
        f"<p class='byline'>{article.date}<span class='dot'>·</span>{minutes} {s['min_read']}</p>",
    ]
    if meta.get("tldr"):
        parts.append(f"<div class='tldr-box'>{html.escape(str(meta['tldr']).strip())}</div>")
    if thread:
        parts.append(_thread_html(article, thread, lang))
    parts.append(f"<div class='prose'>{article.body_html}</div>")

    claims = meta.get("claims") or []
    if claims:
        rows = []
        for claim in claims:
            verdict_key = claim.get("verdict", "")
            verdict = s["verdicts"].get(verdict_key, verdict_key)
            css = VERDICT_CLASS.get(verdict_key, "v-single")
            refs = " ".join(f"[{i}]" for i in (claim.get("evidence") or []))
            rows.append(
                f"<div class='claim'><span class='badge {css}'>{html.escape(verdict)}</span>"
                f"<span>{html.escape(claim.get('text', ''))}</span>"
                f"<span class='refs'>{refs}</span></div>"
            )
        parts.append(
            f"<div class='verify'><h2>{s['verification']}</h2>{''.join(rows)}</div>"
        )

    sources = meta.get("sources") or []
    if sources:
        items = "".join(
            f"<li><a href='{html.escape(src['url'])}'>{html.escape(src['name'])}</a>"
            f"<span class='domain'>{html.escape(_domain(src['url']))}</span></li>"
            for src in sources
        )
        parts.append(
            f"<h2 class='section'>{s['sources']}</h2><ol class='sources'>{items}</ol>"
        )

    updates = meta.get("updated") or []
    if updates:
        items = "".join(f"<li>{html.escape(str(entry))}</li>" for entry in updates)
        parts.append(
            f"<h2 class='section'>{s['updated']}</h2><ul class='updates'>{items}</ul>"
        )

    parts.append("</article>")
    return "\n".join(parts)


def build_site(repo_root: Path | str, out_dir: Path | str) -> dict[str, int]:
    repo_root, out_dir = Path(repo_root), Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "articles").mkdir(parents=True)
    (out_dir / "tr" / "articles").mkdir(parents=True)

    digest = build_digest(repo_root / "data")
    counts = {}
    for lang, index_path, article_prefix, home in (
        ("en", out_dir / "index.html", "articles/", "index.html"),
        ("tr", out_dir / "tr" / "index.html", "articles/", "index.html"),
    ):
        articles = load_articles(repo_root / "content", lang)
        threads = resolve_threads(articles)
        counts[lang] = len(articles)
        other = "tr/index.html" if lang == "en" else "../index.html"
        index_body = _article_list_html(articles, lang, article_prefix) + _digest_html(
            digest, lang
        )
        index_path.write_text(
            _page(lang=lang, title="noiseless.news", body=index_body, home=home,
                  other_lang_href=other),
            encoding="utf-8",
        )
        for article in articles:
            article_dir = out_dir / ("tr/articles" if lang == "tr" else "articles")
            counterpart = (
                f"../../articles/{article.slug}.html"
                if lang == "tr"
                else f"../tr/articles/{article.slug}.html"
            )
            (article_dir / f"{article.slug}.html").write_text(
                _page(lang=lang, title=f"{article.title} — noiseless.news",
                      body=_article_html(article, lang, home="../index.html",
                                         thread=threads.get(article.slug)),
                      home="../index.html",
                      other_lang_href=counterpart,
                      description=str(article.meta.get("tldr", "")).strip()),
                encoding="utf-8",
            )

    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    return counts
