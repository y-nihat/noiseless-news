---
title: DeepSeek, artan AI fiyat rekabeti ortasında V4-Flash-0731'i genel beta sürümüne açtı
date: 2026-07-31
slug: deepseek-v4-flash-0731-beta
lang: tr
tldr: >
  DeepSeek, 31 Temmuz 2026'da API'si üzerinden DeepSeek-V4-Flash-0731'i genel
  beta sürümüne açtı; bu, 24 Nisan'da önizleme olarak açık kaynak yaptığı
  V4-Flash modelinin, daha iyi ajan (agentic), kodlama ve araç kullanımı
  performansı hedefleyen yeniden eğitilmiş bir güncellemesi. Aynı gün Nisan
  ayında önizlemesi yapılan V4-Pro güncellenmedi. Fiyatlandırma değişmedi ve
  lansman, OpenAI'nin GPT-5.6 Luna fiyatlarını düşürdüğü haftaya denk gelerek
  önde gelen laboratuvarlar arasındaki maliyet rekabetini yoğunlaştırdı.
sources:
  - name: DeepSeek API (güncelleme kaydı)
    url: https://api-docs.deepseek.com/updates/
  - name: DeepSeek API (V4 önizleme duyurusu)
    url: https://api-docs.deepseek.com/news/news260424/
  - name: DeepSeek API (fiyatlandırma)
    url: https://api-docs.deepseek.com/quick_start/pricing
  - name: Nikkei Asia
    url: https://asia.nikkei.com/business/technology/artificial-intelligence/deepseek-releases-beta-version-of-v4-models-as-ai-price-war-heats-up
  - name: VentureBeat
    url: https://venturebeat.com/technology/ai-price-wars-openai-cuts-gpt-5-6-luna-prices-by-80-as-model-competition-shifts-toward-cost
  - name: Artificial Analysis
    url: https://artificialanalysis.ai
claims:
  - text: "DeepSeek, 31 Temmuz 2026'da API'si üzerinden DeepSeek-V4-Flash-0731'i genel beta sürümüne açtı; bu, geliştirilmiş ajan, kodlama ve araç kullanımı performansı hedefleyen, yeniden eğitilmiş bir V4-Flash güncellemesi"
    type: announcement
    verdict: confirmed
    evidence: [1, 4]
  - text: "V4-Flash, 24 Nisan 2026'da V4-Pro ile birlikte bir önizlemenin parçası olarak açık kaynak yapılmıştı; V4-Pro'nun kendisi 31 Temmuz'da güncellenmedi"
    type: announcement
    verdict: confirmed
    evidence: [2, 1]
  - text: "DeepSeek, V4-Flash-0731'in Terminal-Bench 2.1'de 82,7 puan aldığını bildiriyor (V4-Pro önizlemesindeki 72,1 ve önceki Flash sürümündeki 56,9-61,8'den yükseldi), DeepSWE'de 54,4 (7,3'ten yükseldi) ve Toolathlon'da 70,3"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Bağımsız bir Artificial Analysis değerlendirmesi, V4-Flash-0731'in Terminal-Bench 2.1 puanını yaklaşık %79 olarak ölçüyor; bu, DeepSeek'in kendi bildirdiği 82,7 rakamıyla tam örtüşmese de yakın, ve önceki Flash sürümünün yaklaşık %62'sinden büyük bir artışı temsil ediyor"
    type: capability
    verdict: confirmed
    evidence: [6]
  - text: "V4-Flash-0731 için API fiyatlandırması önizlemeden değişmedi: önbellek kaçırma durumunda milyon girdi jetonu başına 0,14 dolar, önbellek isabetinde milyon başına 0,0028 dolar ve milyon çıktı jetonu başına 0,28 dolar"
    type: announcement
    verdict: confirmed
    evidence: [3]
  - text: "Lansman, öncü yapay zekâ laboratuvarları arasında artan fiyat rekabeti ortamında geldi; OpenAI'nin GPT-5.6 Luna fiyatlarını yaklaşık %80 düşürdüğü haftaya denk geldi"
    type: business
    verdict: confirmed
    evidence: [4, 5]
updated: []
---

## Ne oldu

DeepSeek, 31 Temmuz 2026'da API'si üzerinden DeepSeek-V4-Flash-0731'i genel
beta sürümüne açtı [1]. Model, DeepSeek'in 24 Nisan 2026'da daha büyük
kardeşi V4-Pro ile birlikte önizleme olarak açık kaynak yaptığı V4-Flash'in
yeniden eğitilmiş bir güncellemesi [2]. Her iki önizleme modeli de 1 milyon
jetonluk bağlam penceresini paylaşıyor; V4-Flash, jeton başına 13 milyar
aktif parametreye sahip 284 milyar parametrelik bir mimari kullanırken,
V4-Pro toplamda 1,6 trilyon parametre ve 49 milyar aktif parametreye sahip
[2]. DeepSeek'in 31 Temmuz güncellemesi yalnızca V4-Flash'i kapsıyor —
V4-Pro güncellenmedi ve DeepSeek'in kendi değişiklik kaydında o tarih için
V4-Pro girdisi bulunmuyor [1].

DeepSeek, yeniden eğitimin ajan, kodlama ve araç kullanımı performansını
iyileştirdiğini söylüyor: şirket, V4-Flash-0731'in Terminal-Bench 2.1'de
82,7 puan aldığını bildiriyor (Nisan ayındaki V4-Pro önizlemesindeki 72,1 ve
önceki Flash sürümündeki 56,9-61,8'den yükseldi), bunun yanında DeepSWE'de
54,4 (7,3'e karşı) ve Toolathlon'da 70,3 [1]. Bu rakamlar DeepSeek'in
kendisinden geliyor. Artificial Analysis'in bağımsız değerlendirmesi,
Terminal-Bench 2.1 puanını yaklaşık %79 olarak ölçüyor -- DeepSeek'in kendi
bildirdiği 82,7 rakamıyla tam örtüşmüyor ama yakın, ve önceki Flash
sürümünün yaklaşık %62'sinden büyük bir artışı temsil ediyor [6]; DeepSWE
veya Toolathlon için bağımsız bir rakam bulunamadı. API fiyatlandırması önizlemeden değişmedi: önbellek kaçırma
durumunda milyon girdi jetonu başına 0,14 dolar, önbellek isabetinde milyon
başına 0,0028 dolar ve milyon çıktı jetonu başına 0,28 dolar [3]. DeepSeek'in
fiyatlandırma sayfası ayrıca, Pekin saatiyle belirli gündüz aralıklarında
oranları kabaca ikiye katlayacak planlanmış bir yoğun/sakin saat
fiyatlandırma yapısı tanımlıyor; bu yapı lansmanda henüz yürürlükte değildi
[3].

Bağımsız basın lansmanı aynı gün haberleştirdi. Nikkei Asia, bunu artan bir
yapay zekâ fiyat savaşının parçası olarak bildirdi ve DeepSeek'in
fiyatlarının büyük ABD'li rakiplerinin fiyatlarının altında kaldığını
belirtti [4]. VentureBeat ise ayrı olarak, OpenAI'nin aynı dönemde GPT-5.6
Luna fiyatlarını yaklaşık %80 düşürdüğünü bildirdi; bunu da öncü
laboratuvarlar arasındaki daha geniş maliyet rekabetinin bir parçası olarak
değerlendiriyor [5].

## Neden önemli

Fiyatlandırma, öncü model rekabetinde yetkinliğin yanı sıra aktif bir cephe
hâline geldi ve DeepSeek'in lansmanı, büyük bir OpenAI fiyat indirimiyle
aynı haftaya denk geliyor — birlikte ele alındığında bu iki bağımsız şekilde
haberleştirilen adım, izole bir pazarlama iddiasından çok, önde gelen
laboratuvarlar arasında gerçek bir maliyet baskısına işaret ediyor.
Bağımsız bir değerlendirme, DeepSeek'in V4-Flash-0731 için bildirdiği
performans kazanımlarını önceki sürüme kıyasla büyük ölçüde -- ama tam
olarak değil -- doğruluyor; DeepSeek'in kendi daha yüksek rakamı ise
doğrulanmadı.
