---
title: Anthropic, Claude'un metin filigranının teknik ayrıntılarını yayımladı
date: 2026-08-14
published: 2026-08-15
slug: anthropic-claude-text-watermark-mechanism
lang: tr
tldr: >
  Anthropic, 11 Ağustos'ta AB Yapay Zeka Yasası'nın şeffaflık kurallarına
  uyum gerekçesiyle Claude modellerinin ürettiği metinleri filigranlamaya
  başlayacağını duyurdu. Şirket 14 Ağustos'ta teknik ayrıntıları paylaştı:
  filigran, birbirine yakın anlam taşıyan, önemsiz kelime seçimlerini gizli
  bir anahtar ve önceki bağlam kullanarak yönlendiriyor -- Google
  DeepMind'ın SynthID-Text'iyle aynı aileden bir yaklaşım. Kod metnine
  uygulanmıyor, gerçeklere sıkı sıkıya bağlı metinlerde zayıf kalıyor;
  hafif düzenlemelere dayanıyor ama ağır yeniden yazım ya da çeviride
  kayboluyor. Anthropic, üçüncü taraflar için bir tespit API'sinin
  yolda olduğunu ama henüz yayımlanmadığını söylüyor ve filigranın
  yazarlığı kanıtlamadığını açıkça belirtiyor -- düzenleyicilerin ve
  kurumların yapay zeka filigranlarını giderek bir şeffaflık güvencesi
  olarak görmeye başladığı bir dönemde önem taşıyan bir sınırlama.
sources:
  - name: Anthropic
    url: https://www.anthropic.com/news/claude-text-watermark
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/15/anthropic-shares-more-details-about-how-claudes-new-watermarks-will-work/
  - name: The Register
    url: https://www.theregister.com/ai-and-ml/2026/08/15/anthropic-says-text-watermarking-scheme-relies-on-inconsequential-words/5288156
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/11/anthropic-says-it-will-watermark-text-generated-by-its-ai-models/
claims:
  - text: "Anthropic, 11 Ağustos 2026'da Claude modellerinin ürettiği metinlere istatistiksel bir filigran gömmeye başlayacağını duyurdu; gerekçe olarak AB Yapay Zeka Yasası'nın şeffaflık Uygulama Kuralları'na uyumu gösterdi"
    type: announcement
    verdict: confirmed
    evidence: [1, 4]
  - text: "Anthropic, 14 Ağustos 2026'da mekanizmanın teknik ayrıntısını yayımladı: birbirine yakın anlam taşıyan, önemsiz kelime seçimlerinde belirteç seçimini gizli bir anahtar ve önceki bağlam kullanarak yönlendiriyor -- şirkete göre bu, Google DeepMind'ın SynthID-Text'iyle aynı aileden bir yaklaşım"
    type: capability
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Anthropic, filigranın koda uygulanmadığını ve gerçeklere sıkı sıkıya bağlı metinlerde zayıf kaldığını; hafif düzenlemelere dayandığını ama ağır yeniden yazım, başka sözcüklerle ifade etme veya çeviride kaybolduğunu söylüyor"
    type: capability
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Anthropic, üçüncü taraflar için bir filigran tespit API'sini yakında sunacağını ama henüz yayımlamadığını ve uygulama ayrıntılarını hâlâ belirlemekte olduğunu söylüyor"
    type: announcement
    verdict: vendor-claim
    evidence: [1, 2]
  - text: "Anthropic, filigranın yazarlığı kanıtlamadığını açıkça belirtiyor: yalnızca Claude'un muhtemelen sürece dahil olduğunu gösterebiliyor, Claude'un yazdığı metinle ağır şekilde düzenlediği metni ayırt edemiyor ve başka şirketlerin yapay zeka sistemlerinin ürettiği metni tanıyamıyor"
    type: statement
    verdict: confirmed
    evidence: [1]
updated: []
follows: null
---

## Ne oldu

Anthropic, 11 Ağustos'ta, 2 Ağustos'ta yürürlüğe giren AB Yapay Zeka
Yasası'nın şeffaflık Uygulama Kuralları'na uyumu gerekçe göstererek Claude
modellerinin ürettiği metinlere istatistiksel bir filigran gömmeye
başlayacağını duyurdu. 14 Ağustos'ta ise mekanizmayı açıklayan bir takip
yazısı yayımladı: bir cümlede anlamca birbirine yakın birden fazla kelime
seçeneği olduğunda, Claude'un belirteç seçimi gizli bir anahtar ve önceki
belirteçler kullanılarak yönlendiriliyor; bu da metnin anlamını değiştirmeden
tespit edilebilir istatistiksel bir örüntü bırakıyor. Anthropic bu
yaklaşımın Google DeepMind'ın SynthID-Text'iyle aynı aileden olduğunu
söylüyor.

Anthropic'in kendi anlatımına göre yöntemin gerçek sınırları var: koda hiç
uygulanmıyor, gerçeklere sıkı sıkıya bağlı metinlerde ise zayıf kalıyor --
çünkü bu tür metinlerde kelime seçimi için az yer kalıyor. Hafif
düzenlemelere dayanıyor ama ağır yeniden yazım, başka sözcüklerle ifade etme
veya çeviride kayboluyor. Anthropic, üçüncü taraflar için "yakında" bir
filigran tespit API'si sunacağını söylüyor, ancak henüz yayımlamadı ve
uygulama ayrıntılarını hâlâ belirliyor. Şirket, filigranın yazarlığı
kanıtlamadığını açıkça belirtiyor: yalnızca Claude'un "muhtemelen" sürece
dahil olduğunu gösterebiliyor, Claude'un yazdığı metinle ağır şekilde
düzenlediği metni ayırt edemiyor ve başka şirketlerin yapay zeka
sistemlerinin ürettiği metni tanıyamıyor.

## Neden önemli

Düzenleyiciler yapay zeka içeriğinde şeffaflık talep ederken ve kurumlar
yazılarda yapay zeka kullanımını daha sıkı denetlerken, filigranlama temel
bir altyapı olarak konumlandırılıyor -- ama Anthropic'in kendi açıklaması
bunun kanıt değil, zayıf ve atlatılabilir bir sinyal olduğunu gösteriyor.
Güvenlik araştırmacıları ayrıca, herkese açık bir tespit API'si
yayımlandığında bunun filigranı adım adım silmek için bir geri bildirim
kaynağı olarak kullanılabileceğini belirtiyor -- Anthropic'in henüz
kamuya açık şekilde ele almadığı bir risk.
