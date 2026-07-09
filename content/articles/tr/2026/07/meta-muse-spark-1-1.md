---
title: Meta, ajan odaklı kodlama modeli Muse Spark 1.1'i fiyatta rakiplerinin altında yayınladı
date: 2026-07-09
slug: meta-muse-spark-1-1
lang: tr
tldr: >
  Meta, 9 Temmuz 2026'da Muse Spark 1.1'i yayınladı — Meta Model API üzerinden
  yalnızca ABD'de genel önizlemede sunulan, 1 milyon token bağlam penceresine
  sahip, çok modlu ve ajan odaklı bir model. Fiyatlandırması karşılaştırılabilir
  Anthropic ve OpenAI tekliflerinin oldukça altında. Meta, modelin rakip kodlama
  modelleriyle rekabet etmeye hazır olduğunu söylüyor; ancak bu Meta'nın kendi
  çerçevelemesi. Bulduğumuz tek bağımsız benchmark ise onu orta sıralarda
  konumlandırıyor: ajan görevlerinde önde, ama en zorlu kodlama testlerinde geride.
sources:
  - name: Meta AI Blog
    url: https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/
  - name: Meta Geliştirici Blogu
    url: https://developer.meta.com/ai/resources/blog/build-with-muse-spark/
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/09/meta-enters-the-crowded-ai-coding-battle-with-muse-spark-1-1/
  - name: The Verge
    url: https://www.theverge.com/ai-artificial-intelligence/963193/meta-muse-spark-model-api
  - name: Vals AI
    url: https://www.vals.ai/models/meta_muse_spark_1_1
claims:
  - text: "Meta, 9 Temmuz 2026'da Muse Spark 1.1'i yayınladı — 1 milyon token bağlam penceresine sahip, çok modlu, ajan odaklı bir model; Meta Model API üzerinden yalnızca ABD'de genel önizlemede ve Meta AI uygulaması ile meta.ai'de 'Düşünme' modunda sunuluyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 4]
  - text: "Muse Spark 1.1 API fiyatlandırması milyon girdi tokenı başına 1,25$ ve milyon çıktı tokenı başına 4,25$; yeni hesaplara 20$ ücretsiz kredi veriliyor; bu, karşılaştırılabilir Anthropic ve OpenAI tekliflerinin altında"
    type: business
    verdict: confirmed
    evidence: [2, 3]
  - text: "Meta, Muse Spark 1.1'in rakip öncü kodlama modelleriyle 'rekabet etmeye hazır' olduğunu söylüyor ve kendi benchmark tablolarını (Meta Internal Coding Bench, Terminal-Bench 2.1, SWE-Bench Pro) gösteriyor; bunlara göre model saf kodlama görevlerinde Claude Opus 4.8 ve GPT-5.5'e yakın ama gerisinde kalıyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 3, 4]
  - text: "Bağımsız Vals AI benchmark'ında (9 Temmuz 2026 itibarıyla test edilen 35 model arasında) Muse Spark 1.1 genel sıralamada 5. sırada yer alıyor ve 27 alt benchmark'tan 3'ünde — MedScribe, TaxEval v2 ve Harvey'nin Hukuk Ajanı Benchmark'ı, hiçbiri kodlamaya özgü değil — önde; en zorlu kodlama görevlerinde ise Claude Opus 4.8 ve GPT-5.5'in gerisinde kalıyor"
    type: capability
    verdict: confirmed
    evidence: [5]
  - text: "Meta CEO'su Mark Zuckerberg, lansman hakkında X'te paylaşım yaptı — bildirildiğine göre platformda yaklaşık üç yıl aradan sonra ilk paylaşımı"
    type: business
    verdict: confirmed
    evidence: [3]
updated: []
---

## Ne oldu

Meta, 9 Temmuz 2026'da Muse Spark 1.1'i yayınladı: 1 milyon token bağlam
penceresine sahip, çok modlu, ajan odaklı bir model; hem OpenAI SDK hem de
Anthropic'in Messages API formatlarıyla uyumlu Meta Model API üzerinden
yalnızca ABD'de genel önizlemede ve Meta AI uygulaması ile meta.ai'de "Düşünme"
modunda sunuluyor [1][3][4]. Fiyatlandırma milyon girdi tokenı başına 1,25$ ve
milyon çıktı tokenı başına 4,25$; yeni hesaplara 20$ ücretsiz kredi veriliyor —
bu, karşılaştırılabilir Anthropic ve OpenAI tekliflerinin altında [2][3].

Meta, modelin araç ve bilgisayar kullanımı, kodlama ve çok modlu anlama
konularında önemli kazanımlar sağladığını ve rakip öncü kodlama modelleriyle
"rekabet etmeye hazır" olduğunu söylüyor [1]. Bu çerçeveleme Meta'nın kendi
değerlendirme raporuna ve benchmark tablolarına (Meta'nın Internal Coding
Bench'i, Terminal-Bench 2.1, SWE-Bench Pro) dayanıyor; bunlara göre Muse Spark
1.1 saf kodlama görevlerinde Claude Opus 4.8 ve GPT-5.5'e yakın ama gerisinde
skor alıyor [1]. Ne TechCrunch ne de The Verge modelin kendi bağımsız
testlerini yaptı; ikisi de büyük ölçüde Meta'nın kendi mesajlarını ve erken
ortak referanslarını aktardı [3][4].

Gerçekten bağımsız tek bir veri noktası bulduk: üçüncü taraf değerlendirici
Vals AI, Muse Spark 1.1'i test ettiği 35 model arasında (9 Temmuz 2026
itibarıyla) genel sıralamada 5. sıraya koyuyor; 27 alt benchmark'tan 3'ünde —
MedScribe, TaxEval v2 ve Harvey'nin Hukuk Ajanı Benchmark'ı, hiçbiri kodlamaya
özgü değil — önde, en zorlu kodlama görevlerinde ise Opus 4.8 ve GPT-5.5'in
gerisinde [5]. Vals AI'nin liderlik tablosu sürekli güncellendiği için bu
rakamlar sabit bir sonucu değil, doğrulama anındaki bir anlık görüntüyü
yansıtıyor.

Ayrı olarak, Meta CEO'su Mark Zuckerberg lansman hakkında X'te paylaşım yaptı —
bildirildiğine göre platformda yaklaşık üç yıl aradan sonra ilk paylaşımı [3].

## Neden önemli

Meta, agresif ve piyasanın altında bir fiyatlandırmayla ücretli AI kodlama/ajan
API pazarına ilk kez giriyor ve doğrudan Anthropic ile OpenAI'nin geliştirici
müşterilerini hedefliyor. "Rekabet etmeye hazır" çerçevelemesi Meta'nın kendi
çerçevelemesi ve kendi benchmark seçimlerine dayanıyor; mevcut tek bağımsız
değerlendirme daha karışık bir tablo gösteriyor — maliyet ve ajan/araç kullanımı
görevlerinde güçlü, ama en zorlu kodlama benchmark'larında hâlâ kodlama
konusunda uzmanlaşmış öncü modellerin gerisinde.
