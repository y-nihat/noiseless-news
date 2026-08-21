---
title: DeepSeek, deneysel çok modlu model V4-Flash-Vision-Exp'i yalnızca API üzerinden yayımladı
date: 2026-08-21
slug: deepseek-v4-flash-vision-exp
lang: tr
tldr: >
  DeepSeek, 21 Ağustos 2026'da API'si üzerinden deneysel bir görsel-metin
  (çok modlu) model olan DeepSeek-V4-Flash-Vision-Exp'i yayımladı; model,
  mevcut V4-Flash-0731 metin modeline görsel anlama yeteneği ekliyor. Temmuz
  ayındaki bu sürümün aksine yeni model yalnızca API üzerinden erişilebiliyor
  — DeepSeek açık ağırlıklı olmadığını açıkça belirtiyor. DeepSeek, kendi
  yaptığı testlerde modelin ajan performansının Claude Opus 4.8'e yakın
  olduğunu söylüyor; ancak şirketin kendi rakamları karışık sonuçlar
  gösteriyor ve bağımsız bir değerlendirme henüz yayımlanmadı.
sources:
  - name: DeepSeek News
    url: https://api-docs.deepseek.com/news/news260821
  - name: The Decoder
    url: https://the-decoder.com/deepseek-releases-experimental-flash-vision-model-that-rivals-opus-4-8-on-agent-benchmarks/
  - name: officechai
    url: https://officechai.com/ai/deepseek-releases-v4-flash-vision-exp-matches-opus-4-8-on-some-multimodal-benchmarks/
  - name: The Next Web
    url: https://thenextweb.com/news/deepseek-v4-flash-vision-exp-opus-benchmarks
claims:
  - text: "DeepSeek, 21 Ağustos 2026'da API'si üzerinden deneysel bir çok modlu model olan DeepSeek-V4-Flash-Vision-Exp'i yayımladı; model, mevcut V4-Flash-0731 metin modeline görsel anlama ekliyor ve o modelin metin performansını koruyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "V4-Flash-Vision-Exp yalnızca DeepSeek'in API'si üzerinden erişilebiliyor; DeepSeek'in kendi duyurusu, üzerine inşa edildiği Temmuz ayındaki V4-Flash-0731 sürümünün aksine bu modelin açık ağırlıklı olmadığını belirtiyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "DeepSeek, modelin çok modlu ajan performansının, kendi ölçüt altyapısında yaptığı değerlendirmelere göre Claude Opus 4.8'e yakın olduğunu söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "The Decoder ve officechai'nin aktardığı DeepSeek'in kendi ölçüt bazlı rakamlarına göre model, Opus 4.8'i bazı görevlerde geride bırakıyor (örneğin Agents' Last Exam'de 27,3'e karşı 25,7) ve NL2Repo gibi diğer görevlerde yaklaşık 12 puana varan farkla geride kalıyor; modele ait bağımsız bir değerlendirme sonucuna rastlanmadı"
    type: capability
    verdict: vendor-claim
    evidence: [2, 3]
  - text: "The Next Web, DeepSeek'in karşılaştırmasının Anthropic'in daha yeni modeli Opus 5 yerine Opus 4.8'e karşı yapıldığını ve DeepSeek'in kendi öncesi/sonrası tablosunun, önceki görsel özelliği olmayan modelini göremediği görseller içeren testlerde puanlamış göründüğünü bildirdi"
    type: capability
    verdict: single-source
    evidence: [4]
updated: []
---

## Ne oldu

DeepSeek, 21 Ağustos 2026'da API'si üzerinden deneysel bir çok modlu model
olan DeepSeek-V4-Flash-Vision-Exp'i yayımladı [1]. Model, DeepSeek'in 31
Temmuz'da açık kaynak olarak yayımladığı metin tabanlı V4-Flash-0731
modeline görsel anlama ekliyor ve o modelin metin performansını koruyor
[1][2]. Temmuz sürümünün aksine V4-Flash-Vision-Exp yalnızca DeepSeek'in
API'si üzerinden erişilebiliyor — DeepSeek'in kendi duyurusu modelin "açık
ağırlıklı olmadığını" açıkça belirtiyor [1]; Hugging Face'te modele ait
resmi bir DeepSeek deposu bulunmuyor.

DeepSeek, yeni modelin çok modlu ajan performansının, kendi ölçüt
altyapısında yaptığı değerlendirmelere göre Claude Opus 4.8'e "yakın"
olduğunu söylüyor [1]. The Decoder ve officechai'nin aktardığı DeepSeek'in
kendi ölçüt bazlı rakamlarına göre model, Opus 4.8'i bazı görevlerde geride
bırakıyor — Agents' Last Exam'de (27,3'e karşı 25,7) ve ZeroBench Pass@5'te
(35,0'a karşı 34,0) gibi — ancak NL2Repo adlı bir kod deposu görevi de dahil
olmak üzere diğer görevlerde yaklaşık 12 puana varan farkla geride kalıyor
[2][3]. DeepSeek bunu bağımsız bir değerlendirme olarak sunmuyor ve yayın
sırasında modele ait bağımsız bir değerlendirme sonucuna rastlanmadı.

The Next Web, DeepSeek'in karşılaştırmasıyla ilgili iki sorun bildirdi:
karşılaştırma, Anthropic'in daha yeni modeli Opus 5 yerine Opus 4.8'e karşı
yapılıyor ve DeepSeek'in kendi öncesi/sonrası tablosu, görsel özelliği
olmayan önceki modelini göremediği görseller içeren testlerde puanlamış
görünüyor — bu da görünürdeki artışı abartıyor olabilir [4].

## Neden önemli

DeepSeek, itibarını inşa eden açık ağırlık yaklaşımından bu sürümde
uzaklaşarak, zaten rekabetçi olan bir metin modelinin üzerine çok modlu
yetenek ekliyor ve bunu yalnızca API üzerinden sunuyor. Opus 4.8 ile yapılan
performans karşılaştırması DeepSeek'in kendi rakamlarına dayanıyor ve
şirketin kendi verilerine göre bile karışık sonuçlar veriyor; bağımsız
doğrulama henüz mevcut değil.
