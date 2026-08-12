---
title: Google DeepMind, işaret dilini metne çeviren yapay zekâ modeli SL2T'yi tanıttı; Pixel 11'de kullanıma sunuluyor
date: 2026-08-12
slug: deepmind-sl2t-sign-language-model
lang: tr
tldr: >
  Google DeepMind, işaret dilini doğrudan metne çeviren bir yapay zekâ
  modeli olan SL2T'yi yayınladı; model Pixel 11'de Gboard ve Live
  Transcribe içinde, önce Amerikan İşaret Dili'nden İngilizceye çeviriyle
  kullanıma sunuluyor. DeepMind, kendisinin de ortak yazarı olduğu
  FLEURS-ASL kıyaslamasında rekor bir puan bildiriyor ve modelin nadir
  işaretlerde ve bazı dilbilgisi yapılarında hâlâ zorlandığını söylüyor.
sources:
  - name: Google DeepMind Blog
    url: https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
  - name: Engadget
    url: https://www.engadget.com/2234618/deepmind-newest-model-allows-pixel-11-devices-to-transcribe-sign-language-into-text/
claims:
  - text: "Google DeepMind, Pixel 11'de Gboard ve Live Transcribe içinde, önce ASL-İngilizce çeviriyle kullanıma sunulan işaret dili-metin yapay zekâ modeli SL2T'yi yayınladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "SL2T, 50'den fazla işaret dilinde toplam 100.000 saatten fazla veriyle eğitildi"
    type: statement
    verdict: vendor-claim
    evidence: [1]
  - text: "SL2T, FLEURS-ASL kıyaslamasında sıfır-atışlı 70 BLEURT puanı elde ediyor; DeepMind bunun şimdiye kadar bildirilen en yüksek puan olduğunu söylüyor, ancak kıyaslamanın ortak yazarlarından biri Google'a bağlı bir araştırmacı olduğundan bu bağımsız olarak belirlenmiş bir rekor değil"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "DeepMind, modelin nadir işaretlerde, hızlı parmak harflemede, edilgen yapılarda, sınıflandırıcı betimlemelerde ve bağlamsız zaman kullanımında hâlâ hata yaptığını, sol elini kullananlar ve tek elle işaret yapanlar için daha fazla optimizasyona ihtiyaç duyduğunu belirtiyor"
    type: statement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Google DeepMind, işaret dili videosunu ara bir "gloss" adımı olmadan
doğrudan yazılı metne çeviren bir yapay zekâ modeli olan SL2T'yi
(sign-language-to-text) yayınladı. Model, cihaz üzerinde kamera
görüntüsünden vücut ve el koordinatlarını çıkarmak için MediaPipe
Holistic'i kullanıyor; SL2T tarafından işlenen tek şey video değil, bu
koordinat dizisi [1].

DeepMind, modeli 50'den fazla işaret dilinde 100.000 saatten fazla veriyle
eğittiğini söylüyor; ancak ilk tüketici sürümü yalnızca Amerikan İşaret
Dili'nden İngilizceyi destekliyor, daha fazla dil planlanıyor [1]. Model,
Gboard'da işaretten-metne bir yazma girdisi olarak ve Live Transcribe'da,
sağır ve işitme güçlüğü çeken kullanıcıların konuşma sırasında yazmak
yerine işaret yapabilmesini sağlayarak kullanıma sunuluyor; her ikisi de
önce Pixel 11'de [1]. Bağımsız teknoloji basını (Engadget ve diğerleri)
aynı ürün ayrıntılarını doğruluyor, ancak bu haberlerin neredeyse tamamı
ayrı bir haber kaynağından değil, DeepMind'ın kendi duyurusundan geliyor
[1, 2].

DeepMind, SL2T'nin FLEURS-ASL kıyaslamasında sıfır-atışlı 70 BLEURT puanı
aldığını ve bunun şimdiye kadar bildirilen en yüksek puan olduğunu
söylüyor. FLEURS-ASL, beş Sertifikalı Sağır Yorumcunun referans
çevirileriyle oluşturulmuş, hakemli ve kamuya açık meşru bir kıyaslama;
ancak ortak yazarlarından biri Google'a bağlı bir araştırmacı olduğundan,
bu Google'ın kendi modelini Google bağlantılı bir kıyaslamada puanlaması
anlamına geliyor, bağımsız olarak doğrulanmış bir rekor değil [1]. DeepMind
ayrıca modelin nadir işaretlerde, hızlı parmak harflemede, edilgen
yapılarda, sınıflandırıcı betimlemelerde ve anlamı zamana ya da bağlama
bağlı işaretlerde hâlâ hata yaptığını, sol elini kullananlar ve tek elle
işaret yapanlar için daha fazla çalışmaya ihtiyaç duyduğunu belirtiyor [1].

## Neden önemli

İşaret dili çevirisi uzun süredir konuşma diline yönelik yapay zekânın
gerisinde kaldı ve DeepMind, SL2T'yi bir araştırma gösterimi değil, ana
akım bir tüketici ürününe gömülen ilk bu tür model olarak sunuyor. Sağır ve
işitme güçlüğü çeken savunucular, daha önce işaretten-metne yapay zekâ
konusunda genel olarak endişelerini dile getirdi; son araştırmalarda ve
anketlerde belgelenen doğruluk, kültürel nüans ve işitenlerin egemen
olduğu geliştirme süreçlerine ilişkin şüphecilik de bunlar arasında. Bu
model bağımsız, dış bir değerlendirmeden henüz geçmedi.
