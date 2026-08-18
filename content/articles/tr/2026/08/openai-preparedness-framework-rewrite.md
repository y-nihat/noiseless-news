---
title: OpenAI, en yeni modellerinde pekiştirmeli öğrenme eğitimini iki hafta durdurduğunu, Preparedness Framework'ü yeniden yazmayı planladığını söyledi
date: 2026-08-18
slug: openai-preparedness-framework-rewrite
lang: tr
tldr: >
  OpenAI, Temmuz'daki Hugging Face ajan güvenliği ihlalinin ve henüz
  yayınlanmamış Astra modelinin en yüksek siber risk eşiğini aşmış
  olabileceğine dair ilk bulguların ardından, en yeni modellerinde
  pekiştirmeli öğrenme (RL) eğitimini iki hafta durdurduğunu; ardından
  araştırma ortamlarını sıkılaştırıp izlemeyi artırdığını açıkladı. İki
  haftalık duraklama sona erdi ve küçük ölçekli eğitimler yeniden başladı,
  ancak OpenAI en büyük sınır eğitim çalıştırmalarının hâlâ askıda
  olduğunu; "Kritik" gibi eşikleri tanımlayan Preparedness Framework
  (Hazırlık Çerçevesi) belgesini dış katkıyla yeniden yazmayı planladığını,
  ancak henüz bir takvim belirlemediğini söylüyor.
sources:
  - name: OpenAI
    url: https://x.com/OpenAI/status/2089777845187031262
  - name: TechCrunch
    url: https://techcrunch.com/2026/08/18/openai-institutes-new-safeguards-after-hugging-face-breach/
  - name: Axios
    url: https://www.axios.com/2026/08/18/openai-pause-astra-preparedness-framework
  - name: Time
    url: https://time.com/article/2026/08/18/openai-slowing-training/
claims:
  - text: "OpenAI, Temmuz'daki Hugging Face ajan güvenliği ihlalini ve henüz yayınlanmamış Astra modelinin Preparedness Framework'teki 'Kritik' siber yetkinlik eşiğine ulaşmış olabileceğine dair ilk bulguları gerekçe göstererek, dağıtıma hazırlanan en yeni modellerinde pekiştirmeli öğrenme (RL) eğitimini iki hafta durdurdu"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "İki haftalık duraklama sona erdi; OpenAI daha az riskli birçok eğitim iş yükünü yeniden başlattığını, ancak en büyük ve en gelişmiş sınır RL çalıştırmalarının yeni güvenlik önlemleri tamamlanana dek askıda kaldığını söylüyor"
    type: announcement
    verdict: confirmed
    evidence: [2, 4]
  - text: "Duraklama sırasında OpenAI araştırma ortamlarını izole etti, tek bir güvenlik ihlalinin başlı başına internete ya da iç ağlara erişim sağlamayacağı şekilde ağ ve araç erişimini kısıtladı, modellerin araç eylemlerine ve akıl yürütme izlerine yönelik izlemeyi genişletti ve anormalliklere yaklaşık 30 dakikada yanıt vermeyi hedefledi"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "OpenAI, 'Kritik' gibi risk eşiklerini tanımlayan Preparedness Framework belgesini geliştirip yeniden yazmayı ve bu süreçte dış kuruluşları dahil etmeyi planlıyor; ancak henüz bir takvim belirlemedi ya da taslak yayınlamadı"
    type: statement
    verdict: confirmed
    evidence: [3, 4]
updated: []
follows: openai-astra-critical-cyber-capabilities
---

## Ne oldu

OpenAI, 18 Ağustos 2026'da, dağıtıma hazırlanan en yeni modellerindeki
pekiştirmeli öğrenme (RL) eğitimini "araştırma ortamlarımızı
sıkılaştırıp kırmızı takım testinden geçirirken" iki hafta süreyle
geçici olarak durdurduğunu açıkladı ve izlemeyi artırdı [1]. Şirket bu
duraklamayı, Temmuz'daki Hugging Face ajan güvenliği ihlaline ve henüz
yayınlanmamış Astra modelinin, OpenAI'nin 7 Ağustos'ta ilk kez
duyurduğu Preparedness Framework'teki "Kritik" siber güvenlik eşiğine
ulaşmış olabileceğine dair ilk bulgulara bağladı [1][2][3].

İki haftalık süre sona erdi. OpenAI, daha az riskli birçok eğitim iş
yükünü yeniden başlattığını, ancak en büyük ve en gelişmiş sınır RL
çalıştırmalarının yeni güvenlik önlemleri geliştirilirken askıda
kaldığını söylüyor [2][4].

Duraklama sırasında OpenAI araştırma ortamlarını izole etti; şirketin
kendi ifadesiyle, tek bir iş yükünün güvenliğinin aşılması başlı başına
internete ya da diğer iç ağlara erişim sağlamayacak şekilde ağ ve araç
erişimini kısıtladı; modellerin araç eylemlerine ve akıl yürütme
izlerine yönelik izlemeyi de genişletti ve anormalliklere yaklaşık 30
dakikada yanıt vermeyi hedefledi [1][2]. OpenAI Araştırma Başkan
Yardımcısı Amelia Glaese, şirketin "güvenli geliştirme için gereklilikler
ve beklentiler ortaya koyduğunu" ve bunların bir modelde görülen risk
düzeyine göre değiştiğini söyledi [2].

OpenAI ayrıca, "Kritik" gibi risk eşiklerini tanımlayan Preparedness
Framework belgesini geliştirip yeniden yazmayı ve bu süreçte dış
kuruluşları dahil etmeyi planladığını, ancak henüz bir takvim
belirlemediğini ya da taslak yayınlamadığını söylüyor [3][4]. Baş
Bilim İnsanı Jakub Pachocki, Time'a çerçeveyi "kesinlikle" geliştirmeleri
gerekeceğini söyledi; CEO Sam Altman ise "yavaşlamak için iyi bir zaman"
olduğunu ve "yapay zekâ güvenliğini doğru yapmanın herhangi bir
şirketin ivmesinden daha önemli olduğunu" belirtti [4].

Bu gelişme, OpenAI'nin Preparedness ekibini feshettiğine dair, hâlâ
doğrulanmamış ayrı bir haberden farklıdır — OpenAI bu personel iddiasını
resmi olarak yalanlamıştı. Bugünkü değişiklikler o ekibin yapısıyla
değil, Preparedness Framework belgesiyle ve genel güvenlik
uygulamalarıyla ilgili.

## Neden önemli

Bu, OpenAI'nin 7 Ağustos'ta Astra hakkında ortaya attığı Kritik-eşik
sorularına verdiği en somut yanıt: şirket tek bir modeli kısıtlamak
yerine, sınır modelleri genel olarak nasıl eğittiğini ve izlediğini
değiştiriyor, bir modelin ne zaman yayınlanamayacak kadar riskli
sayılacağını tanımlayan belgeyi yeniden gözden geçiriyor. Değişikliklerin
etkili olduğuna dair bağımsız bir doğrulama — ve Astra için nihai yayın
kararı — hâlâ bekleniyor.
