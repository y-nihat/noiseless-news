---
title: Nvidia'nın Groq 3 LPX çıkarım rafı tam üretime geçti, ilk lansman ortağı Nebius oldu
date: 2026-08-24
slug: nvidia-groq-3-lpx-full-production
lang: tr
tldr: >
  Nvidia, 24 Ağustos 2026'da Groq 3 LPX çıkarım rafının tam üretime geçtiğini
  ve ilk lansman ortağının bulut sağlayıcı Nebius olduğunu duyurdu; Nvidia,
  daha geniş dağıtımın 2026 sonundan önce başlayacağını söylüyor. Raf,
  Nvidia'nın Aralık 2025'te yaklaşık 20 milyar dolar değerinde bildirilen bir
  anlaşmayla Groq'tan lisansladığı teknolojiye ve işe aldığı personele
  dayanıyor — Nvidia o dönemde bunun bir satın alma olmadığını söylemişti ve
  Groq bağımsız bir şirket olarak faaliyetine devam ediyor. Nvidia'nın kendi
  belirttiği bir karşılaştırma, rafın en yakın alternatifinden yaklaşık 4 kat
  daha hızlı olduğunu iddia ediyor; bu, henüz bağımsız olarak doğrulanmamış
  bir satıcı rakamı.
sources:
  - name: Nvidia Newsroom
    url: https://nvidianews.nvidia.com/news/nvidia-groq-3-lpx-now-in-full-production-with-world-class-speed-for-agentic-ai
  - name: CNBC
    url: https://www.cnbc.com/2026/08/24/nvidia-says-groq-racks-will-be-online-this-year-after-20-billion-deal.html
  - name: The Register
    url: https://www.theregister.com/systems/2026/08/24/what-nvidias-first-groq-3-lpu-benchmarks-do-and-dont-tell-us-about-its-20b-gamble/5291880
  - name: CNBC
    url: https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html
  - name: TrendForce
    url: https://www.trendforce.com/news/2025/12/29/news-nvidia-reportedly-denies-usd-20b-groq-acquisition-rumors
claims:
  - text: "Nvidia'nın Groq 3 LPX çıkarım rafı tam üretime geçti; Nebius ilk bulut lansman ortağı oldu."
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Nvidia, Nebius aracılığıyla da dahil olmak üzere Groq 3 LPX raflarının daha geniş dağıtımının 2026 sonundan önce başlayacağını söylüyor."
    type: announcement
    verdict: confirmed
    evidence: [2]
  - text: "Nvidia'nın Groq ile ilişkisi, Aralık 2025'te yaklaşık 20 milyar dolar değerinde bildirilen bir anlaşmaya dayanıyor; Nvidia o dönemde bunun Groq'un çıkarım teknolojisi için münhasır olmayan bir lisans ile kurucu Jonathan Ross ve başkan Sunny Madra dahil kilit personelin işe alınması olduğunu, şirketin satın alınması olmadığını söylemişti ve Groq bağımsız faaliyetine devam etti."
    type: business
    verdict: confirmed
    evidence: [4, 5]
  - text: "Nvidia, Groq 3 LPX rafının Gemma 4 31B üzerinde 100K bağlamda saniyede yaklaşık 3.400 çıktı token'ı sunduğunu ve en yakın alternatiften yaklaşık 4 kat daha hızlı olduğunu, duyurusunda atıfta bulunduğu bir Artificial Analysis karşılaştırmasına dayanarak belirtiyor."
    type: capability
    verdict: vendor-claim
    evidence: [1, 3]
updated: []
---

## Ne oldu

Nvidia, 24 Ağustos 2026'da Groq 3 LPX çıkarım rafının tam üretime geçtiğini açıkladı ve bulut sağlayıcı Nebius'u ilk lansman ortağı olarak duyurdu; Nebius'un kendi Teknoloji Sorumlusu, Nvidia'nın duyurusunda doğrudan alıntılanıyor [1]. Nvidia, Nebius'un Token Factory platformu üzerinden de dahil olmak üzere daha geniş kullanılabilirliğin 2026 sonundan önce geleceğini söylüyor — ancak Nvidia'nın açıklaması bu daha geniş kullanım için kesin bir tarih vermiyor [1][2].

Raf, Nvidia'nın Groq'un LPU tarzı çıkarım çip tasarımına yönelmesinin bir ürünü. Bu ilişki, Aralık 2025'te yaklaşık 20 milyar dolar değerinde bildirilen ve o dönemde bir satın alma olarak tanımlanan bir anlaşmayla başladı. Nvidia, anlaşmanın aslında Groq'un çıkarım teknolojisine yönelik münhasır olmayan bir lisans ile kurucu Jonathan Ross ve başkan Sunny Madra dahil kilit Groq personelinin işe alınması olduğunu — şirketin satın alınması olmadığını — söyledi; Groq o tarihten beri bağımsız faaliyetine devam ediyor [4][5].

Nvidia, Groq 3 LPX'in Gemma 4 31B üzerinde 100K bağlamda saniyede yaklaşık 3.400 çıktı token'ı sunduğunu ve en yakın alternatiften yaklaşık dört kat daha hızlı olduğunu gösteren bir Artificial Analysis karşılaştırmasına atıfta bulunuyor — bağımsız olarak henüz yeniden üretilmemiş, satıcı tarafından sağlanan bir rakam [1]. Aynı gün yayımlanan bağımsız sektör haberleri, testin görece küçük ve yoğun (dense) bir model kullandığını, Nvidia'nın bir rakibin diğer iş yüklerinde sadece bir veya iki çiple ulaştığı verimi yakalamak için 64 veya daha fazla çipe ihtiyaç duyduğunu ve daha büyük modellerdeki performansın henüz test edilmediğini belirtti [3].

## Neden önemli

Groq'un çip mimarisi, Nvidia'nın GPU'larının başlangıçta tasarlanmadığı bir alan olan hızlı çıkarım için özel olarak geliştirildi. Bu teknolojiyi — Groq'u nominal olarak bağımsız bırakırken — kendi ürün hattına katmak, Nvidia'ya resmi bir satın alma yapmadan özel çıkarım donanımında rekabet etme imkânı veriyor ve Nebius gibi bulut sağlayıcılarına, çıkarım talebi arttıkça Nvidia markalı başka bir seçenek sunuyor.
