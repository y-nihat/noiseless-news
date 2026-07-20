---
title: Microsoft, AMD çipleri üzerine kurulu üç yeni Azure sanal makine ailesini duyurdu
date: 2026-07-20
slug: microsoft-azure-amd-helios-vms
lang: tr
tldr: >
  Microsoft, 20 Temmuz 2026'da AMD donanımı üzerine kurulu üç yeni Azure
  sanal makine (VM) ailesi geleceğini açıkladı: veri ve yapay zekâ iş
  yükleri için HDv2, çip tasarımı ve teknik hesaplama için HXv2, ve yapay
  zekâ çıkarımı için ND MI455X v7 — sonuncusu AMD'nin henüz sevkiyata
  başlamamış "Helios" raf ölçekli platformu üzerine kurulu. AMD da kendi
  duyurusunda aynı ortaklığı doğruladı. Üç VM ailesinden hiçbiri henüz
  müşterilere açık değil; Microsoft ve AMD ikisi de bunu AMD donanımının
  2026'nın ikinci yarısında sevk edilmesine bağlıyor — bazı analistlerin
  kamuoyu önünde sorguladığı, AMD'nin ise kamuoyu önünde savunduğu bir
  takvim.
sources:
  - name: Microsoft Source (resmi blog)
    url: https://blogs.microsoft.com/blog/2026/07/20/microsoft-expands-azure-ai-and-hpc-infrastructure-with-amd/
  - name: AMD Newsroom
    url: https://newsroom.amd.com/news/microsoft-azure-ai-infrastructure/
  - name: Tom's Hardware
    url: https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-will-deploy-amds-helios-rack-scale-ai-accelerator-at-scale-on-azure-radeon-instinct-mi455x-and-epyc-venice-power-will-be-available-through-redmonds-cloud-infrastructure
claims:
  - text: "20 Temmuz 2026'da Microsoft, AMD donanımı üzerinde çalışacak üç yeni Azure VM ailesini duyurdu: HDv2 (veri işleme ve yapay zekâ iş yükleri, yaklaşık 500 fiziksel 6. nesil AMD EPYC çekirdeği, 4TB RAM, 32TB yerel NVMe depolama, 400Gb Azure Boost ağı), HXv2 (elektronik tasarım otomasyonu ve teknik hesaplama, 5GHz üzeri hızda 176 AMD 6. nesil EPYC çekirdeği, 4TB'a kadar RAM, 800Gb InfiniBand), ve ND MI455X v7 (yapay zekâ çıkarımı, AMD'nin Helios raf ölçekli platformu üzerine kurulu)"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "AMD'nin Helios platformu, AMD Instinct MI455X GPU'larını AMD'nin yakında çıkacak EPYC 'Venice' CPU'larıyla eşliyor; AMD'nin kendi duyurusu, Microsoft dahil müşterilere sevkiyatın 2026'nın ikinci yarısında başlayacağını doğruluyor"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "Üç VM ailesinden hiçbiri henüz Azure müşterilerine açık değil — fiyatlandırma veya bölge kullanılabilirliği yayınlanmadı; Microsoft ve AMD ikisi de bunu AMD donanımının 2026'nın ikinci yarısında sevk edilmesine bağlıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Duyuru, mevcut bir Microsoft-AMD iş birliği üzerine kuruluyor: AMD 3D V-Cache teknolojisini kullanan Azure HX serisi VM'ler ilk olarak 2023'te AMD ortaklığıyla piyasaya sürülmüştü"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Microsoft, 20 Temmuz 2026'da Azure'ın yapay zekâ ve yüksek performanslı
hesaplama altyapısını AMD donanımı üzerine kurulu üç yeni sanal makine
ailesiyle genişlettiğini açıkladı [1]. HDv2, veri işleme ve yapay zekâ iş
yüklerini hedefliyor; her örnekte yaklaşık 500 fiziksel 6. nesil AMD EPYC
çekirdeği, 4 terabayt RAM, 32 terabayt yerel NVMe depolama ve 400Gb Azure
Boost ağı bulunuyor [1]. HXv2, elektronik tasarım otomasyonu ve diğer
teknik hesaplama iş yüklerini hedefliyor; 5GHz üzerinde saat hızına sahip
176 AMD 6. nesil EPYC çekirdeği, 4 terabayta kadar RAM ve 800Gb InfiniBand
ağı sunuyor [1]. ND MI455X v7 ise yapay zekâ çıkarımı için AMD'nin Instinct
MI455X GPU'larını yakında çıkacak EPYC "Venice" CPU'larıyla birleştiren
"Helios" raf ölçekli platformu üzerine kurulu [1].

AMD aynı gün, ortaklığı doğrulayan ve Helios tabanlı sevkiyatların
Microsoft dahil müşterilere 2026'nın ikinci yarısında başlayacağını
belirten eşleşen bir duyuru yayımladı [2]. Tom's Hardware, CNBC,
SiliconANGLE ve StorageReview dahil bağımsız yayın organları, aynı gün
eşleşen teknik özelliklerle haberi işledi [3]. Hiçbir şirket üç VM
ailesinden herhangi biri için fiyatlandırma veya bölge kullanılabilirlik
tarihi yayımlamadı; ikisi de genel kullanılabilirliği AMD'nin 2026'nın
ikinci yarısı sevkiyat takvimine bağlıyor [1][2]. Microsoft, haberi
Azure'ın mevcut AMD iş birliğinin bir uzantısı olarak sunuyor; Azure'ın
HX serisi VM'lerinin ilk olarak 2023'te AMD ile ortaklık içinde, AMD'nin
3D V-Cache teknolojisini kullanarak piyasaya sürüldüğünü belirtiyor [1].

Bu ikinci yarı 2026 sevkiyat takvimi kamuoyu önünde tartışmaya yol açtı:
Şubat 2026'da yayımlanan bir rapor, MI455X'in seri üretiminin 2027'ye
kayıp kaymayacağını sorguladı; AMD'nin yazılım liderliği bunu o dönem
kamuoyu önünde reddederek Helios'un 2026'nın ikinci yarısı için
takviminde kaldığını söyledi [3].

## Neden önemli

Bu, Microsoft'un Azure için çoklu tedarikçi çip stratejisinin somut bir
genişlemesi; mevcut Nvidia tabanlı sunumların yanına AMD tabanlı çıkarım
ve teknik hesaplama kapasitesi ekliyor — ne kadar yapay zekâ hesaplama
kapasitesinin ve kaç tedarikçiden geleceği açısından önemli. Üç VM
ailesinden hiçbiri henüz sağlanamadığından, pratik etki AMD'nin 2026'nın
ikinci yarısı sevkiyat takviminin tutup tutmayacağına bağlı.
