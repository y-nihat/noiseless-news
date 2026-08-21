---
title: Cohere Labs ön baskısı, kültürel işaretlerin LLM eğitim verisinde pretraining sonrasında büyük ölçüde kaybolduğunu buldu
date: 2026-08-19
published: 2026-08-21
slug: cohere-culture-funnel-training-data
lang: tr
tldr: >
  Cohere Labs'ın 5,6 milyon LLM eğitim örneğini analiz eden bir ön baskısı,
  açık kültürel sinyallerin pretraining ile post-training arasında keskin
  biçimde azaldığını ve geriye kalanların coğrafi olarak Hindistan, Çin ve
  ABD'ye yoğunlaştığını bildiriyor. İnce ayar deneylerinde kültürel
  işaretlerin geri eklenmesi, genel yetenekte bildirilen bir düşüş olmadan
  üç kültür/önyargı benchmark'ını iyileştirdi. Bulgu, henüz hakem
  denetiminden geçmemiş bir arXiv ön baskısında açıklanıyor.
sources:
  - name: Cohere Blog
    url: https://cohere.com/blog/the-culture-funnel-you-cant-align-what-isnt-in-the-data
  - name: arXiv cs.AI+cs.LG+cs.CL
    url: https://arxiv.org/abs/2606.13808
claims:
  - text: "Cohere Labs araştırmacıları, pretraining, denetimli ince ayar (SFT), hizalama ve muhakeme aşamaları boyunca 5,6 milyon eğitim örneğini analiz etti; kültürel sinyalleri Cohere'in kendi Command A modeliyle etiketledi ve bir alt kümeyi altı dilde manuel olarak doğruladı; açık kültürel sinyallerin post-training sırasında keskin biçimde azaldığını, geriye kalan kültürel olarak etiketlenmiş verinin ise coğrafi olarak yoğunlaştığını bildiriyorlar -- Hindistan, Çin ve ABD baskın, Güney Amerika ve Afrika'nın temsili ise minimal (ön baskı -- hakem denetiminden geçmedi)"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "Sonraki ince ayar deneylerinde, kültürel işaretlerin eğitim verisine geri eklenmesi, genel yetenek puanlarında bildirilen bir düşüş olmadan NormAd'da +%8, BBQ'da +%6 ve GMMLU'da +%2,3 performans artışı sağladı (ön baskı -- hakem denetiminden geçmedi)"
    type: research
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## Ne oldu

19 Ağustos 2026'da yayınlanan bir Cohere Labs ön baskısı, büyük dil
modellerinin pretraining'den tamamlanmış, post-training sonrası modele giden
yolda açık kültürel bağlamlarının çoğunu kaybettiğini öne sürüyor [1][2].
Ekip, pretraining, denetimli ince ayar, hizalama ve muhakeme aşamaları
boyunca 5,6 milyon eğitim örneği genelinde kültürel sinyalleri -- alan, görev
niyeti, dil, coğrafi konum ve kültürel özellikler -- etiketledi; verileri
otomatik etiketlemek için Cohere'in kendi Command A modelini kullandı ve bir
alt kümeyi altı dilde manuel olarak doğruladı [1][2]. Kültürel olarak
işaretlenmiş verinin pretraining sırasında görece bol olduğunu, ancak
pipeline post-training'e doğru ilerledikçe -- az kültürel sinyal taşıyan
matematik ve kod gibi teknik alanlara giderek daha fazla öncelik verildiği
için -- keskin biçimde azaldığını bildiriyorlar [1]. Geriye kalan kültürel
olarak etiketlenmiş veri içinde temsil, uzun kuyruklu bir çarpıklık
izliyor: Hindistan, Çin ve ABD baskın konumda, Güney Amerika ve Afrika ise
neredeyse hiç temsil edilmiyor; daha fazla dil eklemek coğrafi yayılımı
yalnızca marjinal olarak artırıyor [1][2].

Bir takip deneyinde araştırmacılar, kültürel işaretleri eğitim verisine geri
ekleyerek ince ayar yaptı ve üç üçüncü taraf kültür/önyargı benchmark'ında
kazanç bildirdi -- NormAd'da +%8, BBQ'da +%6 ve GMMLU'da +%2,3 -- genel
yetenek puanlarında bildirilen bir düşüş olmadan [1][2]. Ekip ayrıca 5,6
milyon örneklik etiketlenmiş veri setini kamuya açık yayınladı. Çalışma, ilk
kez 11 Haziran 2026'da gönderilen bir arXiv ön baskısında (2606.13808)
açıklanıyor; bu baskı henüz hiçbir yerde hakem denetiminden geçmedi veya
kabul edilmedi [2]; bulguların bağımsız bir tekrar üretimi şu an mevcut
değil.

## Neden önemli

Sohbet botlarını kültürel olarak daha bilinçli hale getirme çabalarının
çoğu, modeli çıkarım (inference) zamanında hedef alıyor -- altta yatan
bilginin zaten orada olduğu varsayımıyla, modeli kültürel olarak bilgili
"davranması" için yönlendirmek veya ince ayar yapmak. Bu ön baskı, daha temel
sorunun yukarı akışta, post-training aşamasına hangi verinin ulaştığında
yattığını öne sürüyor. Geri kazanım deneyi, bağımsız olarak tekrar üretilmiş
bir bulgu değil, tek bir ekibin kendi ön baskısındaki, kendi modeli ve görev
setiyle elde ettiği bir sonuç -- ama yalnızca bir teşhis değil, somut bir
kaldıraç sunuyor: ince ayara hangi verinin girdiği.
