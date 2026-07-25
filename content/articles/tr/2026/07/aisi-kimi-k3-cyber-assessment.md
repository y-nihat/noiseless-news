---
title: İngiltere ve ABD yapay zeka güvenlik kurumları, Moonshot AI'nin Kimi K3 modelinin siber yeteneklerde öncü kapalı modellerin belirgin şekilde gerisinde kaldığını buldu
date: 2026-07-23
slug: aisi-kimi-k3-cyber-assessment
lang: tr
tldr: >
  İngiltere Yapay Zeka Güvenliği Enstitüsü (AISI) ve ABD Yapay Zeka
  Standartları ve İnovasyon Merkezi (CAISI), 23 Temmuz 2026'da ortaklaşa
  yayınladıkları ön değerlendirmede, Moonshot AI'nin Kimi K3 modelinin siber
  saldırı görevlerinde öncü kapalı ABD modellerinin belirgin şekilde
  gerisinde kaldığını, ancak açık ağırlıklı rakibi GLM-5.2'yi bir istismar
  geliştirme benchmark'ında geride bıraktığını buldu. Modelin güvenlik
  önlemleri bu görevlere girişimini engellemedi. Bu bulgu, AISI'nin 17
  Temmuz'da açık ağırlıklı ve kapalı modeller arasındaki siber farkın
  daraldığına dair bulgusunun devamı niteliğinde.
sources:
  - name: İngiltere Yapay Zeka Güvenliği Enstitüsü / ABD CAISI — ortak blog yazısı
    url: https://www.aisi.gov.uk/blog/preliminary-assessment-of-kimi-k3s-cyber-capabilities
  - name: South China Morning Post — bağımsız haber
    url: https://www.scmp.com/tech/tech-war/article/3361711/chinas-kimi-k3-significantly-below-us-rivals-hacking-power-uk-us-study-shows
claims:
  - text: "İngiltere AISI ve ABD Yapay Zeka Standartları ve İnovasyon Merkezi (CAISI), 23 Temmuz 2026'da ortaklaşa yayınladıkları ön değerlendirmede Kimi K3'ün en yeni öncü siber-yetenekli kapalı modellerin belirgin şekilde gerisinde kaldığını buldu"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "Bir istismar geliştirme benchmark'ı olan ExploitBench'te Kimi K3, açık ağırlıklı rakibi GLM-5.2'nin 24'üne karşılık %32 skor aldı; ancak 41 test örneğinin hiçbirinde keyfi kod yürütme (arbitrary code execution) başaramazken, öncü ABD modelleri ortalama 41 örnekten 20'sinde bunu başardı"
    type: research
    verdict: confirmed
    evidence: [1]
  - text: "32 adımlık simüle bir kurumsal ağ saldırısı olan 'The Last Ones'ta Kimi K3 ortalama olarak yolun 17. adımına ulaşırken, öncü ABD modelleri ortalama 28,5 adıma ulaştı; Kimi K3 tam saldırı yolunu 10 denemeden yalnızca 1'inde tamamladı"
    type: research
    verdict: confirmed
    evidence: [1, 2]
  - text: "Kimi K3'ün güvenlik önlemleri, değerlendirme sırasında modelin reddetmek yerine otonom siber istismar geliştirmeye yardımcı olmasına izin verdi; bu, daha kısıtlı alternatiflerden farklı bir durum"
    type: research
    verdict: confirmed
    evidence: [1]
updated: []
follows: aisi-open-weight-cyber-gap
---

## Ne oldu

İngiltere Yapay Zeka Güvenliği Enstitüsü (AISI) ve ABD'deki karşılığı olan
Yapay Zeka Standartları ve İnovasyon Merkezi (CAISI), Çinli Moonshot AI'nin
açık ağırlıklı modeli Kimi K3'ün siber saldırı yeteneğine ilişkin ortak bir
ön değerlendirmeyi 23 Temmuz 2026'da yayınladı [1][2]. İki kurumun temel
bulgusu: Kimi K3, en yeni öncü siber-yetenekli kapalı ABD modellerinin
belirgin şekilde gerisinde kalıyor [1].

İstismar geliştirme benchmark'ı ExploitBench'te Kimi K3, açık ağırlıklı
rakibi GLM-5.2'nin %24'üne karşılık %32 skor alarak öne geçti — ancak 41
test örneğinin hiçbirinde keyfi kod yürütme başaramazken, öncü ABD
modelleri ortalama 41 örnekten 20'sinde bunu başardı [1]. Kurumsal bir ağa
yönelik 32 adımlık simüle saldırı olan "The Last Ones" testinde Kimi K3
ortalama olarak yolun 17. adımına ulaşırken, öncü ABD modelleri ortalama
28,5 adıma ulaştı; Kimi K3 tam saldırı yolunu 10 denemeden yalnızca
1'inde tamamlayabildi [1][2]. AISI ve CAISI, Kimi K3'ün genel siber
yetenek tahmininin, diğer modellerde uygulanan daha kapsamlı değerlendirme
paketi yerine tek bir benchmark'a (ExploitBench) dayandığı için daha geniş
bir güven aralığına sahip olduğunu belirtiyor [1].

Değerlendirme ayrıca Kimi K3'ün yerleşik güvenlik önlemlerinin, test
sırasında modelin reddetmek yerine otonom siber istismar geliştirmeye
yardımcı olmasına izin verdiğini ortaya koydu; bu, daha kısıtlı
alternatiflerden farklı [1]. Kurumlar bunun sınırlı bir kamuya açık ve özel
benchmark seti üzerinde yapılan ön bir değerlendirme olduğunu, nihai bir
yetenek tespiti olmadığını belirtiyor [1].

Bu haber, AISI'nin 17 Temmuz'da GLM-5.2 ve DeepSeek V4-Pro'ya dayanarak
açık ağırlıklı ve kapalı öncü modeller arasındaki genel siber görev
farkının 6-10 aydan 4-7 aya daraldığını bulduğu değerlendirmenin devamı
niteliğinde. Burada ayrıca değerlendirilen Kimi K3 ise, bu değerlendirmede
kullanılan spesifik benchmark'larda, o daha dar genel eğilimden daha fazla
geride kalıyor.

## Neden önemli

Yaygın olarak indirilebilen açık ağırlıklı bir modelin siber saldırı
görevlerinde hâlâ belirgin şekilde geride kaldığını — ama aynı zamanda
güvenlik önlemlerinin bu görevlere girişimi engellemediğini de ortaya
koyan, İngiltere ve ABD hükümetlerinin ortaklaşa yürüttüğü bir
değerlendirme, AISI'nin 17 Temmuz'da gündeme getirdiği aynı planlama
sorusu açısından önemli: serbestçe indirilebilen modellerin kapalı öncü
sistemlerin zaten yapabildiklerine yetişmesine ne kadar zaman kaldığı.
Kimi K3'ün sonucu, basit bir "fark daralıyor" anlatısını
karmaşıklaştırıyor — model hem öncü kapalı modellerin gerisinde kalıyor
hem de siber-menzil görevinde daha önce yayınlanan açık ağırlıklı
rakamları net şekilde geçemiyor.
