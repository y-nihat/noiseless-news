---
title: Nvidia, Claude Opus 5 ile çalışan AVO ajan altyapısını ARC-AGI-3 testine soktu
date: 2026-08-21
published: 2026-08-22
slug: nvidia-avo-arc-agi-3
lang: tr
tldr: >
  Nvidia, aylar önce GPU çekirdek optimizasyonu için geliştirdiği AVO adlı ajan
  altyapısını ilk kez Anthropic'in Claude Opus 5 modeliyle birlikte ARC-AGI-3
  testinde kullandığını duyurdu. Şirketin kendi yürüttüğü testte 183 genel
  seviyenin tamamında mükemmel skor alındığı bildiriliyor — ancak bu sonuç
  ARC Prize'ın resmi lider tablosunda yer almıyor ve bağımsız olarak
  doğrulanmadı.
sources:
  - name: NVIDIA Developer Blog
    url: https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/21/nvidia-just-showed-that-the-harness-not-the-ai-model-is-now-the-real-hero/
  - name: arXiv preprint (2603.24517)
    url: https://arxiv.org/abs/2603.24517
  - name: ARC Prize
    url: https://arcprize.org/leaderboard
claims:
  - text: "Nvidia, Claude Opus 5 ile çalışan AVO ajan altyapısını ARC-AGI-3 testinde kullandığını 21 Ağustos 2026'da duyurdu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "AVO, ilk olarak Nvidia'nın Blackwell B200 donanımında otonom GPU çekirdek optimizasyonu için geliştirildi; bu, Mart 2026 tarihli bir ön baskı (preprint) makalede anlatılıyor ve ARC-AGI-3 kullanımından aylar önceye dayanıyor"
    type: research
    verdict: confirmed
    evidence: [1, 3]
  - text: "Nvidia, AVO'nun RHAE metriğinde 25 genel ARC-AGI-3 ortamının tamamında (183 seviyenin tamamında) mükemmel skor olan 100,00 aldığını bildiriyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "ARC Prize'ın resmi ARC-AGI-3 sitesinde ve lider tablosunda Nvidia veya AVO'ya ait bir kayıt bulunmuyor"
    type: statement
    verdict: confirmed
    evidence: [4]
  - text: "Nvidia, AVO'nun aynı seviyeleri önceki bir sistem olan VISTA'ya göre yaklaşık yüzde 12 daha az eylemle tamamladığını söylüyor; ancak bunun kontrollü bir karşılaştırma olmadığı konusunda kendisi de uyarıda bulunuyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Nvidia'nın yazısı, ARC Prize'ın ayrı bir değerlendirmesine atıfla, Claude Opus 5'in yardımsız skorunu yüksek akıl yürütme ayarında yaklaşık yüzde 30 olarak veriyor"
    type: capability
    verdict: single-source
    evidence: [1]
updated: []
---

## Ne oldu

Nvidia, 21 Ağustos 2026'da, önce Blackwell B200 donanımında otonom GPU çekirdek
optimizasyonu için geliştirdiği ve Mart 2026 tarihli bir ön baskı makalede anlatılan
AVO (Agentic Variation Operators) adlı ajan altyapısını yeni bir alanda kullandığını
duyurdu: Anthropic'in Claude Opus 5 modeli üzerinde çalışan AVO, ARC-AGI-3 testine
sokuldu [1, 3]. Nvidia, AVO'nun testin RHAE metriğinde mükemmel skor olan 100,00
aldığını, 25 genel ortamın tamamını, yani 183 seviyenin tamamını tamamladığını
bildiriyor [1]. TechCrunch, bir Nvidia başkan yardımcısından alıntı yaparak duyuruyu
bağımsız şekilde haberleştirdi, ancak testi kendisi yeniden çalıştırıp doğrulamadı
[2]. ARC Prize'ın resmi ARC-AGI-3 sitesi ve lider tablosu doğrudan kontrol edildiğinde
Nvidia veya AVO'ya ait bir kayda rastlanmadı [4].

Nvidia ayrıca AVO'nun aynı seviyeleri, VISTA adlı önceki bir sistemin 7.542
eyleminin aksine 6.624 eylemle, yani yaklaşık yüzde 12 daha az eylemle
tamamladığını söylüyor; ancak iki sistemin tasarımının yeterince farklı olması
nedeniyle bunun kontrollü bir karşılaştırma sayılmayacağını kendisi de belirtiyor
[1]. Nvidia'nın yazısı, ARC Prize'ın ayrı bir değerlendirmesine atıfla, Claude
Opus 5'in yardımsız skorunu yüksek akıl yürütme ayarında yaklaşık yüzde 30 olarak
veriyor [1].

## Neden önemli

Ezberlemeye karşı dayanıklı olacak şekilde tasarlanmış bir testte yaklaşık yüzde
30'dan yüzde 100'e çıkmak, bağımsız olarak doğrulanırsa, yalnızca modelin değil
ajan altyapısı tasarımının da yetenek artışını sürüklediğinin dikkat çekici bir
göstergesi olurdu. Ancak mevcut sonuç Nvidia'nın kendi yürüttüğü, ARC Prize'ın
resmi lider tablosunda yer almayan bir test olduğu için, doğrulanmış bir test
sonucu değil satıcı iddiası olarak değerlendiriliyor.
