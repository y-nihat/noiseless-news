---
title: Alibaba açık ağırlıklı Qwen3.8 modellerini yayımladı, ticari lisans için 50 milyon dolarlık gelir eşiği belirledi
date: 2026-08-14
slug: alibaba-qwen-revenue-share-plan
lang: tr
tldr: >
  Alibaba'nın Qwen ekibi, Ağustos 2026 ortasında iki Qwen3.8 modelinin açık
  ağırlıklarını yayımladı: izin verici Apache 2.0 lisanslı Qwen3.8-27B ve
  amiral gemisi Qwen3.8-Max'in açık ağırlıklı sürümü olan Qwen3.8-2.4T-A95B.
  İkincisi, "model olarak hizmet" ya da "yapay zeka iş asistanı" işinden
  herhangi bir 12 aylık dönemde 50 milyon doları aşan gelir elde eden
  şirketlerden ayrı bir ücretli ticari lisans talep eden yeni, özel bir
  lisansla geliyor. Bu, Reuters'in isimsiz kaynaklara dayanarak bildirdiği
  yüzde bazlı gelir paylaşımı haberini netleştiriyor: yayımlanan koşullar
  sabit bir gelir eşiği kapısı, yüzdelik bir gelir kesintisi değil.
sources:
  - name: Hugging Face — Qwen/Qwen3.8-2.4T-A95B model kartı
    url: https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B
  - name: Hugging Face — Qwen/Qwen3.8-27B model kartı
    url: https://huggingface.co/Qwen/Qwen3.8-27B
  - name: South China Morning Post
    url: https://www.scmp.com/tech/tech-trends/article/3363927/alibaba-adds-commercial-restrictions-open-weight-qwen38-max-ai-model
  - name: Investing.com (Reuters)
    url: https://www.investing.com/news/stock-market-news/alibaba-plans-revenuesharing-for-commercial-users-of-next-qwen-ai-model--reuters-4845019
claims:
  - text: "Alibaba'nın Qwen ekibi, Ağustos 2026 ortasında Apache 2.0 lisanslı Qwen3.8-27B ve Qwen3.8-Max'in açık ağırlıklı sürümü olan Qwen3.8-2.4T-A95B modellerinin ağırlıklarını yayımladı"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Qwen3.8-2.4T-A95B, özel bir \"Qwen3.8-Max Lisansı\" ile geliyor: indirmek, kullanmak ve dahili ticari kullanım dahil değiştirmek ücretsiz, ancak toplam \"model olarak hizmet\" ya da \"yapay zeka iş asistanı\" geliri herhangi bir 12 aylık dönemde 50 milyon doları aşan şirketlerin (ve bağlı kuruluşlarının) ayrı bir ücretli ticari lisans alması gerekiyor"
    type: business
    verdict: confirmed
    evidence: [1, 3]
  - text: "Bu, Reuters'in 7 Ağustos 2026'da isimsiz kaynaklara dayanarak bildirdiği yüzde bazlı gelir paylaşımı düzenlemesi değil, sabit bir gelir eşiği kapısı"
    type: business
    verdict: confirmed
    evidence: [3, 4]
updated: []
---

## Ne oldu

Alibaba'nın Qwen ekibi, Ağustos 2026 ortasında iki yeni Qwen3.8 modelinin açık
ağırlıklarını yayımladı [1][2]. Daha küçük bir görsel-dil modeli olan
Qwen3.8-27B, izin verici Apache 2.0 lisansı altında sunuluyor [2]. Alibaba'nın
amiral gemisi Qwen3.8-Max'in açık ağırlıklı sürümü olan Qwen3.8-2.4T-A95B ise
bunun yerine yeni, özel bir "Qwen3.8-Max Lisansı" ile geliyor [1][3].

Bu lisans; çıktılar ve model yetenekleri üçüncü taraflarla paylaşılmadığı
sürece, dahili ticari kullanım dahil olmak üzere indirmek, kullanmak ve
değiştirmek için ücretsiz [1][3]. Ayrı, ücretli bir ticari lisans yalnızca —
bağlı kuruluşları da dahil olmak üzere — "model olarak hizmet" ya da "yapay
zeka iş asistanı" ürünü işleten ve bu işten elde ettiği toplam geliri herhangi
bir 12 aylık dönemde 50 milyon doları aşan şirketler için gerekiyor [1][3].
Alibaba, modelin kendi barındırdığı API'sini de ayrıca fiyatlandırıyor; bu
fiyat Claude Opus 5'in uluslararası girdi-token ücretinin yaklaşık %40'ına
denk geliyor [3].

Bu koşullar, sitemizin 7 Ağustos 2026'dan beri takip ettiği bir soruyu
netliğe kavuşturuyor: Reuters o tarihte isimsiz kaynaklara dayanarak,
Alibaba'nın bir sonraki Qwen modelinin büyük ticari kullanıcıları için yüzde
bazlı bir gelir paylaşımı düzenlemesi planladığını bildirmişti [4].
Alibaba'nın fiilen yayımladığı lisans ise sabit bir gelir eşiği kapısı —
yüzdelik bir gelir kesintisi değil [3][4].

## Neden önemli

Çin merkezli yapay zeka laboratuvarları, bu yılki açık ağırlık ivmesinin
büyük bölümünü sınır ötesi düzeydeki modelleri ücretsiz sunarak yönlendirdi.
Qwen3.8-Max'in lisansı, bir laboratuvarın bu ivmeyi korurken en büyük ticari
kullanıcılardan gelir elde etmeye çalıştığı somut örneklerden biri: meraklılar,
girişimler ve dahili kullanımlar ücretsiz kalıyor, ancak bu ağırlıklar
üzerine önemli boyutta bir yapay zeka modeli ya da asistan işi kuran her
şirket sonunda doğrudan Alibaba'ya ödeme yapmak zorunda kalıyor.
