---
title: OpenAI, Broadcom ile geliştirdiği Jalapeño çipi için ilk kıyaslama sonuçlarını yayımladı
date: 2026-08-25
slug: openai-jalapeno-chip-benchmarks
lang: tr
tldr: >
  OpenAI, 25 Ağustos 2026'da Broadcom ile birlikte geliştirdiği ve Haziran
  ayında tanıtılan özel yapay zekâ çıkarım çipi Jalapeño için ilk performans
  sonuçlarını yayımladı. OpenAI, çipin Nvidia'nın mevcut Blackwell nesli
  çiplerine göre watt başına 1,5-1,9 kat daha fazla verim ve 3,6 kata kadar
  daha düşük gecikme sunduğunu açıklıyor — bunlar şirketin kendi rakamları
  olup henüz bağımsız olarak doğrulanmadı ve karşılaştırma yalnızca
  Blackwell ile yapıldı, Nvidia'nın daha yeni Rubin çipleriyle değil.
sources:
  - name: OpenAI News
    url: https://openai.com/index/jalapeno-first-results
  - name: OpenAI News
    url: https://openai.com/index/openai-broadcom-jalapeno-inference-chip
  - name: Broadcom (yatırımcı ilişkileri)
    url: https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor
  - name: SemiAnalysis
    url: https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/
  - name: Tom's Hardware
    url: https://www.tomshardware.com/tech-industry/semiconductors/openai-says-its-jalapeno-chip-beats-nvidias-gb300-in-first-published-benchmarks
claims:
  - text: "OpenAI ve Broadcom, 24 Haziran 2026'da tanıttıkları yapay zekâ çıkarımına özel çip Jalapeño'yu birlikte geliştirdi"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "Jalapeño yalnızca yapay zekâ çıkarımı için tasarlandı ve modelleri eğitmek için kullanılamıyor"
    type: announcement
    verdict: confirmed
    evidence: [3, 6]
  - text: "OpenAI ve Broadcom, Jalapeño'nun tasarımdan üretim bandına (tape-out) geçişinin yaklaşık dokuz ay sürdüğünü açıklıyor"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "OpenAI, 25 Ağustos 2026'da yayımladığı ilk Jalapeño kıyaslama sonuçlarında, çipin GPT-OSS 120B, DeepSeek R1 670B ve Kimi K2.5 1T modellerinde Nvidia'nın mevcut Blackwell nesli çiplerine (GB200 ve GB300) göre watt başına 1,5-1,9 kat daha fazla verim ve 1,7-3,6 kat daha düşük gecikme sunduğunu açıklıyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 4, 5]
  - text: "Jalapeño için açıklanan kıyaslama sonuçları, henüz test edilebilir durumda olmayan Nvidia'nın yeni nesil Rubin çipleriyle bir karşılaştırma içermiyor"
    type: announcement
    verdict: confirmed
    evidence: [4, 6]
updated: []
---

## Ne oldu

OpenAI, Broadcom ile birlikte geliştirdiği özel yapay zekâ çıkarım çipi
Jalapeño için ilk performans sonuçlarını 25 Ağustos 2026'da yayımladı [1].
OpenAI ve Broadcom, çipi ilk kez 24 Haziran 2026'da tanıtmış [2][3] ve
tasarımdan üretim bandına geçişin yaklaşık dokuz ay sürdüğünü açıklamıştı
[2][3]. Jalapeño yalnızca yapay zekâ çıkarımı — eğitilmiş modelleri
çalıştırma — için tasarlandı; yeni modelleri eğitmek için kullanılamıyor
[3][6].

OpenAI, bugünkü açıklamasında Jalapeño'nun GPT-OSS 120B, DeepSeek R1 670B
ve Kimi K2.5 1T dahil üç açık ağırlıklı modelde, Nvidia'nın mevcut
Blackwell nesli çiplerine (GB200 ve GB300) kıyasla watt başına 1,5-1,9 kat
daha fazla yapay zekâ verimi ve 1,7-3,6 kat daha düşük gecikme sunduğunu
söylüyor [1][4][5]. Bunlar OpenAI'nin kendi rakamları; bağımsız analiz
kuruluşu SemiAnalysis, kıyaslama testlerini yerinde izlediğini ancak
testlerin tamamını bağımsız olarak çalıştırmadığını belirtiyor [4] ve şu
ana kadar başka hiçbir bağımsız doğrulama yayımlanmadı. Karşılaştırma
yalnızca Nvidia'nın Blackwell ailesini kapsıyor — Jalapeño için açıklanan
sonuçlar, henüz test edilebilir durumda olmayan Nvidia'nın yeni nesil
Rubin çipleriyle bir karşılaştırma içermiyor [4][6].

## Neden önemli

OpenAI, Nvidia'nın en büyük müşterilerinden biri; bu yüzden güvenilir bir
kendi yapay zekâ çıkarım çipi hem maliyetlerini hem de gelecekteki donanım
pazarlıklarındaki konumunu değiştirebilir. Ancak şu ana kadar yayımlanan
tek performans verisi OpenAI'nin kendisine ait, yalnızca OpenAI'nin
izlemeye davet ettiği bir kuruluş tarafından gözlemlendi ve yalnızca
Nvidia'nın bir önceki nesli olan Blackwell'e karşı ölçüldü. Jalapeño'nun
sahada asıl rakibi olacak Rubin karşısında nasıl bir performans
göstereceği henüz test edilmedi.
