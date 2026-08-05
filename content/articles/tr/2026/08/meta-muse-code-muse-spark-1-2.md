---
title: Meta, terminal tabanlı kodlama ajanı Muse Code'u Muse Spark 1.2 ile birlikte yayınladı
date: 2026-08-05
slug: meta-muse-code-muse-spark-1-2
lang: tr
tldr: >
  Meta, 5 Ağustos 2026'da ilk kodlama ajanı Muse Code'u yayınladı — macOS ve
  Linux'ta genel beta aşamasında, tamamen terminalden çalışan ve yeni Muse
  Spark 1.2 modeliyle çalışan bir araç. Fiyatlandırma, Temmuz'daki Muse Spark
  1.1 API oranlarıyla aynı ve Anthropic ile OpenAI'nin altında; kullanım
  verisini paylaşmayı kabul eden geliştiriciler için ayrıca indirimli bir
  katman da var. Meta'nın kendi benchmark tabloları rakip ajanlara karşı
  rekabetçi bir konum iddia ediyor; henüz bağımsız bir değerlendirme yok.
sources:
  - name: Meta AI Research
    url: https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2
  - name: CNBC Technology
    url: https://www.cnbc.com/2026/08/05/meta-debuts-muse-code-to-take-on-anthropic-and-openai-.html
  - name: VentureBeat AI
    url: https://venturebeat.com/orchestration/meta-enters-the-ai-coding-wars-with-muse-spark-1-2-and-muse-code-with-persistent-async-background-agents
claims:
  - text: "Meta, yeni Muse Spark 1.2 modeliyle çalışan terminal tabanlı kodlama ajanı Muse Code'u 5 Ağustos 2026'da macOS ve Linux için genel beta aşamasında yayınladı; komut satırından tek komutla kuruluyor ve genişletilmiş küresel erişimle Meta Model API üzerinden de sunuluyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Muse Code'un kullandıkça öde API fiyatlandırması milyon girdi tokenı başına 1,25$ ve milyon çıktı tokenı başına 4,25$ — Temmuz'daki Muse Spark 1.1 ile aynı oran ve karşılaştırılabilir Anthropic ile OpenAI tekliflerinin altında — ayrıca modelin geliştirilmesine yardımcı olmak için kullanım verisini paylaşmayı kabul eden geliştiriciler için ayrı, daha indirimli bir 'katkıda bulunan' katmanı var"
    type: business
    verdict: confirmed
    evidence: [2, 3]
  - text: "Meta, Muse Spark 1.2'nin Muse Code ile birlikte eğitildiğini ve 1.1'e kıyasla kod üretimi, karmaşık hata ayıklama, kod tabanını anlama ve uçtan uca geliştirici iş akışlarında iyileşmeler gösterdiğini söylüyor; bunun için kendi benchmark tablolarını (Terminal-Bench 2.1, DeepSWE 1.1, Meta Internal Coding Bench) rakip kodlama ajanlarına karşı gösteriyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
follows: meta-muse-spark-1-1
---

## Ne oldu

Meta, 5 Ağustos 2026'da Muse Code'u yayınladı — ilk yapay zekâ kodlama ajanı ve şirketin Anthropic'in Claude Code'u ile OpenAI'nin Codex'i gibi terminal tabanlı kodlama ajanı kategorisindeki ilk ürünü [1][2]. Tamamen komut satırından çalışıyor, tek bir komutla kuruluyor ve macOS ile Linux için genel beta aşamasında sunuluyor; oturumları tekrar-oynatılabilir ve yeniden başlatmaya dayanıklı hale getirmeyi amaçlayan kalıcı arka plan ajanları ve yerel bir olay günlüğü var [1]. Ayrıca, Meta'nın artık genişletilmiş küresel erişime sahip olduğunu söylediği Meta Model API üzerinden de kullanılabiliyor [1].

Muse Code, Meta'nın Temmuz ayındaki Muse Spark 1.1'in kodlamaya odaklı bir güncellemesi olarak tanımladığı ve ajanla birlikte eğitilen yeni bir model olan Muse Spark 1.2 tarafından çalıştırılıyor [1]. Kullandıkça öde API fiyatlandırması 1.1'den değişmedi: milyon girdi tokenı başına 1,25$ ve milyon çıktı tokenı başına 4,25$ — karşılaştırılabilir Anthropic ve OpenAI tekliflerinin hâlâ altında [2][3]. Ayrı bir "katkıda bulunan" katmanı, modelin geliştirilmesine yardımcı olmak için kullanım verisini paylaşmayı kabul eden geliştiricilere ek indirim sunuyor [2].

Meta'nın kendi benchmark tabloları — Terminal-Bench 2.1, DeepSWE 1.1 ve kendi Meta Internal Coding Bench'i — Muse Spark 1.2'yi rakip kodlama ajanlarına karşı rekabetçi gösterecek şekilde sunuluyor [1]. Ne CNBC ne de VentureBeat modelin bağımsız testlerini yaptığını bildirdi; ikisi de büyük ölçüde Meta'nın kendi lansman materyallerini ve benchmark tablolarını aktardı [2][3]. Muse Spark 1.1 için Vals AI'nin yayınladığı türden bağımsız bir üçüncü taraf değerlendirmesi bu sürüm için henüz mevcut değil.

## Neden önemli

Bu, Meta'nın Temmuz'daki Muse Spark 1.1 API lansmanının ardından bir ay içinde ücretli yapay zekâ kodlama pazarına ikinci hamlesi ve Anthropic ile OpenAI'nin zaten rekabet ettiği terminal ajanı kategorisindeki ilk özel ürünü — doğrudan bu kategoriyi hedefliyor. Fiyatlandırmanın aynı kalması, Meta'nın asıl kaldıracının maliyette rakiplerinin altında kalmaya devam etmek olduğunu, iddia edilen kapasite üstünlüğünün ise şimdilik tamamen Meta'nın kendi benchmark seçimine dayandığını gösteriyor.
