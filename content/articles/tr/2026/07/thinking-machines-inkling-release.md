---
title: Thinking Machines Lab, ilk açık ağırlıklı modeli Inkling'i yayınladı
date: 2026-07-16
slug: thinking-machines-inkling-release
lang: tr
tldr: >
  Mira Murati'nin OpenAI'den ayrıldıktan sonra kurduğu şirket Thinking
  Machines Lab, 15 Temmuz 2026'da Inkling'i yayınladı: Apache 2.0 lisanslı,
  975 milyar parametreli açık ağırlıklı bir mixture-of-experts modeli, ve
  daha küçük bir önizleme modeli olan Inkling-Small. Bu, şirketin ilk model
  yayını. Satıcı tarafından bildirilen benchmark puanları güçlü ama henüz
  bağımsız olarak doğrulanmadı.
sources:
  - name: Thinking Machines Lab — duyuru
    url: https://thinkingmachines.ai/news/introducing-inkling/
  - name: Thinking Machines Lab — model kartı
    url: https://thinkingmachines.ai/model-card/inkling/
  - name: Hugging Face — Thinking Machines organizasyonu
    url: https://huggingface.co/thinkingmachines
  - name: Hugging Face — Inkling duyuru yazısı
    url: https://huggingface.co/blog/thinkingmachines-inkling
claims:
  - text: "Thinking Machines Lab, 15 Temmuz 2026'da Inkling'i duyurdu: 975 milyar toplam / 41 milyar aktif parametreli seyrek mixture-of-experts modeli (66 katmanlı decoder-only transformer, 256 yönlendirilen uzman artı 2 paylaşılan uzman, token başına 6 aktif uzman), 1 milyon token'a kadar bağlam penceresi, 45 trilyon çok-modlu (metin, görüntü, ses, video) token ile eğitilmiş, yalnızca metin çıktısı veren bir model"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Inkling'in ağırlıkları Apache 2.0 lisansı altında yayınlandı; Hugging Face'te BF16 ve NVFP4 nicemlenmiş biçimlerde indirilebiliyor, transformers/SGLang/vLLM'de aynı gün destek ve Tinker, Together AI, Fireworks, Modal, Databricks, Baseten üzerinden barındırılan erişim mevcut; ağırlıkların kullanımı ayrıca Thinking Machines'in gözetim, aldatma ve tamamen otomatikleştirilmiş yüksek riskli kararları yasaklayan kabul edilebilir kullanım politikasına tabi"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Daha küçük bir eş model olan Inkling-Small (276 milyar toplam / 12 milyar aktif parametre) önizleme olarak duyuruldu; ağırlıkları duyuru anında henüz yayınlanmamıştı, testlerin tamamlanmasını bekliyordu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Inkling, yanıt kalitesi ile token maliyeti/gecikme arasında denge kurmayı sağlayan, kullanıcı tarafından ayarlanabilir bir 'kontrol edilebilir düşünme eforu' ayarına sahip; en yüksek efor ayarında (0.99) bildirilen satıcı benchmark'ları AIME 2026'da %97,1, GPQA Diamond'da %87,2, SWE-bench Verified'de %77,6, araç kullanımlı HLE'de %46,0 ve VoiceBench'te %91,4"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "Thinking Machines Lab, Inkling'in 'bugün mevcut olan en güçlü model, açık ya da kapalı, olmadığını' kendisi belirtiyor"
    type: statement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Mira Murati'nin OpenAI baş teknoloji sorumluluğu görevinden ayrıldıktan
sonra kurduğu yapay zeka şirketi Thinking Machines Lab, ilk modeli
Inkling'i 15 Temmuz 2026'da yayınladı [1][2]. Inkling, 975 milyar toplam
parametreye ve token başına 41 milyar aktif parametreye sahip seyrek bir
mixture-of-experts modeli (256 uzman artı 2 paylaşılan uzman arasında
yönlendirme yapan, token başına 6 aktif uzmanlı 66 katmanlı bir
transformer), 1 milyon token'a kadar bağlam penceresi ve metin, görüntü,
ses ve video içeren 45 trilyon token ile eğitim, metin çıktısı üretiyor
[1][2]. Daha küçük bir önizleme eşlik modeli olan Inkling-Small (276 milyar
toplam / 12 milyar aktif parametre) da birlikte duyuruldu, ancak ağırlıkları
duyuru anında henüz yayınlanmamıştı [1][2].

Ağırlıklar Apache 2.0 lisansı altında yayınlanıyor ve Hugging Face'ten hem
BF16 hem de NVFP4 nicemlenmiş biçimlerde indirilebiliyor; transformers,
SGLang ve vLLM çıkarım kütüphanelerinde aynı gün destek ve Tinker, Together
AI, Fireworks, Modal, Databricks, Baseten üzerinden barındırılan erişim
sunuluyor [1][2][3]. Ağırlıkların kullanımı, Apache 2.0 lisansının üzerine
eklenen ve gözetim, aldatma, bireyler hakkında tamamen otomatikleştirilmiş
yüksek riskli kararları yasaklayan Thinking Machines'in kendi kabul
edilebilir kullanım politikasına da tabi [1][2].

Inkling, kullanıcının yanıt kalitesi ile maliyet ve gecikme arasında denge
kurmasını sağlayan bir "kontrol edilebilir düşünme eforu" ayarına sahip.
En yüksek ayarda Thinking Machines, AIME 2026'da %97,1, GPQA Diamond'da
%87,2, SWE-bench Verified'de %77,6, araç kullanımlı HLE'de %46,0 ve
VoiceBench'te %91,4 benchmark puanları bildiriyor [1][2] — bunlar şirketin
kendi model kartından gelen, henüz bağımsız olarak doğrulanmamış rakamlar.
Şirket, Inkling'in "bugün mevcut olan en güçlü model, açık ya da kapalı,
olmadığını" kendisi açıkça belirtiyor [1].

## Neden önemli

Bu, Thinking Machines Lab'ın kuruluşundan bu yana yayınladığı ilk model ve
eski bir OpenAI CTO'sunun kurduğu, iyi finanse edilmiş bir laboratuvardan
gelen tam anlamıyla açık ağırlıklı bir yayın (Apache 2.0, tüm kontrol
noktaları herkese açık) — bu, öncü ölçekteki ağırlıkları kapalı tutan
laboratuvarlarla tezat oluşturuyor. Benchmark rakamları satıcı tarafından
sağlanıyor ve şimdiye kadar bağımsız bir değerlendirici tarafından
doğrulanmadı; modelin dışarıdan araştırmacılar ve değerlendiriciler
tarafından bağımsız olarak test edildiğinde nasıl performans göstereceği
açık bir soru olarak kalıyor.
