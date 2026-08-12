---
title: SpaceXAI, Grok 4.6'yı çıkardı; bağımsız bir benchmark skorunda GPT-5.6 Sol'a eşitlendi
date: 2026-08-12
slug: grok-4-6-release
lang: tr
tldr: >
  SpaceXAI (yeniden markalanan xAI), Grok 4.6'yı 12 Ağustos 2026'da, yüksek
  akıl yürütme katmanı için milyon girdi/çıktı tokenı başına 2$/6$ fiyatla
  yayınladı. Bağımsız değerlendirici Artificial Analysis'in canlı olarak
  çekilen verilerine göre modelin Intelligence Index skoru 61 — OpenAI'nin
  GPT-5.6 Sol'una fiilen eşit ve Kimi K3'ün az önünde, ancak Anthropic'in
  Claude Opus 5 (63) ve Claude Fable 5'inin (62) hâlâ gerisinde.
sources:
  - name: xAI News (SpaceXAI)
    url: https://x.ai/news/grok-4-6
  - name: Artificial Analysis (model sayfası)
    url: https://artificialanalysis.ai/models/grok-4-6
  - name: Artificial Analysis (benchmark makalesi)
    url: https://artificialanalysis.ai/articles/grok-4-6-benchmarks-and-analysis
claims:
  - text: "SpaceXAI, Grok 4.6'yı 12 Ağustos 2026'da yayınladı; yüksek akıl yürütme katmanı milyon girdi tokenı başına 2$, milyon çıktı tokenı başına 6$ (önbellek isabetinde milyon başına 0,50$) fiyatlandırılıyor; ayrı bir 'hızlı' seçenek iki katı fiyata satılıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Grok 4.6, Artificial Analysis'in Intelligence Index'inde 61 puan alıyor; bu, GPT-5.6 Sol (61) ile fiilen eşit ve Kimi K3'ün (60) bir puan önünde, ancak Claude Opus 5 (63) ve Claude Fable 5'in (62) gerisinde"
    type: capability
    verdict: confirmed
    evidence: [2, 3]
updated: []
follows: grok-4-5-release
---

## Ne oldu

xAI'nin Temmuz 2026'daki SpaceX çatısı altındaki yeniden markalanmasından bu
yana kullandığı marka olan SpaceXAI, Grok 4.6'yı 12 Ağustos 2026'da yayınladı
[1]. Yüksek akıl yürütme katmanı milyon girdi tokenı başına 2$ ve milyon çıktı
tokenı başına 6$ olarak fiyatlandırılıyor; önbellek isabeti oranı milyon
başına 0,50$; ayrı bir "hızlı" seçenek iki katı fiyata satılıyor [1][2].

Bağımsız bir benchmark takipçisi olan Artificial Analysis, yayın anında canlı
olarak çektiği verilere göre Grok 4.6'ya Intelligence Index'te 61 puan
veriyor — bunu OpenAI'nin GPT-5.6 Sol'u (o da 61 puan) ile "fiilen aynı" skor
olarak tanımlıyor ve Kimi K3'ün 60 puanının bir puan önünde [2][3]. Her ikisi
de Anthropic'in mevcut ürün yelpazesinin gerisinde kalmaya devam ediyor:
Claude Opus 5 (63) ve Claude Fable 5 (62) [2][3]. Yayının haber kapsamı
genişti, ancak neredeyse tamamı ayrı, bağımsız muhabirlik yerine yalnızca bu
iki kaynağa — xAI'nin kendi duyurusu ve Artificial Analysis'in benchmark
verisine — dayanıyor.

## Neden önemli

Temmuz'da yayınlanan Grok 4.5, yetenek bakımından Anthropic'in üst düzey
modellerinin gerisinde kalırken fiyat ve verimlilik üzerinden konumlanmıştı.
Grok 4.6, aynı agresif fiyatlandırmayı korurken bu farkı bağımsız bir
endekste kapatıyor — OpenAI'nin amiral gemisinin belirgin biçimde gerisinde
kalmak yerine neredeyse eşitleniyor. Anthropic'in Opus 5 ve Fable 5 modelleri
takip edilen alanda hâlâ önde.
