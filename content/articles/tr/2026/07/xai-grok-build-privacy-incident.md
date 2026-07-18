---
title: SpaceXAI, veri yükleme skandalının ardından Grok Build kodlama ajanını açık kaynak yaptı
date: 2026-07-18
slug: xai-grok-build-privacy-incident
lang: tr
tldr: >
  SpaceXAI (eski adıyla xAI), terminal tabanlı kodlama ajanı Grok Build'in
  kaynak kodunu 15 Temmuz 2026'da Apache 2.0 lisansıyla GitHub'da yayımladı
  -- bağımsız güvenlik araştırmacısı cereblab'ın, aracın kullanıcıların tüm
  kod depolarını, gizlilik ayarından bağımsız olarak ve şifreler dahil,
  xAI'nin sunucularına yüklediğini ortaya çıkarmasından üç gün sonra.
  xAI, yükleme yolunu devre dışı bıraktığını ve önceden toplanan verileri
  sildiğini söylüyor; sorunu bulan araştırmacı bu iddianın bağımsız olarak
  doğrulanmadığını belirtiyor.
sources:
  - name: GitHub — xai-org/grok-build deposu
    url: https://github.com/xai-org/grok-build
  - name: The Register
    url: https://www.theregister.com/ai-and-ml/2026/07/14/musk-promises-purge-after-grok-build-caught-sending-entire-repos-to-the-cloud/5271123
  - name: The Decoder
    url: https://the-decoder.com/xai-open-sources-grok-build-on-github-after-massive-data-breach/
  - name: cereblab — bağımsız güvenlik araştırması
    url: https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547
  - name: OECD.AI Olay İzleme Sistemi
    url: https://oecd.ai/en/incidents/2026-07-13-acb3
claims:
  - text: "SpaceXAI (6 Temmuz 2026'da xAI'den yeniden adlandırıldı), Grok Build kodlama ajanının çalıştırma katmanını ve terminal arayüzünü 15 Temmuz 2026'da Apache 2.0 lisansıyla GitHub'da açık kaynak olarak yayımladı; aracın çalıştığı grok-build-0.1 modelinin kendisi kapalı ve ücretli API üzerinden erişilebilir durumda kalıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "Bağımsız güvenlik araştırmacısı cereblab, 12 Temmuz 2026'da yayımladığı ağ trafiği analizinde, grok-build 0.2.93 sürümünün -- tam commit geçmişini kanıtlayan bir 'canary' dosyası ve ayrıca .env gizli anahtar dosyaları dahil -- kullanıcıların tam git depolarını, 'modeli geliştir' ayarı açık ya da kapalı olsun, xAI'ye ait bir Google Cloud Storage kovasına yüklediğini gösterdi"
    type: research
    verdict: confirmed
    evidence: [4, 2]
  - text: "xAI, Elon Musk'ın bir paylaşımı üzerinden, önceden yüklenen kullanıcı verilerinin silindiğini, yükleme yolunun sunucu tarafında devre dışı bırakıldığını ve veri saklamanın 12 Temmuz 2026 itibarıyla varsayılan olarak kapalı hale getirildiğini duyurdu"
    type: business
    verdict: single-source
    evidence: [2]
  - text: "cereblab, xAI'nin düzeltmeyi anlatış biçimine itiraz ediyor: xAI kamuoyuna mevcut oturum bazlı '/privacy' saklama ayarını işaret etti, oysa yüklemeleri asıl durduran şey daha önce belgelenmemiş, ayrı bir sunucu tarafı bayraktı; ayrıca önceden yüklenen tüm verilerin silindiğine dair bağımsız bir doğrulamanın henüz bulunmadığını söylüyor"
    type: business
    verdict: disputed
    evidence: [4, 2]
updated: []
---

## Ne oldu

Eski adıyla xAI olan ve 6 Temmuz 2026'da SpaceXAI olarak yeniden adlandırılan
şirket, terminal tabanlı kodlama ajanı Grok Build'in kaynak kodunu 15 Temmuz
2026'da Apache 2.0 lisansıyla GitHub'da yayımladı [1][3]. Yalnızca ajan
çalıştırma katmanı ve terminal arayüzü açık kaynak; aracın çalıştığı
grok-build-0.1 modeli kapalı kalmaya devam ediyor ve yalnızca ücretli bir API
üzerinden erişilebiliyor [1].

Yayımlama, bağımsız güvenlik araştırmacısı cereblab'ın aracın ağ trafiğine
dair yaptığı analizi yayımlamasından üç gün sonra geldi. Analiz, Grok
Build'in 0.2.93 sürümünün kullanıcıların tüm git depolarını -- commit
geçmişi dahil -- xAI'nin kontrolündeki bir Google Cloud Storage kovasına
yüklediğini gösteriyordu [4]. Yükleme, aracın "modeli geliştir" gizlilik
ayarı açık ya da kapalı olsun gerçekleşiyordu; ayrıca API anahtarları gibi
gizli bilgiler içeren `.env` dosyaları da ayrı olarak yakalanıyordu [4].
cereblab, yüklemelerin yalnızca ajanın okuması istenen dosyaları değil tüm
depo geçmişini kapsadığını, ajana hiç açması söylenmemiş bir "canary"
dosyası yerleştirip bu dosyayı sonradan yüklenen bir arşivden geri
kurtararak kanıtladı [4]. The Register bu temel bulguları bağımsız olarak
doğruladı [2].

Açıklamanın ardından Musk, X üzerinden önceden yüklenen tüm verilerin
silindiğini, yükleme yolunun sunucu tarafında devre dışı bırakıldığını ve
veri saklamanın artık varsayılan olarak kapalı olduğunu duyurdu [2].
cereblab, xAI'nin bu düzeltmeyi anlatış biçimine itiraz ediyor: xAI'nin
kamuoyuna işaret ettiği ayar, oturum bazlı veri saklamayı kontrol eden bir
ayar; sorunu asıl çözen şey ise ayrı, daha önce belgelenmemiş bir sunucu
tarafı bayrak. cereblab ayrıca, önceden toplanan tüm verilerin gerçekten
silindiğine dair bağımsız bir doğrulama bulunmadığını belirtiyor [4][2].
OECD'nin Yapay Zeka Olay İzleme Sistemi de olayı kaydına geçirdi [5].

## Neden önemli

Geniş dosya sistemi erişimine sahip bir kodlama ajanının -- gizlilik ayarı
açık ya da kapalı fark etmeksizin -- kullanıcı depolarının tamamını,
şifreler dahil, satıcının kendi sunucularına yüklemesi, geliştiricilerin
özel kod tabanları içinde çalışmak üzere tasarlanmış bir araç için ciddi
bir güven sorunu. Birkaç gün sonra çalıştırma katmanının açık kaynak
yapılması bundan sonraki süreç için şeffaflığı artırıyor, ancak tek başına
xAI'nin temel düzeltme iddiasını doğrulamıyor; bu iddia şu an için bağımsız
bir teyitten çok şirketin kendi açıklamasına dayanıyor.
