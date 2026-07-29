---
title: "NIST, yapay zeka modeli performansını değerlendirmek için izole bir test ortamı olan AITE'yi başlattı"
date: 2026-07-27
published: 2026-07-29
slug: nist-aite-model-evaluation-testbed
lang: tr
tldr: >
  ABD Ulusal Standartlar ve Teknoloji Enstitüsü'nün (NIST) Teknoloji Test ve
  Değerlendirme Bölümü, yapay zeka modellerini eğitim/test veri kirlenmesi
  riskini azaltmak için izole bir ortamda, daha önce görülmemiş kör verilere
  karşı test eden AITE programını başlattı -- satıcıların kendi bildirdiği
  kıyaslamalara devlet destekli bir alternatif. İlk odak, kuantum bilimi,
  genomik ve kamu güvenliğinde görüntü analizi yapan büyük görsel-dil
  modelleri; başlatma Nextgov/FCW ve Defense One tarafından bağımsız olarak
  doğrulandı.
sources:
  - name: NIST AI
    url: https://www.nist.gov/news-events/news/2026/07/announcing-nists-artificial-intelligence-technology-evaluation-aite
  - name: Nextgov/FCW
    url: https://www.nextgov.com/artificial-intelligence/2026/07/nist-unveils-new-ai-evaluation-platform/415035/
  - name: Defense One
    url: https://www.defenseone.com/technology/2026/07/nist-unveils-new-ai-evaluation-platform/415044/
claims:
  - text: "NIST'in Teknoloji Test ve Değerlendirme Bölümü, kuantum bilimi, genomik ve kamu güvenliğinde görsel-dil modeli görüntü analizi görevleriyle başlayan, yapay zeka modeli performansını kör verilerle izole bir test ortamında değerlendiren gönüllü bir program olan AITE'yi başlattı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "AITE iki tür katılımcı kabul ediyor: kamuya açık olmayan orijinal veri setlerini ve bir görevi sunan veri sağlayıcıları ile bu verilere karşı test edilecek modelleri sunan model sağlayıcıları, tümü bir AITE Katılım Anlaşması kapsamında"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

ABD Ulusal Standartlar ve Teknoloji Enstitüsü'nün (NIST) Teknoloji Test ve Değerlendirme Bölümü, yapay zeka modellerini izole bir ortamda kör verilere karşı test ederek eğitim/test veri kirlenmesi riskini azaltmayı amaçlayan AITE (AI Technology Evaluation) programını başlattı [1]. Katılım gönüllü ve iki biçimde açık: veri sağlayıcıları, kamuya açık olmayan orijinal veri setlerini bir görevle birlikte sunuyor; model sağlayıcıları ise modellerini bu verilere karşı test edilmek üzere sunuyor, her ikisi de bir AITE Katılım Anlaşması kapsamında [1]. AITE'nin ilk kapsamı, kuantum bilimi, genomik ve kamu güvenliğinde görüntü analizi yapan büyük görsel-dil modelleri için üç görevi kapsıyor; ileride daha fazla görev planlanıyor [1]. NIST'in kendi sitesinde 27 Temmuz 2026 tarihli olan başlatma, Nextgov/FCW ve Defense One tarafından bağımsız olarak bildirildi [2][3].

## Neden önemli

Model sağlayıcıları şu anda çoğu yetenek kıyaslamasını kendileri raporluyor. AITE, NIST'e, özellikle test verisinin eğitim setlerinin dışında tutulması için tasarlanmış, hükümet tarafından yürütülen, bağımsız bir alternatif sağlıyor; bu da bu sitenin kendi doğrulama standardının yetenek iddiaları için en güvenilir kaynak saydığı türden bağımsız değerlendirme altyapısı. Program şimdilik dar kapsamlı: belirli bilimsel ve kamu güvenliği alanlarında sadece üç görev, dolayısıyla yapay zeka yetenek iddialarının daha geniş çapta nasıl denetlendiği üzerindeki etkisi, kaç laboratuvarın katılmayı seçeceğine ve NIST'in görev listesini ne kadar genişleteceğine bağlı olacak.
