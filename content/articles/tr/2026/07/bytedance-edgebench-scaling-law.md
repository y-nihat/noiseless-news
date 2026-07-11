---
title: ByteDance Seed, EdgeBench'i yayınladı; AI ajanlarının gerçek dünya ortamlarından öğrenmesi için yeni bir ölçeklendirme yasası bildiriyor
date: 2026-07-02
slug: bytedance-edgebench-scaling-law
lang: tr
tldr: >
  ByteDance'in Seed ekibi, 2 Temmuz 2026'da EdgeBench'i yayınladı; bu, AI
  ajanlarının eğitimden sonra bir ortamla uzun süre etkileşerek ne kadar
  geliştiğini ölçmek için tasarlanmış, her biri 12+ saat süren 134 gerçek
  dünya görevinden oluşan bir benchmark. Ekip, yaklaşık 38.000 saatlik ajan
  etkileşimini analiz ederek, ajanların dağıtım-sonrası öğrenme hızının son
  model nesilleri boyunca kabaca her üç ayda bir iki katına çıktığını gösteren
  log-sigmoid bir "ölçeklendirme yasası" (R² = 0,998) bildiriyor. Bulgu, henüz
  hakem denetiminden geçmemiş bir arXiv ön baskısında (preprint) açıklanıyor.
sources:
  - name: ByteDance Seed
    url: https://seed.bytedance.com/en/blog/edgebench-measuring-real-world-environment-learning-and-discovering-a-new-scaling-law
  - name: arXiv cs.AI+cs.LG+cs.CL
    url: https://arxiv.org/abs/2607.05155
  - name: South China Morning Post
    url: https://www.scmp.com/tech/big-tech/article/3359373/chinas-bytedance-discovers-new-scaling-law-could-sustain-ai-boom
claims:
  - text: "ByteDance Seed, 2 Temmuz 2026'da EdgeBench'i yayınladı; bu, altı alanı (bilimsel keşif, yazılım mühendisliği, kombinatoryal optimizasyon, bilgi işi, formal matematik, interaktif oyunlar) kapsayan, her biri en az 12 saat kesintisiz ajan çalışması gerektiren 134 gerçek dünya görevinden oluşan bir benchmark; 134 görevden 51'i ve değerlendirme çerçevesi kamuya açık yayınlandı, kalanı kirlenmeyi önlemek için saklı tutuldu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Yaklaşık 38.000 saatlik ajan etkileşimini (402 öğrenme eğrisi) analiz eden ekip, ortam-öğrenme aşamasındaki genel ajan performansının etkileşim süresine karşı log-sigmoid bir eğri izlediğini (ortalama R² = 0,998) ve ajanların ortam etkileşiminden öğrenme hızının ardışık model nesilleri boyunca kabaca her üç ayda bir iki katına çıktığını bildiriyor (ön baskı — hakem denetiminden geçmedi)"
    type: research
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## Ne oldu

ByteDance'in Seed araştırma ekibi, 2 Temmuz 2026'da EdgeBench'i yayınladı; bu
benchmark çoğu mevcut testten farklı bir şeyi ölçmek için tasarlandı: bir
modelin zaten ne bildiğini değil, bir AI ajanının eğitildikten ve
dağıtıldıktan sonra gerçek bir ortamla ne kadar süre etkileştiği ölçüde ne
kadar geliştiğini [1][2]. Set, bilimsel keşif, yazılım mühendisliği,
kombinatoryal optimizasyon, profesyonel bilgi işi, formal matematik ve
interaktif oyunları kapsayan 134 görevden oluşuyor; her görev bir ajanı en az
12 saat kesintisiz çalıştırıyor, bazıları 72 saati aşıyor [1]. Ekip, 134
görevden 51'ini tam değerlendirme çerçevesiyle birlikte kamuya açık
yayınladı; kalan görevler özellikle benchmark kirlenmesini önlemek için saklı
tutuldu [1][2].

Benchmark'ı kullanarak ekip, 402 öğrenme eğrisi genelinde yaklaşık 38.000
saatlik ajan etkileşimini analiz etti ve bu "ortam öğrenme" aşamasındaki
performansın etkileşim süresine karşı log-sigmoid bir eğri izlediğini,
ortalama uyumun R² = 0,998 olduğunu bildiriyor [1]. Bu eğriden yola çıkarak,
ajanların ortam etkileşiminden öğrenme hızının son model nesilleri boyunca
kabaca her üç ayda bir iki katına çıktığını bildiriyorlar [1][2]. Bulgu,
arXiv'e yüklenen (2607.05155) ve henüz hiçbir yerde hakem denetiminden
geçmemiş veya kabul edilmemiş bir ön baskıda açıklanıyor [2]. South China
Morning Post, 4 Temmuz'da aynı rakamları bağımsız olarak haberleştirdi ama
bunları doğrulamadı veya bağımsız bir tekrar üretim bildirmedi [3].

## Neden önemli

AI laboratuvarları, modelleri geliştirmek için eğitim verisi ve hesaplama
gücünü ölçeklendirmeye dayandı; Epoch AI dahil araştırmacılar, kamuya açık
metin verisinin birkaç yıl içinde tükenebileceğini işaret etti. ByteDance'in
sonucu, ikinci bir kaldıraca kanıt olarak sunuluyor — ajanların yeniden
eğitimden bağımsız olarak, dağıtım sonrası gerçek ortamlarla etkileşerek
ölçülebilir şekilde gelişmesi — ama şu an tek bir ekibin kendi ön baskısına
ve kendi seçtiği görev setine dayanıyor, henüz bağımsız bir tekrar üretim
yok. R² uyumu, eğrinin ByteDance'in kendi ölçümleriyle ne kadar örtüştüğünü
gösteriyor, altta yatan eğilimin daha fazla model nesli ve dış
laboratuvarlarla test edildiğinde geçerli kalıp kalmayacağını değil.
