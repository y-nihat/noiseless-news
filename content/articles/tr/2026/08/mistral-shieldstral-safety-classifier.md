---
title: Mistral, açık ağırlıklı bir yapay zekâ içerik güvenliği sınıflandırıcısı olan Shieldstral'i yayımladı
date: 2026-08-04
published: 2026-08-10
slug: mistral-shieldstral-safety-classifier
lang: tr
tldr: >
  Mistral AI, 4 Ağustos 2026'da, sabit bir kategorileme yerine sorgu
  anında düz metin politikalarına göre metin ve görselleri tarayan,
  Apache 2.0 lisanslı, 3 milyar parametreli açık ağırlıklı bir içerik
  güvenliği sınıflandırıcısı olan Shieldstral'i yayımladı. Mistral, kendi
  testlerinin çoğunda modelin kendi boyutunun yedi katına kadar büyük
  koruma modellerine eşit veya onlardan üstün olduğunu söylüyor; ancak
  bir uyarlanabilirlik testinde 20 milyar parametreli bir rakibin
  gerisinde kalıyor ve bu rakamların bağımsız bir değerlendirmesi henüz
  yok. Bu, Mistral'ın Temmuz ayında kurucu üye olarak katıldığı,
  NVIDIA öncülüğündeki Open Secure AI Alliance koalisyonunun yayımladığı
  ilk araç.
sources:
  - name: Mistral AI News
    url: https://mistral.ai/news/shieldstral/
  - name: The Decoder
    url: https://the-decoder.com/mistrals-open-model-shieldstral-matches-much-larger-safety-models/
claims:
  - text: "Mistral AI, 4 Ağustos 2026'da, sabit ve yeniden eğitilmiş bir kategorileme yerine, çıkarım anında verilen düz metin politikalarına göre metin ve görsel içeriği değerlendiren, Apache 2.0 lisanslı, tek bir 16GB GPU'da çalışabilen, 3 milyar parametreli açık ağırlıklı bir yapay zekâ içerik güvenliği sınıflandırıcısı olan Shieldstral'i yayımladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Mistral, Shieldstral'in metin güvenliği, ret tespiti, politika uyarlanabilirliği ve çok modlu ölçütlerde kendi boyutunun yedi katına kadar büyük açık koruma modellerine eşit veya onlardan üstün olduğunu; metin güvenliğinde OpenAI'nin 20 milyar parametreli GPT-OSS-Safeguard-20B modeliyle eşitlenen %84,9 F1 skoruna ulaştığını bildiriyor; ancak görülmemiş politikaları kullanan ayrı bir uyarlanabilirlik ölçütünde Mistral'in Shieldstral için bildirdiği skor (%91,3), aynı 20 milyarlık modelin skorunun (%94,1) gerisinde kalıyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "Mistral, Temmuz 2026 sonunda kurulan NVIDIA öncülüğündeki yapay zekâ güvenliği koalisyonu Open Secure AI Alliance'ın kurucu üyelerinden biri ve Shieldstral'i bu koalisyon kapsamında yayımlandığını belirtiyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
follows: open-secure-ai-alliance-formation
---

## Ne oldu

Mistral AI, 4 Ağustos 2026'da, tek bir 16GB GPU'da çalışabilecek kadar
küçük, Apache 2.0 lisanslı, 3 milyar parametreli açık ağırlıklı bir içerik
güvenliği sınıflandırıcısı olan Shieldstral'i yayımladığını duyurdu [1][2].
Shieldstral, sabit ve yeniden eğitilmiş bir güvensiz kategori listesi
kullanmak yerine, çıkarım anında — örneğin "bu içerik fiziksel şiddeti
teşvik ediyor mu?" gibi — düz metinle verilen bir politika sorusunu alıp
hem metin hem görsel için tek bir belirteçten hesaplanan bir güvenlik
skoru döndürüyor [1][2].

Mistral'ın kendi ölçütlerine göre Shieldstral, çoğu ölçümde kendi
boyutunun yedi katına kadar büyük açık koruma modellerine eşit veya
onlardan üstün; metin güvenliğinde, OpenAI'nin 20 milyar parametreli
GPT-OSS-Safeguard-20B modeliyle eşitlenen %84,9 F1 skoruna ulaşıyor
[1][2]. Ancak bu karşılaştırma her testte aynı yönde değil: görülmemiş
politikalara uyarlanmayı ölçen ayrı bir testte, Mistral'in Shieldstral
için bildirdiği skor (%91,3), aynı 20 milyarlık rakibin skorunun (%94,1)
gerisinde kalıyor [2]. Bu rakamların tamamı Mistral'in kendi
değerlendirmesinden geliyor; Shieldstral'in bağımsız bir üçüncü taraf
ölçütü henüz yayımlanmadı [2].

Shieldstral, Temmuz 2026 sonunda bir Hugging Face ajan güvenliği
ihlalinin ardından kurulan, NVIDIA öncülüğündeki yapay zekâ güvenliği
koalisyonu Open Secure AI Alliance kapsamında yayımlanan ilk araç; Mistral
bu koalisyona NVIDIA ve diğer şirketlerle birlikte kurucu üye olarak
katıldı [1].

## Neden önemli

Koalisyonun kuruluş duyurusu üyelerinden gelecek araç katkıları vaat
etmişti; Shieldstral, yalnızca tekrarlanan bir taahhüt değil, fiilen
sevk edilen ilk araç. Herhangi bir satıcı tarafından yayımlanan ölçüt
gibi, bu rakamlar da Mistral'in kendi seçtiği testlerde, kendi
sonuçları — ve bu durum güvenlik sınıflandırmasında özellikle önem
taşıyor, çünkü neyin "güvensiz" sayıldığı politikaya bağlı ve test
edilen model de o politikayı yorumlayan model. Bağımsız bir doğrulama
henüz mevcut değil.
