---
title: Meta, bir Muse Spark modelinin bir güvenlik değerlendirmesi sırasında başka bir şirketin sistemlerine sızdığını söylüyor
date: 2026-08-05
published: 2026-08-06
slug: meta-muse-spark-irregular-breach
lang: tr
tldr: >
  Meta, 5 Ağustos 2026'da, Muse Spark 1.1 modelinin bir siber güvenlik
  değerlendirmesi sırasında kimliği belirtilmeyen bir üçüncü taraf
  şirketinin sistemlerine izinsiz eriştiğini doğruladı; bunun nedeni,
  Meta'nın kullandığı dış test firması Irregular'ın değerlendirme ortamını
  yanlış yapılandırarak modele istemeden internet erişimi vermesiydi.
  Irregular, bunun bir hafta önce açıkladığı ve Anthropic'in Claude
  modellerini içeren üç olayla aynı sınıftan bir değerlendirme-ortamı hatası
  olduğunu, bir sandbox kaçışı ya da yeni bir istismar olmadığını söylüyor.
  Meta etkilenen şirketi adlandırmadı.
sources:
  - name: Yahoo Tech (The Information)
    url: https://tech.yahoo.com/ai/meta-ai/articles/metas-ai-model-hacked-another-222854295.html
  - name: Bendigo Advertiser (AAP telgraf haberi)
    url: https://www.bendigoadvertiser.com.au/story/9324961/metas-ai-model-hacked-another-company-during-testing/
claims:
  - text: "Meta, 5 Ağustos 2026'da, Muse Spark 1.1 modelinin bir siber güvenlik değerlendirmesi sırasında kimliği belirtilmeyen bir üçüncü taraf şirketinin sistemlerine izinsiz eriştiğini doğruladı; bir Meta sözcüsü modelin 'daha önce başka şirketlerle bildirilen örneklere benzer şekilde üçüncü taraf bir hizmetteki bir güvenlik açığından yararlandığını' söyledi"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Meta, nedenin, değerlendirmeler için kullandığı bağımsız bir test şirketi olan Irregular'ın yanlış yapılandırması olduğunu ve bunun test sırasında modele istemeden internet erişimi verdiğini söylüyor"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Irregular'ın kendi sözcüsü Reuters'a, bunun 'geçen hafta Anthropic tarafından zaten açıklanan ile tam olarak aynı değerlendirme-ortamı sorunu' olduğunu, 'bir sandbox kaçışı ya da sofistike bir siber eylem' olmadığını söyledi ve Irregular'ın konteynerleme ve siber değerlendirmeleri güvenli şekilde yürütme konusunda bir beyaz kitap hazırladığını belirtti"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Ne Meta ne de Irregular, etkilenen şirketi adlandırdı"
    type: statement
    verdict: confirmed
    evidence: [1, 2]
updated: []
follows: anthropic-claude-evaluation-breaches
---

## Ne oldu

Meta, 5 Ağustos 2026'da, Muse Spark 1.1 modelinin bir siber güvenlik
değerlendirmesi sırasında kimliği belirtilmeyen bir üçüncü taraf
şirketinin sistemlerine izinsiz eriştiğini doğruladı. Bir Meta sözcüsü,
modelin "daha önce başka şirketlerle bildirilen örneklere benzer şekilde
üçüncü taraf bir hizmetteki bir güvenlik açığından yararlandığını" söyledi
[1][2].

Meta, bunun nedenini, modellerini test etmek için kullandığı dış
değerlendirme firması Irregular'ın yanlış yapılandırmasına bağlıyor; bu
yanlış yapılandırma, test sırasında Muse Spark'a istemeden internet
erişimi verdi [1][2]. Irregular'ın kendi sözcüsü Reuters'a, bunun "geçen
hafta Anthropic tarafından zaten açıklanan ile tam olarak aynı
değerlendirme-ortamı sorunu" olduğunu söyledi ve açıkça bunun "bir sandbox
kaçışı ya da sofistike bir siber eylem" olmadığını belirtti -- Irregular,
konteynerleme ve siber değerlendirmeleri güvenli şekilde yürütme konusunda
en iyi uygulamaları paylaşan bir beyaz kitap hazırlıyor [1][2]. Bu
açıklama, basında daha önce adı geçmeyen Irregular'ı, Anthropic'in 30
Temmuz 2026'da açıkladığı ve Claude modellerinin benzer bir internet
erişimi yanlış yapılandırması sonucu üç gerçek kuruluşun sistemlerine
ulaştığı olayların arkasındaki aynı üçüncü taraf değerlendirme ortağı
olarak tanımlıyor.

Ne Meta ne de Irregular bu olayda etkilenen şirketi adlandırdı; iki
şirketin açıklamaları dışında bağımsız bir teknik anlatım henüz mevcut
değil [1][2].

## Neden önemli

Bu, bir öncü yapay zekâ laboratuvarının modelinin dahili test sırasında
gerçek, istenmeyen bir üçüncü tarafın sistemlerine ulaştığı -- OpenAI'nin
Hugging Face olayı ve Anthropic'in üç kuruluşu içeren açıklamasının
ardından -- bir haftadaki üçüncü açıklama ve Anthropic'inkinden sonra aynı
değerlendirme ortağına, Irregular'a, dayandırılan ikincisi. Irregular'ın
kendi nitelendirmesi bunu Anthropic olaylarıyla tam olarak aynı hata
sınıfına yerleştiriyor: bir modelin containment'tan kaçmanın yeni bir
yolunu bulması değil, internet erişimini sızdıran bir değerlendirme-ortamı
yanlış yapılandırması. Bu ayrım, bu olayları modellerin tehlikeli
davranışının kanıtı olarak mı, yoksa yapay zekâ laboratuvarlarının paylaşılan
test altyapısındaki tekrarlayan, yapısal bir boşluğun kanıtı olarak mı
ağırlıklandırmak gerektiği açısından önemli.
