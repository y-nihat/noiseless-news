---
title: Sakana AI, siber savunma amaçlı orkestrasyon modeli Fugu-Cyber'ı yayımladı
date: 2026-07-21
published: 2026-07-27
slug: sakana-fugu-cyber-release
lang: tr
tldr: >
  Sakana AI, 21 Temmuz 2026'da Fugu-Cyber'ı yayımladı: güvenlik açıklarını
  doğrulamak ve tehdit istihbaratından tespit kuralları üretmek için
  tasarlanmış, görevleri birden fazla temel model arasında dağıtırken kendini
  tek bir model gibi sunan çok-etmenli bir sistem. Sakana'nın yayın için
  verdiği kıyaslama rakamları — CyberGym'de %86,9 ve CTI-REALM'de %72,1 —
  şirketin kendi beyanına dayanıyor: Fugu-Cyber, CyberGym'in bağımsız lider
  tablosunda görünmüyor ve bağımsız kaynaklar Sakana'nın değerlendirme
  yöntemini açıklamadığını bildiriyor.
sources:
  - name: Sakana AI — Fugu-Cyber yayın sayfası
    url: https://sakana.ai/fugu-cyber-release/
  - name: MarkTechPost
    url: https://www.marktechpost.com/2026/07/25/sakana-ai-releases-fugu-cyber-orchestration-model-cybergym-cti-realm/
  - name: Tech Times
    url: https://www.techtimes.com/articles/321267/20260722/sakana-ai-fugu-cyber-claims-869-vulnerability-score-benchmark-methodology-not-disclosed.htm
  - name: llm-stats.com — CyberGym lider tablosu
    url: https://llm-stats.com/benchmarks/cybergym
  - name: CyberGym kıyaslama makalesi (arXiv, ICLR 2026)
    url: https://arxiv.org/abs/2506.02548
claims:
  - text: "Sakana AI, siber savunma amaçlı çok-etmenli orkestrasyon modeli Fugu-Cyber'ı 21 Temmuz 2026'da yayımladı"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Sakana, Fugu-Cyber'ın CyberGym kıyaslamasında %86,9, CTI-REALM'de %72,1 puan aldığını bildiriyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Fugu-Cyber, CyberGym'in bağımsız lider tablosunda yer almıyor ve bağımsız kaynaklar Sakana'nın değerlendirme yöntemini açıklamadığını bildiriyor"
    type: statement
    verdict: confirmed
    evidence: [2, 3, 4]
  - text: "CyberGym'in akademik makalesindeki (ICLR 2026) yayımlanmış sonuçlar, en iyi model/iskelet kombinasyonlarının yaklaşık %18-20'ye ulaştığını gösteriyor; bu, Sakana'nın Fugu-Cyber için kendi beyan ettiği rakamın oldukça altında"
    type: research
    verdict: confirmed
    evidence: [5]
updated: []
---

## Ne oldu

Sakana AI, 21 Temmuz 2026'da Fugu-Cyber'ı yayımladı [1]: güvenlik açıklarını doğrulamak ve tehdit istihbaratından tespit kuralları üretmek için geliştirilmiş, Sakana'nın "tek bir model gibi davranıyor" dediği ama görevleri gizli tuttuğu birden fazla temel model arasında dağıtan çok-etmenli bir sistem; erişim bir başvuru formunun ardında kısıtlı [1]. Bu, 22 Haziran 2026'da çıkan temel sürümün ardından Sakana'nın Fugu serisindeki ikinci yayın [1].

Sakana'nın yayın sayfası, Fugu-Cyber'ın CyberGym kıyaslamasında %86,9, CTI-REALM'de %72,1 puan aldığını belirtiyor [1], ancak deneme sayısını veya değerlendirme iskeletini açıklamıyor. 27 Temmuz itibarıyla Fugu-Cyber, llm-stats.com'daki bağımsız CyberGym lider tablosunun on kaydı arasında yer almıyor [4]. Tech Times ve MarkTechPost, rakamların şirketin kendi beyanına dayandığını ve CTI-REALM'in ölçütünün geçme/kalma oranı değil 0-1 aralığında bir "yörünge ödülü" puanı olduğunu belirtiyor — yani Sakana, kıyaslamanın üretmek üzere tasarlanmadığı bir "başarı oranı"nı sunuyor [2][3]. CyberGym'in kendi akademik makalesi (ICLR 2026), en iyi model/iskelet kombinasyonlarını yaklaşık %18-20'de bırakmıştı [5] — Sakana'nın Fugu-Cyber için beyan ettiği rakamın epey altında, ancak bu makale daha eski bir iskelet kullanmıştı.

## Neden önemli

Siber savunma araçlarının değeri, rakamlarının bağımsız testlerde tutup tutmamasına bağlı. Fugu-Cyber'ın yayınlanması doğrulanmış bir bilgi, ama öne çıkan kıyaslama rakamları değil: bunlar, CyberGym'in kendi lider tablosunda yer almayan, Sakana dışında yeniden üretilmemiş ve açıklanan akademik tavan değerlerden bu denli uzak üretici beyanları — gerçek kabul edilmeden önce bağımsız incelemeyi gerektiriyor.
