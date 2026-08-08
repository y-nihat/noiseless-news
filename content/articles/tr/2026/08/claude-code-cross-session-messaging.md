---
title: Anthropic, Claude Code'a oturumlar arası mesajlaşma özelliği ekledi
date: 2026-08-07
slug: claude-code-cross-session-messaging
lang: tr
tldr: >
  Anthropic, 2.1.224 sürümüyle birlikte Claude Code'a, ayrı Claude Code
  oturumlarının birbirine kısa metin mesajları göndermesini sağlayan bir
  özellik ekledi -- bir bulguyu aktarmak, bekleyen bir soruyu yanıtlamak
  veya başka bir oturumun işini etkileyen bir değişikliği bildirmek için.
  Özellik macOS ve Linux'ta çalışıyor, oturumlar birbirini yeni bir
  `ListAgents` aracıyla buluyor ve mesajların iletilmesi kullanıcının
  ayarladığı, oturum bazlı gelen kutusu denetimlerine tabi.
sources:
  - name: Claude Code belgeleri (Anthropic)
    url: https://code.claude.com/docs/en/cross-session-messaging
  - name: Claude Code değişiklik günlüğü (Anthropic)
    url: https://code.claude.com/docs/en/changelog
  - name: ClaudeDevs (X)
    url: https://x.com/ClaudeDevs/status/2085817074816070014
  - name: 9to5Mac
    url: https://9to5mac.com/2026/08/07/claude-code-now-lets-sessions-talk-to-each-other-on-macos/
claims:
  - text: "Anthropic, 7 Ağustos 2026 tarihli Claude Code 2.1.224 sürümüyle oturumlar arası mesajlaşmayı kullanıma sundu; bu özellik, yeni bir SendMessage aracıyla bir Claude Code oturumunun diğerine metin mesajı göndermesini sağlıyor, ulaşılabilir oturumları bulmak için ise ListAgents aracı kullanılıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Özellik macOS ve Linux'ta (WSL 2 içindeki Linux dahil) kullanılabiliyor; yerel Windows'ta kullanılamıyor, ayrıca Amazon Bedrock, AWS üzerindeki Claude Platform, Google Cloud'un Agent Platform'u veya Microsoft Foundry üzerinden çalıştırıldığında da kullanılamıyor"
    type: capability
    verdict: confirmed
    evidence: [1]
  - text: "Bir mesaj yalnızca düz metinden oluşuyor, gönderenin sohbet geçmişini veya dosyalarını asla içermiyor; aynı makinedeki oturumlar arasında iletim yerel bir soket üzerinden yapılırken, kullanıcının başka bir makinesindeki veya web üzerindeki Claude Code oturumuna iletim Remote Control aracılığıyla Anthropic'in sunucuları üzerinden gerçekleşiyor ve bu makineler arası durumda alıcı taraf yeni bir mesaj başlatamıyor, yalnızca yanıt verebiliyor"
    type: capability
    verdict: confirmed
    evidence: [1]
  - text: "Gelen bir mesajın doğrudan iletilip iletilmeyeceği, onay için bekletilip bekletilmeyeceği veya reddedilip reddedilmeyeceği, oturum bazlı crossSessionInbound ayarı ve oturumların izin modlarıyla belirleniyor; bekletilen mesajlar, onaylanmadığı takdirde varsayılan olarak beş dakika sonra süresi doluyor (dialogExpiry ayarı)"
    type: capability
    verdict: confirmed
    evidence: [1]
  - text: "Anthropic'in kendi hesabı ClaudeDevs, özelliği aynı gün duyurdu ve bunu 'geçmişinizi değil, bir özet' gönderdiği, böylece başka bir oturumun işi kaldığı yerden devam ettirebildiği şeklinde tanımladı"
    type: statement
    verdict: confirmed
    evidence: [3]
updated: []
---

## Ne oldu

Anthropic, terminal tabanlı kodlama ajanı Claude Code'a, 7 Ağustos 2026
tarihli 2.1.224 sürümüyle oturumlar arası mesajlaşma özelliği ekledi
[1][2]. Özellik, çalışan bir Claude Code oturumunun yeni bir `SendMessage`
aracıyla başka bir oturuma kısa bir metin mesajı göndermesini sağlıyor;
tamamlayıcı bir `ListAgents` aracı ise bir oturumun hangi diğer oturumlara
ulaşabildiğini bulmasına yarıyor [1]. Anthropic'in kendi hesabı ClaudeDevs,
özelliği aynı gün duyurdu ve bunu terminaller arasında bağlamı tekrar
anlatma zorunluluğunu ortadan kaldıran bir yöntem olarak tanımladı: Claude
"geçmişinizi değil, bir özet" gönderiyor ve alıcı oturum "işi kaldığı
yerden devam ettiriyor" [3].

Anthropic'in belgelerine göre bir mesaj yalnızca düz metin içeriyor,
gönderenin tam sohbet geçmişini veya dosyalarını asla taşımıyor [1]. Aynı
makinede çalışan oturumlar mesajları yerel, oturuma özel bir soket
üzerinden alışverişte bulunuyor; farklı bir makinedeki bir oturuma veya web
üzerindeki bir Claude Code oturumuna mesaj göndermek ise ayrı bir özellik
olan Remote Control aracılığıyla Anthropic'in kendi sunucuları üzerinden
gerçekleşiyor ve bu makineler arası durumda alıcı taraf yalnızca gelen bir
mesaja yanıt verebiliyor, yeni bir mesaj başlatamıyor [1]. Gelen bir
mesajın otomatik olarak iletilip iletilmeyeceği, kullanıcının onayı için
bekletilip bekletilmeyeceği yoksa doğrudan reddedilip reddedilmeyeceği,
oturum bazlı bir `crossSessionInbound` ayarı ve oturumların izin
modlarıyla belirleniyor; bekletilen bir mesaj, onaylanmazsa varsayılan
olarak beş dakika içinde süresi dolarak düşüyor [1].

Özellik macOS ve Linux'ta (WSL 2 içindeki Linux dahil) kullanılabiliyor,
ancak yerel Windows'ta kullanılamıyor; Claude Code'un Amazon Bedrock, AWS
üzerindeki Claude Platform, Google Cloud'un Agent Platform'u veya
Microsoft Foundry üzerinden çalıştırıldığı durumlarda da kullanılamıyor
[1].

## Neden önemli

Aynı anda birden fazla Claude Code oturumu çalıştıran geliştiriciler --
örneğin aynı deponun ayrı git worktree'lerinde -- şimdiye kadar bir
oturumun diğerine ilgili bir değişikliği bildirmesinin tek yolu olarak
kullanıcının bunu elle aktarmasına bağlıydı. Oturumlar arası mesajlaşma bu
aktarımı otomatikleştiriyor; bunun karşılığında ise Anthropic'in her
yapılandırmada varsayılan olarak açık bırakmak yerine açık, kullanıcının
ayarlayabildiği izin denetimlerinden geçirdiği yeni bir ajanlar arası
iletişim kanalı ortaya çıkıyor [1].
