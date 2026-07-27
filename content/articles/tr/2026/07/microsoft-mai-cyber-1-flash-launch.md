---
title: Microsoft, kendi geliştirdiği ilk siber güvenlik modelini tanıttı; en zor vakaları OpenAI'ye yönlendiriyor
date: 2026-07-27
slug: microsoft-mai-cyber-1-flash-launch
lang: tr
tldr: >
  Microsoft, 27 Temmuz 2026'da siber güvenlik için özel olarak geliştirdiği ilk
  kendi yapay zeka modeli MAI-Cyber-1-Flash'ı tanıttı; model, şirketin güvenlik
  açığı tespit sistemi MDASH'ın içine yerleştirildi. Microsoft'a göre MDASH,
  güvenlik açığı analizi görevlerinin yaklaşık yüzde 90'ını yeni modele
  yönlendiriyor, en zor yüzde 10'luk kısmı ise OpenAI'nin GPT-5.4 modeline
  devrediyor. Şirket ayrıca, otomatik tehdit tespiti ve yama uygulaması için
  bir ajan tabanlı platform olan Project Perception'ı duyurdu; platform 3
  Ağustos 2026'da herkese açık ön izlemeye giriyor. Microsoft'un kendi
  ölçütlerine göre sistem CyberGym testinde yüzde 96 puan alıyor ve önceki
  yapılandırmaya kıyasla maliyeti yaklaşık yarı yarıya düşürüyor; bu rakamların
  hiçbiri bağımsız olarak doğrulanmadı.
sources:
  - name: Official Microsoft Blog
    url: https://blogs.microsoft.com/blog/2026/07/27/rethinking-security-for-the-age-of-ai/
  - name: Microsoft AI News
    url: https://microsoft.ai/news/introducing-mai-cyber-1-flash-inside-mdash/
  - name: TechCrunch
    url: https://techcrunch.com/2026/07/27/microsoft-launches-its-first-cyber-model-and-a-new-agentic-cybersecurity-system/
  - name: The Register
    url: https://www.theregister.com/security/2026/07/27/microsofts-solution-to-ai-security-more-ai-and-more-acronyms/5279140
  - name: The Decoder
    url: https://the-decoder.com/microsoft-launches-its-own-cybersecurity-model-mai-cyber-1-flash-but-still-depends-on-openai-for-the-toughest-tasks/
claims:
  - text: "Microsoft, 27 Temmuz 2026'da ilk özel siber güvenlik modeli MAI-Cyber-1-Flash'ı MDASH içine yerleştirilmiş şekilde tanıttı ve ajan tabanlı Project Perception platformunu duyurdu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "MDASH, güvenlik açığı analizi görevlerinin yaklaşık yüzde 90'ını MAI-Cyber-1-Flash'a yönlendiriyor, en zor yüzde 10'luk vakaları ise OpenAI'nin GPT-5.4 modeline devrediyor"
    type: business
    verdict: confirmed
    evidence: [2]
  - text: "Microsoft'a göre MAI-Cyber-1-Flash ve GPT-5.4 ile çalışan MDASH, CyberGym testinde yüzde 96 (tam olarak yüzde 95,95) puan alarak OpenAI'nin bağımsız modelleri GPT-5.5 Cyber (yüzde 85,6) ve GPT-5.6 Sol (yüzde 83,6) ile Anthropic'in Mythos 5 (yüzde 83) modelinin önüne geçiyor; bu da önceki MDASH yapılandırmasına göre maliyeti yaklaşık yarı yarıya düşürüyor"
    type: capability
    verdict: vendor-claim
    evidence: [1, 2, 4]
  - text: "Güvenlik açıklarını bulmak, önceliklendirmek ve yamalamak için 'kırmızı takım', 'mavi takım' ve 'yeşil takım' ajanlarını koordine eden Project Perception, 3 Ağustos 2026'da herkese açık ön izlemeye giriyor"
    type: business
    verdict: confirmed
    evidence: [1, 3]
updated: []
---

## Ne oldu

Microsoft, 27 Temmuz 2026'da MAI-Cyber-1-Flash'ı tanıttı ve bunu şirketin özel olarak siber güvenlik için geliştirdiği ilk yapay zeka modeli olarak nitelendirdi [1, 2]. Model, Microsoft'un yazılım güvenlik açıklarını bulup düzeltmek için kullandığı mevcut çok ajanlı sistem MDASH'ın içine yerleştirildi. Microsoft'un kendi duyurusuna göre MDASH artık güvenlik açığı analizi görevlerinin yaklaşık yüzde 90'ını MAI-Cyber-1-Flash'a devrediyor ve yalnızca en zor yüzde 10'luk vakaları OpenAI'nin GPT-5.4 modeline yönlendiriyor [2] — bu detay basının çıkarımı değil, Microsoft'un kendisinin açıkladığı bir bilgi.

Modelin yanı sıra Microsoft, istismar edilebilir yolları arayan "kırmızı takım" ajanları, riski araştırıp önceliklendiren "mavi takım" ajanları ve düzeltmeleri yazıp uygulayan "yeşil takım" ajanlarını koordine eden ajan tabanlı bir güvenlik platformu olan Project Perception'ı da duyurdu [1]. Project Perception, 3 Ağustos 2026'da herkese açık ön izlemeye giriyor [1, 3].

Microsoft'un kendi verilerine göre MDASH içindeki MAI-Cyber-1-Flash ve GPT-5.4 kombinasyonu, yapay zeka destekli güvenlik açığı tespiti için sektör ölçütü olan CyberGym testinde yüzde 96 (tam olarak yüzde 95,95) puan alıyor; bu da OpenAI'nin bağımsız modelleri GPT-5.5 Cyber (yüzde 85,6) ve GPT-5.6 Sol (yüzde 83,6) ile Anthropic'in Mythos 5 (yüzde 83) modelinin önünde, ayrıca Microsoft'un önceki MDASH yapılandırmasına kıyasla maliyeti yaklaşık yarı yarıya düşürüyor [1, 2]. Bunlar Microsoft'un kendi ölçüm sonuçları; The Register'ın haberi bu rakamları açıkça Microsoft yöneticilerinin iddiaları olarak çerçeveliyor ve CyberGym puanlarının bağımsız olarak yeniden üretildiğine dair herhangi bir kaynağa rastlanmadı [4].

## Neden önemli

Bu lansman, Microsoft'un dar kapsamlı ve göreve özel kendi güvenlik modelini geliştirirken en zor vakaları hâlâ OpenAI'ye yönlendirdiğini gösteriyor; bu da şirketin küçük, kendi bünyesinde geliştirdiği modeli sahip olmadığı sınır modellerin tam bir yerine geçen değil, bir maliyet aracı olarak gördüğünü ortaya koyuyor. Project Perception'ın otomatik yama uygulamaya doğru attığı adım, bu mimari tercihin önemini artırıyor: yönlendirme ve ölçüt iddiaları bağımsız testlerde doğrulanırsa, bu durum yapay zeka sistemlerinin güvenlik operasyonlarında şimdiye kadar olduğundan daha büyük ve daha özerk bir rol üstlendiğine işaret ediyor.
