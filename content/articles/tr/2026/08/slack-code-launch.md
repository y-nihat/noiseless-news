---
title: Slack, yapay zeka kodlama ajanlarını ekip kanallarına taşıyan Slack Code'u duyurdu
date: 2026-08-20
published: 2026-08-22
slug: slack-code-launch
lang: tr
tldr: >
  Slack (Salesforce), 20 Ağustos 2026'da Slack Code'u duyurdu: bir ekibin ve
  bir yapay zeka kodlama ajanının Slack içinde birlikte kod yazıp incelediği
  ve gönderdiği, diff'lerin ve canlı önizlemenin tüm kanala açık olduğu özel
  "Kod Kanalları". Claude Code, GitHub Copilot, Devin ve Vercel'in ajanı
  lansmanda hazır; OpenAI'ın ChatGPT'si yakında geliyor olarak duyuruldu.
sources:
  - name: Slack
    url: https://slack.com/blog/news/slack-code-channels-for-agents
  - name: VentureBeat
    url: https://venturebeat.com/orchestration/slack-wants-to-drag-ai-coding-out-of-the-terminal-and-into-the-group-chat
  - name: SiliconANGLE
    url: https://siliconangle.com/2026/08/20/salesforce-introduces-slack-code-to-bring-agentic-team-coding-into-the-open/
claims:
  - text: "Slack, 20 Ağustos 2026'da \"Slack Code\"u başlattı: bir ekibin Slack içinde bir yapay zeka kodlama ajanıyla birlikte çalıştığı, sohbet, plan, kod diff'leri ve canlı önizlemenin kanalda yer aldığı, herhangi bir şey gönderilmeden önce incelenip onaylanabildiği özel \"Kod Kanalları\"."
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Claude Code (Anthropic), GitHub Copilot, Devin (Cognition) ve Vercel'in ajanı lansmanda hazır; OpenAI'ın ChatGPT'si ortak olarak duyuruldu ancak ilk gün aktif değil, yakında geliyor olarak listelendi."
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "Lansman etkinliğinde Cognition başkanı Jeff Wang, Slack Code'un kendisini değil şirket genelindeki mühendislik hızını gösteren bir bağlam verisi paylaştı: birleştirilen pull request sayısının \"son birkaç ayda 10 kat\" arttığını, buna karşılık çalışan sayısının \"yaklaşık yüzde 40\" arttığını söyledi."
    type: capability
    verdict: vendor-claim
    evidence: [2]
  - text: "Slack Code, lansmanda her Slack planında kullanılabiliyor; müşterilerin yine de kullanmak istedikleri her ortak yapay zeka ajanına kendi ayrı erişimlerinin/lisanslarının olması gerekiyor."
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
updated: []
---

## Ne oldu

Salesforce'a bağlı Slack, 20 Ağustos 2026'da Slack Code'u tanıttı: bir ekibin ve bir yapay zeka kodlama ajanının, ayrı bir araca geçmeden, Slack içinde birlikte kod yazıp incelediği ve gönderdiği özel "Kod Kanalları" oluşturan bir özellik [1]. Herhangi bir konuşmada bir ajanı etiketlemek; sohbet, plan, kod diff'leri ve canlı önizleme için sekmeleri olan bir kanal başlatıyor, böylece tüm ekip bir şey gönderilmeden önce izleyip yorum yapabiliyor [1][2].

Lansmanda Claude Code (Anthropic), GitHub Copilot, Devin (Cognition) ve Vercel'in ajanı kullanılabiliyor; OpenAI'ın ChatGPT'si ortak olarak duyuruldu ancak ilk gün aktif değil, yakında geliyor olarak listelendi [1][2][3]. Slack Code, ek ücret olmadan her Slack planında kullanılabiliyor; ancak müşterilerin kullanacakları ortak ajana kendi ayrı erişimlerinin olması gerekiyor [2][3].

Lansman etkinliğinde Cognition başkanı Jeff Wang, aynı gün başlayan Slack Code'un kendi performansını değil, şirket genelindeki mühendislik hızını gösteren bir veriyi bağlam olarak paylaştı: Devin'in genel kullanımıyla birleştirilen pull request sayısının "son birkaç ayda 10 kat" arttığını, buna karşılık çalışan sayısının "yaklaşık yüzde 40" arttığını söyledi [2] — bu, Cognition'ın kendi verdiği, bağımsız denetimden geçmemiş bir rakam.

## Neden önemli

Mevcut kodlama ajanları çoğunlukla tek başına, bir terminal ya da IDE içinde, çıktıyı tek bir geliştiricinin incelediği şekilde çalışıyor. Slack Code bu çalışmayı ekibin grup sohbetinin içine taşıyor ve bir ajanın çıktısını varsayılan olarak tüm kanala açıyor. Bu aynı zamanda Slack için bir dağıtım hamlesi: kendi kodlama ajanını inşa etmek yerine, OpenAI'ınki de dahil olmak üzere rakip ajanların yan yana çalıştığı ortak yüzey olmayı hedefliyor.
