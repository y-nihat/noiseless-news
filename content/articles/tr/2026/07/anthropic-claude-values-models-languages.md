---
title: Anthropic araştırması, Claude'un ifade ettiği değerlerin modele ve dile göre değiştiğini buldu
date: 2026-07-14
slug: anthropic-claude-values-models-languages
lang: tr
tldr: >
  Anthropic, 13 Temmuz 2026'da yayımladığı araştırmada 309.815 Claude.ai
  konuşmasını inceleyerek Claude'un ifade ettiği değerlerin hem model
  sürümüne hem de konuşma diline göre sistematik olarak değiştiğini buldu —
  örneğin en fazla sıcaklığı Hintçe'de, en fazla titizliği ise Rusça'da
  gösteriyor. Anthropic'in "Values in the Wild" çalışmasının devamı olan bu
  araştırma, binlerce tespit edilen değeri ölçülebilir dört eksene indirgiyor.
sources:
  - name: Anthropic News
    url: https://www.anthropic.com/research/claude-values-models-languages
claims:
  - text: "Anthropic, Claude'un ifade ettiği değerlerin modellere ve dillere göre nasıl değiştiğini ölçmek için 309.815 Claude.ai konuşmasını inceleyen bir araştırmayı 13 Temmuz 2026'da yayımladı"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Veri seti, üç model — Sonnet 4.6, Opus 4.6 ve Opus 4.7 — ile Claude.ai'de en çok kullanılan 20 dil arasında eşit şekilde örneklendi; model-dil çifti başına yaklaşık 5.000 konuşma olacak şekilde, Mayıs 2026'da iki haftalık bir sürede toplandı"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic, tespit ettiği değerleri dört eksene indirgedi — Saygı/Uyum'a karşı Temkin, Sıcaklık'a karşı Titizlik, Derinlik'e karşı Kısalık ve Açıksözlülük'e karşı Uygulama — bu eksenler birlikte Claude'un ifade ettiği değerlerdeki varyasyonun yaklaşık %15'ini açıklıyor"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Modele göre, Sonnet 4.6 saygı/uyum, sıcaklık ve kısalığa; Opus 4.6 titizlik, saygı/uyum ve kısalığa; Opus 4.7 ise temkin, titizlik, derinlik ve açıksözlülüğe eğilim gösterdi"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Dile göre, Claude en fazla sıcaklığı Hintçe'de, en fazla titizliği Rusça'da gösterdi; en fazla saygı/uyumu Arapça'da, en fazla temkini ise İngilizce'de sergiledi"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic, dile göre değişen bu farkı çözümlenmemiş bir soru olarak sunuyor: bir kısmı Claude'un kültürel konuşma normlarına uygun şekilde uyum sağlamasını yansıtıyor olabilir, bir kısmı ise dillere göre eşit yatırılmamış hizalama çalışmasındaki bir boşluğu yansıtıyor olabilir; araştırma bu ikisi arasında bir sonuca varmıyor"
    type: research
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Anthropic, 13 Temmuz 2026'da Claude'un ifade ettiği değerlerin model sürümüne ve konuşmanın yapıldığı dile göre nasıl değiştiğini ölçen bir araştırma yayımladı [1]. Bu, şirketin daha önceki "Values in the Wild" çalışmasının devamı niteliğinde ve kullanıcıların Claude'a öznel bir görev verdiği 309.815 Claude.ai konuşmasını inceliyor; üç model — Sonnet 4.6, Opus 4.6 ve Opus 4.7 — ile platformda en çok kullanılan 20 dil arasında eşit şekilde örneklenmiş, model-dil çifti başına yaklaşık 5.000 konuşma olmak üzere, Mayıs 2026'da iki haftalık bir sürede toplanmış [1].

Anthropic, bu konuşmalarda tespit ettiği değerleri ölçülebilir dört eksene indirgedi — Saygı/Uyum'a karşı Temkin, Sıcaklık'a karşı Titizlik, Derinlik'e karşı Kısalık ve Açıksözlülük'e karşı Uygulama — ve bu eksenler birlikte Claude'un ifade ettiği değerlerdeki varyasyonun yaklaşık %15'ini açıklıyor [1]. Modele göre, Sonnet 4.6 saygı/uyum, sıcaklık ve kısalığa; Opus 4.6 titizlik, saygı/uyum ve kısalığa; Opus 4.7 ise temkin, titizlik, derinlik ve açıksözlülüğe eğilim gösterdi [1]. Dile göre, Claude en fazla sıcaklığı Hintçe'de, en fazla titizliği Rusça'da gösterdi; en fazla saygı/uyumu Arapça'da, en fazla temkini ise İngilizce'de sergiledi [1].

## Neden önemli

Bu bulgunun pratik bir yanı var: aynı planı biri Hintçe biri Rusça olmak üzere inceletmesini isteyen iki kullanıcı, salt dil farkından dolayı istatistiksel olarak farklı kalibrasyonda yanıtlar alabiliyor — biri daha yumuşak, diğeri daha sert. Anthropic, bunun Claude'un kültürel bağlamı doğru okumasını mı yansıttığını, yoksa daha az yatırım yapılan dillerde modelin hizalama ve karakter eğitimindeki bir boşluğu mu yansıttığını çözümlemeden ortaya koyuyor [1]. Altta yatan konuşma verisi Mayıs 2026'ya ait; dolayısıyla anlatılan model davranışları o döneme ait bir kesit, Anthropic'in güncel model dizisi hakkında bir iddia değil.
