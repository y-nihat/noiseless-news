---
title: Cerebras, yapay zekâ çıkarımı için yeni raf ölçekli sistemi CS-4'ü tanıttı
date: 2026-08-18
published: 2026-08-19
slug: cerebras-cs4-inference-system
lang: tr
tldr: >
  Cerebras, 18 Ağustos 2026'da üç adet Wafer Scale Engine 3 "Turbo" işlemciden
  oluşan yeni raf ölçekli yapay zekâ çıkarım sistemi CS-4'ü tanıttı. Şirket,
  sistemin CS-3 modeline göre iki kata kadar, GPU tabanlı sistemlere göre ise
  çıkarım hızında 30 kata kadar daha hızlı olduğunu ve sevkiyatların bu
  çeyrekte başlayacağını açıkladı — bu rakamlar Cerebras'ın kendi iddiaları
  olup henüz bağımsız olarak doğrulanmadı.
sources:
  - name: Cerebras (şirket blogu)
    url: https://www.cerebras.ai/blog/introducing-cerebras-cs-4
  - name: Yahoo Finance
    url: https://finance.yahoo.com/technology/article/cerebras-says-latest-offering-is-fastest-ai-accelerator-in-the-industry-as-it-takes-aim-at-nvidia-000000090.html
claims:
  - text: "Cerebras, 18 Ağustos 2026'da yeni bir raf ölçekli yapay zekâ çıkarım sistemi olan CS-4'ü tanıttı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "CS-4, CS-3'te de kullanılan aynı WSE-3 çip neslinden üç 'Turbo' işlemciyi yeni bir raf ölçekli tasarımda birleştiriyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Cerebras, CS-4'ün GPU tabanlı sistemlere göre 30 kata kadar, CS-3'e göre ise iki kata kadar daha hızlı çıkarım sunduğunu ve CS-3'e göre watt başına 10 kata kadar daha fazla verim sağladığını açıklıyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "Cerebras, ilk CS-4 sevkiyatlarının bu çeyrekte (2026 3. çeyrek) başlayacağını açıklıyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Cerebras, 18 Ağustos 2026'da düzenlediği SUPERNOVA etkinliğinde yeni raf
ölçekli yapay zekâ çıkarım sistemi CS-4'ü tanıttı [1][2]. Sistem, CS-3'te
de kullanılan aynı WSE-3 çip neslinden üç "WSE-3 Turbo" işlemciyi,
şirketin "Cerebras Nexus" platformunun ilk üyesi olarak nitelendirdiği yeni
bir raf ölçekli tasarımda bir araya getiriyor [1].

Cerebras, CS-4'ün CS-3'e göre iki kata kadar hızlı olduğunu ve GPU tabanlı
sistemlere kıyasla çıkarımda 30 kata kadar hız sunduğunu, CS-3'e göre watt
başına 10 kata kadar daha fazla verim sağladığını açıklıyor [1][2]. Bunlar
şirketin kendi ölçüm rakamları; henüz hiçbir bağımsız değerlendirme kuruluşu
CS-4'e özgü bir ölçüm yayımlayıp bu rakamları doğrulamadı veya çürütmedi.
Cerebras, ilk CS-4 sevkiyatlarının bu çeyrek içinde başlayacağını
belirtiyor [1].

## Neden önemli

Cerebras, yapay zekâ çıkarımına — modelleri eğitmek değil, eğitilmiş
modelleri çalıştırmaya — özel çipler üretiyor ve CS-4'ü hız ve güç
verimliliğinde Nvidia'nın GPU tabanlı sistemlerine doğrudan bir meydan
okuma olarak konumlandırıyor. İddia edilen sıçrama, Cerebras'ın CS-3'te de
kullandığı aynı WSE-3 çip neslinin üzerine kuruluyor; dolayısıyla esas
olarak yeni bir çipten değil, sistem ve raf düzeyindeki mühendislikten
kaynaklanıyor — şirketin kendi materyallerinin desteklediği ancak
performans iddialarının henüz bağımsız bir doğrulaması bulunmayan bir
ayrım.
