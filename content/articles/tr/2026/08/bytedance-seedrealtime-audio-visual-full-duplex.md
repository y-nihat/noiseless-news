---
title: "ByteDance'in Seed ekibi, sesli-görsel tam çift yönlü bir model olan SeedRealtime'ı yayımladı"
date: 2026-08-05
published: 2026-08-10
slug: bytedance-seedrealtime-audio-visual-full-duplex
lang: tr
tldr: >
  ByteDance'in Seed ekibi, 5 Ağustos 2026'da, ses, görüntü ve metin
  akışlarını birlikte işleyerek gerçek zamanlı olarak izleyip dinleyip
  konuşabilen, sesli-görsel tam çift yönlü (full-duplex) bir model olan
  SeedRealtime'ı yayımladı; model Doubao uygulaması üzerinden kullanıma
  sunuluyor. Bu, Seed'in Nisan 2026'daki yalnızca sesli tam çift yönlü
  modeline görüntü ekleyerek genişletilmiş hali. ByteDance, kendi insan
  değerlendirmesinin, modelin eski art arda işleyen (cascaded) sistemlere
  kıyasla konuşma akışındaki tuhaf duraksamaları azalttığını gösterdiğini
  söylüyor; ancak bu iddianın bağımsız bir ölçütü henüz yok.
sources:
  - name: ByteDance Seed
    url: https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction
claims:
  - text: "ByteDance'in Seed ekibi, 5 Ağustos 2026'da, ses, görüntü ve metin akışlarını doğrudan birleştirerek gerçek zamanlı ve proaktif konuşma etkileşimini mümkün kılan, Doubao uygulaması üzerinden kullanıma sunulan sesli-görsel tam çift yönlü bir model olan SeedRealtime'ı yayımladı; bu model, Seed'in Nisan 2026'da yayımladığı yalnızca sesli tam çift yönlü modeli ('Seed Full-Duplex Speech LLM') görüntü ekleyerek genişletiyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "ByteDance, SeedRealtime'ın konuşmadaki belirsizlikleri çözmek için görsel bağlamı kullandığını ve kendi insan değerlendirmesine göre, eski art arda işleyen (cascaded) sesli asistan sistemlerine kıyasla tuhaf duraksama ve sözü kesme sorunlarını önemli ölçüde azalttığını söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

ByteDance'in Seed ekibi, 5 Ağustos 2026'da, ses, görüntü ve metin
akışlarını birlikte alıp aynı anda izleyip dinleyip konuşabilen tek bir
sistem olan sesli-görsel tam çift yönlü bir model olan SeedRealtime'ı
yayımladığını duyurdu; model, bir isteği işleyip sırayla yanıt vermek
yerine bunu gerçek zamanlı yapıyor [1]. Model, Doubao uygulaması üzerinden
kullanıma sunuluyor [1]. Bu yayın, Seed ekibinin Nisan 2026'da yayımladığı
yalnızca sesli tam çift yönlü modeli "Seed Full-Duplex Speech LLM"i
genişletiyor — SeedRealtime, aynı gerçek zamanlı etkileşim yaklaşımına
görüntüyü ekliyor [1].

ByteDance, modelin konuşmacının söylediklerindeki belirsizlikleri çözmek
için görsel bağlamı kullandığını ve kendi insan değerlendirmesinin,
SeedRealtime'ın; konuşmayı metne çevirme, akıl yürütme ve metni sese
çevirmeyi ayrı aşamalar olarak işleyen eski, art arda işleyen (cascaded)
sesli asistan sistemlerine yaygın olan tuhaf duraksama ve sözü kesme
sorunlarını önemli ölçüde azalttığını gösterdiğini söylüyor [1]. Bu
rakamlar yalnızca ByteDance'in kendi değerlendirmesinden geliyor; yetenek
iddialarının bağımsız bir ölçütü veya üçüncü taraf tekrarı henüz
yayımlanmadı.

## Neden önemli

SeedRealtime, bir araştırma önizlemesi değil, kullanıcılara sunulan gerçek
bir ürün ve Seed'in yalnızca sesli tam çift yönlü etkileşimden dört ay
içinde birleşik sesli-görsel bir sürüme geçtiğini gösteriyor. Satıcı
tarafından bildirilen her insan değerlendirmesinde olduğu gibi, duraksama
iyileştirme rakamları da ByteDance'in kendi seçtiği bir karşılaştırmaya
dayanıyor. Bağımsız bir doğrulama henüz mevcut değil.
