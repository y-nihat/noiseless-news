---
title: Anthropic, biyolojik silah sınıflandırıcılarının yüklenici trafiğinde 11 ay devre dışı kaldığını ve 133 milyon görüşmenin etkilendiğini açıkladı
date: 2026-08-14
published: 2026-08-16
slug: anthropic-bio-classifier-logging-gap
lang: tr
tldr: >
  Anthropic, Ağustos 2026 Risk Raporu'nda, biyolojik silahlarla ilgili
  içerikleri engellemesi gereken sınıflandırıcıların, Mayıs 2025'ten Nisan
  2026'ya kadar tüm insan-geri-bildirimi yüklenici trafiğinde devre dışı
  kaldığını açıkladı -- yanlış etiketlenmiş bir dahili bayrak bu durumu
  kayıt ve incelemeden de gizledi. Bu on bir aylık sürede yaklaşık 50.000
  dış yüklenici, yaklaşık 133 milyon görüşme gerçekleştirdi. Anthropic'in
  sonradan yaptığı inceleme net bir kötüye kullanım bulmadı, ancak bir
  avuç çift kullanımlı görüşmeyi işaretledi ve hiçbir müşteri verisinin
  etkilenmediğini söylüyor.
sources:
  - name: Anthropic
    url: https://www.anthropic.com/aug-2026-risk-report
  - name: The Decoder
    url: https://the-decoder.com/anthropics-bio-weapons-filter-was-down-for-nearly-a-year-exposing-133-million-requests/
  - name: TheNextWeb
    url: https://thenextweb.com/news/anthropic-risk-report-bio-classifiers-human-feedback-gap
claims:
  - text: "Anthropic, 14 Ağustos 2026'da yayımlanan Ağustos 2026 Risk Raporu'nda, biyolojik silahlarla ilgili içerikleri engellemesi gereken sınıflandırıcıların Mayıs 2025'ten Nisan 2026'ya kadar tüm insan-geri-bildirimi yüklenici trafiğinde devre dışı kaldığını, yani on bir aylık bir boşluk olduğunu açıkladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Bu boşluk, o dönemde Anthropic'in modelleriyle yaklaşık 133 milyon görüşme gerçekleştiren yaklaşık 50.000 dış yükleniciyi etkiledi; bu yükleniciler Anthropic tarafından değil, yalnızca dış tedarikçiler tarafından denetlendi"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Sorunun nedeni, yalnızca dahili kullanım için tasarlanmış bir bayrağın hem sınıflandırıcıların engelleme davranışını hem de işaretlerinin kaydedilmesini devre dışı bırakmasıydı; bu nedenle etkilenen trafik o dönemde herhangi bir inceleme mekanizmasına iletilmedi ve kaydedilmedi"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Anthropic'in, saklanan görüşme kayıtlarını yeniden taramak için Claude Sonnet 5'i kullandığı sonradan yaptığı inceleme, 1.197 görüşmeyi yüksek biyolojik zarar riski taşıdığı gerekçesiyle işaretledi; dahili ekiplere veya bilinen kırmızı takım tatbikatlarına atfedilemeyen işaretlerin elle incelenmesi, bir tehdit aktörüne anlamlı bir katkı sağlayabilecek net bir kötüye kullanım bulmadı, ancak Anthropic'in akademik düzeyde tanımladığı bir avuç potansiyel çift kullanımlı görüşme tespit edildi"
    type: research
    verdict: vendor-claim
    evidence: [1]
  - text: "Anthropic, hiçbir müşteri verisinin, iç sistemin veya model ağırlığının erişilmediğini veya ifşa olmadığını söylüyor; boşluk yalnızca insan-geri-bildirimi veri etiketleme yüklenici hattıyla sınırlıydı"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic sorunu Nisan 2026'da düzeltti ve Şubat 2026'daki kendi risk değerlendirmesini bu kategori için 'çok düşük'ten 'düşük'e geriye dönük olarak güncelledi"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## Ne oldu

Anthropic, 14 Ağustos 2026'da yayımlanan Ağustos 2026 Risk Raporu'nda,
model çıktılarındaki biyolojik silahlarla ilgili içerikleri engellemesi
gereken sınıflandırıcıların, bu güvenlik önlemlerini içeren modelleri ilk
kez devreye aldığı Mayıs 2025'ten Nisan 2026'ya kadar tüm
insan-geri-bildirimi yüklenici trafiğinde devre dışı kaldığını açıkladı
[1][2][3]. Sorunun nedeni, yalnızca dahili kullanım için tasarlanmış bir
bayraktı; bu bayrak hem sınıflandırıcıların engelleme davranışını hem de
işaretlerinin kaydedilmesini devre dışı bırakıyordu, dolayısıyla normalde
işaretlenecek trafik hiçbir zaman kaydedilmedi veya herhangi bir inceleme
mekanizmasına gönderilmedi [1][2][3].

Bu boşluk, on bir aylık süre boyunca aralarında toplam yaklaşık 133 milyon
görüşme gerçekleştiren yaklaşık 50.000 dış yükleniciyi kapsadı [1][2][3].
İnsan-geri-bildirimi veri toplama sürecinin bir parçası olarak
Anthropic'in modellerini değerlendiren bu yükleniciler, yalnızca dış
tedarikçiler tarafından denetlendi -- Anthropic'e göre bu tedarikçilerden
bazılarının "CB-1 tehdit aktörlerini bile durdurabilecek denetim
süreçleri yoktu" [1].

Arıza kayıt tutmayı da devre dışı bıraktığı için Anthropic, ne olduğunu
sonradan saklanan ham görüşme kayıtlarından yeniden inşa etmek zorunda
kaldı. Bu trafiği yeniden taramak ve yüksek biyolojik zarar riski taşıyan
görüşmeleri işaretlemek için Claude Sonnet 5'i kullandı; bu süreç 1.197
işaretli görüşme üretti. Bunlardan 757'si aynı altyapıyı kullanan
Anthropic'in kendi iç ekiplerinden geldi; kalanların ise 62'si dışında
tamamı kasıtlı dahili veya harici kırmızı takım tatbikatlarına
dayanıyordu. Anthropic bu 62 görüşmeyi ve kırmızı takım işaretlerinden
30 görüşmelik bir örneklemi elle inceledi; "bir tehdit aktörüne anlamlı
bir katkı sağlayabilecek net bir CB kötüye kullanımı gözlemlemedik"
derken, "bir avuç potansiyel çift kullanımlı görüşme veya oldukça
akademik düzeyde kırmızı takım etkileşimi tespit ettik" diye ekliyor [1].
Anthropic, hiçbir müşteri verisinin, iç sistemin veya model ağırlığının
erişilmediğini söylüyor -- boşluk, ticari API'si veya diğer ürün
yüzeyleri değil, yalnızca insan-geri-bildirimi yüklenici hattıyla
sınırlıydı [1].

Anthropic, altta yatan bayrağı Nisan 2026'da düzelttiğini ve artık
yüklenici trafiğinin büyük çoğunluğunda engelleme sınıflandırıcılarını
çalıştırdığını, istisnaların yalnızca belirli bir proje için yeterli
gördüğü denetimlere sahip tedarikçilere tanındığını söylüyor [1]. Bu
açıklama yeni: Anthropic'in Şubat 2026'da yayımlanan önceki Risk
Raporu, insan-geri-bildirimi platformlarını hiç risk yüzeyi olarak
değerlendirmemişti. Ağustos raporunda Anthropic, Şubat'taki bu
değerlendirmeyi bu risk kategorisi için geriye dönük olarak "çok
düşük"ten "düşük"e revize etti [1].

## Neden önemli

Bu, Anthropic'in, yapay zekâ destekli biyolojik silah yardımı girişimlerini
yakalamak için özel olarak tasarlanmış bir güvenlik önleminde -- şirketin
tekrar tekrar en ciddiye aldığını söylediği risk kategorilerinden biri --
bir boşluğun kendi hesabı. En önemli unsurlar, on bir aylık süre ve aynı
hatanın bu tür sorunları yakalaması gereken izleme mekanizmasını da
susturmuş olması: şirket, pencere kapandıktan çok sonrasına kadar kendi
boşluğundan haberdar değildi. Anthropic'in kendi incelemesi
metodolojisi konusunda şeffaf, ancak yine de bir öz değerlendirme --
işaretlenen trafiğin yalnızca bir kısmını örnekliyor ve incelemeci olarak
Anthropic'in kendi modelini kullanıyor -- ve şirketin kendisi de bu
keşfin "sistemlerimizin başka yerlerinde benzer boşluklar olmadığına
dair güvenimizi azalttığını" söylüyor.
