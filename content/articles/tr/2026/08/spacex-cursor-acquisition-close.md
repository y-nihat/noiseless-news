---
title: SpaceX, yapay zeka destekli kodlama girişimi Cursor'ı 60 milyar dolara satın aldı
date: 2026-08-14
published: 2026-08-15
slug: spacex-cursor-acquisition-close
lang: tr
tldr: >
  SpaceX, Cursor'ın arkasındaki şirket Anysphere'i tamamen hisse senedi
  karşılığında satın alma işlemini 14 Ağustos'ta tamamladı; bir SEC
  bildirimine göre bu, Anysphere için 60 milyar dolarlık zımni özsermaye
  değeri anlamına geliyor. Anlaşma, SpaceX'in Nisan'da aldığı opsiyonla
  başlayıp Haziran'da, kendi halka arzından günler sonra kullanılmasıyla
  ilerledi. Cursor artık SpaceX'in tamamına sahip olduğu bir yan kuruluş
  ve Colossus kümesi dahil SpaceX'in GPU kapasitesine erişimi olduğunu
  söylüyor -- bu da en çok kullanılan yapay zeka kodlama araçlarından
  birine, işlem gücüne erişimin yapay zeka laboratuvarları için bağlayıcı
  bir kısıt olduğu bir dönemde kendine ait bir donanım kaynağı sağlıyor.
sources:
  - name: Cursor
    url: https://cursor.com/blog/joining-spacex
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/15/spacex-officially-closes-its-cursor-acquisition/
  - name: CNBC
    url: https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html
  - name: SEC bildirimi (StockTitan üzerinden)
    url: https://www.stocktitan.net/sec-filings/SPCX/8-k-space-exploration-technologies-corp-reports-material-event-c660405680ba.html
claims:
  - text: "SpaceX'in, Cursor'ı geliştiren Anysphere'i satın alması 14 Ağustos 2026'da yürürlüğe girdi; SpaceX'in yan kuruluşu X67 Inc., Anysphere ile birleşti ve Anysphere artık SpaceX'in tamamına sahip olduğu bir yan kuruluş"
    type: announcement
    verdict: confirmed
    evidence: [1, 4]
  - text: "Anlaşma tamamen hisse senedi karşılığında yapıldı: SpaceX, Anysphere'in mevcut adi ve imtiyazlı hisselerinin yanı sıra hak kazanılmış RSU'lar için, kapanıştan önceki yedi işlem gününün hacim ağırlıklı ortalama fiyatıyla belirlenen bir fiyattan yaklaşık 391 milyon A Sınıfı hisse ihraç etti; bu da Anysphere için 60,0 milyar dolarlık zımni özsermaye değerine işaret ediyor"
    type: business
    verdict: confirmed
    evidence: [4]
  - text: "SpaceX, Nisan 2026'da Anysphere'i satın alma opsiyonu edindi, ardından bu opsiyonu kullanarak satın almayı, kendi halka arzından dört gün sonra, 16 Haziran 2026'da duyurdu"
    type: business
    verdict: confirmed
    evidence: [2, 3]
  - text: "Cursor, SpaceX'in Colossus GPU kümesi dahil olmak üzere bilgi işlem altyapısına artık erişimi olduğunu ve bunun kendisine dünyanın en büyük GPU filosuna erişim sağladığını söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
follows: null
---

## Ne oldu

SpaceX'in, yapay zeka destekli kodlama aracı Cursor'ın arkasındaki şirket
Anysphere'i satın alması, bir SpaceX düzenleyici bildirimine göre 14
Ağustos'ta yürürlüğe girdi. Anlaşma tamamen hisse senedi karşılığında
yapılan bir birleşme şeklinde yapılandırıldı: SpaceX'in yan kuruluşu X67
Inc., Anysphere ile birleşti ve Anysphere artık SpaceX'in tamamına sahip
olduğu bir yan kuruluş. SpaceX, Anysphere'in mevcut hisselerini ve hak
kazanılmış özkaynak ödüllerini karşılamak için, kapanıştan önceki yedi
günün SpaceX hisse fiyatı ortalamasına göre fiyatlanan yaklaşık 391 milyon
A Sınıfı hisse ihraç etti -- bu da Anysphere için 60,0 milyar dolarlık
zımni özsermaye değerine işaret ediyor; hak kazanılmamış opsiyonlar ve
RSU'lar için ayrılan ek hisseler bunun dışında.

İşlem, SpaceX'in Anysphere'i satın alma opsiyonu edindiği Nisan 2026'ya ve
bu opsiyonu kullanarak anlaşmayı kamuoyuna duyurduğu, kendi halka arzından
dört gün sonrasına denk gelen 16 Haziran'a dayanıyor. Cursor, kapanışı bir
blog yazısıyla doğruladı ve SpaceX'in bilgi işlem altyapısına -- Colossus
GPU kümesi dahil -- artık erişimi olduğunu, bunun da kendi ifadesiyle
dünyanın en büyük GPU filosuna erişim sağladığını belirtti. Cursor, aynı
ürün odağıyla çalışmaya devam edeceğini söylüyor.

## Neden önemli

Anlaşma, Cursor'ın kendi ifadesiyle on binlerce işletme tarafından
kullanılan, en yaygın kullanılan yapay zeka kodlama araçlarından birini
SpaceX'in bilgi işlem yatırımının içine katıyor ve Anysphere'e, eğitim ve
çıkarım donanımına erişimin yapay zeka laboratuvarları için bağlayıcı bir
kısıt olduğu bir dönemde kendine ait bir GPU kaynağı sağlıyor. Bu adım
aynı zamanda SpaceX'in roketler ve uyduların ötesine, yapay zeka
ürünlerine doğru genişlemesini de sürdürüyor; şirketin yapay zeka
çalışmaları, daha önceki xAI birleşmesinin ardından artık SpaceX çatısı
altında yürütülüyor.
