---
title: OpenAI, ChatGPT'nin Mac uygulamasına Apple Mesajlar eklentisi ekledi
date: 2026-08-20
slug: openai-chatgpt-apple-messages-plugin
lang: tr
tldr: >
  OpenAI, 20 Ağustos 2026'da ChatGPT'nin macOS masaüstü uygulaması için bir
  Apple Mesajlar eklentisi yayına aldı: Apple Silicon Mac'lerde ChatGPT artık
  iMessage, SMS ve RCS konuşmalarını okuyabiliyor, arayabiliyor ve
  gönderebiliyor; gönderme işlemi varsayılan olarak mesaj başına onay
  adımıyla sınırlandırılıyor. OpenAI, Bloomberg'e özelliğin mesajları yerel
  olarak işlediğini ve kullanıcının mesajlarının tam bir dizinini
  oluşturmadığını söyledi; ancak işlem sırasında ne kadar mesaj içeriğinin
  yine de OpenAI'nin sunucularına ulaştığı, hiçbir bağımsız haberin
  doğrulayamadığı açık bir soru olarak kalıyor.
sources:
  - name: OpenAI (learn.chatgpt.com eklenti belgeleri)
    url: https://learn.chatgpt.com/docs/plugins
  - name: 9to5Mac
    url: https://9to5mac.com/2026/08/20/chatgpt-update-adds-apple-messages-integration-on-mac/
  - name: Bloomberg (Yahoo Finance üzerinden)
    url: https://finance.yahoo.com/technology/ai/articles/chatgpt-now-control-imessage-potentially-205633657.html
claims:
  - text: "OpenAI, ChatGPT'nin macOS masaüstü uygulaması için yalnızca Apple Silicon (arm64) Mac'lerle sınırlı bir Apple Mesajlar eklentisi yayına aldı; eklenti kullanıcının iMessage, SMS ve RCS konuşmalarını okuyup arayabiliyor, kullanıcı adına mesaj hazırlayıp gönderebiliyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "Gönderme işlemi varsayılan olarak mesaj başına onay adımıyla (\"Bir kez izin ver\") sınırlandırılıyor; kullanıcılar isterse daha sonra ChatGPT ayarlarından geri alabilecekleri kalıcı bir \"Bu sohbete göndermeye her zaman izin ver\" erişimi de verebiliyor; OpenAI'nin kendi belgeleri, güvenilmeyen talimatlar içeren sohbetlerde kalıcı onayın açılmamasını öğütlüyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Eklenti, OpenAI'nin kendi sürüm notlarına göre 20 Ağustos 2026'da yayına girdi ve Intel Mac'lerde, web'de, mobilde ya da diğer ChatGPT yüzeylerinde kullanılamıyor"
    type: announcement
    verdict: confirmed
    evidence: [1, 2]
  - text: "OpenAI, Bloomberg'e eklentinin mesajları kullanıcının Mac'inde yerel olarak işlediğini ve kullanıcının mesaj geçmişinin tam bir dizinini oluşturmadığını söyledi; Bloomberg'in haberi, işlem sırasında ne kadar mesaj içeriğinin OpenAI'nin sunucularına ulaştığını kendi haberciliğinin bağımsız olarak doğrulayamadığı açık bir soru olarak çerçeveliyor"
    type: statement
    verdict: single-source
    evidence: [3]
updated: []
---

## Ne oldu

OpenAI, 20 Ağustos 2026'da ChatGPT'nin macOS masaüstü uygulaması için,
yalnızca Apple Silicon Mac'lerle sınırlı bir Apple Mesajlar eklentisini
yayına aldı [1, 2]. Etkinleştirildiğinde ChatGPT, kullanıcının iMessage,
SMS ve RCS konuşmalarını okuyup arayabiliyor, kullanıcı adına mesaj
hazırlayıp gönderebiliyor [1]. Gönderme işlemi varsayılan olarak mesaj
başına onay adımıyla ("Bir kez izin ver") sınırlandırılıyor; kullanıcılar
bunun yerine, daha sonra ChatGPT ayarlarından geri alabilecekleri kalıcı
bir "Bu sohbete göndermeye her zaman izin ver" erişimi de verebiliyor —
OpenAI'nin kendi belgeleri, güvenilmeyen talimatlar içeren sohbetlerde
kalıcı onayın açılmamasını öğütlüyor [1]. Eklenti Intel Mac'lerde, web'de,
mobilde ya da diğer ChatGPT yüzeylerinde kullanılamıyor [1, 2].

Bloomberg'in, ChatGPT'nin kullanıcı mesajlarını okumasının gizlilik
etkilerine ilişkin sorusuna karşılık OpenAI, eklentinin mesajları Mac'te
yerel olarak işlediğini ve kullanıcının mesaj geçmişinin tam bir dizinini
oluşturmadığını söyledi [3]. İşlem sırasında ne kadar mesaj içeriğinin
yine de OpenAI'nin sunucularına ulaştığı bu açıklamada yanıtlanmıyor ve
hiçbir bağımsız haber bunu şimdiye dek doğrulamadı [3].

## Neden önemli

Apple Mesajlar, OpenAI'nin ChatGPT'yi Mac'te açtığı, cihazdaki en hassas
kişisel veri kümelerinden birine erişim karşılığında kolaylık sunan az
sayıdaki yerel-veri eklentisinden birine daha katılıyor. OpenAI'nin kendi
onay adımı tasarımı ve güvenilmeyen sohbetler için toptan "her zaman izin
ver" erişimine karşı uyarısı, şirketin riskin farkında olduğunu
düşündürüyor; Bloomberg'e göre yanıtlanmamış soru ise bu mesaj içeriğinin
ne kadarının zaten cihazdan çıktığı.
