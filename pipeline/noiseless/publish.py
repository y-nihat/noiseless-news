"""Publish stage: render content/ and data/ into a static site (site/dist).

Deliberately dependency-light: markdown + hand-rolled templates. The site is
bilingual — English is canonical, Turkish mirrors it (policy/verification.md §7).
"""

from __future__ import annotations

import html
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import markdown as md
import yaml

REPO_URL = "https://github.com/y-nihat/noiseless-news"

STRINGS = {
    "en": {
        "lang_name": "English",
        "other_lang": "Türkçe",
        "tagline": "AI news that survives verification. Nothing else.",
        "articles": "Articles",
        "no_articles": (
            "No verified articles yet — the verification pipeline is being built. "
            "Below is a live sample of what the scanner currently ingests."
        ),
        "digest": "Latest scanned items (pipeline test — unverified)",
        "digest_note": (
            "Raw headlines exactly as their sources published them; nothing below has "
            "been verified by us yet. Listed only to show the scanner working."
        ),
        "methodology": "Methodology",
        "footer": "Built in the open — every verdict's evidence trail is public.",
        "verification": "Verification",
        "sources": "Sources",
        "updated": "Updates",
        "tiers": {
            0: "Tier 0 — Primary / official",
            1: "Tier 1 — Literature",
            2: "Tier 2 — Press",
            3: "Tier 3 — Community (discovery only)",
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
        "articles": "Haberler",
        "no_articles": (
            "Henüz doğrulanmış haber yok — doğrulama hattı inşa ediliyor. Aşağıda "
            "tarayıcının şu anda topladığı içeriklerden canlı bir örnek görüyorsunuz."
        ),
        "digest": "Son taranan içerikler (deneme çalışması — doğrulanmamış)",
        "digest_note": (
            "Başlıklar kaynakların yayımladığı hâliyle, ham olarak listelenmiştir; "
            "hiçbiri henüz tarafımızca doğrulanmamıştır. Yalnızca tarayıcının "
            "çalıştığını göstermek için sunulmaktadır."
        ),
        "methodology": "Yöntem",
        "footer": "Açık inşa ediliyor — her hükmün kanıt zinciri kamuya açık.",
        "verification": "Doğrulama",
        "sources": "Kaynaklar",
        "updated": "Güncellemeler",
        "tiers": {
            0: "Katman 0 — Birincil / resmî",
            1: "Katman 1 — Literatür",
            2: "Katman 2 — Basın",
            3: "Katman 3 — Topluluk (yalnızca keşif)",
        },
        "verdicts": {
            "confirmed": "Doğrulandı",
            "vendor-claim": "Üretici beyanı",
            "single-source": "Tek kaynak",
            "disputed": "İhtilaflı",
        },
    },
}

CSS = """
:root { --bg:#ffffff; --fg:#1a1a1a; --muted:#666; --accent:#0a5c36; --rule:#e3e3e3; --box:#f6f6f4; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#14161a; --fg:#e6e4df; --muted:#9a978f; --accent:#7fc9a2; --rule:#2c2f36; --box:#1c1f26; }
}
* { box-sizing: border-box; }
body { margin:0 auto; max-width:44rem; padding:2rem 1.25rem 4rem; background:var(--bg);
       color:var(--fg); font:17px/1.65 Georgia, 'Times New Roman', serif; }
header.site { border-bottom:2px solid var(--fg); padding-bottom:.75rem; margin-bottom:2rem; }
header.site h1 { font-size:1.6rem; margin:0; letter-spacing:-.01em; }
header.site h1 a { color:var(--fg); text-decoration:none; }
.tagline { color:var(--muted); margin:.25rem 0 0; font-style:italic; }
nav.top { font-family:system-ui,sans-serif; font-size:.85rem; margin-top:.6rem; }
nav.top a { color:var(--accent); text-decoration:none; margin-right:1rem; }
h2 { font-size:1.15rem; margin:2.2rem 0 .8rem; }
h3 { font-size:1rem; }
a { color:var(--accent); }
.muted { color:var(--muted); }
.note { color:var(--muted); font-size:.9rem; margin:.2rem 0 1rem; }
ul.items { list-style:none; padding:0; margin:0; }
ul.items li { padding:.55rem 0; border-bottom:1px solid var(--rule); }
ul.items .meta { display:block; font-family:system-ui,sans-serif; font-size:.75rem; color:var(--muted); margin-top:.15rem; }
.tier { font-family:system-ui,sans-serif; font-size:.72rem; text-transform:uppercase;
        letter-spacing:.05em; color:var(--muted); margin:1.6rem 0 .2rem; }
article header h1 { font-size:1.5rem; line-height:1.25; margin:0 0 .3rem; }
.tldr { background:var(--box); border-left:3px solid var(--accent); padding:.8rem 1rem; margin:1.2rem 0; }
.verify { background:var(--box); padding: .9rem 1rem; margin:1.5rem 0; font-size:.92rem; }
.verify table { width:100%; border-collapse:collapse; font-family:system-ui,sans-serif; font-size:.8rem; }
.verify td { padding:.3rem .4rem .3rem 0; vertical-align:top; border-top:1px solid var(--rule); }
.badge { font-family:system-ui,sans-serif; font-size:.72rem; padding:.1rem .45rem;
         border:1px solid var(--accent); border-radius:99px; color:var(--accent); white-space:nowrap; }
ol.sources { font-size:.9rem; }
footer.site { margin-top:3.5rem; border-top:1px solid var(--rule); padding-top:1rem;
              font-family:system-ui,sans-serif; font-size:.8rem; color:var(--muted); }
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


def _page(*, lang: str, title: str, body: str, root: str, other_lang_href: str) -> str:
    s = STRINGS[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <h1><a href="{root}{'tr/' if lang == 'tr' else ''}index.html">noiseless news</a></h1>
  <p class="tagline">{s['tagline']}</p>
  <nav class="top">
    <a href="{other_lang_href}">{s['other_lang']}</a>
    <a href="{REPO_URL}/blob/main/policy/verification.md">{s['methodology']}</a>
    <a href="{REPO_URL}">GitHub</a>
  </nav>
</header>
{body}
<footer class="site">{s['footer']}</footer>
</body>
</html>
"""


def _digest_html(digest: dict, lang: str) -> str:
    s = STRINGS[lang]
    if not digest["tiers"]:
        return ""
    parts = [f"<h2>{s['digest']}</h2>", f"<p class='note'>{s['digest_note']}</p>"]
    for tier in sorted(digest["tiers"]):
        parts.append(f"<p class='tier'>{s['tiers'][tier]}</p><ul class='items'>")
        for item in digest["tiers"][tier]:
            published = (item.get("published") or "")[:10]
            parts.append(
                f"<li><a href='{html.escape(item['url'])}'>{html.escape(item['title'])}</a>"
                f"<span class='meta'>{html.escape(item['source'])}"
                f"{' · ' + published if published else ''}</span></li>"
            )
        parts.append("</ul>")
    return "\n".join(parts)


def _article_list_html(articles: list[Article], lang: str, article_prefix: str) -> str:
    s = STRINGS[lang]
    if not articles:
        return f"<h2>{s['articles']}</h2><p class='muted'>{s['no_articles']}</p>"
    parts = [f"<h2>{s['articles']}</h2><ul class='items'>"]
    for article in articles:
        tldr = html.escape(str(article.meta.get("tldr", "")).strip())
        parts.append(
            f"<li><a href='{article_prefix}{article.slug}.html'>"
            f"{html.escape(article.title)}</a>"
            f"<span class='meta'>{article.date}</span>"
            f"{f'<span class=meta>{tldr}</span>' if tldr else ''}</li>"
        )
    parts.append("</ul>")
    return "\n".join(parts)


def _article_html(article: Article, lang: str) -> str:
    s = STRINGS[lang]
    meta = article.meta
    parts = [
        "<article><header>",
        f"<h1>{html.escape(article.title)}</h1>",
        f"<p class='muted'>{article.date}</p>",
        "</header>",
    ]
    if meta.get("tldr"):
        parts.append(f"<div class='tldr'>{html.escape(str(meta['tldr']).strip())}</div>")
    parts.append(article.body_html)

    claims = meta.get("claims") or []
    if claims:
        rows = []
        for claim in claims:
            verdict = s["verdicts"].get(claim.get("verdict", ""), claim.get("verdict", ""))
            evidence = ", ".join(f"[{i}]" for i in (claim.get("evidence") or []))
            rows.append(
                f"<tr><td>{html.escape(claim.get('text', ''))}</td>"
                f"<td><span class='badge'>{html.escape(verdict)}</span></td>"
                f"<td>{evidence}</td></tr>"
            )
        parts.append(
            f"<div class='verify'><strong>{s['verification']}</strong>"
            f"<table>{''.join(rows)}</table></div>"
        )

    sources = meta.get("sources") or []
    if sources:
        items = "".join(
            f"<li><a href='{html.escape(src['url'])}'>{html.escape(src['name'])}</a></li>"
            for src in sources
        )
        parts.append(f"<h2>{s['sources']}</h2><ol class='sources'>{items}</ol>")

    updates = meta.get("updated") or []
    if updates:
        items = "".join(f"<li>{html.escape(str(entry))}</li>" for entry in updates)
        parts.append(f"<h2>{s['updated']}</h2><ul class='items'>{items}</ul>")

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
    for lang, root, index_path, article_prefix in (
        ("en", "", out_dir / "index.html", "articles/"),
        ("tr", "../", out_dir / "tr" / "index.html", "articles/"),
    ):
        articles = load_articles(repo_root / "content", lang)
        counts[lang] = len(articles)
        other = "tr/index.html" if lang == "en" else "../index.html"
        index_body = _article_list_html(articles, lang, article_prefix) + _digest_html(
            digest, lang
        )
        index_path.write_text(
            _page(lang=lang, title="noiseless news", body=index_body, root=root,
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
                _page(lang=lang, title=article.title,
                      body=_article_html(article, lang),
                      root="../../" if lang == "tr" else "../",
                      other_lang_href=counterpart),
                encoding="utf-8",
            )

    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    return counts
