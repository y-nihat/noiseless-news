---
title: İngiltere Yapay Zeka Güvenliği Enstitüsü, açık ağırlıklı modellerin siber yeteneklerde öncü modellerin 4-7 ay gerisinde kaldığını buldu; önceki fark 6-10 aydı
date: 2026-07-18
slug: aisi-open-weight-cyber-gap
lang: tr
tldr: >
  İngiltere Yapay Zeka Güvenliği Enstitüsü (AISI), 17 Temmuz 2026'da
  yayınladığı değerlendirme sonuçlarında, yakın zamanlı açık ağırlıklı
  modellerin — Zhipu'nun GLM-5.2'si ve DeepSeek'in V4-Pro'su — artık kapalı
  öncü modellerin 4 ila 7 ay önceki siber saldırı yeteneğine ulaştığını
  gösterdi; bu fark, AISI'nin 2025'in büyük bölümünde ölçtüğü 6-10 aylık
  farktan daha dar. Aynı siber-menzil görevlerini açık modellerde çalıştırmak
  da kapalı öncü modellere kıyasla çok daha ucuza mal oluyor.
sources:
  - name: İngiltere Yapay Zeka Güvenliği Enstitüsü — blog yazısı
    url: https://www.aisi.gov.uk/blog/how-far-behind-the-frontier-are-leading-open-weight-models-on-cyber
  - name: The Decoder — bağımsız haber
    url: https://the-decoder.com/open-weight-models-now-match-frontier-cyber-performance-from-just-four-months-ago-at-a-fraction-of-the-cost/
claims:
  - text: "AISI'nin değerlendirmesi, yakın zamanlı açık ağırlıklı modeller GLM-5.2 ve DeepSeek V4-Pro'nun siber görevlerde, kendilerinden 4 ila 7 ay önce yayınlanan kapalı öncü modellere benzer performans gösterdiğini buldu; bu, AISI'nin 2025'in büyük bölümünde ölçtüğü 6-10 aylık farktan daha dar"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "Dört zorluk seviyesindeki 70 görevlik dar siber benchmark'ta, GLM-5.2 yaklaşık 4 ay önce yayınlanan en siber-yetenekli modellere benzer performans gösterdi; DeepSeek V4-Pro, 5 ay önce yayınlanan Opus 4.5'e benzer performans gösterdi"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "Çok adımlı otonom siber-menzil senaryolarında GLM-5.2, 7 aydan kısa süre önce yayınlanan Opus 4.5'e kadar ulaştı; DeepSeek V4-Pro ise aynı senaryolarda Sonnet 4.5'in altında kaldı"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "100 milyon token'lık bir siber-menzil görevini çalıştırmak Opus 4.5/4.6'da yaklaşık 85 dolara mal olurken, GLM-5.2'de yaklaşık 46 dolara, DeepSeek V4-Pro'da ise 1,19 dolara mal oldu"
    type: research
    verdict: confirmed
    evidence: [1, 2]
updated: []
---

## Ne oldu

Öncü yapay zeka sistemlerini güvenlik açısından değerlendiren İngiliz
hükümet kurumu İngiltere Yapay Zeka Güvenliği Enstitüsü (AISI), 17 Temmuz
2026'da yayınladığı bulgularda iki yakın zamanlı açık ağırlıklı modelin —
Zhipu'nun GLM-5.2'si ve DeepSeek'in V4-Pro'su — birkaç ay önce yayınlanan
kapalı öncü modellerin siber saldırı yeteneğine yaklaştığını gösterdi
[1][2]. 70 görevlik dar bir siber benchmark'ta GLM-5.2, kendisinden yaklaşık
4 ay önce yayınlanan modellere denk performans gösterdi; DeepSeek V4-Pro ise
5 ay önce yayınlanan Opus 4.5'e denk performans gösterdi [1]. Daha uzun bir
saldırı dizisini simüle eden, çok adımlı ve daha zor siber-menzil
senaryolarında GLM-5.2, 7 aydan kısa bir süre önce yayınlanan Opus 4.5'e
kadar ulaşırken, DeepSeek V4-Pro aynı görevlerde Sonnet 4.5'in altında
kaldı [1]. AISI, bu genel 4-7 aylık farkın, 2025'in büyük bölümünde
ölçtüğü 6-10 aylık farktan daha dar olduğunu belirtiyor [1][2].

Aynı siber-menzil iş yükünü çalıştırmak açık modellerde de çok daha ucuz:
AISI, 100 milyon token'lık bir siber-menzil görevinin maliyetini Opus
4.5/4.6'da yaklaşık 85 dolar, GLM-5.2'de yaklaşık 46 dolar, DeepSeek
V4-Pro'da ise 1,19 dolar olarak veriyor [1][2].

AISI, kendi kurulumunun açık modellerin tavanını muhtemelen olduğundan
düşük gösterdiğini belirtiyor — GLM-5.2 veya DeepSeek V4-Pro için ekstra
bir "elicitation" (yetenek çıkarma) veya optimizasyon uygulamadı — ve
siber-menzil karşılaştırması, dar görev benchmark'ından daha küçük bir
senaryo kümesine dayanıyor, dolayısıyla 4-5 aylık dar görev rakamına göre
daha az istatistiksel güvenilirliğe sahip [1]. Yayınlanan karşılaştırma
kümesi, GLM-5.2'den önce piyasaya çıkan Anthropic'in daha yeni modelleri
Opus 4.7 veya Opus 4.8'i içermiyor; dolayısıyla ölçülen fark, test
zamanındaki en güncel Anthropic modeline karşı değil, belirli bir daha eski
Opus neslinin karşısında ölçülmüş [1]. Bu, hakem denetiminden geçmiş bir
makale değil, AISI'nin kendi değerlendirme ekibinin blog yazısı.

## Neden önemli

Serbestçe indirilebilen modeller ile kapalı öncü sistemler arasındaki
yetenek farkının daralması, tehlikeli yeteneklere erişimin yalnızca kapalı
model API fiyatlarını ödeyebilenlerle sınırlı olmadığı anlamına geliyor —
bu nokta, açık modellerin aynı görevleri çalıştırmak için kapalı modellere
göre kabaca yarı fiyattan yetmiş kata kadar daha ucuz olduğunu gösteren
maliyet verileriyle daha da belirginleşiyor. AISI, açık modellerin kapalı
öncü sistemlerin aylar önce yapabildiklerine yetişmesiyle savunanların
hazırlık için daha az süresi kaldığını vurguluyor.
