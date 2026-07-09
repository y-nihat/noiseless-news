---
title: xAI, Grok 4.5'i çıkardı; ham benchmark skoru yerine fiyat ve token verimliliğiyle konumlandırıyor
date: 2026-07-09
slug: grok-4-5-release
lang: tr
tldr: >
  Artık SpaceXAI markasıyla duyuru yapan xAI, Grok 4.5'i 8 Temmuz 2026'da milyon
  girdi/çıktı token başına 2$/6$ fiyatla ve 500.000 token bağlam penceresiyle
  yayınladı. Elon Musk modeli "Opus 4.7'ye kabaca denk" olarak nitelendirdi;
  xAI'nin kendi benchmark tablosunda SWE-Bench Pro'da Anthropic'in Opus 4.8 ve
  Claude Fable 5 modellerinin gerisinde kalırken, görev başına belirgin ölçüde
  daha az çıktı tokenı kullanıyor.
sources:
  - name: xAI News (SpaceXAI)
    url: https://x.ai/news/grok-4-5
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/08/spacexai-releases-grok-4-5-which-elon-describes-as-an-opus-class-model/
  - name: InfoWorld
    url: https://www.infoworld.com/article/4194895/spacexai-launches-grok-4-5-touts-lower-coding-task-costs-than-ai-rivals.html
claims:
  - text: "SpaceXAI markası altında faaliyet gösteren xAI, Grok 4.5'i 8 Temmuz 2026'da yayınladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Grok 4.5, milyon girdi tokenı başına 2$ ve milyon çıktı tokenı başına 6$ fiyatlandırılıyor; bağlam penceresi 500.000 token"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "Musk, Grok 4.5'i yetenek bakımından Opus 4.7'ye kabaca denk olarak tanımladı; xAI'nin kendi SWE-Bench Pro tablosunda model Opus 4.8 ve Claude Fable 5'in gerisinde skor alırken, çözülen görev başına Opus 4.8'e kıyasla yaklaşık 4 kat daha az çıktı tokenı kullanıyor"
    type: capability
    verdict: vendor-claim
    evidence: [2, 3]
updated: []
---

## Ne oldu

Artık duyurularını SpaceXAI markasıyla yayımlayan xAI, Grok 4.5'i 8 Temmuz
2026'da yayınladı [1][2]. Model, milyon girdi tokenı başına 2$ ve milyon çıktı
tokenı başına 6$ olarak fiyatlandırılıyor; bağlam penceresi 500.000 token [1][3].

Elon Musk, modeli Anthropic'in güncel amiral gemisini geçtiğini iddia etmek
yerine, önceki nesil amiral gemisi Opus 4.7'ye "kabaca denk" olarak
nitelendirdi [2]. Birden fazla yayın organı tarafından aktarılan xAI'nin kendi
benchmark tablosuna göre Grok 4.5, SWE-Bench Pro kodlama testinde hem Opus 4.8
hem de Claude Fable 5'in gerisinde kalıyor; ancak Opus 4.8'e kıyasla görev
başına yaklaşık dört kat daha az çıktı tokenı kullanarak çözüyor — şirketin
esas iddiası liderlik tablosunda zirveye çıkmak değil, verimlilik ve fiyat [2][3].

## Neden önemli

Grok 4.5, kodlama-ajanı pazarında benchmark lideri değil bir değer seçeneği
olarak konumlanıyor: xAI, Opus 4.8 ve Claude Fable 5'in gerisinde kaldığını
tartışmıyor, bunun yerine daha düşük görev başı maliyet ve token kullanımının
her benchmark'ta en yüksek skoru almaya ihtiyaç duymayan geliştiricileri
kazanacağına bahis oynuyor. Yetenek karşılaştırmaları xAI'nin kendi
raporlamasından geliyor ve henüz bağımsız olarak tekrarlanmadı — bağımsız
üçüncü taraf değerlendirmeleri çıkana kadar belirtilen benchmark farklarını
şirketin kendi beyanı olarak değerlendirin.
