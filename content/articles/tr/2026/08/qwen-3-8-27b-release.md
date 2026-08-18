---
title: Qwen, açık ağırlıklı Qwen3.8-27B'yi yayınladı; bağımsız kıyaslamada GPT-5.6 Luna ile eşitlendi
date: 2026-08-14
published: 2026-08-18
slug: qwen-3-8-27b-release
lang: tr
tldr: >
  Alibaba'nın Qwen ekibi, 14 Ağustos civarında Qwen3.8-27B'yi yayınladı:
  Apache 2.0 lisansı altında, 27 milyar parametreli, yoğun (dense) açık
  ağırlıklı bir model; görüntü ve video anlama yeteneğine ve 262.144
  token'lık bir bağlam penceresine sahip. Artificial Analysis'in bağımsız
  testi, modeli Zeka Endeksi'nde 52 puanla OpenAI'nin GPT-5.6 Luna'sıyla
  eşit, GLM-5.2 ve DeepSeek V4 Pro 0813'ün -- ikisi de çok daha büyük
  karma-uzman modelleri -- bir puan gerisinde konumlandırdı. Qwen'in kendi
  kodlama kıyaslama rakamları satıcı beyanı niteliğinde ve bağımsız olarak
  doğrulanmadı.
sources:
  - name: Qwen (Hugging Face model card)
    url: https://huggingface.co/Qwen/Qwen3.8-27B
  - name: Simon Willison's Weblog
    url: https://simonwillison.net/2026/Aug/16/qwen-38-27b/
  - name: VentureBeat AI
    url: https://venturebeat.com/technology/qwen3-8-27b-runs-frontier-class-coding-agents-and-reasoning-locally-no-cloud-api-required
  - name: Artificial Analysis (Qwen3.8-27B)
    url: https://artificialanalysis.ai/models/qwen3-8-27b
  - name: Artificial Analysis (GPT-5.6 Luna)
    url: https://artificialanalysis.ai/models/gpt-5-6-luna
  - name: Artificial Analysis (GLM-5.2)
    url: https://artificialanalysis.ai/models/glm-5-2
  - name: Artificial Analysis (DeepSeek V4 Pro 0813)
    url: https://artificialanalysis.ai/models/deepseek-v4-pro
claims:
  - text: "Alibaba'nın Qwen ekibi, yaklaşık 14 Ağustos 2026'da, Hugging Face üzerinde Apache 2.0 lisansı altında 27 milyar parametreli, yoğun (dense), açık ağırlıklı, çok modlu Qwen3.8-27B modelini yayınladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Qwen3.8-27B, doğal olarak 262.144 token'lık (YaRN ile 1 milyona kadar genişletilebilir) bir bağlam penceresine ve görüntü/video anlama yeteneğine sahip; model 16-bit hassasiyette yaklaşık 56GB, FP8'de yaklaşık 28GB, 4-bit nicelleştirmede ise yaklaşık 17GB GPU belleğiyle yerel olarak çalıştırılabiliyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 2]
  - text: "Artificial Analysis'in bağımsız testi Qwen3.8-27B'yi Zeka Endeksi'nde 52 puanla GPT-5.6 Luna (52) ile eşit, GLM-5.2 ve DeepSeek V4 Pro 0813'ün (ikisi de 53 puan) bir puan gerisinde konumlandırdı -- bu iki model sırasıyla 753 milyar toplam/40 milyar aktif ve 1,6 trilyon toplam/49 milyar aktif parametreli, çok daha büyük karma-uzman (MoE) modelleri; Qwen3.8-27B ise 27 milyar parametrenin tamamını kullanan yoğun bir model"
    type: capability
    verdict: confirmed
    evidence: [4, 5, 6, 7]
  - text: "Qwen, modelin SWE-bench Pro'da 61,7 ve Terminal Bench 2.1'de 73,0 puan aldığını bildiriyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

Alibaba'nın Qwen araştırma ekibi, yaklaşık 14 Ağustos 2026'da Qwen3.8-27B'yi
Hugging Face üzerinde yayınladı: izin verici Apache 2.0 koşulları altında
lisanslanmış, 27 milyar parametreli, yoğun bir model [1]. Hem görüntüleri hem
videoları anlayabilen, doğal bir görme-dil modeli; bağlam penceresi doğal
olarak 262.144 token, YaRN ile 1 milyona kadar genişletilebiliyor [1]. Modeli
kendisi çalıştıran bağımsız geliştirici Simon Willison, modelin kutudan
çıktığı haliyle akıl yürütme çabası ayarının kötü seçildiğini belirterek
düşürülmesini önerdi; ayar kullanıcı tarafından değiştirilebiliyor [2].

Modelin donanım ayak izi, yetenek sınıfına göre alışılmadık derecede küçük.
VentureBeat, tam 16-bit hassasiyette çalıştırmanın yaklaşık 56GB GPU belleği
gerektirdiğini ve FP8 sürümünün yaklaşık 28GB'a ihtiyaç duyduğunu
bildiriyor [3]; 4-bit nicelleştirilmiş sürüm ise yaklaşık 17GB'a iniyor -- tek
bir üst düzey tüketici GPU'sunun erişimi dahilinde -- ve bu rakam Willison'ın
kendi yerel 4-bit testiyle bağımsız olarak örtüşüyor [2].

Artificial Analysis'in bağımsız testi, Qwen3.8-27B'yi Zeka Endeksi'nde 52
puanla, OpenAI'nin tescilli GPT-5.6 Luna'sıyla (o da 52) eşit, GLM-5.2 ve
DeepSeek V4 Pro 0813'ün (ikisi de 53 puan) ise bir puan gerisinde
konumlandırdı [4][5][6][7]. Daha yüksek puan alan bu iki model de,
Qwen3.8-27B'nin 27 milyar yoğun parametresine kıyasla token başına daha fazla
parametre aktive eden karma-uzman (MoE) sistemleri -- GLM-5.2, 753 milyar
toplam parametresinin 40 milyarını; DeepSeek V4 Pro 0813 ise 1,6 trilyon
toplamının 49 milyarını aktive ediyor -- yani aktif hesaplamada gerçek ama
mütevazı, 1,5-1,8 kat'lık bir fark var; salt toplam parametre sayılarının
düşündürdüğü kadar büyük bir fark değil [4][5][6]. Artificial Analysis'in
kendi değerlendirme verileri, Qwen3.8-27B'nin test sırasında modeller arası
ortalama yaklaşık 43 milyona karşılık yaklaşık 160 milyon çıktı token'ı
ürettiğini gösteriyor; yani puanının bir kısmı, aynı maliyetle daha büyük
modellerle eşleşmekten değil, yanıt başına önemli ölçüde daha fazla çıktı
üretmekten kaynaklanıyor [4]. Qwen'in kodlama ve ajan görevi
kıyaslamalarında bildirdiği kendi rakamları -- SWE-bench Pro'da 61,7 ve
Terminal Bench 2.1'de 73,0 dahil -- bağımsız olarak yeniden üretilmedi [1].

## Neden önemli

Kendisinden çok daha büyük iki karma-uzman modelin bir puan gerisinde kalan
ve tescilli bir sınır modeliyle tam olarak eşitlenen, 27 milyar parametreli
yoğun bir modelin varlığı, açık ağırlıklı küçük modellerin bu yılki genel
yetenek açığını daraltma eğilimini sürdürüyor; üstelik bunu veri merkezi
ölçeğinde donanım yerine tek bir tüketici GPU'suyla yapabiliyor. Bu
karşılaştırmanın bir kaydı var: Qwen3.8-27B'nin puanının bir kısmı,
endeksteki tipik modellerden belirgin şekilde daha fazla çıktı üretmesini
yansıtıyor ve bağımsız testler, varsayılan akıl yürütme ayarının kutudan
çıktığı haliyle kötü ayarlandığını buldu -- büyük modellerle eşleşmek
bedelsiz değil.
