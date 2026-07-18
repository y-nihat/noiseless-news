---
title: Hugging Face, üretim altyapısındaki bir ihlale otonom bir yapay zekâ ajanının yol açtığını söylüyor
date: 2026-07-16
slug: huggingface-ai-agent-security-breach
lang: tr
tldr: >
  Hugging Face, 16 Temmuz 2026'da üretim altyapısının bir kısmının ele
  geçirildiğini ve saldırının "baştan sona, otonom bir yapay zekâ ajan
  sistemi tarafından yürütüldüğünü" açıkladı; saldırının veri kümesi
  hattındaki açıklardan yararlandığı, kimlik bilgilerini topladığı ve bir
  hafta sonu boyunca dahili sistemler arasında hareket ettiği belirtiliyor.
  Şirket, herkese açık modellerde, veri kümelerinde veya Spaces'te herhangi
  bir kurcalamaya rastlamadığını ancak ortak veya müşteri verilerinin
  etkilenip etkilenmediğini hâlâ değerlendirdiğini söylüyor -- bir insan
  operatör yerine bir yapay zekâ ajanının iddia edilen şekilde bir izinsiz
  girişi yürüttüğü erken bir gerçek dünya örneği.
sources:
  - name: Hugging Face — Güvenlik olayı açıklaması
    url: https://huggingface.co/blog/security-incident-july-2026
  - name: TechRepublic
    url: https://www.techrepublic.com/article/news-hugging-face-ai-agent-cyberattack-production-systems/
claims:
  - text: "Hugging Face, 16 Temmuz 2026 tarihli bir blog yazısında, üretim altyapısının bir kısmının, baştan sona otonom bir yapay zekâ ajan sistemi tarafından yürütüldüğünü söylediği bir saldırıyla ele geçirildiğini açıkladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Hugging Face'in saldırı anlatımına göre: kötü amaçlı bir veri kümesi, bir veri kümesi yükleyicisindeki uzaktan kod yürütme açığından ve veri kümesi yapılandırmasındaki bir şablon enjeksiyonu açığından yararlanarak bir veri işleme işçisi üzerinde kod yürütme elde etti; ardından saldırgan yetkilerini yükseltti, bulut ve küme kimlik bilgilerini topladı ve bir hafta sonu boyunca dahili altyapı genelinde yanal olarak hareket etti"
    type: statement
    verdict: single-source
    evidence: [1]
  - text: "Hugging Face, sınırlı sayıda dahili veri kümesine ve birkaç hizmet kimlik bilgisine izinsiz erişim tespit ettiğini, ancak herkese açık, kullanıcıya yönelik modellerde, veri kümelerinde veya Spaces'te herhangi bir kurcalama kanıtı bulamadığını ve yazılım tedarik zincirinin (konteyner imajları ve yayımlanan paketler) temiz olduğunun doğrulandığını söylüyor"
    type: statement
    verdict: single-source
    evidence: [1]
  - text: "Hugging Face, ortak veya müşteri verilerinin etkilenip etkilenmediğine ilişkin değerlendirmesini hâlâ tamamlamakta olduğunu ve etkilenen taraflarla doğrudan iletişime geçeceğini belirtiyor"
    type: statement
    verdict: confirmed
    evidence: [1]
  - text: "Hugging Face'in kendi adli analiz ekibi, ticari API modellerinin güvenlik korkulukları bu talepleri engelledikten sonra, kaydedilen saldırgan eylemlerini ve istismar yüklerini analiz etmek için dahili altyapıda çalıştırılan açık ağırlıklı GLM 5.2 modelini kullandı ve hassas verilerin şirket dışına çıkmasını önledi"
    type: statement
    verdict: single-source
    evidence: [1]
updated: []
---

## Ne oldu

Hugging Face, 16 Temmuz 2026'da üretim altyapısının bir kısmının ele
geçirildiğini ve izinsiz girişin "baştan sona, otonom bir yapay zekâ ajan
sistemi tarafından yürütüldüğünü" açıkladı [1][2]. Şirketin kendi
anlatımına göre, kötü amaçlı bir veri kümesi, bir veri kümesi
yükleyicisindeki uzaktan kod yürütme açığı ile veri kümesi
yapılandırmasındaki bir şablon enjeksiyonu açığını birlikte kullanarak
saldırgana bir veri işleme işçisi üzerinde kod yürütme imkânı sağladı.
Hugging Face'e göre saldırgan buradan itibaren yetkilerini yükseltti,
bulut ve küme kimlik bilgilerini topladı ve bir hafta sonu boyunca dahili
sistemler arasında yanal olarak hareket etti [1].

Hugging Face, sınırlı sayıda dahili veri kümesine ve hizmetlerinde
kullanılan birkaç kimlik bilgisine izinsiz erişim tespit ettiğini, ancak
herkese açık, kullanıcıya yönelik modellerde, veri kümelerinde veya
Spaces'te herhangi bir kurcalama kanıtı bulamadığını ve yazılım tedarik
zincirinin -- konteyner imajları ve yayımlanan paketler -- temiz olduğunun
doğrulandığını söylüyor [1]. Şirket, ortak veya müşteri verilerinin
etkilenip etkilenmediğine ilişkin değerlendirmesinin hâlâ sürdüğünü ve bu
inceleme tamamlandığında etkilenen taraflarla doğrudan iletişime
geçeceğini belirtiyor [1].

Tespit, güvenlik telemetrisinin LLM tabanlı triyajına dayandı; sonraki
adli inceleme ise 17.000'den fazla kaydedilen saldırgan eylemini işlemek
için LLM analiz ajanlarını kullandı [1]. Bu adli çalışma sırasında Hugging
Face'in kendi analistleri, ticari modellerin güvenlik korkulukları
istismar yüklerini analiz etme taleplerini engellediği için, dahili
altyapıda çalıştırılan açık ağırlıklı GLM 5.2 modeline geçti -- bu,
Hugging Face'in savunma tarafının bir çözümüdür, saldırgan davranışı
değildir [1].

Saldırı zincirinin ayrıntıları, saldırganın araç setine ilişkin "otonom
yapay zekâ ajanı" nitelendirmesi ve kimlik bilgisi/veri kümesi erişimi
rakamlarının hiçbiri Hugging Face'in kendi açıklamasının ötesinde bağımsız
olarak doğrulanmadı; herhangi bir saldırgan, tehdit aktörü grubu veya ajan
çerçevesi adı belirlenmedi [1][2].

## Neden önemli

Hugging Face'in anlatımı doğrulanırsa, bu, bir şirketin gerçek dünyadaki
bir üretim ihlalini, klavye başında doğrudan bir insan yerine baştan sona
otonom çalışan bir yapay zekâ ajanına atfettiği kamuya açıklanmış ilk
vakalardan biri olur -- güvenlik araştırmacılarının şimdiye kadar
belgelemek yerine öngördüğü türden bir senaryo [1][2]. Yapay zekâ
sektörünün büyük bir kısmına model ve veri kümesi barındıran bir
platformda, ortak ve müşteri verilerinin etkilenip etkilenmediğine dair
hâlâ açık olan soru, Hugging Face'in soruşturması devam ettikçe
değişmesi en muhtemel ayrıntı.
