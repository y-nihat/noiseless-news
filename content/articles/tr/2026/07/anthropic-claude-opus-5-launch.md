---
title: Anthropic, Claude Opus 5'i tanıttı; fiyatlandırma milyon token başına 5/25 dolarda sabit kaldı
date: 2026-07-24
slug: anthropic-claude-opus-5-launch
lang: tr
tldr: >
  Anthropic, 24 Temmuz 2026'da Claude Opus 5'i piyasaya sürdü; model aynı gün
  Claude API, claude.ai, Claude Code, Bedrock, Google Cloud ve Microsoft
  Foundry üzerinden kullanıma açıldı (GitHub Copilot erişimi kademeli olarak
  geliyor). Standart fiyatlandırma, Opus 4.8 ile aynı şekilde milyon giriş
  token'ı başına 5 dolar ve milyon çıkış token'ı başına 25 dolarda sabit
  kaldı. Bağımsız takip kuruluşu Artificial Analysis, modeli Intelligence
  Index sıralamasında zirveye yerleştirdi; Anthropic'in rakip modellere karşı
  yaptığı karşılaştırmalı performans iddiaları henüz bağımsız olarak
  doğrulanmadı.
sources:
  - name: Anthropic News
    url: https://www.anthropic.com/news/claude-opus-5
  - name: GitHub Changelog
    url: https://github.blog/changelog/2026-07-24-claude-opus-5-is-now-available-in-github-copilot/
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/models/claude-opus-5
  - name: CodeRabbit
    url: https://www.coderabbit.ai/blog
  - name: VentureBeat
    url: https://venturebeat.com/
claims:
  - text: "Anthropic, Claude Opus 5'i 24 Temmuz 2026'da piyasaya sürdü"
    type: announcement
    verdict: confirmed
    evidence: [1, 5]
  - text: "Opus 5, ilk günden itibaren Claude API, claude.ai, Claude Code, Claude Cowork, Pro ve Max planları, Amazon Bedrock, Google Cloud Vertex AI ve Microsoft Foundry üzerinden kullanıma sunuldu; GitHub Copilot erişimi Pro+, Max, Business ve Enterprise kullanıcılarına kademeli olarak açılıyor"
    type: business
    verdict: confirmed
    evidence: [1, 2]
  - text: "Standart fiyatlandırma, Opus 4.8 ile aynı şekilde milyon giriş token'ı başına 5 dolar ve milyon çıkış token'ı başına 25 dolar; daha hızlı bir çıkarım modu yaklaşık iki katı fiyatlanıyor"
    type: business
    verdict: confirmed
    evidence: [1, 5]
  - text: "Anthropic, kendi Frontier-Bench v0.1 (yüzde 43,3'e karşı Fable 5'in yüzde 33,7'si) ve ARC-AGI-3 (yüzde 30,2'ye karşı bir sonraki en iyi modelin yüzde 7,8'i) sonuçlarına dayanarak Opus 5'in Fable 5'in zekasına yaklaşık yarı fiyatla yaklaştığını iddia ediyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Bağımsız Artificial Analysis Intelligence Index sıralamasında, Claude Opus 5 (maksimum performans ayarında) 24 Temmuz 2026 tarihli canlı sıralama verisine göre 61 puanla takip edilen modeller arasında birinci sırada yer alıyor"
    type: capability
    verdict: confirmed
    evidence: [3]
  - text: "Kod inceleme şirketi CodeRabbit'in bağımsız testine göre Opus 5, işaretlediği sorunlarda kendi temel değerlendiricilerinden daha isabetli (yüzde 39,3'e karşı yüzde 35,2) ancak bilinen sorunları yakalamada daha düşük başarı gösterdi (yüzde 55,2'ye karşı yüzde 61,1) ve yaklaşık dört kat daha fazla küçük çaplı yorum üretti; CodeRabbit, bulgularının Opus 5'in tek başına inceleyici olarak kullanılmasını desteklemediğini belirtiyor"
    type: capability
    verdict: confirmed
    evidence: [4]
updated: []
---

## Ne oldu

Anthropic, Claude Opus 5'i 24 Temmuz 2026'da piyasaya sürdü ve modeli aynı gün Claude API, claude.ai, Claude Code, Claude Cowork ile Pro/Max abonelik planlarının yanı sıra Amazon Bedrock, Google Cloud Vertex AI ve Microsoft Foundry üzerinden kullanıma açtı [1]. GitHub, Copilot erişimini ayrıca doğruladı; ancak buradaki erişimin herkese anında değil, Pro+, Max, Business ve Enterprise katmanlarına kademeli olarak açıldığını belirtti [2]. Standart API fiyatlandırması, Opus 4.8 ile aynı oranda kaldı: milyon giriş token'ı başına 5 dolar, milyon çıkış token'ı başına 25 dolar; daha hızlı bir çıkarım modu ise yaklaşık iki katı fiyatlanıyor [1].

Anthropic'in kendi pazarlama anlatısı Fable 5 ile yapılan bir karşılaştırmaya odaklanıyor: şirket, Opus 5'in bu modelin zekasına yaklaşık yarı maliyetle yaklaştığını, kendi yürüttüğü Frontier-Bench v0.1 (yüzde 43,3'e karşı Fable 5'in yüzde 33,7'si) ve ARC-AGI-3 (yüzde 30,2, bir sonraki en iyi modelin yüzde 7,8'inin üç katından fazla) sonuçlarıyla destekliyor [1]. Her iki ölçüt de bağımsız olarak yeniden üretilmediğinden, burada doğrulanmış sonuçlar değil Anthropic'in kendi iddiaları olarak sunuluyor.

Bağımsız kanıtlar daha sınırlı ama mevcut. Üçüncü taraf bir sıralama olan Artificial Analysis Intelligence Index, 24 Temmuz 2026'da yapılan canlı bir veri çekiminde Opus 5'i maksimum performans ayarında 61 puanla sıralamanın zirvesine yerleştirdi [3]. Ayrı olarak, kod inceleme şirketi CodeRabbit kendi karşılaştırmasını yaptı ve karışık bir tablo ortaya çıktı: Opus 5, işaretlediği sorunlarda CodeRabbit'in temel değerlendiricisinden daha isabetliydi (yüzde 39,3'e karşı yüzde 35,2) ancak CodeRabbit'in test kümesindeki bilinen sorunların daha azını yakaladı (yüzde 55,2'ye karşı yüzde 61,1) ve yaklaşık dört kat daha fazla düşük değerli "ince ayrıntı" yorumu üretti. CodeRabbit'in kendi sonucu, verilerinin Opus 5'in tek başına bir inceleyici olarak kullanılmasını desteklemediği yönünde [4].

## Neden önemli

Önceki amiral gemisi modele göre sabit tutulan fiyatlandırma, Anthropic'in sattığı hemen her büyük bulut ve kodlama platformunda ilk günden sağlanan erişimle birleşince, şirketin Opus 5'i pahalı yeni bir katman değil, doğrudan yerine geçen bir yükseltme olarak konumlandırdığını gösteriyor. Anthropic'in kendi performans iddiaları ile şu ana kadarki daha sınırlı bağımsız kanıtlar arasındaki fark — bir olumlu üçüncü taraf sıralaması, bir karışık üçüncü taraf değerlendirmesi — aynı gün yapılan bir lansman için tipik; önümüzdeki haftalarda yapılacak bağımsız testler bu boşluğu dolduracak.
