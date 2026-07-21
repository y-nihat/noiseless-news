---
title: Meta'nın SAM 3 ve DINOv3 görü modelleri, DOE'nin Genesis Mission bilim girişiminde kullanılıyor
date: 2026-07-21
slug: meta-synaps-genesis-mission
lang: tr
tldr: >
  Meta, 21 Temmuz 2026'da, açık kaynaklı görüntü işleme modelleri SAM 3 ve
  DINOv3'ün, röntgen ve nötron bilimi verilerinin analizini hızlandırmak
  için Enerji Bakanlığı süper bilgisayarlarına dağıtıldığını açıkladı. Bu,
  Beyaz Saray'ın Genesis Mission girişimi altında, Berkeley Lab
  öncülüğündeki SYNAPS-I projesinin bir parçası. İddia edilen işlem hızı
  artışı ve donanım ayrıntıları Meta'nın kendi anlatımına dayanıyor ve
  henüz DOE ya da ilgili ulusal laboratuvarlar tarafından bağımsız olarak
  doğrulanmadı.
sources:
  - name: Meta AI Blog
    url: https://ai.meta.com/blog/genesis-mission-lawrence-berkeley-national-laboratory-segment-anything-dino/
  - name: ABD Enerji Bakanlığı — Genesis Mission duyurusu
    url: https://www.energy.gov/articles/energy-department-launches-genesis-mission-transform-american-science-and-innovation
  - name: Lawrence Berkeley Ulusal Laboratuvarı — Elements
    url: https://elements.lbl.gov/news/supporting-does-genesis-mission/
claims:
  - text: "Genesis Mission, yapay zeka kullanarak bilimsel keşfi hızlandırmayı amaçlayan, ABD Enerji Bakanlığı öncülüğünde ulusal bir girişim; 24 Kasım 2025'te bir Beyaz Saray başkanlık kararnamesiyle başlatıldı ve DOE Bilim Alt Sekreteri Darío Gil misyon direktörü olarak atandı"
    type: announcement
    verdict: confirmed
    evidence: [2]
  - text: "SYNAPS-I, Berkeley Lab öncülüğünde, Argonne, Brookhaven, Oak Ridge ve SLAC'ın ortak olduğu çok laboratuvarlı bir girişim; DOE'nin kullanıcı tesislerinde röntgen ve nötron bilimi veri analizini gerçek zamanlı keşif sistemlerine dönüştürmeyi amaçlıyor"
    type: announcement
    verdict: confirmed
    evidence: [3]
  - text: "Meta, SAM 3 ve DINOv3 görü modellerini bilimsel görüntüleme verileri üzerinde ince ayardan geçirdiğini ve SYNAPS-I'in bölütleme (segmentasyon) hattının bir parçası olarak, NERSC dahil ulusal süper bilgisayar tesislerinde 300 A100 GPU üzerinde dağıttığını söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Meta, bir örnek uygulama için — kuraklığa tepkiyi incelemek amacıyla asma çubuklarının mikro-BT taramaları — daha önce zaman adımı başına bir aylık uzman etiketleme gerektiren işin artık 15 dakika sürdüğünü söylüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Meta'nın yazısı, Darío Gil'in Trillion Parameter Consortium'da verdiği ve verinin üretildiği anda analiz edilmesi yaklaşımını anlatan destekleyici bir alıntıyı SYNAPS-I için kullanıyor; alıntı, Meta'nın belirli araçlarını onaylamaktan çok genel olarak SYNAPS-I'e değiniyor"
    type: statement
    verdict: confirmed
    evidence: [1]
  - text: "Meta, SYNAPS-I'de beş ulusal laboratuvarda yaklaşık 60 araştırmacının yer aldığını ve DOE'nin röntgen ve nötron kaynağı tesislerindeki veri üretim hızının altı saniyede bir görüntüden saniyede 100.000 görüntüye kadar çıktığını söylüyor"
    type: research
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

Meta, 21 Temmuz 2026'da, açık kaynaklı görüntü işleme modelleri SAM 3
(Segment Anything Model 3) ve DINOv3'ün bilimsel görüntüleme verileri
üzerinde ince ayardan geçirildiğini ve NERSC dahil Enerji Bakanlığı süper
bilgisayarlarına, Lawrence Berkeley Ulusal Laboratuvarı öncülüğündeki bir
araştırma girişimi olan SYNAPS-I için analizleri hızlandırmak amacıyla
dağıtıldığını açıkladı [1]. SYNAPS-I, Beyaz Saray'ın 24 Kasım 2025'te bir
başkanlık kararnamesiyle başlattığı, yapay zeka ile bilimsel keşfi
hızlandırmayı amaçlayan DOE öncülüğündeki ulusal program Genesis Mission'ın
altında yer alıyor; DOE Bilim Alt Sekreteri Darío Gil misyon direktörü
olarak görev yapıyor [2]. SYNAPS-I'in kendisi, Berkeley Lab tarafından
bağımsız olarak, Argonne, Brookhaven, Oak Ridge ve SLAC'ın ortak olduğu,
DOE'nin yedi röntgen ve nötron kaynağı kullanıcı tesisinde çalışan çok
laboratuvarlı bir çaba olarak belgelenmiş durumda [3].

Meta'nın kendi modelleri için tanımladığı belirli rol — 300 A100 GPU
üzerinde ince ayardan geçirilip çalıştırılan SAM 3 ve DINOv3 — yalnızca
Meta'nın yazısına dayanıyor; ne DOE'nin ne de Berkeley Lab'ın kendi
materyalleri, SYNAPS-I'i anlatırken Meta, SAM veya DINOv3'ten bahsediyor
[1][2][3]. Aynı durum Meta'nın öne çıkan performans iddiası için de geçerli:
bir örnek olarak, kuraklığa tepkiyi incelemek için kullanılan asma
çubuklarının mikro-BT taramalarında, Meta daha önce zaman adımı başına bir
aylık uzman etiketleme gerektiren analizin artık 15 dakika sürdüğünü
söylüyor [1] — bu, Meta'nın kendi anlatımına dayanan, henüz bağımsız olarak
doğrulanmamış bir yetenek iddiası. Meta'nın yazısı ayrıca Gil'in, verinin
üretildiği anda analiz edilmesi yaklaşımına dair bir alıntısını içeriyor;
Trillion Parameter Consortium'da verilen bu alıntı, Meta'nın araçlarını özel
olarak onaylamaktan çok genel olarak SYNAPS-I projesine değiniyor [1]. Meta
ayrıca beş ulusal laboratuvarda yaklaşık 60 araştırmacının yer aldığını ve
DOE tesislerindeki veri üretim hızının altı saniyede bir görüntüden saniyede
100.000 görüntüye kadar çıktığını belirtiyor; bu rakamlar da yalnızca
Meta'nın kendi anlatımında yer alıyor [1]; Berkeley Lab'ın kamuya açık
materyalleri, tesislerin petabayt ölçeğinde veri ürettiğini doğruluyor ancak
Meta'nın verdiği yıllık rakamı veya hızı vermiyor [3].

## Neden önemli

Genesis Mission, yapay zekayı ABD'nin ulusal laboratuvar biliminin
merkezine yerleştirmeye yönelik önemli bir federal girişim ve bu, Meta'nın
buradaki rolüne dair ilk ayrıntılı kamuya açık anlatımı — ancak somut teknik
iddialar (GPU sayısı, hız artışı rakamı, araştırmacı sayısı) şu an için
yalnızca Meta'nın anlatımına dayanıyor; DOE ve Berkeley Lab'ın kendi
materyalleri projeyi ve hedeflerini doğruluyor ama Meta'nın belirli katkısını
teyit etmiyor.
