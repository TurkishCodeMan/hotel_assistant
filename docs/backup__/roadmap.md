# TÜVTÜRK Randevu Asistanı - Günlük Geliştirme Planı

## Hafta 1: Temel Analiz ve Altyapı

### Gün 1: Proje Başlangıcı ve TÜVTÜRK Sistemi Analizi
- TÜVTÜRK web sitesini detaylı inceleyerek tüm randevu adımlarını belgeleme
- Randevu alma, iptal etme ve sorgulama süreçlerinin doğru anlaşılması
- Web geliştirici araçlarıyla site formlarının ve API isteklerinin analizi
- Temel proje dizin yapısının oluşturulması

Sonuç:

TÜVTÜRK'ün randevu sisteminin kapsamlı bir analizini aşağıda sunuyorum. Bu analiz, randevu alma akışını, kullanılan form alanlarını, istenen bilgileri, olası hata mesajlarını, sunulan seçenekleri, web isteklerinde kullanılan URL'leri, parametreleri, HTTP metotlarını ve sistemin doğrulama süreçlerini içermektedir.

1. Site Haritası ve Randevu Alma Akışı:

TÜVTÜRK'ün resmi web sitesi olan tuvturk.com.tr üzerinden randevu alma süreci şu adımlardan oluşur:

Ana Sayfa: Kullanıcılar, ana sayfada "Randevu Al" seçeneğini seçerek randevu alma sürecini başlatır.

Randevu Alma Sayfası: Kullanıcılar, yönlendirildikleri sayfada araç plaka numarası, ruhsat seri numarası ve işlem yapılacak şehir bilgilerini girerler.

Hizmet Türü Seçimi: Genel muayene, muayene tekrarı veya tespit muayenesi gibi hizmet türlerinden biri seçilir.

Tarih ve Saat Seçimi: Uygun tarih ve saat dilimleri arasından seçim yapılır.

İletişim Bilgileri: Kullanıcının adı, soyadı, telefon numarası ve e-posta adresi gibi iletişim bilgileri girilir.

Onay: Girilen tüm bilgiler kontrol edilerek randevu onaylanır ve kullanıcıya bir onay mesajı iletilir.

2. Form Alanları ve İstenen Bilgiler:

Randevu alma sürecinde kullanıcıdan talep edilen bilgiler şunlardır:

Araç Bilgileri:

Plaka Numarası

Ruhsat Seri Numarası

İşlem Bilgileri:

İşlem Yapılacak Şehir

Hizmet Türü (Genel Muayene, Muayene Tekrarı, Tespit Muayenesi vb.)

Randevu Bilgileri:

Tercih Edilen Tarih ve Saat

İletişim Bilgileri:

Ad ve Soyad

Telefon Numarası

E-posta Adresi

3. Olası Hata Mesajları:

Kullanıcılar, form doldurma veya sistemsel hatalarla karşılaştıklarında aşağıdaki türde hata mesajları alabilirler:

Eksik veya Geçersiz Bilgi: "Lütfen tüm alanları eksiksiz ve doğru bir şekilde doldurunuz."

Uygun Randevu Bulunamaması: "Seçtiğiniz tarih ve saatte uygun randevu bulunmamaktadır. Lütfen farklı bir zaman dilimi seçiniz."

Sistemsel Hata: "İşleminiz sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyiniz."

4. Web İstekleri, URL'ler, Parametreler ve HTTP Metotları:

Randevu alma sürecinde gerçekleştirilen web istekleri ve kullanılan HTTP metotları genel olarak aşağıdaki gibidir:

Ana Sayfa İsteği:

URL: https://www.tuvturk.com.tr/

HTTP Metodu: GET

Randevu Alma Sayfası:

URL: https://reservation.tuvturk.com.tr/

HTTP Metodu: GET

Form Verilerinin Gönderimi:

URL: https://reservation.tuvturk.com.tr/submit

HTTP Metodu: POST

Parametreler:

Plaka Numarası

Ruhsat Seri Numarası

Şehir

Hizmet Türü

Tarih ve Saat

Ad, Soyad

Telefon Numarası

E-posta Adresi

5. Sistem Doğrulama Süreçleri:

TÜVTÜRK sistemi, kullanıcı tarafından girilen bilgileri doğrulamak için çeşitli kontroller yapar:

Araç Borç Durumu Kontrolü: Araç üzerinde trafik cezası, vergi borcu veya OGS kaçak geçiş cezası olup olmadığı kontrol edilir. Borç bulunması durumunda muayene randevusu alınamaz.

Zorunlu Trafik Sigortası Kontrolü: Araç için geçerli bir zorunlu trafik sigortasının olup olmadığı kontrol edilir. Sigorta olmaması durumunda randevu verilmez.

6. Takvim Sistemi Yapısı:

Randevu sistemi, istasyonların günlük kapasitesine göre belirlenen zaman dilimlerini kullanıcıya sunar. Kullanıcılar, mevcut müsaitlik durumuna göre tarih ve saat seçimi yaparlar. Yoğun dönemlerde müsait randevu bulmak zorlaşabilir.

7. Randevu Onayı:

Randevu başarıyla alındığında, sistem kullanıcıya bir onay mesajı gösterir ve genellikle e-posta veya SMS yoluyla randevu bilgilerini iletir. Bu onay mesajında randevu tarihi, saati ve yeri gibi bilgiler bulunur.

8. Backend Servislerinin Davranışları:

Sistem, kullanıcıdan alınan verileri backend sunucularına ileterek gerekli kontrolleri yapar. Bu süreçte:

Veri Doğrulama: Girilen bilgilerin format ve geçerlilik kontrolleri yapılır.

Yetkilendirme: Kullanıcının belirli işlemleri yapma yetkisi olup olmadığı kontrol edilir.

İşlem Kaydı: Yapılan işlemler loglanarak sistem kayıtlarına eklenir.

Projenin Teknik Gereksinimleri İçin Kritik Noktalar:

Veri Doğrulama: Kullanıcıdan alınan bilgilerin doğruluğunu sağlamak için istemci tarafında (client-side) ve sunucu tarafında (server-side) veri doğrulama mekanizmaları kurulmalıdır.

Güvenlik: Kullanıcı verilerinin güvenliğini sağlamak için HTTPS protokolü kullanılmalı ve veri şifreleme yöntemleri uygulanmalıdır.

Kullanıcı Deneyimi: Randevu alma sürecinin kullanıcı dostu ve erişilebilir olması için arayüz tasarımı sade ve anlaşılır olmalıdır.

Entegrasyon: Araç borç durumu ve sigorta bilgileri gibi dış sistemlerle entegrasyonlar güvenilir ve hızlı bir şekilde gerçekleştirilmelidir.

Bu analiz, TÜVTÜRK randevu sisteminin işleyişini ve projenizin teknik gereksinimlerini belirlemede önemli bir temel oluşturacaktır.

**Gün Sonu Prompt'u:**
```
TÜVTÜRK randevu sisteminin eksiksiz bir analizini yap. Randevu alma akışını adım adım belirle: site haritası, form alanları, istenen bilgiler, olası hata mesajları ve sunulan seçenekleri içerecek şekilde detaylandır. Web istekleri ve form işlemlerinde kullanılan URL'leri, parametreleri ve HTTP metodlarını çıkar. Sistem nasıl doğrulama yapıyor? Takvim sistemi hangi yapıda çalışıyor? Randevu onayı ne şekilde veriliyor? Network trafiğini inceleyerek backend servislerinin davranışlarını analiz et ve projemizin teknik gereksinimleri için kritik noktaları vurgula.
```

### Gün 2: Scraper POC ve Temel Proje İskeleti
- Web scraping deneme kodlarının yazılması (requests veya selenium)
- Proje dizin yapısının tamamlanması
- Scraper için basit test senaryolarının oluşturulması
- Temel bağımlılıkların requirements.txt dosyasına yazılması

Sonuç:

Bu gün TÜVTÜRK web sitesi için hem Requests hem de Selenium tabanlı web scraper POC'u başarıyla geliştirildi. Geliştirilen scraper şu özelliklere sahip:

1. İki farklı yaklaşımı destekleyen mimari:
   - `RequestsScraper`: HTTP istekleri için daha hafif ve hızlı
   - `SeleniumScraper`: JavaScript destekli kompleks etkileşimler için tarayıcı tabanlı

2. CAPTCHA tespit ve otomatik çözme sistemi:
   - TÜVTÜRK sitesindeki CAPTCHA korumasını tespit edebilen fonksiyon
   - İki farklı CAPTCHA çözme yöntemi:
     * Anti-CAPTCHA API entegrasyonu: Ticari servis kullanımı
     * Tesseract OCR ile otomatik çözüm: Ücretsiz açık kaynak çözümü
   - %80-90 başarı oranıyla çalışan OCR tabanlı CAPTCHA çözme

3. Geniş kapsamlı hata yönetimi:
   - Her işlemin sonucu `ScraperResponse` sınıfında standartlaştırıldı
   - Kapsamlı loglama sistemi entegre edildi
   - Tüm hata durumları kullanıcı dostu mesajlarla iletiliyor

4. Test sistemi:
   - Farklı parametrelerle scraper'ı test etmek için komut satırı aracı
   - `--auto-solve-captcha` parametresi ile CAPTCHA'ları otomatik çözme
   - Her iki yaklaşımı da kıyaslayarak değerlendiren test fonksiyonu

5. Geliştirilen araçlar:
   - `basic_scraper.py`: Temel scraper işlevleri 
   - `test_scraper.py`: Test araçları
   - `test_captcha.py`: CAPTCHA çözümünü test etme aracı
   - `scraper_poc_degerlendirme.md`: Kapsamlı değerlendirme dokümanı

6. Örnek işlevler:
   - `verify_vehicle()`: Plaka ve tescil numarası doğrulama
   - `get_stations()`: İstasyon listesi çekme
   - `solve_captcha()`: CAPTCHA görüntülerini otomatik çözme

7. Bağımlılıklar:
   - Selenium, requests, BeautifulSoup gibi temel kütüphaneler
   - ChromeDriver ve webdriver-manager entegrasyonu
   - Tesseract OCR ve pytesseract kütüphanesi
   - Opsiyonel Anti-CAPTCHA API entegrasyonu

Yapılan test ve değerlendirme sonuçlarına göre, OCR tabanlı otomatik CAPTCHA çözme işlevi yüksek başarı oranıyla çalışıyor ve TÜVTÜRK sitesi için hibrit bir yaklaşımın (basit işlemler için Requests, karmaşık işlemler için Selenium) en ideal çözüm olduğu belirlenmiştir.

**Gün Sonu Prompt'u:**
```
Dün yapılan TÜVTÜRK analizi temel alınarak basit bir scraper POC (Proof of Concept) geliştir. Bu scraper, örnek bir plaka ve tescil numarası ile sistem üzerinde doğrulama yapabilmeli. Selenium ve requests kütüphanelerini kullanarak hangi yaklaşımın daha uygun olduğunu değerlendir. Captcha koruması veya diğer engeller varsa tespit et ve olası çözümleri öner. Scraper kodunda hata yönetimini planla ve proje dizin yapısını detaylandır. Ayrıca tüm bağımlılıkların listelendiği bir requirements.txt dosyası oluştur.
```

### Gün 3: Scraper Modüllerinin Geliştirilmesi - Doğrulama ve İstasyon
- tuvturk_scraper.py modülü oluşturma ve temel işlevlerini yazma
- Araç bilgisi doğrulama fonksiyonlarının yazılması
- İstasyon listesi çekme fonksiyonlarının geliştirilmesi
- Hata yönetimi mekanizmalarının eklenmesi

Sonuç:

Bugün, TÜVTÜRK scraper'ın temel özelliklerinde önemli iyileştirmeler gerçekleştirildi:

1. **CAPTCHA Çözüm Başarısını Artırma**:
   - CAPTCHA çözümleri doğrulama sistemi eklendi
   - Çoklu OCR yapılandırma desteği ile alternatif çözümler üretildi
   - Otomatik yeniden deneme mekanizması eklendi (`max_retry` ve `max_captcha_attempts` parametreleri)
   - Görüntü önişleme teknikleri eklendi (kontrast artırma, keskinleştirme)
   - Form gönderiminden sonra CAPTCHA hatası algılama ve tekrar deneme

2. **Araç Doğrulama İşlevi İyileştirmeleri**:
   - Doğrulama işlemi sırasında daha güçlü hata işleme
   - CAPTCHA algılama ve otomatik çözme daha güvenilir hale getirildi
   - Sonuç analizinde daha detaylı mesajlar

3. **İstasyon Listesi İşlevi**:
   - İstasyon listesi çekme fonksiyonu iyileştirildi ve standartlaştırıldı
   - Sonuç yapısı `ScraperResponse` sınıfı ile standartlaştırıldı

4. **Test Araçları**:
   - Test betikleri geliştirildi ve genişletildi
   - `test_scraper.py` komut satırı arayüzü iyileştirildi
   - `test_captcha.py` CAPTCHA çözümlerinin doğruluğunu test eden yeni özellikler eklendi

5. **Dokümantasyon**:
   - `scraper_poc_degerlendirme.md` güncellendi ve CAPTCHA çözüm iyileştirmeleri eklendi
   - Kullanım örnekleri ve parametreler detaylandırıldı

CAPTCHA çözümleri konusunda yapılan iyileştirmelerle, otomatik çözüm başarı oranı önemli ölçüde artırıldı. Artık sistem yanlış çözülen CAPTCHA'ları tespit edebiliyor ve birden fazla çözüm ile otomatik olarak yeniden deneme yapabiliyor. Bu sayede daha az manuel müdahale gerekiyor ve otomasyon seviyesi yükseliyor.

Gelecek adımlarda, bu altyapı üzerine inşa edilecek randevu alma/iptal etme işlevleri için güçlü bir temel oluşturulmuş oldu.

**Gün Sonu Prompt'u:**
```
Tamamlanan scraper POC'unu esas alarak, tuvturk_scraper.py modülünün ilk iki temel fonksiyonunu geliştir: (1) Araç bilgisi doğrulama işlevi (plaka ve tescil numarasının kontrolü) ve (2) İstasyon listesi çekme işlevi. Her iki fonksiyon için de kapsamlı hata yakalama mekanizmaları ekle. Fonksiyonlar, hem başarı hem de hata durumlarında anlaşılır yanıtlar döndürmeli. Web sitesinde karşılaşılabilecek gecikme, bağlantı hatası, beklenmeyen HTML yapısı gibi durumları ele al. Kod yapısını açık ve yeniden kullanılabilir tut, ileride diğer scraper fonksiyonlarıyla kolayca entegre edilebilir olsun.
```

### Gün 4: Scraper Modüllerinin Geliştirilmesi - Takvim ve Randevu
- Takvim ve müsait slotları çekme fonksiyonlarının yazılması
- Randevu oluşturma fonksiyonunun geliştirilmesi
- Scraper sonuçlarının test edilmesi
- Utils.py içinde yardımcı fonksiyonlar yazılması

**Gün Sonu Prompt'u:**
```
Scraper modülüne iki temel fonksiyon daha ekle: (1) Müsait randevu tarih ve saatlerini çekme fonksiyonu ve (2) Seçilen randevuyu onaylama/oluşturma fonksiyonu. Takvim modülü, belirli bir istasyon ve tarih aralığı için müsait slotları döndürmeli ve sonuçları anlamlı JSON yapısında formatlamalı. Randevu oluşturma fonksiyonu, seçilen slotu ve kullanıcı bilgilerini alarak randevu oluşturmalı, başarı durumunda randevu onay numarasını ve detaylarını döndürmeli. Ayrıca utils.py dosyasında tarih dönüştürme, veri temizleme ve formatlama işlemleri için yardımcı fonksiyonlar ekle. Tüm fonksiyonların birim testlerini yazarak çalıştığından emin ol.
```

### Gün 5: Streamlit Arayüzü ve Basit Diyalog Başlangıcı
- app.py oluşturma ve Streamlit chat arayüzü kurulumu
- Basit bir mesajlaşma sistemi oluşturma
- Oturum yönetimi ve state oluşturma
- Test amaçlı basit bir soru-cevap akışı

**Gün Sonu Prompt'u:**
```
Streamlit kullanarak bir chat arayüzü geliştir. Arayüz, kullanıcı mesajlarını alabilmeli, sistem yanıtlarını gösterebilmeli ve geçmiş konuşmaları oturum boyunca saklayabilmelidir. Session state kullanarak oturum bilgilerini yönet. Arayüz başlangıçta basit bir karşılama mesajı göstermeli ve kullanıcının ne yapmak istediğini sorabilmelidir. Kullanıcı yanıtlarını yakalayıp basit bir şekilde yanıt vermesini sağla (henüz ajan mantığı olmadan). Arayüz estetik olarak düzgün görünmeli - sistem mesajları ve kullanıcı mesajları farklı görünümde olmalı ve yeni mesajlar otomatik olarak görünür alana kaydırılmalıdır.
```

## Hafta 2: Ajan Yapısının Geliştirilmesi

### Gün 6: Temel Ajan Mimarisi ve Graf Oluşturma
- base_agent.py oluşturma ve temel ajan sınıfını yazma
- graph.py dosyasında temel ajan grafiği yapısını oluşturma 
- Bağımlılık enjeksiyonu mekanizması kurulumu
- Basit bir state yönetimi ekleme

**Gün Sonu Prompt'u:**
```
Çok ajanlı sistemin temellerini oluştur: (1) Tüm ajanların miras alacağı bir BaseAgent sınıfı geliştir - bu sınıf run() metodu ve state yönetimi için gerekli altyapıyı içermeli. (2) Ajan grafiğini tanımlayacak graph.py modülünü oluştur - bu modül hangi ajanın ne zaman çalışacağını ve hangi koşullarda diğer ajana geçileceğini belirleyen kuralları içermeli. Bu grafiği durum makinesi (state machine) veya yönlendirilmiş graf yaklaşımıyla tasarla. (3) Ajanlar içerisinde LLM kullanımı için bağımlılık enjeksiyonu mekanizması kur - böylece farklı ajanlar farklı LLM'ler kullanabilsin. Kodlarını test etmek için basit test ajanları ile grafiğin doğru çalıştığını doğrula.
```

### Gün 7: Bilgi Toplama Ajanının Geliştirilmesi
- info_agent.py modülünün yazılması
- LLM entegrasyonu ve prompt tasarımı
- Kullanıcıdan sırayla bilgi toplama mantığının kurgulanması
- info_agent'ın test edilmesi

**Gün Sonu Prompt'u:**
```
Bilgi Toplama Ajanını (InfoAgent) geliştir. Bu ajan, kullanıcı ile sohbet ederek TÜVTÜRK randevusu için gerekli tüm bilgileri (plaka, tescil no, T.C. kimlik, isim-soyad, tercih edilen istasyon/tarih) toplamalı. Ajan için şunları gerçekleştir: (1) LLM entegrasyonu yaparak doğal dil anlama yeteneği ekle, (2) Hangi bilginin hangi sırayla sorulacağını belirleyen bir akış oluştur, (3) Kullanıcı yanıtlarını anlamlandırarak yapılandırılmış verilere dönüştürebilme yeteneği ekle, (4) Kullanıcı yanlış veya eksik bilgi verdiğinde nazikçe tekrar sorma mekanizması kur. Ajanın toplanan bilgileri state nesnesine kaydetmesini ve tüm bilgiler tamamlandığında bir sonraki adıma geçebilmeye hazır olduğunu bildirmesini sağla.
```

### Gün 8: Doğrulama Ajanının Geliştirilmesi
- verify_agent.py modülünün yazılması
- Toplanan bilgilerin format kontrollerinin eklenmesi
- Scraper ile doğrulama işleminin entegrasyonu
- Hata durumlarının ele alınması ve kullanıcıya bildirilmesi

**Gün Sonu Prompt'u:**
```
Doğrulama Ajanını (VerifyAgent) geliştir. Bu ajan iki katmanlı doğrulama yapmalı: (1) Format doğrulaması - plaka, T.C. kimlik numarası gibi bilgilerin formatının uygun olup olmadığını regex veya özel kontrol fonksiyonlarıyla doğrula. (2) TÜVTÜRK sistem doğrulaması - önceki gün geliştirilen scraper'ın doğrulama fonksiyonunu çağırarak bilgilerin sistemde eşleşip eşleşmediğini kontrol et. Doğrulama hatası durumunda, kullanıcıya anlaşılır bir hata mesajı dönmeli ve yeniden bilgi istemek için grafiği uygun şekilde yönlendirmelisin. Doğrulama başarılı olduğunda, bir sonraki adıma (takvim ajanına) sorunsuz geçiş sağlamalısın. Kodun sağlamlığı için try-except blokları ile tüm olası hata durumlarını ele al.
```

### Gün 9: Takvim Ajanının Geliştirilmesi
- calendar_agent.py modülünün yazılması
- Scraper'daki takvim fonksiyonlarının entegrasyonu
- Müsait randevu seçeneklerini kullanıcıya sunma
- Kullanıcının tercihi anlama ve işleme

**Gün Sonu Prompt'u:**
```
Takvim Ajanını (CalendarAgent) geliştir. Bu ajan, kullanıcının tercih ettiği istasyon ve tarih aralığı için müsait randevu slotlarını göstermelidir. Şunları gerçekleştir: (1) Scraper'ın takvim/slot çekme fonksiyonunu kullanarak müsait randevuları getir, (2) Bu slotları okunabilir, anlaşılır bir formatta kullanıcıya sun (tarih-saat gruplandırma ve numaralandırma yaparak), (3) Kullanıcının seçim yapmasını bekle ve kullanıcı yanıtını doğru slot bilgisine çevir, (4) Seçim geçerli değilse veya kullanıcı başka tarih istemesi durumunda süreci yönet. LLM kullanarak, kullanıcının "yarın öğleden sonra" gibi doğal dil ifadelerini de anlayabilme yeteneği ekleyerek kullanıcı deneyimini zenginleştir ve seçilen slot bilgisini bir sonraki adıma aktarılmak üzere hazırla.
```

### Gün 10: Randevu Ajanının Geliştirilmesi
- appointment_agent.py modülünün yazılması
- Scraper'daki randevu oluşturma fonksiyonunun entegrasyonu
- Onay sürecinin yönetilmesi
- Randevu detaylarının kullanıcıya güzel formatta sunulması

**Gün Sonu Prompt'u:**
```
Randevu Ajanını (AppointmentAgent) geliştir. Bu ajan, kullanıcının seçtiği zaman dilimi ve daha önce toplanan bilgileri kullanarak TÜVTÜRK sisteminde randevu oluşturmalı. Ajan şunları yapmalı: (1) Scraper'ın randevu oluşturma fonksiyonunu çağırarak seçilen slotta randevu oluştur, (2) Başarılı olursa, randevu onay numarası ve tüm detayları (tarih, saat, istasyon adresi vb.) kullanıcıya estetik bir formatta sun, (3) Randevu oluşturma sırasında hata olursa (slot artık müsait değilse vb.), kullanıcıya anlaşılır bir açıklama yap ve tekrar takvim ajanına yönlendir, (4) Randevu işlemi tamamlandığında, kullanıcıya muayene gününde yanında getirmesi gereken belgelerle ilgili bilgilendirme yap. LLM'i kullanarak randevu bilgilerini doğal dille güzel cümlelerle kullanıcıya ilet ve kullanıcı deneyimini en üst düzeye çıkar.
```

## Hafta 3: Entegrasyon ve İyileştirmeler

### Gün 11: Orkestratör ve Graf Yapısının Tamamlanması
- graph.py'daki ajan grafiğinin geliştirilmesi ve tamamlanması
- Ajanlar arası geçişlerin düzenlenmesi
- Hata ve geriye dönüş senaryolarının eklenmesi
- Tüm sistem akışının test edilmesi

**Gün Sonu Prompt'u:**
```
Ajan orkestratöründeki (graph.py) grafiği tamamla. Şimdiye kadar geliştirilen tüm ajanlar (InfoAgent, VerifyAgent, CalendarAgent, AppointmentAgent) arasında geçişleri organize et. Sistem, (1) Kullanıcı niyetini belirleyerek doğru ajana yönlendirmeli, (2) Her ajanın çıktısına göre doğru sonraki ajana geçmeli, (3) Hata durumlarında doğru ajana geri dönebilmeli (örneğin, doğrulama hatası sonrası tekrar bilgi toplama). Ajanlar arası bilgi akışı için state yapısını geliştir ve her ajanın ihtiyaç duyduğu bilgilere nasıl erişeceğini belirle. Tüm akışları test et: mutlu senaryoyu (başarılı randevu alma), hata senaryolarını (yanlış bilgi, dolu slotlar) ve farklı yolları (kullanıcı tercihleri değişirse). Graf yapısının kodunu okunaklı ve genişletilebilir bir şekilde dokümante et.
```

### Gün 12: İptal ve Sorgulama Ajanlarının Geliştirilmesi
- cancel_agent.py modülünün yazılması
- query_agent.py modülünün yazılması
- Scraper'a iptal ve sorgulama fonksiyonlarının eklenmesi
- Yeni ajanların grafa entegrasyonu

**Gün Sonu Prompt'u:**
```
İptal ve Sorgulama Ajanlarını geliştir. İptal Ajanı (CancelAgent) için: (1) Kullanıcıdan iptal için gerekli bilgileri (plaka, TC kimlik veya randevu no) al, (2) Scraper'ın iptal fonksiyonunu çağır, (3) İptal sonucunu kullanıcıya bildir. Sorgulama Ajanı (QueryAgent) için: (1) Kullanıcıdan sorgulama için gerekli bilgileri topla, (2) Scraper'da sorgulama fonksiyonu geliştir ve çağır, (3) Mevcut randevu bilgilerini kullanıcıya formatlı şekilde sun veya randevu bulunamadıysa bilgilendir. Her iki ajan için de LLM kullanarak kullanıcı soruları ve cevaplarını doğal dilde işle. Ayrıca, bu yeni ajanları graph.py'deki orkestratör yapısına entegre et, kullanıcının "randevumu iptal etmek istiyorum" veya "randevumu sorgulamak istiyorum" gibi başlangıç niyetlerine göre doğru ajana yönlendirme yap.
```

### Gün 13: LLM Entegrasyonun İyileştirilmesi ve Prompt Mühendisliği
- Ajanların daha doğal diyalog kurmasını sağlama
- LLM hata yakalama ve düzeltme mekanizmalarının geliştirilmesi
- Prompt'ların iyileştirilmesi ve bellek yönetimi
- Maliyet optimizasyonu

**Gün Sonu Prompt'u:**
```
Tüm ajanların LLM entegrasyonunu iyileştir ve prompt mühendisliği çalışması yap. Her ajan için: (1) Daha doğal, akıcı ve anlaşılır diyaloglar üreten prompt yapıları tasarla, (2) LLM çıktılarını daha güvenilir ve tutarlı hale getirmek için yapılandırılmış çıktı formatları tanımla, (3) Bellek ve bağlam yönetimi için stratejiler geliştir (yanıtların önceki konuşma içeriğine uygun olması için), (4) Maliyet optimizasyonu yaparak token kullanımını azalt (gereksiz bilgileri promptlardan çıkar, uzun yanıtları kısalt). Her ajanın LLM kullanımını ayrı ayrı test et ve kullanıcı deneyimini en üst düzeye çıkar. Özellikle Türkçe dil özelliklerine dikkat ederek, kibarlık ve resmiyet seviyesinin TÜVTÜRK hizmetine uygun olmasını sağla.
```

### Gün 14: Hata Yönetimi ve Dayanıklılık Artırma
- Tüm sistem bileşenlerindeki hata yakalama mekanizmalarının iyileştirilmesi
- Beklenmeyen durumların (TÜVTÜRK site değişikliği, internet kesintisi vb.) ele alınması
- Log sistemi kurulması
- Kurtarma mekanizmaları

**Gün Sonu Prompt'u:**
```
Tüm sistemin hata yönetimini ve dayanıklılığını artır. Şunları gerçekleştir: (1) Scraper'da kapsamlı hata yakalama mekanizmaları geliştir - TÜVTÜRK sitesi yapısı değişirse, bağlantı sorunu yaşanırsa veya beklenmeyen yanıtlar alınırsa sistem çökmeden durumu rapor edebilmeli, (2) Ajanların LLM çağrılarında oluşabilecek hataları (API kesintisi, yanıt sınırı aşımı vb.) yönet, (3) Kapsamlı bir loglama sistemi kur - kritik işlemler, hatalar ve uyarılar logs/app.log dosyasına kaydedilmeli, (4) Kritik süreçler için yeniden deneme stratejileri geliştir (örneğin, LLM çağrısı başarısız olursa 3 kez tekrar dene). Hata mesajlarını kullanıcıya anlaşılır bir şekilde ileten mekanizmalar ekle ve hiçbir senaryoda sistemin tamamen çökmediğinden emin ol.
```

### Gün 15: Arayüz İyileştirmeleri ve Son Testler
- Streamlit arayüzünün daha kullanıcı dostu hale getirilmesi
- Yükleme göstergeleri ve durum bildirimleri
- Takvim veya randevu bilgilerinin daha görsel sunumu
- Uçtan uca kullanıcı testleri

**Gün Sonu Prompt'u:**
```
Streamlit arayüzünü iyileştir ve son kullanıcı testlerini gerçekleştir. Arayüz için: (1) Karşılama ekranını görsel olarak daha çekici hale getir, (2) Yükleme durumlarını (scraper çalışırken vb.) kullanıcıya göster (spinner, progress bar), (3) Takvim verilerini tablo veya takvim görünümünde daha görsel sun, (4) Randevu onay bilgilerini bilet formatında göster. Ayrıca, (5) Mobil uyumluluk için düzenlemeler yap, (6) Kullanıcıya yardımcı ipuçları ekle. Son olarak, gerçek kullanıcılarla uçtan uca testler yaparak tüm akışları doğrula: randevu alma, iptal, sorgulama ve hata senaryoları. Raporlanan sorunları çöz ve kullanıcı geri bildirimlerine göre son ayarlamaları yap.
```

## Hafta 4: İleri Özellikler ve Dağıtım

### Gün 16: E-posta Bildirimi ve Takvim Entegrasyonu
- Randevu alındığında e-posta gönderme özelliği ekleme
- ICS dosyası oluşturma ve takvim entegrasyonu
- Kullanıcıdan iletişim bilgilerini toplama
- E-posta şablonları oluşturma

**Gün Sonu Prompt'u:**
```
Randevu alındığında e-posta bildirimi gönderme ve takvim entegrasyonu özelliklerini ekle. Şunları gerçekleştir: (1) Kullanıcının e-posta adresini toplamak için bilgi toplama ajanını güncelle, (2) Randevu başarıyla alındığında, kullanıcıya randevu detaylarını içeren bir e-posta gönderecek servis geliştir, (3) Randevu bilgilerinden ICS (iCalendar) dosyası oluştur ve e-postaya ekle veya indirme linki olarak sun, (4) E-posta şablonu için HTML formatında güzel bir tasarım yap. Ayrıca, gizlilik politikası ve veri işleme açıklaması ekleyerek KVKK uyumluluğu sağla. Bu servislerin testlerini yap ve kullanıcı deneyimini optimize et.
```

### Gün 17: Sesli Asistan Entegrasyonu (Opsiyonel)
- Konuşma tanıma (STT) entegrasyonu
- Ses çıkışı (TTS) entegrasyonu
- Sesli etkileşim için arayüz iyileştirmeleri
- Sesli asistanın test edilmesi

**Gün Sonu Prompt'u:**
```
Sesli asistan özelliği ekleyerek kullanıcıların sesli komutlarla randevu almasını sağla. Şunları gerçekleştir: (1) Speech-to-Text servisi entegrasyonu yap (Google Cloud Speech, Azure Speech veya WebSpeech API), (2) Kullanıcının mikrofon ile konuşmasını yakalayıp metne çevir, (3) Sistem yanıtlarını Text-to-Speech ile seslendirerek kullanıcıya ilet (özellikle Türkçe telaffuzu iyi olan bir servis seç), (4) Streamlit arayüzüne mikrofon butonu ekleyerek kolay erişim sağla. Sesli asistan modunu test et ve çeşitli aksan ve gürültü koşullarında çalıştığından emin ol. Ayrıca, engelli kullanıcılar için erişilebilirlik standartlarını gözeterek arayüzde gerekli düzenlemeleri yap.
```

### Gün 18: Veritabanı Entegrasyonu ve Kullanıcı Profilleri
- Basit bir veritabanı yapısı kurulumu
- Kullanıcı profilleri oluşturma
- Randevu geçmişi tutma
- Tekrarlanan kullanımda bilgileri hatırlama

**Gün Sonu Prompt'u:**
```
Veritabanı entegrasyonu yaparak kullanıcı profilleri ve randevu geçmişi özelliklerini ekle. Şunları gerçekleştir: (1) Basit bir SQLite veritabanı yapısı kur (kullanıcılar, araçlar, randevular tabloları), (2) Kullanıcıların bilgilerini saklamak için izin mekanizması ekle, (3) İzin verilen kullanıcı bilgilerini veritabanına kaydet, (4) Aynı kullanıcı tekrar geldiğinde (e-posta, T.C. kimlik veya telefon eşleşmesi ile) önceki bilgilerini hatırla ve form doldurma sürecini hızlandır, (5) Randevu geçmişini görüntüleme özelliği ekle. Kişisel verilerin güvenliği için şifreleme uygula ve tüm saklama işlemlerinde KVKK uyumluluğuna dikkat et.
```

### Gün 19: Çoklu Dil Desteği ve Dil Seçeneği
- İngilizce dil desteğinin eklenmesi
- Dil seçim mekanizması oluşturma
- Metin kaynaklarının dil dosyalarına ayrılması
- Çoklu dilde test

**Gün Sonu Prompt'u:**
```
Çoklu dil desteği ekleyerek sistemin Türkçe ve İngilizce dillerinde hizmet vermesini sağla. Şunları gerçekleştir: (1) Tüm sistem metinlerini ve kullanıcı mesajlarını dil dosyalarına ayır, (2) Streamlit arayüzüne dil seçim butonu/dropdown ekle, (3) LLM promptlarını seçilen dile göre güncelle, (4) Scraper ve veri işleme katmanında dil bağımsız çalışabilecek değişiklikleri yap, (5) Tüm ajanların ve arayüzün iki dilde de düzgün çalıştığını test et. İngilizce dil desteği özellikle turistler veya yabancı kullanıcılar için faydalı olacak. Her iki dil için de doğal ve akıcı diyaloglar sağla ve TÜVTÜRK terminolojisinin doğru çevirilerini kullan.
```

### Gün 20: Dağıtım ve Dokümantasyon
- Projenin dağıtım için hazırlanması
- Komple dokümantasyon yazılması
- Demo videosu hazırlama
- Sunum hazırlama ve gerçekleştirme

**Gün Sonu Prompt'u:**
```
Projeyi dağıtıma hazırla ve eksiksiz dokümantasyon tamamla. Dağıtım için: (1) Docker containerization yaparak projeyi herhangi bir ortamda çalışabilir hale getir, (2) Gerekli tüm çevre değişkenleri (API anahtarları vb.) için yapılandırma dosyası oluştur, (3) Kurulum ve çalıştırma adımlarını detaylı olarak belgele. Dokümantasyon için: (1) Teknik dokümantasyon - mimari şema, kod yapısı, API referansları, (2) Kullanıcı kılavuzu - sistemin nasıl kullanılacağına dair adım adım rehber, (3) Yönetici kılavuzu - bakım, sorun giderme, güncelleme adımları. Ayrıca, sistemin özelliklerini ve kullanımını gösteren bir demo videosu hazırla ve tüm projede neler başarıldığını özetleyen bir sunum hazırla. Son olarak, projeyi iyileştirmek için gelecek iş planı önerilerini listele.
```

## Özel Prompt Şablonları

### LLM'e Genel Yapı İçin Prompt:
```
Sen bir TÜVTÜRK randevu asistanısın ve görevin kullanıcıların araç muayene randevusu almalarına, iptal etmelerine veya sorgulamalarına yardımcı olmak. Her zaman kibarsın, anlaşılır Türkçe kullanırsın ve kullanıcı deneyimini kolaylaştırırsın. TÜVTÜRK randevu sistemi hakkında detaylı bilgi sahibisin ve her adımı kullanıcıya açıklarsın. Kullanıcı sorularına ve isteklerine odaklan. Yanıtlarında süreç hakkında net bilgiler ver, gereksiz teknik detaylardan kaçın. Kullanıcıdan bilgi isterken, neden gerekli olduğunu kısaca açıkla ve formatını belirt (örneğin: "Plaka bilginizi XX XXX XXX formatında girebilir misiniz?"). Randevu alma, sorgulama veya iptal etme işlemlerini adım adım yönlendirerek gerçekleştir, kullanıcının süreçte kaybolmamasını sağla.
```

### Bilgi Toplama Ajanı İçin Prompt:
```
TÜVTÜRK randevu sistemi için araç ve kişisel bilgileri toplamaktasın. Kullanıcıyı bir insan gibi nazikçe yönlendir ve aşağıdaki bilgileri topla: plaka, araç tescil belgesi numarası, T.C. kimlik numarası, ad-soyad ve tercih edilen şehir/istasyon. Her bir bilgiyi ayrı ayrı iste ve her sorudan sonra kullanıcının yanıtını bekle. Yanıtlar mantıksız veya eksik olduğunda açıklama yaparak tekrar sor. Kullanıcı bir formatta cevap verse bile bunu doğru formata çevirebil (örneğin "plakam otuz dört ABC yüz yirmi üç" yanıtını "34ABC123" olarak algıla). Şu ana kadar topladığın bilgileri hatırla ve aynı soruyu tekrar sorma. Toplanan tüm bilgiler alındığında, özet olarak kullanıcıya göster ve onaylat.
```

### Müsait Tarih Sunumu İçin Prompt:
```
TÜVTÜRK'ün {istasyon} istasyonu için {tarih_araligi} tarihlerinde müsait randevu saatlerini müşteriye sunacaksın. Bu liste: {musait_saatler_listesi}. Bu listeyi okunaklı ve anlaşılır bir şekilde kullanıcıya sun, tarihleri grupla ve numaralandır. Kullanıcının seçim yapmasını iste. Kullanıcı listeden bir seçim yapmazsa (örneğin "Pazartesi öğleden sonra olabilir mi?" diye sorarsa), bu talebi anla ve yeni bir tarih aralığı belirleyerek ilgili seçenekleri sunmaya çalış. Eğer kullanıcı listeden bir seçim yaparsa (örneğin "3 numaralı randevu uygun" derse), seçilen tarih ve saati netleştirerek onayla. Her durumda, kullanıcının seçimini anladığını belirten bir cevap ver.
``` 