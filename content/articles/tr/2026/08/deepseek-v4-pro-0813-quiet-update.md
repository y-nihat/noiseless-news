---
title: DeepSeek, V4-Pro'yu önizlemeden çıkardı, yoğun saat API fiyatlarını 4,5 kat artırdı
date: 2026-08-13
published: 2026-08-14
slug: deepseek-v4-pro-0813-quiet-update
lang: tr
tldr: >
  DeepSeek'in V4-Pro modeli, 13 Ağustos 2026'da API önizlemesinden çıkarak
  uygulama, web arayüzü ve API üzerinden genel kullanıma açıldı; DeepSeek bu
  sürümü ajan (agent) yetenekleri etrafında konumlandırıyor. Şirket ayrıca
  çıktı jetonu API fiyatlandırmasını sabit orandan, yoğun saatlerde yaklaşık
  4,5 kat daha yüksek bir yoğun/sakin saat yapısına çıkarıyor; değişiklik 16
  Ağustos'ta yürürlüğe girecek. DeepSeek kendi benchmark setinde büyük
  kazanımlar bildiriyor, ancak bağımsız bir değerlendirme modeli mevcut
  öncü tescilli rakiplerinin gerisinde konumlandırıyor.
sources:
  - name: DeepSeek API (GA sürüm duyurusu)
    url: https://api-docs.deepseek.com/news/news260813/
  - name: DeepSeek API (güncelleme kaydı)
    url: https://api-docs.deepseek.com/updates
  - name: DeepSeek API (fiyatlandırma)
    url: https://api-docs.deepseek.com/quick_start/pricing
  - name: Reuters (TradingView üzerinden)
    url: https://www.tradingview.com/news/reuters.com,2026:newsml_FWN44A0IU:0-deepseek-says-launching-deepseek-v4-pro-today/
  - name: Nikkei Asia
    url: https://asia.nikkei.com/business/technology/artificial-intelligence/deepseek-releases-official-v4-pro-model-with-sharply-higher-user-prices
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/models/deepseek-v4-pro
  - name: South China Morning Post
    url: https://www.scmp.com/tech/big-tech/article/3363895/deepseeks-updated-v4-pro-ai-model-struggles-benchmarks-shines-cybersecurity
claims:
  - text: "DeepSeek, V4-Pro'yu 13 Ağustos 2026'da API önizlemesinden çıkararak uygulama, web arayüzü ve API üzerinden genel kullanıma açtı; sürüm ajan yetenekleri ve yeni yapılandırılabilir akıl yürütme (reasoning-effort) seviyeleri etrafında kurgulandı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 4, 5]
  - text: "DeepSeek, V4-Pro API çıktı jetonu fiyatlandırmasını milyon başına sabit 0,87 dolardan, yoğun saatlerde (01:00-04:00 ve 06:00-10:00 UTC) milyon başına 3,96 dolar ve yoğun olmayan saatlerde milyon başına 1,98 dolar olan bir yapıya çıkarıyor; değişiklik 16 Ağustos 2026, 16:00 UTC itibarıyla yürürlüğe giriyor"
    type: announcement
    verdict: confirmed
    evidence: [3, 4, 5]
  - text: "DeepSeek, V4-Pro-0813'ün Terminal-Bench 2.1'de 87,9 (Nisan önizleme sürümündeki 72,1'den yükseldi), DeepSWE'de 62,7, CyberGym'de 83,3, NL2Repo'da 61,5 ve Humanity's Last Exam'de araçsız/araçlı 42,7/60,0 puan aldığını bildiriyor"
    type: capability
    verdict: vendor-claim
    evidence: [2]
  - text: "Yayın anında canlı olarak kontrol edilen bağımsız bir Artificial Analysis değerlendirmesi, V4-Pro-0813'e Intelligence Index'te 53 puan veriyor; bu, modeli karşılaştırılabilir açık ağırlıklı modeller arasında üçüncü sıraya koyarken mevcut öncü tescilli sistemlerin gerisinde bırakıyor"
    type: capability
    verdict: confirmed
    evidence: [6]
  - text: "South China Morning Post, Vals AI'nin bağımsız değerlendirmesinin V4-Pro-0813'ü sandbox terminal görevlerinde ve karmaşık finansal e-tablo modellemesinde rakiplerinden belirgin şekilde zayıf bulduğunu, buna karşın siber güvenlik performansının araştırmacıları görece etkilediğini bildirdi"
    type: capability
    verdict: single-source
    evidence: [7]
updated: []
---

## Ne oldu

DeepSeek, V4-Pro modelini 13 Ağustos 2026'da API önizlemesinden çıkararak
uygulama, web arayüzü ("Expert Mode") ve API üzerinden genel kullanıma açtı
[1]. DeepSeek, sürümü ajan yetenekleri -- araç kullanımı, kod çalıştırma ve
çok adımlı iş akışları -- etrafında konumlandırıyor ve hem V4-Pro hem de
V4-Flash için üç yapılandırılabilir akıl yürütme seviyesi (düşük, yüksek,
maksimum) ile OpenAI'nin Responses API biçimine yerel destek ekliyor [1].
Reuters ve Nikkei Asia, lansmanı aynı gün birbirinden bağımsız olarak
haberleştirdi [4][5].

Sürümle birlikte DeepSeek API fiyatlarını da artırıyor. Çıktı jetonu
fiyatlandırması şu anda milyon jeton başına sabit 0,87 dolar; 16 Ağustos
2026, 16:00 UTC itibarıyla bu fiyat, belirli yoğun talep saatlerinde
(01:00-04:00 ve 06:00-10:00 UTC) milyon başına 3,96 dolarlık bir yoğun-saat
oranına ve günün geri kalanında yoğun oranın yarısı olan milyon başına 1,98
dolarlık bir yoğun-olmayan-saat oranına bölünüyor [3]. Yoğun saat oranı,
mevcut sabit fiyatın kabaca 4,5 katı.

DeepSeek, yeni sürüm için büyük benchmark kazanımları bildiriyor:
Terminal-Bench 2.1'de Nisan önizleme sürümündeki 72,1'den 87,9'a yükseliş;
DeepSWE'de 62,7; CyberGym'de 83,3; NL2Repo'da 61,5; ve Humanity's Last
Exam'de araçsız ve araçlı sırasıyla 42,7/60,0 [2]. Bunlar DeepSeek'in kendi
bildirdiği rakamlar olup bağımsız olarak yeniden üretilmedi. Yayın anında
kontrol edilen bir Artificial Analysis değerlendirmesi, V4-Pro-0813'e
Intelligence Index'te 53 puan veriyor; bu da modeli karşılaştırılabilir açık
ağırlıklı modeller arasında üçüncü sıraya koyarken mevcut öncü tescilli
sistemlerin gerisinde bırakıyor [6]. South China Morning Post ayrıca, Vals
AI'nin bağımsız değerlendirmesinin modeli sandbox terminal görevlerinde ve
karmaşık finansal e-tablo modellemesinde rakiplerinden belirgin şekilde zayıf
bulduğunu, buna karşın araştırmacıların siber güvenlik performansından daha
etkilendiğini bildirdi [7].

## Neden önemli

Lansman ve fiyat değişikliği doğrudan DeepSeek'ten teyit edildi ve iki
bağımsız kaynak tarafından haberleştirildi, ancak yetenek tablosu karışık:
DeepSeek'in kendi rakamları Nisan önizlemesine göre büyük bir sıçrama
gösterirken, basında yer alan bağımsız değerlendirmeler modeli mevcut öncü
tescilli rakiplerinin genel olarak gerisine koyuyor. Yoğun saatlerde kabaca
4,5 katlık fiyat artışı da, en azından yoğun talep saatlerinde, model
ailesinin başlıca satış noktalarından biri olan maliyet avantajını
daraltıyor.
