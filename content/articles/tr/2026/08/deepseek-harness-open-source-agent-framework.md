---
title: DeepSeek, eklenti tabanlı bir kodlama ajanı çerçevesi olan Harness'ı açık kaynak yaptı
date: 2026-08-13
published: 2026-08-14
slug: deepseek-harness-open-source-agent-framework
lang: tr
tldr: >
  DeepSeek, kodlama ajanları oluşturmak ve çalıştırmak için MIT lisanslı,
  açık kaynaklı bir çerçeve olan Harness'ı 13 Ağustos 2026'da geliştirici
  önizlemesi olarak yayınladı. Sistemin her parçası -- modeller, araçlar,
  oturumlar, sandbox'lar ve ajan döngüsünün kendisi -- değiştirilebilir bir
  eklenti olarak tasarlandı. DeepSeek'in kendi materyalleri herhangi bir
  rakip karşılaştırması yapmıyor; bazı yayınlar bunu Anthropic'in kodlama
  araçlarına rakip olarak konumlandırdı, ancak bu basının kendi çerçevelemesi,
  DeepSeek'in bir iddiası değil.
sources:
  - name: DeepSeek Harness (GitHub deposu)
    url: https://github.com/deepseek-ai/deepseek-harness
  - name: DeepSeek Harness (LICENSE dosyası)
    url: https://github.com/deepseek-ai/deepseek-harness/blob/master/LICENSE
  - name: DeepSeek AI (resmi duyuru, X)
    url: https://x.com/deepseek_ai/status/2087887408440164663
  - name: The New Stack
    url: https://thenewstack.io/deepseek-harness-open-source-plugins/
  - name: VentureBeat
    url: https://venturebeat.com/technology/deepseek-harness-launches-as-open-source-rival-to-claude-code-alongside-v4-pro-on-api-with-higher-prices
claims:
  - text: "DeepSeek, kodlama ajanları oluşturmak ve çalıştırmak için açık kaynaklı bir ajan çalışma zamanı çerçevesi olan Harness'ı (CLI takma adı `dsh`) 13 Ağustos 2026'da GitHub'da geliştirici önizlemesi olarak yayınladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 3, 4]
  - text: "Harness kod tabanı MIT lisansı altında yayınlandı"
    type: announcement
    verdict: confirmed
    evidence: [2]
  - text: "Harness'ın mimarisi; modelleri, araçları, becerileri, oturumları, sandbox'ları, dosya sistemlerini, ajan döngüsünü, orkestrasyonu ve arayüzü değiştirilebilir eklentiler olarak uyguluyor -- bu, hem GitHub README'sinde hem de DeepSeek'in duyuru gönderisinde bağımsız olarak kullanılan DeepSeek'in kendi tanımı"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "DeepSeek'in kendi yayın materyalleri herhangi bir rakiple karşılaştırma yapmıyor; bazı basın yayınları Harness'ı Anthropic'in kodlama araçlarına rakip olarak çerçeveledi, ancak yayınlar hangi ürünü (Claude Code mü Claude Cowork mü) rakip aldığı konusunda birbirinden farklı"
    type: announcement
    verdict: single-source
    evidence: [5]
updated: []
---

## Ne oldu

DeepSeek, kodlama ajanları oluşturmak ve çalıştırmak için açık kaynaklı bir
çerçeve olan Harness'ı 13 Ağustos 2026'da GitHub'da, MIT lisansı altında ve
geliştirici önizlemesi olarak yayınladı [1][2]. Depo ve DeepSeek'in kendi
duyurusu, sistemin her parçasının -- modeller, araçlar, beceriler, oturumlar,
sandbox'lar, dosya sistemleri, ajan döngüsü, orkestrasyon ve kullanıcı
arayüzü -- değiştirilebilir veya yerine başkası konabilir bir eklenti olarak
uygulandığı bir mimariyi tanımlıyor [1][3]. Komut satırı aracı `dsh` takma
adıyla geliyor ve `npx @deepseek-ai/dsh web` komutuyla başlatılabiliyor;
DeepSeek, önizlemenin yinelemeli geliştirme sırasında uyumluluğu bozan
değişiklikler içereceği konusunda uyarıyor [1].

Yayın, DeepSeek'in kendi GitHub deposu ve duyurusunun ötesinde, aynı hafta
The New Stack tarafından bağımsız olarak haberleştirildi [4]. DeepSeek'in
kendi materyallerinde herhangi bir rakip ürüne değinilmiyor. Buna rağmen
bazı basın yayınları Harness'ı Anthropic'in kodlama araçlarına meydan okuyan
bir ürün olarak çerçeveledi -- VentureBeat'in başlığı bunu "Claude Code'a
rakip" olarak nitelerken, başka bir yayın bunu farklı bir Anthropic ürünü
olan "Claude Cowork"e karşı konumlandırdı; yayınlar arasındaki bu
tutarsızlık, karşılaştırmanın DeepSeek'in söylediği bir şey değil, her
yayının kendi çerçevelemesi olduğunu gösteriyor [5].

## Neden önemli

Yayının kendisi -- DeepSeek'ten MIT lisanslı, eklenti mimarili bir ajan
çerçevesi -- şirketin kendi GitHub deposundan ve duyurusundan, ayrıca bağımsız
basın haberlerinden doğrudan teyit edildi. Bunun belirli bir Anthropic
ürününü hedef aldığı yönündeki her türlü çerçeveleme, DeepSeek'in bir iddiası
değil, basının kendi yorumudur ve yayınlar hangi ürünün kastedildiği
konusunda bile hemfikir değil.
