---
title: ByteDance, AI video üretim modelinin güncellemesi Seedance 2.5'i piyasaya sürdü
date: 2026-07-31
slug: bytedance-seedance-2-5-launch
lang: tr
tldr: >
  ByteDance, 31 Temmuz 2026'da AI video üretim modelinin güncellemesi olan
  Seedance 2.5'i kullanıma sundu; şirkete göre model, tek çekimde 30 saniyeye
  kadar klip üretebiliyor ve daha uzun sekanslar için çok turlu bir uzatma
  modu sunuyor. Model, tek istekte 50'ye kadar çok modlu referans girdisini
  (30 görsel, 10 video klip, 10 ses klibi) kabul ediyor ve zaman damgası
  düzeyinde düzenleme sunuyor; Jimeng AI ve Doubao Pro üzerinden kullanıma
  açılırken, BytePlus ModelArk üzerinden API erişimi lansmanda henüz aktif
  değildi.
sources:
  - name: ByteDance Seed
    url: https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
  - name: TechNode
    url: https://technode.com/2026/07/31/bytedance-launches-seedance-2-5-video-generation-model/
claims:
  - text: "ByteDance, AI video üretim modelinin güncellemesi olan Seedance 2.5'i 31 Temmuz 2026'da kullanıma sundu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Seedance 2.5, tek çekimde 30 saniyeye kadar video klip üretiyor ve sekansları daha da uzatmak için çok turlu bir mod sunuyor (üretici iddiası; bağımsız tekrar üretim bulunamadı)"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Model, tek bir istekte 50'ye kadar çok modlu referans girdisini -- 30 görsel, 10 video klip ve 10 ses klibine kadar -- kabul ediyor ve ses ile video içeriğinde zaman damgası düzeyinde düzenlemeyi destekliyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Seedance 2.5, Jimeng AI ve Doubao'nun Pro katmanı üzerinden kullanıma sunuluyor; Volcano Engine'in BytePlus ModelArk üzerinden API erişiminin yakında geleceği belirtildi ve lansmanda henüz aktif değildi"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## Ne oldu

ByteDance, AI video üretim modelinin güncellemesi olan Seedance 2.5'i 31
Temmuz 2026'da kullanıma sundu [1][2]. Şirkete göre model, tek çekimde 30
saniyeye kadar klip üretebiliyor ve sekansları daha da uzatmak için çok turlu
bir mod sunuyor -- bu, ByteDance'in kendi iddiası olup bağımsız bir tekrar
üretim bulunamadı [1]. Model, tek bir istekte 50'ye kadar çok modlu referans
girdisini -- 30 görsel, 10 video klip ve 10 ses klibine kadar -- kabul
ediyor ve tüm klibi yeniden üretmeden bir bölümünü değiştirebilen zaman
damgası düzeyinde düzenleme özelliği ekliyor [1]. ByteDance, önceki nesle
kıyasla görsel, ses ve hareket kalitesinde genel iyileştirmelerden söz
ediyor ancak nicel bir benchmark veya üçüncü taraf karşılaştırması
yayınlamadı [1]. Lansmanda model, Jimeng AI ve Doubao'nun Pro katmanı
üzerinden kullanıma sunuluyor; Volcano Engine'in BytePlus ModelArk
platformu üzerinden API erişimi "yakında" olarak tanımlandı ve henüz aktif
değildi [1][2].

Bazı erken toplayıcı (aggregator) haberleri bu lansmanı, ByteDance'in 23
Haziran'da Volcano Engine FORCE konferansında gösterdiği Seedance 2.5'in
kurumsal beta önizlemesiyle karıştırdı; düşük güvenilirlikli bir kaynak ise
API'nin 16 Temmuz itibarıyla zaten aktif olduğunu iddia etti -- her iki
iddia da ne ByteDance'in kendi 31 Temmuz tarihli blog yazısında ne de
TechNode'un aynı gün yayınlanan haberinde destekleniyor; ikisi de API'yi
hâlâ beklenen bir özellik olarak tanımlıyor [1][2].

## Neden önemli

Yapay zekâ ile video üretimi şu anda üretken yapay zekânın en rekabetçi
alanlarından biri; ByteDance, OpenAI, Google ve Kuaishou bu yıl birbirine
haftalar arayla model güncellemeleri çıkardı. ByteDance'in Seedance 2.5 için
öne çıkardığı özellikler -- daha uzun tek çekim klipler, daha yoğun çok
modlu referans girdisi ve daha ince, zaman damgası düzeyinde düzenleme --
alandaki daha geniş bir eğilimi yansıtıyor: kısa, meraktan ibaret kliplerden
üretim tarzı düzenleme iş akışlarına yönelik araçlara doğru bir kayma. Yetkinlik
iddialarının hiçbiri henüz bağımsız olarak doğrulanmadı ve ByteDance,
ModelArk API'sinin dış geliştiricilere ne zaman, hatta açılıp
açılmayacağını belirtmedi.
