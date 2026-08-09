---
title: Anthropic, Fable 5'in biyoloji güvenlik sınıflandırıcısını yanlış engellemeleri azaltmak için yeniden yazdı
date: 2026-08-07
slug: anthropic-fable-5-biology-safeguards-update
lang: tr
tldr: >
  Anthropic, 7 Ağustos 2026'da Claude Fable 5'teki biyoloji sorularını
  yöneten güvenlik sınıflandırıcısını yeniden yazdığını, bunun kendi
  testlerinde daha zayıf bir modele yönlendirmeleri (fallback) yaklaşık
  %85 azalttığını duyurdu. Tahlil sonuçları ve semptomlar gibi günlük
  sorular artık daha rahat yanıtlanırken, viroloji, toksikoloji ve
  moleküler tasarım sorguları hâlâ engelleniyor ve Opus 5'e
  yönlendiriliyor.
sources:
  - name: Anthropic News
    url: https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards
  - name: The Decoder
    url: https://the-decoder.com/anthropic-loosens-fable-5s-biology-restrictions-but-keeps-the-guardrails-on-for-virology-and-toxicology/
claims:
  - text: "Anthropic, Claude Fable 5'in biyoloji güvenlik sınıflandırıcısını 7 Ağustos 2026'da güncelledi"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic, güncellemenin kendi testlerinde ürün yüzeyleri genelinde biyoloji kaynaklı yönlendirmeleri (daha zayıf bir modele otomatik aktarım) yaklaşık %85 azalttığını; platform bazında düşüşün Claude.ai'de yaklaşık %67, Cowork'te %55, Claude Code'da %17 ve Claude Platform API'sinde %7 olduğunu bildiriyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Fable 5, viroloji, toksikoloji ve moleküler tasarım içeren sorguları hâlâ engelliyor ve Opus 5'e yönlendiriyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Anthropic, sınıflandırıcının kural setini ('anayasasını') yeniden yazdı, iç ve dış uzmanlardan geri bildirim topladı ve sınıflandırıcıyı güncellenmiş eğitim verileriyle yeniden eğitti"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic, hâlâ kısıtlı olan çift kullanımlı alanlarda çalışacak onaylı araştırmacılar için bir 'güvenilir erişim yolu' geliştirdiğini, ancak bir lansman tarihi belirlemediğini söylüyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Anthropic, 7 Ağustos 2026'da Claude Fable 5'in hangi biyoloji sorularını
doğrudan yanıtlayabileceğine ve hangilerinin daha zayıf Opus 5 modeline
yönlendirileceğine karar veren güvenlik sınıflandırıcısını yeniden
yazdığını duyurdu [1]. Anthropic'in kendi testlerinde, bu değişiklik tüm
ürün yüzeyleri genelinde bu yönlendirmeleri yaklaşık %85 azalttı; düşüş
en çok Claude.ai'de (yaklaşık %67 daha az yönlendirme) ve Cowork'te
(yaklaşık %55) görülürken, Claude Code'da (yaklaşık %17) ve Claude
Platform API'sinde (yaklaşık %7) çok daha küçük kaldı [1]. Bunlar
Anthropic'in kendi bildirdiği iç rakamlar olup bağımsız olarak
doğrulanmış bir kıyaslama değildir.

Fable 5, model bazı biyolojik silahlarla ilgili görevlerde çift kullanımlı
(dual-use) fayda sağlayabildiği için varsayılan olarak çoğu biyoloji
sorgusu engellenmiş şekilde piyasaya sürülmüştü; Anthropic, kendi
testlerinin modelin potansiyel bir biyolojik silah geliştiricisine
"başka hiçbir yerde bulamayacağı" yetenekler sunabildiğini gösterdiğini
belirtmişti [1][2]. Güncelleme, önceden aynı geniş filtre tarafından
yakalanan gündelik ve zararsız-ama-profesyonel sorulara — tahlil
sonuçlarını okumak, semptomları anlamak, genel biyoloji eğitimi ve sağlık
çalışanlarının klinik sorularına — yöneliktir [1]. Anthropic, güvenlik
kapsamına giren ve girmeyen içerik arasında daha keskin bir çizgi
çizmek için sınıflandırıcının kural setini yeniden yazdığını, iç ve dış
biyoloji ve biyogüvenlik uzmanlarından geri bildirim topladığını ve
sınıflandırıcıyı yeni kurallardan oluşturulan verilerle yeniden
eğittiğini söylüyor [1].

Viroloji, toksikoloji ve moleküler tasarım hâlâ engelli olup Opus 5'e
yönlendirilmeye devam ediyor; dolayısıyla güncelleme, modeli profesyonel
çift kullanımlı araştırma veya ilaç geliştirme için açmıyor [1][2].
Anthropic, bu kısıtlı alanlarda çalışacak onaylı araştırmacılar için bir
"güvenilir erişim yolu" inşa ettiğini ancak henüz bir lansman tarihi
belirlemediğini söylüyor [1].

## Neden önemli

Fable 5'in genel biyoloji kısıtlamaları, zararsız sağlık ve bilim
sorularını soran sıradan kullanıcılar için görünür bir sürtüşme
kaynağı haline gelmişti; buna karşın Anthropic'in lansmanda öne sürdüğü
altta yatan çift kullanım riski — aynı model yeteneklerinin hem meşru
biyoloji araştırmalarına hem de biyolojik silah geliştirmeye yardımcı
olabilmesi — hâlâ engelli tutulan belirli alanlar için ortadan kalkmış
değil. Yönlendirme mekanizmasının kendisi kullanıcılar için büyük ölçüde
görünmezdir; bir sorgunun sessizce daha zayıf bir modele aktarıldığı
kullanıcıya bildirilmez, dolayısıyla %85 rakamı, kullanıcıların bağımsız
olarak denetleyemeyeceği bir sisteme yapılan değişikliğin Anthropic'in
kendi anlatımıdır.
