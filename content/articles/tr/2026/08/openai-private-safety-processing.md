---
title: "OpenAI, sıfır veri saklamayı koruyan kötüye kullanım tespit sistemi Private Safety Processing'i önizliyor"
date: 2026-08-19
slug: openai-private-safety-processing
lang: tr
tldr: >
  OpenAI, 19 Ağustos 2026'da, Private Safety Processing adlı yeni bir
  sistemi ilk kurumsal ve API müşterileriyle test ettiğini açıkladı. Sistem,
  altta yatan istemleri veya yanıtları değil, yalnızca dar kapsamlı bir
  güvenlik sinyalini OpenAI'ye göndererek bir müşterinin birbiriyle ilişkili
  etkileşimleri arasındaki kötüye kullanım örüntülerini tespit etmeyi
  hedefliyor; bu sırada OpenAI'nin mevcut Sıfır Veri Saklama (ZDR)
  koşullarıyla uyumlu kalıyor. OpenAI, Eylül 2026'da daha geniş bir kullanıma
  sunum ve teknik bir beyaz kağıt yayımlamayı planlıyor; özellik şimdilik
  yalnızca kurumsal ve API müşterileri için geçerli, tüketici ChatGPT
  planları için değil.
sources:
  - name: OpenAI News
    url: https://openai.com/index/offering-zero-data-retention-for-frontier-models
  - name: Bloomberg
    url: https://www.bloomberg.com/news/articles/2026-08-19/openai-to-enhance-safety-processes-for-paid-tool-customers
  - name: Axios
    url: https://www.axios.com/2026/08/19/openai-previews-zero-retention-safety-system-as-anthropic-requires-data-logs
  - name: OpenAI News
    url: https://openai.com/index/responding-next-frontier-critical-cyber-capabilities
claims:
  - text: "OpenAI'nin Sıfır Veri Saklama (ZDR) koşullarına göre, uygun API müşterilerinin gönderdiği istemler ve yanıtlar istek işlendikten sonra saklanmaz, OpenAI personelinin incelemesine açılmaz ve müşteri onay vermedikçe modellerini eğitmek için kullanılmaz"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "OpenAI, bir müşterinin birbiriyle ilişkili etkileşimleri arasındaki kötüye kullanım örüntülerini, altta yatan istemler veya yanıtlar yerine OpenAI'ye yalnızca dar kapsamlı tanımlanmış bir güvenlik sinyali göndererek tespit etmeyi hedefleyen yeni bir sistem olan Private Safety Processing'i önizliyor; müşteri verileri müşterinin altyapısında kalabilir veya OpenAI tarafından müşterinin kontrol ettiği anahtarlarla şifrelenerek saklanabilir ve sistem ZDR ile uyumlu kalır"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Private Safety Processing şu anda ilk kurumsal ve API müşterileriyle test ediliyor; OpenAI, Eylül 2026'da daha geniş bir kullanıma sunum ve teknik bir beyaz kağıt yayımlamayı planladığını söylüyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 3]
  - text: "Yeni sistem kurumsal ve API müşterileriyle sınırlı olup şu an için tüketici ChatGPT abonelik planlarını kapsamıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "OpenAI ayrıca, henüz yayımlanmamış Astra modelinin şirketin en yüksek siber risk eşiğini aşabileceğini söyledi ve buna bağlı pekiştirmeli öğrenme çalışmasını ek güvenlik önlemleri devreye girene kadar durdurdu"
    type: announcement
    verdict: confirmed
    evidence: [4]
updated: []
---

## Ne oldu

OpenAI'nin mevcut Sıfır Veri Saklama (ZDR) koşullarına göre, uygun API
müşterilerinin gönderdiği istemler ve yanıtlar istek işlendikten sonra
saklanmıyor, OpenAI personelinin incelemesine açılmıyor ve müşteri açıkça
onay vermedikçe modellerini eğitmek için kullanılmıyor [1]. OpenAI, 19
Ağustos 2026'da, bu temelin üzerine Private Safety Processing adını verdiği
yeni bir sistemi ilk kurumsal ve API müşterileriyle önizlemeye başladığını
duyurdu [1][2][3].

Private Safety Processing, bir müşterinin birbiriyle ilişkili etkileşimleri
arasındaki kötüye kullanım örüntülerini tespit etmek için tasarlandı --
OpenAI, bugünün ZDR uyumlu güvenlik araçlarının bunu yapamadığını, çünkü
her etkileşimi ayrı ayrı değerlendirdiklerini söylüyor. OpenAI, altta yatan
istemleri ve yanıtları görmek yerine yalnızca "dar kapsamlı olarak
tanımlanmış bir güvenlik sinyali" aldığını belirtiyor; müşteri verileri
müşterinin kendi altyapısında kalabilir veya OpenAI tarafından müşterinin
kontrol ettiği anahtarlarla şifrelenerek saklanabilir [1][2][3]. Sistem şu
anda ilk müşterilerle test ediliyor; OpenAI, Eylül 2026'da daha geniş bir
kullanıma sunum ve teknik bir beyaz kağıt yayımlamayı planladığını söylüyor
[1][3]. Şimdilik yalnızca kurumsal ve API müşterileriyle sınırlı, tüketici
ChatGPT abonelik planlarını kapsamıyor [1][2].

## Neden önemli

Bu duyuru, OpenAI'nin henüz yayımlanmamış Astra modelinin şirketin en
yüksek siber risk eşiğini aşabileceğini ve buna bağlı pekiştirmeli öğrenme
çalışmasını ek güvenlik önlemleri devreye girene kadar durdurduğunu ayrıca
açıkladığı haftaya denk geliyor [4] -- bu da şirketin gizlilik taahhütleri
ile kendi en yetenekli modelleri hakkındaki güvenlik endişelerinin paralel,
her zaman güven verici olmayan raylarda ilerlediğinin bir hatırlatıcısı.
Private Safety Processing'in kendisi de henüz bir önizleme aşamasında: bir
güvenlik sinyalinin içeriği dolaylı yoldan sızdırıp sızdıramayacağına dair
henüz bağımsız bir teknik inceleme yapılmadı ve Eylül'deki kullanıma sunum,
sevk edilmiş bir ürün değil, beyan edilmiş bir plan.
