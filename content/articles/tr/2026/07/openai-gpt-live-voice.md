---
title: OpenAI, ChatGPT'nin ses modunu konuşurken dinleyebilen GPT-Live model ailesiyle değiştirdi
date: 2026-07-09
slug: openai-gpt-live-voice
lang: tr
tldr: >
  OpenAI, tam çift yönlü (full-duplex) yeni ses modeli ailesi GPT-Live'ı yayımladı
  ve onu iOS, Android ve web'de ChatGPT Voice'un motoru yaptı. Ücretli aboneler
  GPT-Live-1, ücretsiz kullanıcılar GPT-Live-1-mini alıyor. Tam çift yönlülük
  iddiaları OpenAI'nin kendi beyanı — bağımsız testler henüz yok.
sources:
  - name: OpenAI — Introducing GPT-Live
    url: https://openai.com/index/introducing-gpt-live/
  - name: The Verge
    url: https://www.theverge.com/ai-artificial-intelligence/962856/chatgpt-upgraded-voice-mode-gpt-live
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/08/openai-releases-new-voice-models-for-more-natural-live-conversations/
  - name: 9to5Mac
    url: https://9to5mac.com/2026/07/08/openai-upgrading-chatgpt-with-all-new-voice-mode-experience-watch-here/
claims:
  - text: "OpenAI, GPT-Live'ı 8 Temmuz 2026'da yayımladı; model artık ChatGPT Voice'u çalıştırıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Lansmanla iki model geliyor: ücretli katmanlara GPT-Live-1, ücretsiz kullanıcılara GPT-Live-1-mini — iOS, Android ve web'de"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 4]
  - text: "GPT-Live tam çift yönlü — aynı anda hem dinliyor hem konuşuyor; söz kesmelerde baştan başlamadan uyum sağlıyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "OpenAI'ye göre karmaşık sorular arka planda bir öncü modele devrediliyor; şu an bu model GPT-5.5"
    type: statement
    verdict: confirmed
    evidence: [1, 3]
updated: []
---

## Ne oldu

OpenAI, 8 Temmuz'da ChatGPT'nin ses modunun motorunu iOS, Android ve web genelinde
değiştiren yeni ses modeli ailesi GPT-Live'ı yayımladı [1]. Lansmanla iki model
geliyor: ücretli aboneler GPT-Live-1'i, ücretsiz kullanıcılar daha küçük
GPT-Live-1-mini'yi kullanacak [1][3].

Asıl değişiklik mimaride. OpenAI, GPT-Live'ı *tam çift yönlü* (full-duplex) olarak
tanımlıyor: model aynı anda hem dinliyor hem konuşuyor; kullanıcı yanıtın ortasında
söze girdiğinde, önceki ses modundaki dur-yeniden-başla sıralaması olmadan uyum
sağlıyor [1][2]. Arama ya da daha derin akıl yürütme gerektiren sorularda ise ses
modeli, OpenAI'nin ifadesiyle, işi arka plandaki bir öncü modele devrediyor — şu an
bu model GPT-5.5 [1][3].

## Neden önemli

Sıra bekleme sürtünmesi, sesli asistanların hâlâ sohbetten çok telsiz gibi hissedilmesinin
başlıca nedeni. Tam çift yönlü tasarım anlatıldığı gibi çalışıyorsa, bu kısıtı daha
hızlı yanıtlarla örtmek yerine arayüz düzeyinde ortadan kaldırıyor. Burada neyin
doğrulandığının sınırına dikkat: eşzamanlı dinleme davranışı OpenAI'nin kendi
tanımı — erken ön izleme haberlerinde yankılanıyor ama henüz bağımsız test edilmedi;
aşağıda *üretici beyanı* etiketi taşımasının nedeni bu.
