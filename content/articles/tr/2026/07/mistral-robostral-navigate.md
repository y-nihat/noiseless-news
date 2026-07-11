---
title: Mistral, ilk robotik modeli Robostral Navigate'i tek kameralı robot navigasyonu için yayınladı
date: 2026-07-08
slug: mistral-robostral-navigate
lang: tr
tldr: >
  Mistral AI, 8 Temmuz 2026'da Robostral Navigate'i yayınladı; bu 8 milyar
  parametreli model, derinlik sensörü veya LiDAR olmadan, yalnızca tek bir RGB
  kamera ve düz metin bir talimatla bir robotu yönlendirebiliyor. Mistral,
  R2R-CE navigasyon benchmark'ında %79,4/%76,6 başarı oranı (görülmüş/görülmemiş
  ortamlar) bildiriyor; bu rakamlar şirketin kendi beyanı olup henüz bağımsız
  olarak doğrulanmadı.
sources:
  - name: Mistral AI News
    url: https://mistral.ai/news/robostral-navigate
  - name: Bloomberg
    url: https://www.bloomberg.com/news/articles/2026-07-08/mistral-robostral-navigate
  - name: TestingCatalog
    url: https://www.testingcatalog.com/mistral-robostral-navigate/
claims:
  - text: "Mistral, 8 Temmuz 2026'da Robostral Navigate'i yayınladı; 8 milyar parametreli bu model, RGB görüntüler ve düz metin bir talimat alarak, derinlik sensörü veya LiDAR gerektirmeden tek bir kamerayla bir robotu bir ortamda hareket ettiriyor; tekerlekli, bacaklı ve uçan robotlarda çalışıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "R2R-CE navigasyon benchmark'ında Mistral, görülmüş ortamlarda %79,4, görülmemiş ortamlarda %76,6 başarı oranı bildiriyor; bunun en iyi tek kameralı yaklaşımı 9,7 puan, derinlik veya çoklu kamera kullanan en iyi sistemi ise 4,5 puan geçtiğini iddia ediyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Model, 6.000 sahne genelinde yaklaşık 400.000 simüle edilmiş yörünge üzerinde eğitildi; Mistral, bir önek önbellekleme (prefix-caching) tekniğinin eğitim token sayısını 22 kat azalttığını ve eğitim süresini aylardan günlere indirdiğini söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Bu, Mistral'in ilk robotik modeli"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
updated: []
---

## Ne oldu

Mistral AI, 8 Temmuz 2026'da Robostral Navigate'i yayınladı ve bunu şirketin
somutlaşmış (embodied) navigasyon için inşa ettiği ilk model olarak tanımladı
[1][2][3]. 8 milyar parametreli model, bir RGB görüntü akışı ile düz metin bir
talimat alarak, derinlik sensörü veya LiDAR olmadan tek bir kamerayla bir robotu
bir ortamda yönlendiriyor. Hedefin kamera karesindeki konumunu tahmin ederek
çalışıyor; hedef kare dışına çıktığında ise yerel hareket komutlarına geçiyor.
Mistral, modelin tekerlekli, bacaklı ve uçan robotlar genelinde çalıştığını
belirtiyor [1].

R2R-CE navigasyon benchmark'ında Mistral, modelin eğitim sırasında gördüğü
ortamlarda %79,4, hiç görmediği ortamlarda ise %76,6 başarı oranına ulaştığını
bildiriyor; şirkete göre bu, önceki en iyi tek kameralı sistemi 9,7 puan,
derinlik veya çoklu kamera kullanan en iyi sistemi ise 4,5 puan geçiyor [1]. Bu
rakamlar Mistral'in kendi duyurusundan geliyor ve henüz bağımsız olarak
doğrulanmadı — R2R-CE, iç mekân ortamları üzerine kurulu, gerçek ve yerleşik bir
benchmark; bu benchmark'ta yayımlanmış bağımsız sonuçlar şu an %65 civarında,
dolayısıyla Mistral'in iddia ettiği sıçrama büyük ama aynı hafta içinde
duyurulan bir üretici rakamı için imkânsız değil. Mistral ayrıca modelin 6.000
sahne genelinde yaklaşık 400.000 simüle edilmiş yörünge üzerinde eğitildiğini ve
bir önek önbellekleme tekniğinin eğitim token sayısını 22 kat azaltarak eğitim
süresini aylardan günlere indirdiğini söylüyor [1]. Her iki rakam da şirketin
kendi beyanı olup bağımsız biri tarafından doğrulanmadı.

## Neden önemli

Robot navigasyon sistemleri genellikle kameraların yanında derinlik sensörü
veya LiDAR'a dayanıyordu; Mistral'in iddiası, tek bir RGB kameranın, dile dayalı
bir modelle birleştiğinde bu donanımla eşleşebileceği veya onu geçebileceği —
bu da robotlara navigasyon dağıtımının maliyetini ve karmaşıklığını
düşürebilir. Kullanılan benchmark olan R2R-CE yalnızca iç mekân ortamlarını
test ediyor; dolayısıyla Mistral'in modelin dış mekân ve hava robotlarına da
genelleştiği iddiasının eşleşen bağımsız bir benchmark'ı henüz yok. Bildirilen
rakamlar bağımsız biri tarafından yeniden üretilene kadar, yetenek rakamları
Mistral'in kendi beyanı olarak okunmalı.
