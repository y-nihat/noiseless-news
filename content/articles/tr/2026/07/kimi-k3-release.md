---
title: Moonshot AI, Kimi K3'ü API ile yayınladı; model ağırlıklarını 27 Temmuz'a kadar bekletiyor
date: 2026-07-17
slug: kimi-k3-release
lang: tr
tldr: >
  Çinli yapay zeka laboratuvarı Moonshot, Kimi K3'ü 16 Temmuz 2026'da
  yayınladı ve API erişimini hemen açtı; modelin tüm ağırlıklarının 27
  Temmuz'da yayınlanması planlanıyor. Moonshot, modeli 1 milyon token bağlam
  penceresine sahip 2,8 trilyon parametreli bir Mixture-of-Experts modeli
  olarak tanımlıyor; parametre sayısı, mimari detaylar ve benchmark
  karşılaştırmaları şirketin kendi rakamları olup henüz bağımsız olarak
  doğrulanmadı.
sources:
  - name: Moonshot AI (Kimi)
    url: https://www.kimi.com/blog/kimi-k3
  - name: VentureBeat
    url: https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems
  - name: Axios
    url: https://www.axios.com/2026/07/17/china-ai-kimi-k3-open-source-anthropic-opus
  - name: Tom's Hardware
    url: https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-releases-2-8-trillion-parameter-kimi-k3
claims:
  - text: "Moonshot AI, Kimi K3'ü 16 Temmuz 2026'da yayınladı; API erişimi hemen sunuldu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Moonshot, modelin tüm ağırlıklarının 27 Temmuz 2026'da yayınlanacağını söylüyor; yani K3 şu an için indirilebilir açık ağırlıklı bir sürüm değil, yalnızca API üzerinden erişilebiliyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Moonshot, K3'ü token başına 896 uzmandan 16'sının etkin olduğu 2,8 trilyon parametreli bir Mixture-of-Experts modeli olarak tanımlıyor; bağlam penceresi 1 milyon token"
    type: capability
    verdict: vendor-claim
    evidence: [1, 4]
  - text: "Moonshot ve basın, ağırlıklar yayınlandığında K3'ün yayınlanmış en büyük açık ağırlıklı model olacağını öngörüyor ve modeli bazı rakip modellerle yakın veya önde gösteren dahili benchmark karşılaştırmalarına atıfta bulunuyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2, 4]
updated: []
---

## Ne oldu

Kimi model ailesinin arkasındaki Pekin merkezli laboratuvar Moonshot AI,
Kimi K3'ü 16 Temmuz 2026'da yayınladı ve API üzerinden erişimi hemen açtı
[1][2][3]. Modelin tüm ağırlıkları 27 Temmuz'da yayınlanacak; yani K3 şu an
için indirilebilir açık ağırlıklı bir sürüm olarak değil, yalnızca
Moonshot'ın barındırdığı API üzerinden erişilebiliyor [1][2].

Moonshot'ın kendi duyurusu K3'ü, token başına 896 uzmandan 16'sının etkin
olduğu 2,8 trilyon parametreli bir Mixture-of-Experts modeli olarak
tanımlıyor; bağlam penceresi 1 milyon token [1][4]. Şirket ve birçok yayın
organı, ağırlıklar kamuya açıldığında K3'ün yayınlanmış en büyük açık
ağırlıklı model olacağını öngörüyor ve modeli rakip öncü modellerle
rekabetçi konumda gösteren dahili benchmark karşılaştırmalarına atıfta
bulunuyor [1][2][4]. Bu parametre sayıları, mimari detaylar ve benchmark
sonuçlarının hepsi Moonshot'ın kendi materyallerine dayanıyor — henüz
bağımsız bir taraf bunları doğrulamadı, basın da şimdiye kadar şirketin
rakamlarını ayrıca test etmek yerine olduğu gibi aktarıyor.

## Neden önemli

K3, Moonshot'ın Kimi serisini sürdürerek bu yıl art arda gelen büyük Çin
kaynaklı açık ağırlıklı model yayınlarının en yenisi olarak geliyor.
Modelin pratik önemi — bağımsız yürütülen benchmark'larda rakiplerine karşı
tutup tutmayacağı ve "en büyük açık ağırlıklı model" iddiasının kamuya açık
indirilebilir ağırlıklarla karşılaştığında geçerliliğini koruyup
korumayacağı — 27 Temmuz'daki ağırlık yayınına kadar değerlendirilemez. O
zamana dek ölçek ve performans iddiaları Moonshot'ın kendi beyanı olarak
değerlendirilmelidir.
