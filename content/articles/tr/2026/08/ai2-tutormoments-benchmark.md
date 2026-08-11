---
title: Ai2, yapay zekâ öğretmenlerinin ne zaman yönlendirmesi ne zaman zorlaması gerektiğini ölçen TutorMoments'ı yayınladı
date: 2026-08-07
slug: ai2-tutormoments-benchmark
lang: tr
tldr: >
  Allen Institute for AI (Ai2), 7 Ağustos 2026'da, dil modellerinin zorlanan
  bir öğrenciyi ne zaman desteklemesi, ne zaman daha derin düşünmeye
  yönlendirmesi gerektiğini bilip bilmediğini test eden TutorMoments
  kıyaslamasını yayınladı. Kıyaslama, 2-7. sınıf öğrencilerini kapsayan
  462 gerçek ABD matematik özel ders transkriptinden öğretmenlerin
  işaretlediği 1.500'den fazla ana anı içeriyor. Ai2, yedi modeli test
  ettiğinde tümünün insan öğretmen temel çizgisine kıyasla aşırı
  yardımcı olma eğiliminde olduğunu ve nadiren zorluk çıkardığını buldu;
  yönlendirme puanında Gemini 2.5 Pro, zorluk puanında ise Claude Opus 4.8
  en yüksek skoru aldı.
sources:
  - name: Allen Institute for AI (Ai2)
    url: https://allenai.org/blog/tutormoments
claims:
  - text: "Ai2, 7 Ağustos 2026'da, 2-7. sınıfları kapsayan 462 anonimleştirilmiş gerçek ABD matematik özel ders transkriptinde öğretmenlerin belirlediği 1.500'den fazla ana öğrenme anından oluşturulan TutorMoments değerlendirme çerçevesini yayınladı"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Ai2, bu anlardan 520'sinde -- yarısı yönlendirme (scaffolding) gerektiren, yarısı daha fazla zorluk gerektiren anlar olacak şekilde -- yedi modeli (Gemini 2.5 Pro, Gemini 3.5 Flash, Claude Opus 4.8, Claude Sonnet 4.6, GPT 5.5, GPT 5.4 mini ve DeepSeek V4 Pro) özel ders veren olarak test etti"
    type: research
    verdict: vendor-claim
    evidence: [1]
  - text: "Uygun yönlendirme puanında (0-1 ölçeği) Gemini 2.5 Pro değerlendirme farkındalıklı bir istemle 0,896 ile en yüksek, GPT 5.4 mini ise sade bir istemle 0,181 ile en düşük skoru aldı; insan öğretmen temel çizgisi 0,458'di. Uygun zorluk puanında Claude Opus 4.8 0,831 ile en yüksek, GPT 5.4 mini 0,023 ile en düşük skoru aldı; insan temel çizgisi 0,182'ydi"
    type: research
    verdict: vendor-claim
    evidence: [1]
  - text: "Ai2'nin genel bulgusu, modellerin aşırı destek vererek fazla yardımcı olma eğiliminde olduğu ve öğrencileri nadiren daha derin düşünmeye ittiği yönünde; ödünleşimi açıkça belirten istemler her modelin skorunu iyileştirse de insan öğretmenlere kıyasla bir fark kalıyor"
    type: research
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

Allen Institute for AI (Ai2), 7 Ağustos 2026'da, dil modellerinin
zorlanan bir öğrenciye ne zaman yardım edeceğini, ne zaman geri durup
öğrencinin bir problemi kendi başına çözmesine izin vereceğini bilip
bilmediğini ölçen bir kıyaslama olan TutorMoments'ı yayınladı [1].
Kıyaslama, deneyimli matematik öğretmenlerinin 2-7. sınıf öğrencilerine
yönelik 462 anonimleştirilmiş gerçek ABD özel ders transkriptinde
işaretlediği 1.500'den fazla anı temel alıyor [1].

Ai2, yedi modeli -- Gemini 2.5 Pro, Gemini 3.5 Flash, Claude Opus 4.8,
Claude Sonnet 4.6, GPT 5.5, GPT 5.4 mini ve DeepSeek V4 Pro -- öğretmenlerin
işaretlediği 520 anın yarısı yönlendirme gerektiren, yarısı öğrenciyi
daha derin düşünmeye itmeyi gerektiren anlar olacak şekilde özel ders
veren olarak test etti [1]. 0-1 ölçeğindeki yönlendirme puanında Gemini
2.5 Pro, ödünleşimi açıkça belirten bir istemle 0,896 ile en yüksek,
GPT 5.4 mini ise sade bir istemle 0,181 ile en düşük skoru aldı; insan
öğretmen temel çizgisi 0,458 idi. Zorluk puanında Claude Opus 4.8 0,831
ile en yüksek, GPT 5.4 mini 0,023 ile en düşük skoru aldı; insan temel
çizgisi 0,182 idi [1]. Bu rakamlar Ai2'nin 7 Ağustos yazısından doğrudan
alınan kendi bildirdiği sonuçlar; henüz hiçbir bağımsız kaynak bu
sonuçları yeniden üretmedi veya raporlamadı.

Ai2'nin ana bulgusu: test edilen tüm modeller, öğrencileri kendi
başlarına düşünmeye itmek yerine aşırı destek vererek "fazla yardımcı
olma" eğiliminde. Modellere yönlendirme-zorluk ödünleşimini açıkça
hatırlatan istemler her modelin skorunu yükseltti, ancak insan
öğretmenlerin uyarlanabilir yargısına kıyasla bir fark kaldı [1].

## Neden önemli

Yapay zekâ destekli özel ders araçları sınıflarda yaygınlaştıkça, bu
bulgu bugünün önde gelen modellerinin -- öğrenmenin merkezinde yer alan
verimli zorlanmaya izin vermek yerine -- öğrencileri gereğinden fazla
desteklemeye eğilimli olduğuna dair somut, veriye dayalı bir işaret
sunuyor. Sonuçlar Ai2'nin kendi sonuçları olup dışarıdan bir
değerlendirici tarafından yeniden üretilmedi; ancak çerçevenin
puanlanmış gerçek transkriptleri yayınlaması, dış araştırmacılara
rakamları denetleme imkânı veriyor.
