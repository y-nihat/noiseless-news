---
title: Mistral, yapay zekâ modelleri için çok adımlı arama aracı Agentic Search'ü duyurdu
date: 2026-08-20
slug: mistral-agentic-search
lang: tr
tldr: >
  Mistral AI, 20 Ağustos 2026'da Agentic Search'ü duyurdu: yapay zekâ
  modellerinin tek geçişli bir alma (retrieval) adımına güvenmek yerine
  karmaşık belgelerde bilgi arayıp gezinmesini, okumasını ve doğrulamasını
  sağlayan beş araçlı, çok adımlı bir yetenek. Mistral Medium 3.5 ve
  Z.ai'nin GLM-5.2 modeliyle test edilen özellik için Mistral'in kendi
  ölçütleri, doğruluğun bir SEC dosyaları değerlendirmesinde %26,7'den
  %86'ya, bir Hazine bültenleri değerlendirmesinde %6,3'ten %51,9'a
  çıktığını bildiriyor; daha düşük gecikme ve token tüketimiyle birlikte
  bu rakamlar Mistral'e ait olup bağımsız olarak doğrulanmadı.
sources:
  - name: Mistral AI
    url: https://mistral.ai/news/agentic-search/
claims:
  - text: "Mistral, karmaşık belgeler ve veri kaynakları genelinde bilgiyi bulma, inceleme ve doğrulama için beş araç -- search, open, navigate, read ve grep -- sunan, Mistral Search Toolkit içine inşa edilmiş çok adımlı bir alma yeteneği olan Agentic Search'ü duyurdu"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Agentic Search, Mistral Medium 3.5 ve Z.ai'nin GLM-5.2 modelleriyle test edildi; Mistral Search Toolkit üzerinden, hem Studio hem de Vibe'daki \"Libraries\" özelliğine entegre biçimde ve GitHub'da bir Search Starter App ile şu anda kullanılabiliyor"
    type: announcement
    verdict: confirmed
    evidence: [1]
  - text: "Mistral'in FinanceBench değerlendirmesinde (368 SEC dosyası, 150 soru) Agentic Search doğruluğu %26,7'den %86'ya çıkardı"
    type: capability
    verdict: vendor-claim
    evidence: [1]
  - text: "Mistral'in GLM-5.2 ile test edilen OfficeQA Pro değerlendirmesinde (696 Hazine Bülteni, 133 soru) Agentic Search doğruluğu %6,3'ten %51,9'a -- 45,6 puanlık bir artış -- çıkardı; Mistral ayrıca p90 gecikmesinde %39,6'ya varan bir azalma ve yaklaşık üçte bir daha düşük token tüketimi bildiriyor"
    type: capability
    verdict: vendor-claim
    evidence: [1]
updated: []
---

## Ne oldu

Mistral AI, 20 Ağustos 2026'da Agentic Search'ü duyurdu: mevcut Mistral
Search Toolkit'in içine inşa edilmiş, yapay zekâ modellerine karmaşık
belgeler ve veri kaynakları genelinde bilgiyi bulma, inceleme ve doğrulama
için beş araç —search, open, navigate, read ve grep— sunan çok adımlı bir
alma yeteneği [1]. Özellik, tek bir alma geçişine güvenmek yerine bu
araçları kullanıyor ve şu anda Mistral Search Toolkit üzerinden, hem
Studio hem de Vibe ürünlerindeki "Libraries" özelliğine entegre biçimde
kullanılabiliyor; GitHub'da da bir Search Starter App yayımlandı [1].
Mistral, özelliği kendi Mistral Medium 3.5 modeliyle ve Z.ai'nin GLM-5.2
modeliyle test etti [1].

Mistral, kendi iç ölçütlerine göre Agentic Search'ün 368 SEC dosyasından
oluşturulan 150 soruluk bir değerlendirmede ("FinanceBench") doğruluğu
%26,7'den %86'ya, 696 Hazine Bülteni'nden oluşturulan 133 soruluk bir
değerlendirmede ("OfficeQA Pro," GLM-5.2 ile test edildi) ise %6,3'ten
%51,9'a —45,6 puanlık bir artış— çıkardığını bildiriyor. Şirket ayrıca
p90 gecikmesinde %39,6'ya varan bir azalma ve yaklaşık üçte bir daha
düşük token tüketimi bildiriyor [1]. Bu rakamlar Mistral'e ait olup henüz
bağımsız olarak doğrulanmadı.

## Neden önemli

Agentic Search, 28 Mayıs 2026'dan bu yana herkese açık önizlemede olan
Search Toolkit'i tek geçişli almadan çok adımlı bir döngüye taşıyor;
bu, standart parça tabanlı (chunk-based) almanın çapraz referansları
kaçırma eğiliminde olduğu dosyalar, bültenler ve sözleşmeler gibi uzun,
yapılandırılmış belgeler için tasarlandı. Kıyaslama kazanımları büyük
olsa da kendi bildirdiği rakamlar olup dış değerlendiricilere karşı test
edilmedi.
