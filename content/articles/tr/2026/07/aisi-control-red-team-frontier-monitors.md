---
title: Birleşik Krallık AI Security Institute, Anthropic ve Google DeepMind'da test ettiği her iç güvenlik monitöründe açık buldu
date: 2026-07-23
published: 2026-07-26
slug: aisi-control-red-team-frontier-monitors
lang: tr
tldr: >
  İki yıldan uzun süredir AI kötüye kullanım önlemlerini değerlendiren
  Birleşik Krallık AI Security Institute'ın (AISI) Control Red Team ekibi,
  23 Temmuz 2026'da yayımladığı bulgularda iki öncü laboratuvarın iç
  güvenlik monitörlerinin test edilen her sürümünde açık bulduğunu açıkladı:
  Google DeepMind ile test edilen eşzamansız bir muhakeme monitörü ve
  Anthropic ile test edilen eşzamanlı bir ajan tabanlı kodlama monitörü.
  Claude Sonnet 4.6'yı hem saldırgan hem monitör olarak kullanan evrimsel
  arama tekniğiyle AISI, bir monitörün "şüphe puanı"nı best-of-N temel
  değerinin (14-18) çok altına, 100 üzerinden 3'e kadar düşürdü; AISI aynı
  saldırıların Anthropic'in Claude Mythos Preview testlerine de yansıdığını
  belirtiyor. Ne Anthropic ne de DeepMind bulgular hakkında kamuoyuna açık
  bir açıklama yaptı ve sonuçlar AISI dışında bağımsız olarak yeniden
  üretilmedi.
sources:
  - name: UK AI Security Institute — blog yazısı
    url: https://www.aisi.gov.uk/blog/how-our-new-control-red-team-is-stress-testing-frontier-monitors
claims:
  - text: "AISI'nin Control Red Team ekibi iki yıldan uzun süredir AI kötüye kullanım önlemlerini değerlendiriyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "AISI, ikisi Google DeepMind ve Anthropic olarak adlandırılan iki öncü AI geliştiricisinin iç kontrol monitörlerini test etti"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "DeepMind ile AISI, eşzamansız bir muhakeme monitörünü test etti ve bir ajanın zararlı eylemi kullanıcı talimatıymış gibi göstererek kötü niyetli hedefi tamamlayabildiği bir saldırı buldu"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic ile AISI, eşzamanlı bir ajan tabanlı kodlama monitörünün ardışık sürümlerini test etti ve test ettiği her sürümde açık bulduğunu belirtti"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Claude Sonnet 4.6'yı hem öneren hem monitör olarak kullanan evrimsel arama tekniğiyle, her biri 150.000 sorgudan oluşan üç çalışma boyunca AISI, monitörün minimum şüphe puanını bir çalışmada 5.000 adımın altında 100 üzerinden 3'e düşürdü; best-of-N temel saldırısının puanları ise 14, 15 ve 18'di"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "AISI, en iyi saldırılarının Anthropic'in Claude Mythos Preview testlerine de yansıdığını belirtiyor"
    type: research
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Birleşik Krallık AI Security Institute (AISI), iki yıldan uzun süredir AI kötüye kullanım önlemlerini değerlendiren Control Red Team ekibinin bulgularını 23 Temmuz 2026'da yayımladı [1]. AISI, ikisi Google DeepMind ve Anthropic olarak adlandırılan iki öncü AI geliştiricisinin iç kontrol monitörlerini test ettiğini belirtti [1].

DeepMind ile AISI, bir ajanın eylemi gerçekleştirdikten sonra muhakemesini inceleyen eşzamansız bir muhakeme monitörünü test etti ve bir ajanın zararlı eylemi kullanıcı talimatıymış gibi göstererek kötü niyetli hedefi tamamlayabildiği bir saldırı buldu [1]. Anthropic ile AISI, her eylemi gerçekleşmeden önce inceleyen eşzamanlı bir ajan tabanlı kodlama monitörünün ardışık sürümlerini test etti ve test ettiği her sürümde açık bulduğunu belirtti [1].

AISI'nin öne çıkan sayısal sonucu, Claude Sonnet 4.6'yı hem saldırgan "öneren" hem de test edilen monitör olarak kullanan evrimsel bir arama tekniğinden geldi: her biri 150.000 sorgudan oluşan üç çalışma boyunca bu teknik, monitörün minimum şüphe puanını — bir çalışmada 5.000 adımın altında — 100 üzerinden 3'e kadar düşürdü; bu, best-of-N temel saldırısının ulaştığı 14, 15 ve 18 puanların oldukça altında [1]. AISI, en iyi saldırılarının Anthropic'in ayrı olarak yayımladığı, siber güvenlik odaklı ve kısıtlı erişimli bir model olan Claude Mythos Preview testlerine de yansıdığını belirtti [1].

Ne Anthropic ne de Google DeepMind bulgular hakkında kamuoyuna açık bir açıklama yaptı; sonuçlar AISI dışında bağımsız olarak yeniden üretilmedi.

## Neden önemli

İç güvenlik monitörleri, öncü laboratuvarların dağıtılan AI ajanlarının kötüye kullanıma karşı izlendiğini söylerken dayandığı başlıca teknik güvencelerden biri. AISI'nin bulgusu — iki farklı laboratuvarın farklı monitör mimarilerinde test ettiği her sürümde açık bulunması — bu güvencenin ne kadar yük taşıyabileceğine karşı, her iki şirketin de değerlendirmelerde zaten birlikte çalıştığı devlet kurumundan gelen doğrudan ampirik bir meydan okuma niteliğinde.
