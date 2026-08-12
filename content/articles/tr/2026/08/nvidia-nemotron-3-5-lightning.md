---
title: Nvidia, ajan görevlerinde hıza odaklanan açık ağırlıklı 30B model Nemotron 3.5 Lightning'i yayınladı
date: 2026-08-11
published: 2026-08-12
slug: nvidia-nemotron-3-5-lightning
lang: tr
tldr: >
  Nvidia, 11 Ağustos'ta Nemotron 3.5 Lightning'i yayınladı; araç çağrıları
  ve bilgi getirme gibi yoğun hacimli ajan görevleri için tasarlanmış,
  3 milyar aktif parametreli, açık ağırlıklı 30 milyar parametrelik bir
  karma-uzman (MoE) model. Artificial Analysis'in bağımsız testi, modeli
  Zeka Endeksi'nde gpt-oss-120b ile eşit puanladı; Nvidia'nın kendi
  PinchBench testinde Qwen3.6 35B'yi yüzde 30 farkla geçtiği iddiası
  şirket dışında doğrulanmadı.
sources:
  - name: NVIDIA Technical Blog
    url: https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/articles/nemotron-3-5-lightning-launch
  - name: The Decoder
    url: https://the-decoder.com/nvidias-open-weight-nemotron-3-5-lightning-prioritizes-speed-over-maximum-intelligence/
claims:
  - text: "Nvidia, 11 Ağustos 2026'da, 3 milyar aktif parametreli, açık ağırlıklı, 30 milyar parametrelik bir karma-uzman (MoE) model olan Nemotron 3.5 Lightning'i yayınladı"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Model, ticari kullanıma açık, izin verici OpenMDW-1.1 lisansı altında yayınlandı; ağırlıklar Hugging Face ve Nvidia'nın build.nvidia.com platformunda mevcut"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Artificial Analysis'in bağımsız testi modeli Zeka Endeksi'nde 24 puanla gpt-oss-120b ile eşit puanladı; tek bir sağlayıcının ön-sürüm ölçümü çıktı hızını saniyede yaklaşık 670 token olarak buldu, ancak Artificial Analysis'in sağlayıcılar arasında topladığı yayın-sonrası rakam bunun altında"
    type: capability
    verdict: confirmed
    evidence: [2, 3]
  - text: "Nvidia, modelin PinchBench ajan görevlerinin yüzde 86'sını doğru tamamladığını ve Qwen3.6 35B'den yüzde 30 daha hızlı bitirdiğini söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

Nvidia, 11 Ağustos'ta Nemotron 3.5 Lightning'i yayınladı; Nemotron 3
ailesinde kullanılan hibrit Mamba-Transformer mimarisi üzerine kurulu,
30 milyar toplam, token başına 3 milyar aktif parametreli, açık ağırlıklı
bir karma-uzman (MoE) model [1]. Model, ticari kullanıma açık, izin verici
OpenMDW-1.1 koşulları altında lisanslandı; ağırlıklar BF16 ve NVFP4
formatlarında Hugging Face ile Nvidia'nın build.nvidia.com platformuna
yüklendi [1].

Nvidia, modeli maksimum akıl yürütme kapasitesinden çok, ajan
sistemlerinin yoğun hacimli "ağır iş" katmanı için konumlandırıyor: araç
çağrıları, doğrulama, bilgi getirme, biçimlendirme [1]. Artificial
Analysis'in bağımsız testi, modeli Zeka Endeksi'nde 24 puanla, aktif
parametresinin yaklaşık dörtte biri kadarını kullanmasına rağmen
gpt-oss-120b ile eşit puanladı [2]. Tek bir barındırma sağlayıcısının
ön-sürüm ölçümü, çıktı hızını Google'ın Gemini 3.5 Flash-Lite'ının neredeyse
iki katı olan saniyede yaklaşık 670 token olarak buldu; Artificial
Analysis'in yayın sonrası sağlayıcılar arasında topladığı canlı takip
sayfası ise saniyede yaklaşık 292 tokenlik daha düşük bir medyan, en hızlı
sağlayıcıda ise yaklaşık 594 token gösteriyor [2]. Nvidia'nın kendi
PinchBench ajan-görev testinden gelen rakamlar, yüzde 86 doğruluk ve
Qwen3.6 35B'den yüzde 30 daha hızlı tamamlama iddia ediyor; bu rakamlar
bağımsız olarak yeniden üretilmedi [1].

## Neden önemli

Nemotron 3.5 Lightning, CEO Jensen Huang'ın Washington'da açık kaynaklı
yapay zekâ politikası tartışmasına dahil olmasından bu yana Nvidia'nın ilk
açık ağırlıklı model yayını. Bağımsız Zeka Endeksi sonucu tek başına
anlamlı: 3 milyar aktif parametreli bir modelin, üçüncü taraf bir
kıyaslamada çok daha büyük açık bir modelle eşleşmesi, Nvidia'nın
ajan-hattı iş yükleri için "büyüklük yerine hız" iddiasını destekliyor —
ancak baştan başa verim ve PinchBench rakamları hâlâ normal kullanımda
sınanması gereken en iyi durum ölçümleri.
