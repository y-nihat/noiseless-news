---
title: Zhipu GLM-5.3'ü kullanıma sunuyor, açık ağırlıkları güvenlik incelemesi için iki hafta sonraya bırakıyor
date: 2026-08-14
published: 2026-08-18
slug: zhipu-glm-5-3-launch
lang: tr
tldr: >
  Çinli yapay zekâ şirketi Zhipu (Z.ai), 14 Ağustos 2026'da GLM-5.3 modelini
  kodlama planı ve API'si üzerinden kullanıma sundu; modeli kodlama ve siber
  güvenlik işleri için konumlandırdı. Model, bağımsız Artificial Analysis
  Intelligence Index'te Kimi K3 ile aynı düzeyde 60 puan alıyor. Zhipu, ek
  güvenlik testleri tamamlanana kadar modelin açık ağırlıklarını ve bazı
  siber güvenlik özelliklerine erişimi yaklaşık iki hafta sonraya
  bıraktığını söylüyor -- bu, önceden verilen bir sözden geri adım değil,
  lansmanla birlikte açıklanan bir plan. Zhipu'nun modelin siber güvenlik
  karşılaştırma iddiaları henüz bağımsız olarak doğrulanmadı.
sources:
  - name: Zhipu AI (Z.ai)
    url: https://www.zhipuai.cn/zh/research/162
  - name: Artificial Analysis
    url: https://artificialanalysis.ai/models/glm-5-3
claims:
  - text: "Zhipu (Z.ai), 14 Ağustos 2026'da GLM-5.3'ü GLM Kodlama Planı ve API'si üzerinden kullanıma sundu; modeli 'Built to Code. Ready for Cyber Defense' ('Kodlamak İçin İnşa Edildi. Siber Savunmaya Hazır') sloganıyla konumlandırdı"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Zhipu, GLM-5.3'ün açık ağırlık paylaşımını ve bazı hassas siber güvenlik özelliklerine erişimi, ek güvenlik değerlendirmesi ve sağlamlaştırma çalışmalarını tamamlamak için lansmandan yaklaşık iki hafta sonrasına bıraktığını açıkladı -- bu zaman çizelgesi lansmanla birlikte duyuruldu, daha sonra ortaya çıkan bir gecikme değil"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "GLM-5.3, azami akıl yürütme yapılandırmasında Artificial Analysis Intelligence Index'te 60 puan alarak takip edilen 181 model arasında 8. sırada yer alıyor; bu puan Kimi K3 ile aynı düzeyde, Opus 5'in (~63) ve Fable 5'in (~62) gerisinde"
    type: capability
    verdict: confirmed
    evidence: [2]
  - text: "Zhipu, GLM-5.3'ün karşılaştırdığı rakip modellere kıyasla bir güvenlik açığı tespit karşılaştırması olan CyberGym'de %84,5 ile önde olduğunu, ancak bir istismar zincirini eksiksiz tamamlamayı ölçen ExploitBench'te rakip modellerin yetmişli yılların üst sınırındaki puanlarının gerisinde kalarak %54,4 aldığını bildiriyor; bu rakamlar tamamen Zhipu'nun kendi testlerine dayanıyor ve bağımsız olarak doğrulanmadı"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

Z.ai markası altında faaliyet gösteren Çinli yapay zekâ şirketi Zhipu, 14
Ağustos 2026'da GLM-5.3 modelini kodlama planı ve API'si üzerinden
kullanıma sundu; modeli "Built to Code. Ready for Cyber Defense" ("Kodlamak
İçin İnşa Edildi. Siber Savunmaya Hazır") sloganıyla pazarladı [1]. Zhipu,
ek güvenlik değerlendirmesi ve sağlamlaştırma çalışmalarını tamamlamak
için modelin açık ağırlık paylaşımını ve bazı hassas siber güvenlik
yeteneklerine erişimi lansmandan yaklaşık iki hafta sonrasına bıraktığını
söylüyor [1]. Bu zaman çizelgesi, daha sonra bir gecikme olarak değil,
lansmanla birlikte açıklandı.

Bağımsız Artificial Analysis Intelligence Index'te GLM-5.3'ün azami akıl
yürütme yapılandırması 60 puan alarak takip edilen 181 model arasında 8.
sırada yer alıyor -- Kimi K3 ile aynı düzeyde, Opus 5'in (yaklaşık 63) ve
Fable 5'in (yaklaşık 62) gerisinde [2]. Ayrı olarak Zhipu, modelin kendi
siber güvenlik karşılaştırma sonuçlarını da paylaştı: GLM-5.3, Zhipu'nun
karşılaştırdığı rakip modellere kıyasla bir güvenlik açığı tespit
karşılaştırması olan CyberGym'de %84,5 puanla önde; ancak bir güvenlik
açığını eksiksiz bir istismar zincirine dönüştürmeyi ölçen ExploitBench'te,
rakip bir modelin yetmişli puanların üst sınırındaki skorunun gerisinde
kalarak %54,4 alıyor [1]. Bu siber güvenlik rakamları tamamen Zhipu'nun
kendi testlerinden geliyor; modelin ağırlıkları henüz herkese açık
olmadığından, hiçbir dış laboratuvar bu sonuçları tekrarlayamadı.

## Neden önemli

GLM-5.3, henüz gelecek bir duyuru değil, canlı ve kullanılabilir bir
lansman -- ağırlıkların bekletilmesi, ürünün alıkonması değil, tek bir
bileşenin aşamalı olarak sunulması anlamına geliyor. Zhipu, iki haftalık
bu aralığı, sonradan açıklanan bir durum olarak değil, modelin kendi
güvenlik açığı bulma yeteneğine bağlı açık bir güvenlik önlemi olarak
sunuyor. Şirketin siber güvenlik sonuçları da tek bir karşılaştırmanın
işaret edebileceğinden daha karışık: güvenlik açıklarını bulmakta güçlü,
bunları çalışan bir istismara dönüştürmekte daha zayıf -- bu yeteneği
tanımlayan her rakamın şu an için yalnızca Zhipu'dan gelmesi nedeniyle
akılda tutulması gereken bir ayrım.
