---
title: Meta, 30 milyar parametreli açık ağırlıklı yapay zekâ modeli Muse Glimmer'ı yayınladı
date: 2026-08-10
slug: meta-muse-glimmer-launch
lang: tr
tldr: >
  Meta, 10 Ağustos 2026'da Apache 2.0 lisanslı, 30 milyar parametreli açık
  ağırlıklı bir model olan Muse Glimmer'ı yayınladı; araç çağırma ve kodlama
  gibi ajansal görevler için tek bir tüketici GPU'sunda yerel olarak
  çalışacak şekilde tasarlandı. Aynı gün CEO Mark Zuckerberg, yapay zekâ
  kapasitesinin az sayıda laboratuvarda toplanmak yerine geniş çapta
  dağıtılması gerektiğini savunan bir deneme yayınladı ve Meta'nın 5
  Ağustos'ta ücretli API üzerinden piyasaya sürdüğü Muse Spark 1.2 modelinin
  ağırlıklarını da önümüzdeki haftalarda açacağını söyledi — bu henüz
  gerçekleşmemiş, sadece açıklanmış bir plan.
sources:
  - name: Meta AI Research
    url: https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
  - name: Meta Newsroom
    url: https://about.fb.com/news/2026/08/the-future-is-for-everyone/
  - name: VentureBeat AI
    url: https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now
claims:
  - text: "Meta, Muse Spark 1.2'den damıtılmış, 30 milyar parametreli yoğun bir model olan Muse Glimmer'ı 10 Ağustos 2026'da Hugging Face üzerinde Apache 2.0 lisansıyla yayınladı; model tek bir tüketici GPU'sunda (yaklaşık 24GB VRAM) yerel olarak çalışacak ve araç çağırma, kodlama, çok adımlı akıl yürütme gibi ajansal görevler için tasarlandı"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "Aynı gün Mark Zuckerberg, Meta'nın kendi sitesinde 'The Future Is for Everyone' başlıklı bir deneme yayınladı; yapay zekâ kapasitesinin az sayıda laboratuvar yerine geniş çapta dağıtılması gerektiğini savundu ve 'kapalı' yapay zekâ model üreticilerini eleştirdi"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "Zuckerberg, Meta'nın 5 Ağustos'ta Muse Code ajanıyla birlikte ücretli API üzerinden piyasaya sürdüğü Muse Spark 1.2 modelinin ağırlıklarını da önümüzdeki haftalarda açacağını söyledi"
    type: statement
    verdict: vendor-claim
    evidence: [2, 3]
updated: []
follows: meta-muse-code-muse-spark-1-2
---

## Ne oldu

Meta, 10 Ağustos 2026'da Muse Glimmer'ı yayınladı; Hugging Face üzerinde Apache 2.0 lisansıyla sunulan, 30 milyar parametreli yoğun bir model [1]. Muse Spark 1.2'den damıtılan model, tek bir tüketici GPU'sunda — yaklaşık 24GB VRAM ile — yerel olarak çalışacak şekilde tasarlandı ve bulutta değil kullanıcının kendi makinesinde yürütülen araç çağırma, kodlama ve çok adımlı akıl yürütme gibi ajansal görevleri hedefliyor [1][3].

Aynı gün Zuckerberg, Meta'nın kendi haber sitesinde yaklaşık 6.500 kelimelik "The Future Is for Everyone" başlıklı bir deneme yayınladı [2]. Deneme, yapay zekâ kapasitesinin az sayıda laboratuvar, hükümet veya şirkette toplanmak yerine geniş çapta dağıtılması gerektiğini savunuyor ve "kapalı" yapay zekâ model üreticilerini hedef alıyor [2][3]. Zuckerberg burada, 5 Ağustos'ta Muse Code ajanıyla birlikte piyasaya sürülen ve o zamandan beri yalnızca Meta'nın ücretli API'si üzerinden erişilebilen Muse Spark 1.2'nin ağırlıklarını da önümüzdeki haftalarda açacaklarını söyledi [2][3]. Bu, sevk edilmiş bir sürüm değil, açıklanmış bir plan: Meta daha önce en yetenekli modellerinin tümünü açık kaynak yapmayacağını söylemişti ve ne Meta'nın blog yazısı ne de bağımsız haberler kesin bir tarih veriyor.

## Neden önemli

Bu, Meta'nın bir hafta içindeki ikinci açık ağırlık hamlesi — 5 Ağustos'ta Spark 1.2'yi yalnızca API üzerinden tutmasının ardından geliyor — ve Çinli laboratuvarlardan gelen açık ağırlıklı sürümlerin artan rekabetiyle aynı döneme denk düşüyor. Glimmer'ın yayınlanması sevk edilmiş, doğrulanabilir bir gerçek; Meta'nın daha güçlü Spark 1.2 modelini açık ağırlıklı hale getirme sözü ise henüz değil — bunun gerçekleşip gerçekleşmeyeceği bir sonraki kontrol noktası.
