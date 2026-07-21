---
title: Google, Gemini 3.6 Flash ve 3.5 Flash-Lite'ı çıkardı; 3.5 Pro amiral gemisini geri tuttu
date: 2026-07-21
slug: google-gemini-3-6-flash-launch
lang: tr
tldr: >
  Google, 21 Temmuz 2026'da Gemini ailesine iki yeni model ekledi: 3.6 Flash
  ve 3.5 Flash-Lite. Ayrıca yalnızca devlet/ortak pilot programına açık,
  siber güvenlik odaklı bir varyant olan 3.5 Flash Cyber'i duyurdu. Google'ın
  kendi verileri önceki Flash neslinden daha hızlı ve ucuz çıkarım iddia
  ediyor; bağımsız bir karşılaştırma kuruluşu verimlilik kazanımlarını
  doğruladı ancak zeka puanlarının arttığını değil sabit kaldığını buldu.
  Birden fazla kaynak, beklenen Gemini 3.5 Pro amiral gemi modelinin,
  Google'ın iç performans hedeflerini tutturamaması nedeniyle geri
  tutulduğunu bildiriyor.
sources:
  - name: Google — Gemini modelleri blogu
    url: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/
  - name: Artificial Analysis — bağımsız karşılaştırma
    url: https://artificialanalysis.ai/articles/gemini-3-6-flash-3-5-flash-lite-halving-time
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/21/google-releases-three-new-gemini-models-but-no-3-5-pro/
claims:
  - text: "Google, 21 Temmuz 2026'da üç yeni Gemini modeli tanıttı: Gemini 3.6 Flash, Gemini 3.5 Flash-Lite ve Gemini 3.5 Flash Cyber"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "3.6 Flash ve 3.5 Flash-Lite; Gemini API, Google AI Studio, Android Studio ve Gemini uygulamasında hemen kullanıma sunuldu; 3.5 Flash Cyber ise yalnızca devletler ve güvenilir ortaklara açık sınırlı bir pilot programla erişilebiliyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "3.6 Flash, milyon girdi/çıktı token'ı başına 1,50 ve 7,50 dolar; 3.5 Flash-Lite ise 0,30 ve 2,50 dolar olarak fiyatlandırıldı; Flash Cyber için fiyat açıklanmadı"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Google'ın kendi benchmark sonuçlarına göre 3.6 Flash, MLE-Bench'te (%63,9'a karşı %49,7) ve OSWorld-Verified'da (%83,0'a karşı %78,4) 3.5 Flash'ı geride bırakıyor; çıktı token kullanımı da yaklaşık %17 azalmış"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Artificial Analysis'in bağımsız ölçümü, 3.6 Flash'ın Intelligence Index puanının 3.5 Flash'a göre sabit kaldığını, ancak gerçek verimlilik kazanımlarını doğruladı: görev başına süre %50'den fazla azaldı (2,7 dakikadan 1,3 dakikaya) ve görev başına maliyet yaklaşık %18 düştü"
    type: capability
    verdict: confirmed
    evidence: [2]
  - text: "Birden fazla kaynak, bir Bloomberg haberine atıfla, Google'ın beklenen Gemini 3.5 Pro amiral gemi güncellemesini iç performans hedeflerini tutturamadığı için geri tuttuğunu; Google'ın ise modelin ortaklarla test edildiğini ve yakında geleceğini söylediğini aktarıyor"
    type: business
    verdict: single-source
    evidence: [3]
updated: []
---

## Ne oldu

Google, 21 Temmuz 2026'da Gemini 3 ailesine iki yeni model ekledi: Gemini
3.6 Flash ve Gemini 3.5 Flash-Lite. Bunların yanında, güvenlik açıklarını
bulup düzeltmek için tasarlanmış ve yalnızca devletler ile güvenilir
ortaklara açık sınırlı bir pilot programla erişilebilen daha dar kapsamlı
üçüncü bir model olan Gemini 3.5 Flash Cyber'i de duyurdu [1]. Genel
kullanıma açık iki model şu anda Gemini API, Google AI Studio, Android
Studio ve Gemini uygulamasında kullanılabiliyor; 3.6 Flash milyon
girdi/çıktı token'ı başına 1,50/7,50 dolar, 3.5 Flash-Lite ise 0,30/2,50
dolar olarak fiyatlandırıldı [1]. Google, Flash Cyber için fiyat açıklamadı.

Google'ın kendi benchmark rakamları, 3.6 Flash'ın MLE-Bench (%63,9'a karşı
%49,7) ve OSWorld-Verified (%83,0'a karşı %78,4) gibi görevlerde 3.5
Flash'ın önünde olduğunu ve çıktı token kullanımının yaklaşık %17 azaldığını
gösteriyor [1] — bunlar satıcı tarafından bildirilen, henüz görev bazında
bağımsız olarak doğrulanmamış rakamlar. Bağımsız izleme kuruluşu Artificial
Analysis ise sürümü doğrudan ölçtü ve gerçek verimlilik kazanımlarını
doğruladı — görev süresi yarıdan fazla kısaldı (2,7 dakikadan 1,3 dakikaya)
ve görev başına maliyet yaklaşık %18 düştü — ancak modelin genel
Intelligence Index puanının 3.5 Flash'a göre değişmediğini buldu; yani bu
bir yetenek sıçraması değil, hız ve maliyet odaklı bir güncelleme [2].

Yayında, birçok kişinin beklediği Gemini 3.5 Pro amiral gemi modeli yok. Bir
Bloomberg haberine atıfla TechCrunch ve diğer kaynaklar, Google'ın iç
performans hedeflerini tutturamadığı için bu modeli geri tuttuğunu
söylüyor; Google ise yalnızca modelin ortaklarla test edildiğini ve yakında
geleceğini açıkladı [3]. Bu bilgi, tek bir Bloomberg haberine dayanıyor ve
diğer kaynaklar tarafından bağımsız olarak doğrulanmış değil, sadece
aktarılıyor.

## Neden önemli

Bu sürüm, bir yetenek sıçramasından çok verimlilik odaklı bir yenileme
izlenimi veriyor — maliyete duyarlı, büyük ölçekli kullanım için faydalı —
ve daha önemli olan amiral gemi güncellemesi henüz yayınlanmadı. Flash
Cyber'in devletler ve onaylı ortaklarla sınırlı tutulması, Google'ın güvenlik
açığı bulmaya yönelik diğer araçlarında uyguladığı çift kullanım
temkinliliğini yansıtıyor.
