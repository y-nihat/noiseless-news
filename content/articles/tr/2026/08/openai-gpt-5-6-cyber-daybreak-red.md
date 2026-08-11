---
title: OpenAI, yetkilendirilmiş saldırı-güvenliği çalışmaları için daha az kısıtlı bir model olan GPT-5.6-Cyber'i tanıttı
date: 2026-08-10
slug: openai-gpt-5-6-cyber-daybreak-red
lang: tr
tldr: >
  OpenAI, 10 Ağustos 2026'da GPT-5.6 Sol tabanlı, siber güvenliğe özel bir
  model olan GPT-5.6-Cyber'i duyurdu. Model, OpenAI'nin diğer modellerinin
  reddettiği saldırı-güvenliği taleplerini yanıtlıyor ve yalnızca onaylanmış
  "güvenilir müşteri ortaklarına" yeni bir erişim katmanı olan "Daybreak Red"
  üzerinden sunuluyor. OpenAI, modelin yamalanmış bir Chrome güvenlik
  açığını (CVE-2026-15903) bulduğunu ve kendi iç testinde gelişmiş
  güvenlik-araştırması taleplerinin %95'ini tamamladığını söylüyor — önceki
  modelde bu oran %57,3'tü; bu rakamlar bağımsız olarak doğrulanmadı. Duyuru,
  OpenAI'nin ayrı ve henüz yayımlanmamış Astra modelinin en yüksek siber-risk
  eşiğini aşmış olabileceğini söylemesinden üç gün sonra geldi; OpenAI
  aradaki farkı kendi iki katmanlı kapasite sınıflandırmasına bağlıyor.
sources:
  - name: OpenAI
    url: https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/10/as-ai-led-attacks-multiply-openai-launches-a-new-cyber-model/
  - name: Axios
    url: https://www.axios.com/2026/08/10/openai-gpt-astra-restrictions-safety-hacking-defenders
  - name: The Decoder
    url: https://the-decoder.com/openai-launches-gpt-5-6-cyber-to-help-defenders-find-vulnerabilities-before-attackers-do/
  - name: NVD (CVE-2026-15903)
    url: https://nvd.nist.gov/vuln/detail/CVE-2026-15903
claims:
  - text: "10 Ağustos 2026'da OpenAI, GPT-5.6 Sol tabanlı GPT-5.6-Cyber'i, yetkilendirilmiş saldırı-güvenliği çalışmaları (güvenlik açığı araştırması, istismar doğrulaması, güvenlik testi) için yeni bir 'Daybreak Red' erişim katmanı üzerinden, savunma amaçlı çalışmalar için 'Daybreak Blue' katmanının yanı sıra duyurdu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3, 4]
  - text: "OpenAI, GPT-5.6-Cyber'in kendi iç 'Gelişmiş Siber Güvenlik Tamamlama Oranı' değerlendirmesinde taleplerin %95'ini tamamladığını, bir önceki model GPT-5.5-Cyber'de bu oranın %57,3, normal güvenlik önlemleri altındaki GPT-5.6 Sol'da ise %1,5-2 olduğunu söylüyor; bu ölçüt modelin hassas bir talebe yanıt verip vermediğini ölçüyor, yanıtın doğru veya işlevsel olup olmadığını değil, ve rakamlar bağımsız bir laboratuvar tarafından doğrulanmadı"
    type: capability
    verdict: vendor-claim
    evidence: [1, 3, 4]
  - text: "Chrome'un V8 motorunda yüksek önem dereceli, sınır dışı okuma/yazma türünde bir güvenlik açığı olan ve CVE-2026-15903 olarak izlenen açık Google tarafından yamalandı; OpenAI, GPT-5.6-Cyber'in testleri sırasında bu açığı ve zincirlenebilir ikinci bir açığı bulduğunu söylüyor, ancak Google bu buluşu OpenAI'ye veya modele ismen atfetmedi"
    type: capability
    verdict: vendor-claim
    evidence: [1, 4, 5]
  - text: "GPT-5.6-Cyber'e erişim şu anda yalnızca onaylanmış 'güvenilir müşteri ortakları' ile sınırlı; OpenAI'nin kendi materyalleri, basına yansıdığı şekliyle, Accenture, IBM, CrowdStrike ve Cloudflare gibi ortakları sayıyor, ancak bu şirketlerin hiçbiri erişimi bağımsız olarak doğrulamadı"
    type: business
    verdict: vendor-claim
    evidence: [1, 2, 3]
  - text: "Duyuru, OpenAI'nin 7 Ağustos 2026'da ayrı ve henüz yayımlanmamış Astra modelinin Hazırlık Çerçevesi'ndeki 'Kritik' siber-kapasite eşiğini aşmış olabileceğini dışlayamadığını açıklamasının ardından geldi; OpenAI, GPT-5.6-Cyber ve GPT-5.6 Sol'un ikisinin de daha düşük 'Yüksek' katmanda kendi kendine sınıflandırıldığını, bu yüzden birinin durdurulup diğerinin piyasaya sürüldüğünü söylüyor"
    type: statement
    verdict: vendor-claim
    evidence: [1, 3]
updated: []
---

## Ne oldu

OpenAI, 10 Ağustos 2026'da GPT-5.6 Sol tabanlı, siber güvenliğe özel bir model
olan GPT-5.6-Cyber'i duyurdu [1]. Model, OpenAI'nin mevcut Daybreak
programının yeni bir erişim katmanı olan "Daybreak Red" üzerinden, savunma
amaçlı çalışmalar için "Daybreak Blue" katmanının yanı sıra sunuluyor;
Daybreak Red, OpenAI'nin genel amaçlı modellerinin yanıtlamayı reddettiği
yetkilendirilmiş saldırı-güvenliği araştırmaları — güvenlik açığı keşfi,
istismar zinciri geliştirme, kimlik doğrulama atlatma ve yetki yükseltme
testleri — için tasarlandı [1][2][3][4]. Erişim, onaylanmış "güvenilir
müşteri ortakları" ile sınırlı; OpenAI'nin kendi materyalleri, basına
yansıdığı şekliyle, Accenture, IBM, CrowdStrike ve Cloudflare gibi ortakları
sayıyor, ancak bu şirketlerin hiçbiri ilişkiyi bağımsız olarak doğrulamadı
[1][2][3].

OpenAI, modelin kendi iç "Gelişmiş Siber Güvenlik Tamamlama Oranı"
değerlendirmesinde taleplerin %95'ini tamamladığını, önceki model
GPT-5.5-Cyber'de bu oranın %57,3, normal güvenlik önlemleri altındaki GPT-5.6
Sol'da ise %1,5-2 olduğunu söylüyor [1][3][4]. Bu ölçüt, modelin hassas bir
talebe yanıt verip vermediğini ölçüyor — yanıtın doğru veya çalışan bir
istismar olup olmadığını değil — ve rakamlar hiçbir bağımsız laboratuvar
tarafından doğrulanmadı [3][4].

Somut bir örnek olarak OpenAI, GPT-5.6-Cyber'i kullanarak Chrome'un V8
motorunda daha önce bilinmeyen, zincirlenebilir iki güvenlik açığı bulduğunu
söylüyor. Açıklardan biri, Google'ın o zamandan beri yamaladığı, sınır dışı
okuma/yazma türünde bir açık olan CVE-2026-15903 olarak izleniyor [1][4][5].
Açığın kendisi ve Google'ın yaması kamuya açık CVE kaydında bağımsız olarak
doğrulanabilir; ancak OpenAI'nin bunu özellikle GPT-5.6-Cyber'in bulduğu
iddiası bağımsız olarak doğrulanmadı — Google, buluşu OpenAI'ye veya modele
ismen atfetmedi [4][5].

Duyuru, OpenAI'nin Hazırlık Çerçevesi'ndeki "Kritik" siber-kapasite eşiğini
ayrı ve henüz yayımlanmamış Astra modelinin aşmış olabileceğini dışlayamadığını
açıklamasından ve modelin güvenlik önlemi olmadan iç kullanımını
durdurmasından üç gün sonra geldi. OpenAI'nin, günler sonra daha az kısıtlı
bir siber model piyasaya sürmesine ilişkin açıklaması, çerçevesinde "Yüksek"
ve "Kritik" olmak üzere iki ilgili katman bulunduğu, GPT-5.6 Sol ve
GPT-5.6-Cyber'in ikisinin de daha düşük "Yüksek" katmanda kendi kendine
sınıflandırıldığı — yalnızca Astra'nın "Kritik" eşiğini aştığı yönünde
[1][3]. Bu sınıflandırma OpenAI'ye ait ve bağımsız olarak denetlenmedi.

## Neden önemli

OpenAI, ayrı bir modelinin kendi en yüksek siber-risk sınırını aşmış
olabileceğini söylediği sırada, yapay zeka destekli saldırı-güvenliği
araştırmalarına bilinçli olarak daha az kısıtlı erişim satıyor. Şirketin
açıklaması tamamen kendi bildirdiği kapasite sınıflandırmasına dayanıyor;
GPT-5.6-Cyber'in gerçekte nerede durduğuna dair dışarıdan bir doğrulama yok —
aynı sınırlılık, %95'lik kıyaslama iddiası ve Chrome açığını bulma anlatısı
için de geçerli.
