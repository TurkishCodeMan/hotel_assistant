# TÜVTÜRK Scraper POC Değerlendirmesi

Bu belge, TÜVTÜRK randevu sistemi için geliştirilmiş olan web scraper Proof of Concept (POC) uygulamasının değerlendirmesini içerir.

## 1. Genel Mimari

Scraper iki farklı yaklaşım üzerine kurulmuştur:

1. **Requests tabanlı yaklaşım** (RequestsScraper sınıfı)
2. **Selenium tabanlı yaklaşım** (SeleniumScraper sınıfı)

Her iki yaklaşım da aynı arayüzü uygular ve aynı operasyonları farklı tekniklerle gerçekleştirir:
- `verify_vehicle()`: Plaka ve tescil numarası ile araç doğrulama
- `get_stations()`: Belirli bir şehirdeki istasyonları listeleme

## 2. Yaklaşımların Karşılaştırılması

| Kriter | Requests | Selenium | Değerlendirme |
|--------|----------|----------|---------------|
| Hız | ⭐⭐⭐⭐⭐ | ⭐⭐ | Requests yaklaşımı çok daha hızlı |
| Kaynak Kullanımı | ⭐⭐⭐⭐⭐ | ⭐⭐ | Requests daha az bellek ve CPU kullanıyor |
| JavaScript Desteği | ❌ | ✅ | Selenium JS ile oluşturulan içeriği görebiliyor |
| CAPTCHA Aşma | ❌ | ⭐⭐⭐⭐ | Selenium otomatik CAPTCHA çözme desteği eklenmiştir |
| Karmaşık Etkileşimler | ❌ | ✅ | Selenium takvim, dropdown vb. widgetlarla etkileşime girebiliyor |
| Bakım Kolaylığı | ⭐⭐⭐⭐ | ⭐⭐ | Requests kodu daha basit ve bakımı daha kolay |
| İstikrar | ⭐⭐⭐ | ⭐⭐ | Selenium tarayıcı sürümü, driver vb. dış etkenlere daha bağımlı |

## 3. CAPTCHA Tespiti ve Çözümü

Geliştirilen `check_captcha_detection()` fonksiyonu sayesinde site üzerindeki CAPTCHA koruması tespit edilebilmektedir. TÜVTÜRK sitesinde tespit edilen CAPTCHA türü için şu çözümler önerilir:

1. **Anti-CAPTCHA API entegrasyonu**: Ticari bir CAPTCHA çözme servisi entegre edilebilir.
2. **OCR tabanlı otomatik çözüm**: Tesseract OCR kullanılarak CAPTCHA'lar otomatik çözülebilir.
3. **Hybrid Yaklaşım**: Otomatik çözüm başarısız olduğunda manuel çözüm için kullanıcıya bildirim gönderilebilir.
4. **Cloud Scraper Entegrasyonu**: Cloudflare ve benzeri korumalardan kaçınmak için cloudscraper kütüphanesi entegre edilebilir.

### 3.1 Otomatik CAPTCHA Çözme Özelliği

Scraper, CAPTCHA'ları otomatik olarak çözebilecek iki farklı strateji ile geliştirilmiştir:

1. **Anti-CAPTCHA API ile çözüm**: 
   - API anahtarı sağlandığında Anti-CAPTCHA servisi kullanılarak CAPTCHA'lar çözülebilir
   - Ticari bir çözüm olduğundan yüksek başarı oranı sağlar

2. **Tesseract OCR ile çözüm**:
   - Açık kaynaklı bir çözüm olarak Tesseract OCR kullanılarak CAPTCHA'lar çözülebilir
   - Basit CAPTCHA'lar için %70-90 doğruluk oranı sağlar
   - Bedava bir çözüm olduğundan tercih edilebilir

### 3.1.1 CAPTCHA Çözüm Doğruluğu İyileştirmeleri

CAPTCHA çözümlerinin her zaman doğru olmaması sorununa karşı şu iyileştirmeler yapılmıştır:

1. **Çoklu OCR Yapılandırması**:
   - Farklı Tesseract OCR modları kullanılarak (PSM 7, PSM 8, PSM 13) alternatif çözümler üretilir
   - Her mod, CAPTCHA karakterlerini farklı şekillerde algılayabilir, böylece doğru çözüm bulma olasılığı artar

2. **Görüntü Ön İşleme**:
   - Kontrast artırma ve keskinleştirme ile CAPTCHA görsellerinin kalitesi yükseltilir
   - İyileştirilmiş görseller OCR için daha iyi sonuçlar verir

3. **Otomatik Yeniden Deneme Mekanizması**:
   - `max_retry` ve `max_captcha_attempts` parametreleriyle sistem otomatik olarak birden fazla deneme yapar
   - Her başarısız denemeden sonra yeni bir CAPTCHA görüntüsü alınır
   - CAPTCHA refresh butonları otomatik tespit edilip kullanılır

4. **Yanıt Doğrulama Kontrolü**: 
   - Form gönderildikten sonra sayfa içeriği analiz edilerek CAPTCHA hataları tespit edilir
   - "Yanlış CAPTCHA" veya "CAPTCHA hatalı" gibi mesajlar algılanırsa otomatik olarak yeni deneme başlatılır
   - Birden fazla çözüm varsa, sırayla tüm çözümler denenir

5. **Başarı Oranı İyileştirme**:
   - Başarısız olan çözümler loglara kaydedilir, böylece sistem zamanla iyileştirilebilir
   - Çözülen CAPTCHA'ların istatistikleri toplanarak hangi modun daha başarılı olduğu tespit edilir

CAPTCHA çözümü için eklenen bu yeniden deneme ve doğrulama mekanizmaları sayesinde, ilk seferde doğru çözülemeyen CAPTCHA'lar için otomatik olarak yeni denemeler yapılır ve tüm olası çözümler denenir. Bu şekilde toplam başarı oranı önemli ölçüde artırılmıştır.

Gerçekleştirilen testlerde, Tesseract OCR ile TÜVTÜRK sitesindeki CAPTCHA'ların başarıyla çözülebildiği gözlemlenmiştir. OCR çözümünün kalitesini artırmak için şu adımlar uygulanmıştır:

- CAPTCHA görüntüsünün doğrudan ekran görüntüsü alınarak OCR için hazırlanması
- OCR yapılandırmasında alfanumerik karakterlerin tanınmasına öncelik verilmesi
- Base64 kodlu görüntüler ve URL tabanlı görüntüler için dinamik işleme stratejileri

Otomatik CAPTCHA çözme, `--auto-solve-captcha` parametresi ile etkinleştirilebilir ve başarısız olursa manuel çözüme geçiş yapabilir.

## 4. Hata Yönetimi

Scraper'da kapsamlı hata yönetimi uygulanmıştır:

- Tüm metodlar `ScraperResponse` tipinde standart bir yanıt döndürür
- Her operasyon try-except blokları ile sarılarak beklenmeyen hatalar yakalanır
- Hata durumları loga kaydedilir
- İstemci tarafında da kolay bir şekilde hata kontrolü yapılabilir

## 5. Önerilen Yaklaşım

TÜVTÜRK sitesi için en ideal yaklaşım **hibrit bir mimari** olacaktır:

1. **Basit operasyonlar için Requests**: Hızlı veri çekimi için Requests tabanlı yaklaşım
2. **Karmaşık etkileşimler için Selenium**: Takvim seçimi, form doldurma gibi etkileşimler için Selenium
3. **CAPTCHA yönetimi**: Otomatik OCR çözümü ile CAPTCHA'ların çözülmesi, başarısız olduğunda manuel çözüme geçilmesi

## 6. Bilinen Sınırlamalar

- TÜVTÜRK sitesinde arka arkaya yapılan istekler IP kısıtlamasına yol açabilir
- Selenium WebDriver için uygun bir ChromeDriver sürümü bulunmalıdır
- Site yapısındaki değişiklikler scraper'ı bozabilir, bu nedenle düzenli bakım gerekir
- Gerçek kişi verileri kullanılırken KVKK uyumluluğu gözetilmelidir
- OCR çözümü, karmaşık CAPTCHA'larda veya görüntü kalitesi düşük olduğunda başarısız olabilir

## 7. İleriki Geliştirmeler

- Selenium WebDriver yönetimi için `webdriver-manager` entegrasyonu (Tamamlandı)
- CAPTCHA çözümü için daha gelişmiş algoritmalar ve eğitilmiş modeller
- IP rotasyonu için Proxy desteği
- Daha fazla operasyon eklenmesi (randevu alma, randevu iptal etme vb.)
- Otomatik test senaryoları ve CI/CD entegrasyonu
- Monitoring ve otomatik hata bildirim mekanizması

## 8. Sonuç

Geliştirilen POC, TÜVTÜRK web sitesi ile etkileşime geçebilen ve otomatik CAPTCHA çözme yeteneklerine sahip bir scraper altyapısının uygulanabilir olduğunu göstermiştir. Site yapısı ve koruma mekanizmaları analiz edilmiş, farklı yaklaşımlar test edilmiş ve birlikte çalışabilecek bir çözüm sunulmuştur. İleriki aşamalarda bu temel altyapı üzerine randevu alma, iptal etme ve sorgulama gibi daha karmaşık işlevler eklenebilir. 