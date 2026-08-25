---
title: Thomson Reuters, kendi yapay zekâ modelini CoCounsel Legal ürününde kullanıma sundu
date: 2026-08-24
published: 2026-08-25
slug: thomson-reuters-ai-model-launch
lang: tr
tldr: >
  Thomson Reuters, en azından bu ürün hattı için dışarıdan model kiralamak
  yerine kendi yapay zekâ modeli Thomson'ı geliştirip kullanıma sundu. Model
  ilk olarak şirketin CoCounsel Legal ürünündeki Tabular Analysis
  özelliğinde devreye giriyor; akademik kullanım için Hugging Face üzerinden
  daha küçük, açık ağırlıklı bir sürüm de yayımlandı. Thomson Reuters,
  modelin Alibaba'nın açık ağırlıklı Qwen modelinden türetildiğini ve
  geliştirme maliyetinin yaklaşık 40 milyon dolar olduğunu, ayrıca GPT-5.5 ve
  Claude Opus 4.8 gibi öncü modellerle yarışabildiğini veya onları geride
  bıraktığını söylüyor — Qwen kökeni, maliyet rakamı ve karşılaştırma
  sonuçlarının tümü yalnızca şirketin kendi açıklamalarına dayanıyor;
  kıyaslama yöntemine yönelik bağımsız bir inceleme ise karşılaştırmanın
  manşette sunulduğu kadar net olmadığını ortaya koydu.
sources:
  - name: Thomson Reuters (PR Newswire)
    url: https://www.prnewswire.com/news-releases/thomson-reuters-leverages-its-world-class-data-assets-to-launch-its-own-frontier-model-302857499.html
  - name: Thomson Reuters
    url: https://www.thomsonreuters.com/en-us/posts/innovation/thomson-reuters-built-its-own-ai-model-that-now-ranks-among-the-worlds-best/
  - name: The Decoder
    url: https://the-decoder.com/thomson-reuters-bets-40m-on-owning-its-ai-instead-of-renting-from-openai-or-anthropic/
  - name: LawSites
    url: https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html
claims:
  - text: "Thomson Reuters, en azından bu ürün hattı için dışarıdan model kiralamak yerine kendi yapay zekâ modeli Thomson'ı geliştirip kullanıma sundu; model ilk olarak CoCounsel Legal'deki Tabular Analysis özelliğinde devreye giriyor ve Hugging Face üzerinden akademik/ticari olmayan kullanım için daha küçük, açık ağırlıklı bir sürümü yayımlandı."
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Thomson Reuters'a göre model, Alibaba'nın açık ağırlıklı Qwen3.5-397B modeli üzerine kurulu \"Snowdon\" adlı ara bir güvenlik-yeniden-eğitimli sürümden türetiliyor; güvenlik ve etik yeniden eğitimini Imperial College üstlendi."
    type: announcement
    verdict: single-source
    evidence: [3]
  - text: "Thomson Reuters, Thomson'ı geliştirmenin iki yılı aşkın sürede yaklaşık 40 milyon dolara mal olduğunu, bunun yaklaşık 450.000 dolarının son eğitim çalıştırmasına harcandığını söylüyor."
    type: business
    verdict: single-source
    evidence: [1]
  - text: "Thomson Reuters, Thomson'ın Claude Opus 4.8, GPT-5.5, Claude Sonnet 5 ve Gemini 3.1 Pro dahil öncü modellerle hukuki ve genel kıyaslamalarda yarışabildiğini veya onları geride bıraktığını söylüyor."
    type: capability
    verdict: vendor-claim
    evidence: [1, 2, 4]
updated: []
---

## Ne oldu

Thomson Reuters, en azından bu ürün hattı için dışarıdan yapay zekâ modeli kiralamak yerine kendi modelini -- Thomson -- geliştirip kullanıma sunduğunu açıkladı [1][2]. Modelin ilk kullanım alanı, şirketin CoCounsel Legal ürünü içindeki Tabular Analysis özelliği; şirket ayrıca akademik ve ticari olmayan kullanım için Hugging Face üzerinden daha küçük, açık ağırlıklı bir sürüm de yayımladı [1]. Thomson Reuters'a göre model, "Snowdon" adını verdikleri ara bir güvenlik-yeniden-eğitimli sürümden türetiliyor; bu ara model de Alibaba'nın açık ağırlıklı Qwen3.5-397B modeli üzerine kuruluyor ve güvenlik/etik yeniden eğitimini Imperial College üstlendi -- ancak bu ayrıntı yalnızca ikincil haberlerde yer alıyor, Thomson Reuters'ın kendi duyuru materyallerinde geçmiyor [3].

Thomson Reuters, projenin iki yılı aşkın sürede yaklaşık 40 milyon dolara mal olduğunu -- bunun yaklaşık 450.000 dolarının son eğitim çalıştırmasına harcandığını -- ve Thomson'ın Claude Opus 4.8, GPT-5.5, Claude Sonnet 5 ve Gemini 3.1 Pro dahil öncü modellerle hukuki ve genel kıyaslamalarda yarışabildiğini veya onları geride bıraktığını söylüyor [1][2]. Her iki rakam da yalnızca şirketin kendi açıklamasına dayanıyor; haber aynı gün birçok farklı mecrada geniş yer bulmuş olsa da, tüm haberler aynı tek kaynağa dayanıyor ve maliyeti doğrulayan bağımsız bir belge veya tahmin bulunmuyor. Hukuk teknolojisi gazetecisi Bob Ambrogi'nin LawSites'taki bağımsız incelemesi, testlerin yürütülme biçiminde asimetriler olduğunu -- örneğin test zamanı ölçeklendirmenin Thomson'a uygulanırken rakiplerine aynı şekilde uygulanmadığını, GPT-5.5'in ise akıl yürütme modu kapalıyken test edildiğini -- tespit etti ve kendi bildirilen karşılaştırmanın "manşetin ima ettiğinden daha karmaşık" olduğu sonucuna vardı [4].

## Neden önemli

Büyük bir hukuki bilgi sağlayıcısının OpenAI veya Anthropic'ten kiralamak yerine kendi modelini geliştirip sahiplenmesi, diğer kurumsal yapay zekâ alıcılarının da değerlendirdiği bir strateji değişikliğine işaret ediyor -- ama bunun maliyeti ve ortaya çıkan modelin öncü rakiplerine karşı durumu, şimdilik yalnızca Thomson Reuters'ın kendi anlatımına dayanıyor.
