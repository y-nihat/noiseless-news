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
# The one place the canonical origin is written down. Canonical links, feed
# entry ids, the sitemap and the Open Graph tags all derive from it, so pointing
# a custom domain at the site is a one-line change here.
SITE_URL = "https://y-nihat.github.io/noiseless-news"
FEED_LIMIT = 30

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
            "Nothing has cleared verification yet. Below is a live sample of what "
            "the scanner is currently watching — unverified, and listed only to "
            "show the pipeline is running."
        ),
        "digest": "Scanner feed",
        "digest_note": (
            "Raw headlines exactly as their sources published them — unverified, "
            "listed only to show what the pipeline watches."
        ),
        "methodology": "Methodology",
        "site_title": "noiseless.news — verified AI news",
        "feed_title": "noiseless.news",
        "feed_link": "Feed",
        "about": "About",
        "corrections": "Corrections",
        "footer": "Built in the open — every verdict's evidence trail is public.",
        "disclosure": (
            "Articles on this site are written and verified by AI agents, "
            "unattended, following a public editorial policy. No person edits "
            "an article before it is published."
        ),
        "operator": "Operated by <a href='https://github.com/y-nihat'>y-nihat</a>.",
        "contact": "Spotted an error?",
        "contact_link": "Report it",
        "last_run": "Last verification run",
        "no_corrections": (
            "No corrections have been issued yet. When an article is corrected, "
            "the correction is listed here and dated on the article itself; the "
            "original wording stays in this repository's git history."
        ),
        "corrections_note": (
            "Every correction the site has made, newest first. A correction "
            "means a published claim was wrong — as distinct from an update, "
            "which adds new information to a story that was right."
        ),
        "about_intro": (
            "noiseless.news publishes artificial-intelligence news that survives "
            "verification, and publishes the verification too. Claims that "
            "cannot be checked against independent sources are not printed as "
            "fact — and stories that fail the bar are held, with the reason "
            "written down."
        ),
        "about_made_h": "How it is made",
        "about_made": (
            "Every article on this site is written and verified by AI agents "
            "running unattended overnight, following the editorial policy linked "
            "below. Nightly the pipeline scans a public registry of named "
            "sources, decomposes candidate stories into individual factual "
            "claims, verifies each claim against independent evidence, and "
            "writes the article from the verified claims only — headline "
            "included. A second agent, working from a fresh context, then tries "
            "to break each claim before anything is published. "
            "<strong>No person reviews an article before it goes live.</strong> "
            "The English article is canonical; the Turkish version mirrors it."
        ),
        "about_verdicts_h": "What the verdicts mean",
        "about_verdicts": {
            "confirmed": "Met the standard of proof for its claim type: a primary source for an announcement, two independent sources for a business claim, the paper itself for a research finding.",
            "vendor-claim": "Stated by the party that benefits from it. Published as their claim, never as settled fact — benchmark results from the company that made the model, for instance.",
            "single-source": "One source only. Published because the claim carries the story, and labelled so you can weigh it.",
            "disputed": "Sources disagree. Both accounts are given.",
        },
        "about_sources_h": "Where the evidence comes from",
        "about_sources": (
            "Sources are registered by name and tier in a public file. Tier 0 is "
            "primary and official — company announcements, filings, legal texts. "
            "Tier 1 is literature. Tier 2 is independent press. Tier 3 — forums, "
            "video, social — is used to <em>find</em> stories and may never "
            "confirm one. Several outlets repeating the same press release count "
            "as one source, not several."
        ),
        "about_wrong_h": "When we get it wrong",
        "about_wrong": (
            "Corrections are published on a dedicated page and dated on the "
            "article itself. The original wording is not deleted — it stays in "
            "the repository's public history. If you think something here is "
            "wrong, or you are named in an article and want to respond, open an "
            "issue and it will be dealt with."
        ),
        "about_open_h": "Open to inspection",
        "about_open": (
            "The editorial policy, the source registry, every article's evidence "
            "log, the nightly run reports and the pipeline itself are all in one "
            "public repository. Articles and evidence logs are licensed CC BY "
            "4.0; the code is MIT."
        ),
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
        "updated_chip": "updated {date}",
        "event_date": "Event {date}",
        "published_date": "published {date}",
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
            "Henüz doğrulamadan geçen haber yok. Aşağıda tarayıcının izlediği "
            "içeriklerden canlı bir örnek var — doğrulanmamıştır, yalnızca hattın "
            "çalıştığını göstermek için listelenmiştir."
        ),
        "digest": "Tarayıcı akışı",
        "digest_note": (
            "Başlıklar kaynakların yayımladığı hâliyle, ham olarak listelenmiştir — "
            "doğrulanmamıştır; yalnızca hattın neyi izlediğini göstermek içindir."
        ),
        "methodology": "Yöntem",
        "site_title": "noiseless.news — doğrulanmış yapay zekâ haberleri",
        "feed_title": "noiseless.news (Türkçe)",
        "feed_link": "Akış",
        "about": "Hakkında",
        "corrections": "Düzeltmeler",
        "footer": "Açık inşa ediliyor — her hükmün kanıt zinciri kamuya açık.",
        "disclosure": (
            "Bu sitedeki haberler, kamuya açık bir yayın politikasını izleyen "
            "yapay zekâ ajanları tarafından, insan gözetimi olmadan yazılıp "
            "doğrulanır. Hiçbir haber yayımlanmadan önce bir kişi tarafından "
            "düzenlenmez."
        ),
        "operator": "Yürüten: <a href='https://github.com/y-nihat'>y-nihat</a>.",
        "contact": "Bir hata mı gördünüz?",
        "contact_link": "Bildirin",
        "last_run": "Son doğrulama turu",
        "no_corrections": (
            "Henüz düzeltme yayımlanmadı. Bir haber düzeltildiğinde, düzeltme "
            "burada listelenir ve haberin kendisinde tarihiyle belirtilir; "
            "ilk hâli bu deponun git geçmişinde kalır."
        ),
        "corrections_note": (
            "Sitenin yaptığı bütün düzeltmeler, en yenisi başta. Düzeltme, "
            "yayımlanmış bir iddianın yanlış olduğu anlamına gelir; doğru olan "
            "bir habere yeni bilgi ekleyen güncellemeden farklıdır."
        ),
        "about_intro": (
            "noiseless.news, doğrulamadan geçen yapay zekâ haberlerini yayımlar "
            "ve doğrulamanın kendisini de yayımlar. Bağımsız kaynaklarla "
            "denetlenemeyen iddialar olgu diye sunulmaz; eşiği geçemeyen "
            "haberler ise gerekçesi yazılarak bekletilir."
        ),
        "about_made_h": "Nasıl hazırlanıyor",
        "about_made": (
            "Bu sitedeki her haber, gece boyunca insan gözetimi olmadan çalışan "
            "yapay zekâ ajanları tarafından, aşağıda bağlantısı verilen yayın "
            "politikasına göre yazılır ve doğrulanır. Hat her gece adı belli "
            "kaynaklardan oluşan açık bir kayıt defterini tarar, aday haberleri "
            "tek tek olgusal iddialara ayırır, her iddiayı bağımsız kanıtlarla "
            "denetler ve haberi — başlığı dahil — yalnızca doğrulanmış "
            "iddialardan yazar. Ardından, hiçbir şeyi bilmeyen ikinci bir ajan "
            "her iddiayı çürütmeye çalışır. "
            "<strong>Hiçbir haber yayına girmeden önce bir kişi tarafından "
            "incelenmez.</strong> İngilizce metin asıldır; Türkçe sürüm onu "
            "birebir yansıtır."
        ),
        "about_verdicts_h": "Hükümler ne anlama geliyor",
        "about_verdicts": {
            "confirmed": "İddia türünün gerektirdiği ispat düzeyini karşıladı: duyuru için birincil kaynak, ticari iddia için iki bağımsız kaynak, araştırma bulgusu için makalenin kendisi.",
            "vendor-claim": "İddiadan çıkarı olan tarafça öne sürüldü. Kesinleşmiş bilgi olarak değil, o tarafın beyanı olarak yayımlanır — örneğin modeli üreten şirketin kendi kıyaslama sonuçları.",
            "single-source": "Tek kaynak var. İddia haberi taşıdığı için yayımlandı, tartabilmeniz için de böyle etiketlendi.",
            "disputed": "Kaynaklar çelişiyor. Her iki taraf da aktarılıyor.",
        },
        "about_sources_h": "Kanıt nereden geliyor",
        "about_sources": (
            "Kaynaklar, kamuya açık bir dosyada adıyla ve katmanıyla kayıtlıdır. "
            "Katman 0 birincil ve resmîdir: şirket duyuruları, resmî başvurular, "
            "hukuki metinler. Katman 1 literatür, Katman 2 bağımsız basındır. "
            "Katman 3 — forumlar, video, sosyal medya — yalnızca haber "
            "<em>bulmak</em> için kullanılır, hiçbir iddiayı doğrulayamaz. Aynı "
            "basın bültenini yineleyen çok sayıda yayın tek kaynak sayılır."
        ),
        "about_wrong_h": "Yanıldığımızda",
        "about_wrong": (
            "Düzeltmeler ayrı bir sayfada yayımlanır ve haberin kendisinde "
            "tarihiyle belirtilir. İlk metin silinmez; deponun açık geçmişinde "
            "kalır. Burada bir şeyin yanlış olduğunu düşünüyorsanız ya da bir "
            "haberde adınız geçiyor ve yanıt vermek istiyorsanız, bir konu "
            "açın; gereği yapılır."
        ),
        "about_open_h": "Denetime açık",
        "about_open": (
            "Yayın politikası, kaynak kaydı, her haberin kanıt dosyası, gece "
            "raporları ve hattın kendisi tek bir kamuya açık depodadır. Haberler "
            "ve kanıt dosyaları CC BY 4.0, kod MIT lisanslıdır."
        ),
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
        "updated_chip": "güncellendi {date}",
        "event_date": "Olay {date}",
        "published_date": "yayım {date}",
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
.section { font-size:.8rem; font-weight:650; text-transform:uppercase;
           letter-spacing:.09em; color:var(--muted); margin:2.4rem 0 .4rem; }
h1.section { margin-top:1.4rem; }
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
footer.site .foot-line { margin:0 0 .4rem; max-width:38rem; line-height:1.55; }
footer.site .foot-line:last-child { margin-bottom:0; }
footer.site .disclosure { color:var(--fg); opacity:.85; }
footer.site .sep { margin:0 .45rem; opacity:.5; }

.page h1 { font-size:1.6rem; line-height:1.25; letter-spacing:-.02em;
           font-weight:750; margin:.2rem 0 .9rem; }
.page .lede { font-size:1.02rem; line-height:1.65; color:var(--fg); margin:0 0 1.6rem; }
.page h2 { font-size:1.02rem; letter-spacing:-.01em; font-weight:700; margin:1.9rem 0 .5rem; }
.page p { margin:0 0 .9rem; line-height:1.7; max-width:38rem; }
dl.verdicts { margin:.6rem 0 0; }
dl.verdicts dt { margin:.9rem 0 .25rem; }
dl.verdicts dd { margin:0; font-size:.93rem; line-height:1.6; color:var(--muted);
                 max-width:38rem; }
ul.corrections { list-style:none; margin:.4rem 0 0; padding:0; }
ul.corrections li { padding:.9rem 0; border-bottom:1px solid var(--rule); }
ul.corrections .date { font-size:.78rem; color:var(--muted); letter-spacing:.02em; }
ul.corrections .what { margin:.25rem 0 .3rem; line-height:1.6; }
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
        """When the event happened. This is what the byline states."""
        return str(self.meta.get("date", ""))

    @property
    def published(self) -> str:
        """When we published it. This is what the reader's ordering follows.

        The two diverge whenever verification takes longer than the news cycle,
        which is often: a story confirmed tonight about an event nine days ago
        used to appear halfway down the homepage, below things the reader had
        already seen, on its own launch day.
        """
        return str(self.meta.get("published") or self.date)

    @property
    def last_touched(self) -> str:
        """Newest of published and any dated `updated:` entry.

        An article that gained material new reporting three times over nine days
        never moved on the index, so a returning reader had no way to see it.
        """
        dates = [self.published]
        for entry in self.meta.get("updated") or []:
            parsed = parse_update_entry(entry)
            if parsed["date"]:
                dates.append(parsed["date"])
        return max(dates)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split '---' frontmatter from body. Returns (meta, body_markdown)."""
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body.strip()
    return {}, text.strip()


def safe_frontmatter(path: Path) -> tuple[dict, str] | None:
    """parse_frontmatter, but a broken file is skipped instead of fatal.

    Article files are written unattended at 03:00. Before this, one malformed
    YAML block took down the site build and `dedup-check` together — so the
    duplicate gate, which is the agent's own way out of the mess, broke at
    exactly the moment it was needed.
    """
    try:
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, ValueError, UnicodeDecodeError, OSError) as exc:
        print(f"[publish] SKIP {path}: {type(exc).__name__}: {exc}")
        return None
    if not isinstance(meta, dict):
        print(f"[publish] SKIP {path}: frontmatter is not a mapping")
        return None
    return meta, body


def load_articles(content_dir: Path, lang: str) -> list[Article]:
    lang_dir = content_dir / "articles" / lang
    articles = []
    for path in sorted(lang_dir.rglob("*.md")):
        parsed = safe_frontmatter(path)
        if parsed is None:
            continue
        meta, body = parsed
        if not meta.get("title") or not meta.get("slug"):
            continue
        articles.append(Article(meta=meta, body_html=md.markdown(body), lang=lang))
    # Newest first by when the reader could first have seen it, then by slug so
    # same-day ordering is deterministic rather than alphabetical-by-filename
    # falling out of a stable sort.
    articles.sort(key=lambda a: (a.last_touched, a.published, a.slug), reverse=True)
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
        try:
            items = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
            print(f"[publish] SKIP raw {path.name}: {exc}")
            continue
        if not isinstance(items, list):
            continue
        for item in items:
            # A truncated write or a feed oddity must not cost us the whole
            # site build — the digest is the least important thing on the page.
            if isinstance(item, dict) and isinstance(item.get("tier"), int):
                tiers.setdefault(item["tier"], []).append(item)
    for tier, items in tiers.items():
        items.sort(key=lambda item: item.get("published") or "", reverse=True)
        tiers[tier] = items[:max_per_tier]
    return {"date": latest.name, "tiers": tiers}


_UPDATE_KIND = re.compile(r"^\s*(correction|düzeltme|update|güncelleme)\s*[:—-]\s*", re.I)
_UPDATE_DATE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*[:—-]\s*")
_CORRECTION_WORDS = {"correction", "düzeltme"}


def parse_update_entry(entry: str) -> dict:
    """Split an `updated:` line into kind, date and text.

    Accepts `2026-07-14: text`, `correction: 2026-07-14: text` and
    `2026-07-14: correction: text`. Untyped entries are updates, which keeps
    every existing entry valid: an update adds information to a story that was
    right, a correction says a published claim was wrong. Only the second
    belongs on the corrections page.
    """
    text = str(entry).strip()
    kind, date = "update", ""
    for _ in range(2):  # kind and date may appear in either order
        matched = _UPDATE_KIND.match(text)
        if matched:
            if matched.group(1).lower() in _CORRECTION_WORDS:
                kind = "correction"
            text = text[matched.end():]
            continue
        matched = _UPDATE_DATE.match(text)
        if matched and not date:
            date = matched.group(1)
            text = text[matched.end():]
    return {"kind": kind, "date": date, "text": text.strip()}


def latest_run_date(data_dir: Path) -> str:
    """Date of the most recent nightly run, from the run-report filenames.

    Run reports exist even on nights that published nothing, so this says "the
    machine ran" rather than "an article appeared" — which is the honest signal
    for a site whose stated policy is to publish nothing when nothing clears
    the bar. A site that has stopped running now says so.
    """
    dates = sorted(
        match.group(1)
        for path in (data_dir / "ledger").glob("run-report-*.md")
        if (match := re.search(r"(\d{4}-\d{2}-\d{2})", path.name))
    )
    return dates[-1] if dates else ""


def reading_minutes(body_html: str) -> int:
    words = len(re.sub(r"<[^>]+>", " ", body_html).split())
    return max(1, round(words / 200))


def _domain(url: str) -> str:
    return re.sub(r"^www\.", "", url.split("//")[-1].split("/")[0])


def _page(*, lang: str, title: str, body: str, home: str, other_lang_href: str,
          description: str = "", prefix: str = "", last_run: str = "",
          path: str = "", alternate_path: str | None = None) -> str:
    s = STRINGS[lang]
    desc = html.escape(description or s["tagline"])
    canonical = f"{SITE_URL}/{path}"
    # Reciprocal hreflang, plus x-default pointing at the canonical English
    # edition. Both index pages previously shipped the identical <title>, so a
    # bookmark or a search result could not tell the two editions apart.
    alternates = ""
    if alternate_path is not None:
        other_lang = "tr" if lang == "en" else "en"
        en_path = path if lang == "en" else alternate_path
        alternates = (
            f'<link rel="alternate" hreflang="{lang}" href="{SITE_URL}/{path}">\n'
            f'<link rel="alternate" hreflang="{other_lang}" href="{SITE_URL}/{alternate_path}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{en_path}">\n'
        )
    feed_path = "feed.xml" if lang == "en" else "tr/feed.xml"
    # The footer carries the three things a reader needs and the site did not
    # say anywhere: who runs it, that no person edits an article before it is
    # published, and how to report an error.
    liveness = (
        f"<span class='sep'>·</span>{s['last_run']}: {html.escape(last_run)}"
        if last_run
        else ""
    )
    footer = (
        f"<p class='foot-line'>{s['footer']}{liveness}</p>"
        f"<p class='foot-line disclosure'>{s['disclosure']}</p>"
        f"<p class='foot-line'>{s['operator']} {s['contact']} "
        f"<a href='{REPO_URL}/issues/new'>{s['contact_link']}</a>.</p>"
    )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<title>{html.escape(title)}</title>
<link rel="canonical" href="{canonical}">
{alternates}<link rel="alternate" type="application/atom+xml" title="{html.escape(s['feed_title'])}" href="{SITE_URL}/{feed_path}">
<meta property="og:type" content="{'article' if path.count('articles/') else 'website'}">
<meta property="og:site_name" content="noiseless.news">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'tr_TR'}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{FAVICON}">
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <div class="wrap">
    <div class="bar">
      <a class="wordmark" href="{home}">noiseless<em>.</em>news</a>
      <nav class="top">
        <a href="{other_lang_href}" hreflang="{'tr' if lang == 'en' else 'en'}" lang="{'tr' if lang == 'en' else 'en'}">{s['other_lang']}</a>
        <a href="{prefix}about.html">{s['about']}</a>
        <a href="{prefix}corrections.html">{s['corrections']}</a>
        <a href="{prefix}feed.xml">{s['feed_link']}</a>
        <a href="{REPO_URL}/blob/main/policy/verification.md">{s['methodology']}</a>
      </nav>
    </div>
    <p class="tagline">{s['tagline']}</p>
  </div>
</header>
<hr class="rule">
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">{footer}</div></footer>
</body>
</html>
"""


def _byline_dates(article: Article, lang: str) -> str:
    """Event date alone when they agree; both, labelled, when they do not."""
    s = STRINGS[lang]
    if article.published == article.date:
        return f"<time datetime='{article.date}'>{article.date}</time>"
    return (
        f"{s['event_date'].format(date=article.date)}"
        f"<span class='dot'>·</span>"
        f"<time datetime='{article.published}'>"
        f"{s['published_date'].format(date=article.published)}</time>"
    )


def _chips_html(article: Article, lang: str) -> str:
    s = STRINGS[lang]
    chips = []
    sources = article.meta.get("sources") or []
    claims = article.meta.get("claims") or []
    if article.meta.get("follows"):
        chips.append(s["thread_chip"])
    if article.last_touched != article.published:
        # "What changed since I last looked" is the question a returning reader
        # actually has, and the index answered it nowhere.
        chips.append(s["updated_chip"].format(date=article.last_touched))
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
        return f"<h1 class='section'>{s['articles']}</h1><p class='empty'>{s['no_articles']}</p>"
    parts = [f"<h1 class='section'>{s['articles']}</h1><ul class='posts'>"]
    for article in articles:
        tldr = html.escape(str(article.meta.get("tldr", "")).strip())
        parts.append(
            f"<li><time class='date' datetime='{article.published}'>"
            f"{article.published}</time>"
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
            url, title = item.get("url"), item.get("title")
            if not url or not title:
                continue
            published = (item.get("published") or "")[:10]
            parts.append(
                f"<li><a href='{html.escape(str(url))}'>{html.escape(str(title))}</a>"
                f"<span class='meta'>{html.escape(str(item.get('source', '')))}"
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
        f"<p class='byline'>{_byline_dates(article, lang)}"
        f"<span class='dot'>·</span>{minutes} {s['min_read']}</p>",
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


def _about_html(lang: str) -> str:
    s = STRINGS[lang]
    verdicts = "".join(
        f"<dt><span class='badge {VERDICT_CLASS[key]}'>"
        f"{html.escape(s['verdicts'][key])}</span></dt><dd>{html.escape(text)}</dd>"
        for key, text in s["about_verdicts"].items()
    )
    return (
        f"<div class='page'><h1>{s['about']}</h1>"
        f"<p class='lede'>{s['about_intro']}</p>"
        f"<h2>{s['about_made_h']}</h2><p>{s['about_made']}</p>"
        f"<h2>{s['about_verdicts_h']}</h2><dl class='verdicts'>{verdicts}</dl>"
        f"<h2>{s['about_sources_h']}</h2><p>{s['about_sources']}</p>"
        f"<h2>{s['about_wrong_h']}</h2><p>{s['about_wrong']}</p>"
        f"<h2>{s['about_open_h']}</h2><p>{s['about_open']} "
        f"<a href='{REPO_URL}'>GitHub</a> · "
        f"<a href='{REPO_URL}/blob/main/policy/verification.md'>{s['methodology']}</a>"
        f"</p></div>"
    )


def collect_corrections(articles: list[Article]) -> list[dict]:
    """Every entry in every article's `updated:` list that is typed as a correction."""
    corrections = []
    for article in articles:
        for entry in article.meta.get("updated") or []:
            parsed = parse_update_entry(entry)
            if parsed["kind"] != "correction":
                continue
            corrections.append({**parsed, "slug": article.slug, "title": article.title})
    corrections.sort(key=lambda c: (c["date"], c["slug"]), reverse=True)
    return corrections


def _corrections_html(corrections: list[dict], lang: str, article_prefix: str) -> str:
    s = STRINGS[lang]
    if not corrections:
        body = f"<p class='empty'>{s['no_corrections']}</p>"
    else:
        items = "".join(
            f"<li><span class='date'>{html.escape(c['date'])}</span>"
            f"<p class='what'>{html.escape(c['text'])}</p>"
            f"<a href='{article_prefix}{c['slug']}.html'>{html.escape(c['title'])}</a>"
            f"</li>"
            for c in corrections
        )
        body = f"<p class='note'>{s['corrections_note']}</p><ul class='corrections'>{items}</ul>"
    return f"<div class='page'><h1>{s['corrections']}</h1>{body}</div>"


def _feed_xml(articles: list[Article], lang: str) -> str:
    """Atom feed of the newest articles.

    The site ingests 48 feeds every night and published none, so a reader who
    found it had no way to be told about the next article. Entries are ordered
    and timestamped by publication rather than by event date — a feed built on
    the event date would have been wrong for 22 of 57 articles and would land in
    subscribers' readers sorted below things they had already seen.
    """
    s = STRINGS[lang]
    base = f"{SITE_URL}/" if lang == "en" else f"{SITE_URL}/tr/"
    feed_url = f"{base}feed.xml"
    recent = articles[:FEED_LIMIT]
    updated = f"{recent[0].last_touched}T00:00:00Z" if recent else "1970-01-01T00:00:00Z"

    entries = []
    for article in recent:
        url = f"{base}articles/{article.slug}.html"
        summary = str(article.meta.get("tldr", "")).strip()
        entries.append(
            "<entry>"
            f"<title>{html.escape(article.title)}</title>"
            f"<link href='{url}'/>"
            f"<id>{url}</id>"
            f"<published>{article.published}T00:00:00Z</published>"
            f"<updated>{article.last_touched}T00:00:00Z</updated>"
            f"<summary>{html.escape(summary)}</summary>"
            "</entry>"
        )
    return (
        "<?xml version='1.0' encoding='utf-8'?>\n"
        f"<feed xmlns='http://www.w3.org/2005/Atom' xml:lang='{lang}'>"
        f"<title>{html.escape(s['feed_title'])}</title>"
        f"<subtitle>{html.escape(s['tagline'])}</subtitle>"
        f"<link href='{base}'/>"
        f"<link rel='self' href='{feed_url}'/>"
        f"<id>{feed_url}</id>"
        f"<updated>{updated}</updated>"
        f"<author><name>noiseless.news</name><uri>{SITE_URL}/about.html</uri></author>"
        f"<rights>CC BY 4.0</rights>"
        + "".join(entries)
        + "</feed>\n"
    )


def _sitemap_xml(paths: list[str]) -> str:
    urls = "".join(f"<url><loc>{SITE_URL}/{path}</loc></url>" for path in paths)
    return (
        "<?xml version='1.0' encoding='utf-8'?>\n"
        "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
        f"{urls}</urlset>\n"
    )


def _robots_txt() -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"


def build_site(repo_root: Path | str, out_dir: Path | str) -> dict[str, int]:
    """Render the whole site, then swap it into place.

    The build is assembled in a sibling directory and moved over the old one
    only once it has completed. The nightly workflow runs its upload and deploy
    steps with `if: always()`, so a build that died halfway through used to be
    a half-rendered site queued for publication.
    """
    repo_root, out_dir = Path(repo_root), Path(out_dir)
    staging = out_dir.parent / f".{out_dir.name}.building"
    if staging.exists():
        shutil.rmtree(staging)
    counts = _render_site(repo_root, staging)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    staging.replace(out_dir)
    return counts


def _render_site(repo_root: Path, out_dir: Path) -> dict[str, int]:
    (out_dir / "articles").mkdir(parents=True)
    (out_dir / "tr" / "articles").mkdir(parents=True)

    digest = build_digest(repo_root / "data")
    last_run = latest_run_date(repo_root / "data")
    counts = {}
    sitemap_paths: list[str] = []
    for lang, lang_root, home, base in (
        ("en", out_dir, "index.html", ""),
        ("tr", out_dir / "tr", "index.html", "tr/"),
    ):
        other_base = "tr/" if lang == "en" else ""
        articles = load_articles(repo_root / "content", lang)
        threads = resolve_threads(articles)
        counts[lang] = len(articles)
        other = "tr/index.html" if lang == "en" else "../index.html"

        def page(title, body, *, path, alternate, home=home, other=other,
                 prefix="", description=""):
            sitemap_paths.append(path)
            return _page(lang=lang, title=title, body=body, home=home,
                         other_lang_href=other, description=description,
                         prefix=prefix, last_run=last_run, path=path,
                         alternate_path=alternate)

        index_body = _article_list_html(articles, lang, "articles/") + _digest_html(
            digest, lang
        )
        (lang_root / "index.html").write_text(
            page(STRINGS[lang]["site_title"], index_body,
                 path=base, alternate=other_base),
            encoding="utf-8",
        )
        (lang_root / "about.html").write_text(
            page(f"{STRINGS[lang]['about']} — noiseless.news", _about_html(lang),
                 path=f"{base}about.html", alternate=f"{other_base}about.html",
                 other="tr/about.html" if lang == "en" else "../about.html",
                 description=STRINGS[lang]["disclosure"]),
            encoding="utf-8",
        )
        (lang_root / "corrections.html").write_text(
            page(f"{STRINGS[lang]['corrections']} — noiseless.news",
                 _corrections_html(collect_corrections(articles), lang, "articles/"),
                 path=f"{base}corrections.html",
                 alternate=f"{other_base}corrections.html",
                 other="tr/corrections.html" if lang == "en" else "../corrections.html",
                 description=STRINGS[lang]["corrections_note"]),
            encoding="utf-8",
        )

        for article in articles:
            counterpart = (
                f"../../articles/{article.slug}.html"
                if lang == "tr"
                else f"../tr/articles/{article.slug}.html"
            )
            (lang_root / "articles" / f"{article.slug}.html").write_text(
                page(f"{article.title} — noiseless.news",
                     _article_html(article, lang, home="../index.html",
                                   thread=threads.get(article.slug)),
                     path=f"{base}articles/{article.slug}.html",
                     alternate=f"{other_base}articles/{article.slug}.html",
                     home="../index.html", other=counterpart, prefix="../",
                     description=str(article.meta.get("tldr", "")).strip()),
                encoding="utf-8",
            )

        (lang_root / "feed.xml").write_text(_feed_xml(articles, lang), encoding="utf-8")

    (out_dir / "sitemap.xml").write_text(_sitemap_xml(sitemap_paths), encoding="utf-8")
    (out_dir / "robots.txt").write_text(_robots_txt(), encoding="utf-8")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    return counts
