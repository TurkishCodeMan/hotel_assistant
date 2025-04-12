TÜVTÜRK Randevu Alma İçin Çok Ajanlı Sistem: Proje Planı ve Dokümantasyon
### Proje Tanımı ve Amaç
TÜVTÜRK araç muayene randevularını internet sitesi üzerinden almak, kullanıcılar için karmaşık ve zaman alıcı olabilmektedir. Bu proje, kullanıcıların doğal dil ile etkileşime geçebileceği bir chatbot aracılığıyla TÜVTÜRK sitesinden adım adım randevu almayı kolaylaştırmayı hedefler. Chatbot, kullanıcıdan araç ve kimlik bilgilerini toplayarak (plaka, araç tescil no, T.C. kimlik no, ad-soyad, son muayene geçerlilik tarihi vb.) otomatik olarak TÜVTÜRK randevu sistemine girer ve uygun bir tarihe randevuyu oluşturur. Sistem, birden fazla yapay zeka ajanının iş birliği içinde çalıştığı bir mimariye sahip olacak ve her ajan belirli bir görevi üstlenecektir. Bu yaklaşım, karmaşık bir işlemi daha küçük adımlara bölerek her adımda uzmanlaşmış ajanlar sayesinde daha verimli ve hatasız bir çözüm sunmayı amaçlar​
SUPERANNOTATE.COM
​
SUPERANNOTATE.COM
. Sonuç olarak kullanıcı, sadece sohbet ederek randevusunu alabilecek; ayrıca randevu iptali ve sorgulama gibi ek işlemler de aynı sistem üzerinden gerçekleştirilebilecektir.
### Genel Mimarinin Planı
Bu proje, çok ajanlı bir yapay zeka sistemi olarak tasarlanacaktır. Çok ajanlı LLM (Large Language Model) sistemlerinde birden fazla ajan, bir “takım” halinde ortak hedef için çalışır. Her bir ajan, belli bir konuda uzmanlığa sahip olup görevin bir bölümünü üstlenir ve diğer ajanlarla koordineli şekilde etkileşime girer​
K2VİEW.COM
. Bu sayede kompleks görevler, tek bir büyük modelin tek seferde yapabileceğinden daha başarılı ve tutarlı bir şekilde tamamlanabilir​
SUPERANNOTATE.COM
. Genel bileşenler ve mimari:
Kullanıcı Arayüzü (Streamlit Web Uygulaması): Kullanıcı ile doğal dilde etkileşim burada gerçekleşir. Kullanıcı soruları ve yanıtları bu arayüz üzerinden sisteme iletilir. Arayüz, yönlendirmeli bir sohbet deneyimi sunacak (örneğin, kullanıcıya seçenekler sunmak veya gerekli bilgileri adım adım istemek).
Ajan Grafiği ve Yönlendirme (graph.py): Ajanların nasıl sıralanacağı ve birlikte çalışacağını tanımlayan yapıdır. Ajanlar bir graf üzerindeki düğümler gibi ele alınır ve bu graf üzerindeki kenarlar bilgi akışını, yani hangi ajanın hangisinden sonra devreye gireceğini belirler​
LANGCHAİN-Aİ.GİTHUB.İO
. Gerekli durumlarda bir orkestratör/süpervizör ajan, süreci denetleyip bir sonraki adımı belirleyebilir​
LANGCHAİN-Aİ.GİTHUB.İO
. graph.py dosyası, bu akışı kodlayarak hangi durumda hangi ajanın çalışacağını ve ajanlar arası veri paylaşımını tanımlayacaktır.
LLM Tabanlı Ajanlar: Her biri farklı bir göreve odaklanan ve gerektiğinde farklı bir LLM modeli veya yöntemi kullanan alt ajanlar. (Örneğin, biri bilgi toplama, biri doğrulama, diğeri randevu oluşturma görevinde uzmanlaşır.) Ajanlar, LLM’lerin doğal dil işleme yeteneklerini kullanarak kullanıcıdan bilgi alma, soruları anlama veya cevap üretme işlerini yaparlar. Bu ajanların her birine, bağımlılık enjeksiyonu (dependency injection) yöntemiyle farklı LLM’ler veya araçlar bağlanabilecektir – böylece her ajanın arkasında en uygun modelin kullanılabilmesi sağlanır​
MEDİUM.COM
.
Orta Katman Servisleri (Scraper ve Veri İşleme): Ajanların ihtiyaç duyduğu dış veriyi almak veya harici işlemleri yapmak için kullanılan yardımcı servisler. TÜVTÜRK’ün web sitesinde randevu alma işlemi bir API sunmadığından, web sayfalarını scraping tekniğiyle otomatik gezip form doldurma ve veri çekme işlemleri gerçekleştirilecektir. Bu katman, istenen randevu tarihlerini takvimden çekmek, kullanıcının girdiği bilgileri TÜVTÜRK sisteminde doğrulamak ve randevuyu onaylamak gibi işleri üstlenir. Elde edilen ham veriler (HTML içerikleri gibi) parse edilerek yapılandırılmış hale getirilir ve karar vermesi veya kullanıcıya sunması için ilgili ajana aktarılır.
Veri Depolama (Opsiyonel): İlk aşamada tüm işlem gerçek zamanlı yürütülecek olsa da, uzun vadede randevu kayıtlarını veya kullanıcı bilgilerini (izin dahilinde) saklamak için bir veritabanı düşünülebilir. Böylece kullanıcı aynı plakayla geldiğinde bilgileri hatırlama veya alınan randevuları kaydetme gibi imkanlar doğacaktır.
Genel mimariyi bir bütün olarak özetlemek gerekirse, kullanıcıdan gelen doğal dil taleplerini alan bir çok ajanlı yapay zeka ekibi vardır. Bu ekip, kendi içinde iletişim kurarak ve görevleri paylaşarak, TÜVTÜRK’ün sitesine arka planda erişip gerekli adımları tamamlar. Her ajan uzmanı olduğu işi yapar ve sonuçlar bir sonraki adıma aktarılır; en sonunda da kullanıcıya anlaşılır bir yanıt/dönüt verilir. Bu yapı, bir zincirleme düşünme (chain-of-thought) süreci gibi ele alınabilir; farklı bilgi ve beceri gerektiren adımlar ardışık olarak işlenir​
K2VİEW.COM
.
### Ajanlar ve Görev Dağılımları
Her bir ajan, sistemin belirli bir fonksiyonunu yerine getirmekten sorumludur. Bu bölümde, önerilen ajanların rollerini ve sorumluluklarını ele alıyoruz:
1. Bilgi Toplama Ajanı
Görevi: Kullanıcıyla ilk etkileşimi yönetmek ve randevu alabilmek için gerekli tüm bilgileri kullanıcıdan doğal bir diyalogla toplamaktır. Bu ajan, bir nevi form doldurma sürecini sohbet ortamına taşır. Kullanıcıya sırasıyla şu soruları sorar ve yanıtları alır:
Araç plakası
Araç tescil numarası (ruhsatta bulunan belge numarası)
T.C. kimlik numarası (veya vergi no, şirket aracı ise)
Araç sahibinin adı ve soyadı
Son muayene geçerlilik tarihi (varsa, araç halihazırda muayeneliyse)
Tercih edilen muayene istasyonu veya şehir (kullanıcıya yakın istasyonun belirlenmesi için)
Tercih edilen tarih/saat aralığı (örneğin, sabah saatleri, belirli bir gün vb. isteği olabilir)
Çalışma Şekli: Ajan, eksik olan her bilgi için kullanıcıya nazik ve anlaşılır bir soru yöneltir. Kullanıcının verdiği cevabı doğrular veya gereken formata sokar (örneğin plaka formatını kontrol etmek, T.C. no 11 hane mi diye bakmak gibi). Gerekirse, yanlış veya eksik bilgi verildiğinde tekrar sorar veya düzeltme ister. Bu ajan, arka planda güçlü bir dil modeli kullanarak kullanıcının farklı ifade biçimlerini anlayabilir; örneğin kullanıcı plakasını söylerken harfleri tek tek okuyabilir veya ad-soyadı ters sırada verebilir – bunları yorumlayıp standart forma dönüştürme görevi bilgi toplama ajanındadır. Sonuç/Çıktı: Bu ajanın topladığı bilgiler, sistem içinde ortak bir durum (state) nesnesine kaydedilir. Tüm gerekli alanlar doldurulduğunda, bu bilgileri doğrulama veya doğrudan randevu oluşturma aşamasına aktarır. Bilgi toplama tamamlandıktan sonra kontrol, Doğrulama Ajanı veya ilgili sonraki adıma geçer.
2. Doğrulama Ajanı
Görevi: Kullanıcıdan alınan bilgilerin doğruluğunu ve tutarlılığını kontrol etmek. İki seviyede doğrulama söz konusu olabilir:
Yerel Doğrulama: Girilen verilerin biçimsel olarak doğru olup olmadığını denetlemek (örneğin plaka yapısı uygun mu, T.C. kimlik numarası doğru hane sayısında mı, son muayene tarihi bir tarih formatında mı gibi).
Harici Doğrulama: Bilgileri TÜVTÜRK sistemine göndererek eşleştirme yapmak. TÜVTÜRK randevu sisteminde randevu alabilmek için genelde plaka ve tescil no birlikte girildiğinde araç doğrulanır. Bu ajan, arka plandaki scraper servislerini kullanarak TÜVTÜRK’ün ilgili sayfasına bu bilgileri gönderir ve sistemin “araç bulundu” onayı verip vermediğine bakar. Eğer TÜVTÜRK sistemi bu bilgileri onaylamazsa (örneğin yanlış tescil no girildiyse), doğrulama ajanı kullanıcıya hatalı bilgiyi belirtip Bilgi Toplama Ajanı aracılığıyla tekrar giriş yaptırabilir.
Çalışma Şekli: İlk aşamada programatik kontroller yapar (hatalı format veya mantık hatası var mı diye). Sonrasında scraper katmanını çağırarak TÜVTÜRK’ün online randevu formuna plaka/tescil bilgilerini gönderir. Bu işlem sonucunda:
Eğer bilgiler doğru ve sistem kabul ettiyse, randevu işlemine devam edilebilir.
Eğer bilgiler eşleşmez veya sistem bir hata döndürürse, doğrulama ajanı bu hatayı yakalar. Örneğin “Girdiğiniz plaka/tescil no bulunamadı” gibi bir mesaj geldiyse, bunu kullanıcıya anlaşılır biçimde iletir ve gerekirse ilgili bilgiyi tekrar sorması için Bilgi Toplama Ajanına talepte bulunur (ajan grafiğinde geriye döner).
Sonuç/Çıktı: Bilgiler başarılı şekilde doğrulanırsa, ajan grafiğinde bir sonraki adıma (Randevu Ajanı’na) geçilir. Aksi halde hata mesajı verilip kullanıcıdan düzeltme istenir. Bu sayede, randevu işleminin ileriki adımlarına yanlış bilgiyle devam edilmesinin önüne geçilir.
3. Takvim Ajanı (Randevu Seçenekleri Ajanı)
Görevi: Mevcut randevu müsaitliklerini ve seçeneklerini kullanıcıya sunmak. Araç ve kullanıcı bilgileri doğrulandıktan sonra, sıradaki adım uygun bir tarih, saat ve istasyon seçmektir. Takvim Ajanı, TÜVTÜRK sistemindeki müsait takvim verilerini çeker ve bunları anlamlı şekilde işler. Çalışma Şekli: Bu ajan, scraper aracılığıyla TÜVTÜRK’ün randevu takvimi sayfasına istek yapar. Genellikle süreç şöyle işler:
Öncelikle kullanıcıdan bir istasyon veya şehir tercihi alınır (eğer sistem bunu plaka veya önceki bilgilere göre otomatik belirlemiyorsa). Bilgi Toplama Ajanı bu tercihi sormuş veya bir varsayılan değer almış olabilir. Takvim Ajanı, bu istasyon bilgisini kullanarak ilgili istasyonun takvimine erişir.
Seçilen istasyon ve varsa tercih edilen tarih bilgisine göre, müsait olan gün ve saatleri listeler. Örneğin TÜVTÜRK’ün takvim arayüzünde kullanıcının seçebileceği tarihler öbek öbek sunulur (takvim görseli üzerinde). Scraper servis, HTML içindeki takvim tablolarını parse ederek uygun günleri ve saat dilimlerini çıkartır.
Bu ajan daha sonra, bulunan müsait zaman dilimlerini kullanıcıya anlaşılır bir listede sunar. Örneğin: “En yakın müsait randevu tarihleri: 12 Nisan 9:30, 12 Nisan 10:15, 13 Nisan 14:00 ...” gibi. Eğer kullanıcı belirli bir tercih belirtmişse (örn. sadece öğleden sonra uygun, veya belirli bir tarih aralığı), ajan bu tercihe uygun filtreleme yaparak sonuçları öyle iletir.
Sonuç/Çıktı: Kullanıcıya uygun randevu seçenekleri listelenmiş olur. Bu liste, doğal dil açıklamasıyla veya numaralandırılmış bir menü şeklinde sunulabilir. Kullanıcı bu noktada listeden bir seçim yapabilir veya farklı bir kriter belirtmek isterse (örn. “daha ileri bir tarih isterim” demesi durumunda), Takvim Ajanı buna göre takvim bilgisini günceller. Seçim yapıldıktan sonra, seçilen zaman dilimi Randevu Ajanına iletilir.
4. Randevu Ajanı
Görevi: Asıl randevu alma işlemini gerçekleştirmek ve süreci tamamlamak. Bu ajan, önceki adımlarda toplanan tüm bilgiler doğrultusunda TÜVTÜRK sistemine randevu girişini yapar ve onay alır. Çalışma Şekli: Randevu Ajanı, kullanıcının seçtiği tarih-saat ve istasyon bilgisini ile birlikte daha önce alınmış kimlik ve araç bilgilerini kullanarak, scraper aracılığıyla TÜVTÜRK’ün randevu onay sayfasına istek yapar. Bu aşamada muhtemel adımlar:
Seçilen randevu slotunun hala müsait olduğunun doğrulanması (bu arada başka biri almış olabilir; sistem genelde seçimi kilitler ama yine de kontrol etmek faydalı).
Randevuyu onaylamak için gerekli son adımların atılması: Örneğin, TÜVTÜRK sistemi genelde bir özet sayfası gösterip “Onayla” butonu sunar. Scraper bu butona tıklayacak isteği de göndererek randevuyu kesinleştirir.
Randevu alındıktan sonra sistem bir onay kodu veya referans numarası üretebilir. Bu önemli bilgiyi yakalayıp almak gerekir. Ayrıca randevu detayları (tarih, saat, istasyon adresi) de çekilir.
Ajan, bu işlemler sırasında LLM’den de faydalanarak, olası sistem mesajlarını yorumlayabilir ve kullanıcıya anlaşılır çıktı hazırlayabilir. Örneğin, TÜVTÜRK başarıyla randevu oluşturduğunda Türkçe bir onay mesajı döndürür; ajan bu mesajı alıp kullanıcının sohbetine uygun bir dile çevirerek sunar: “Randevunuz başarıyla alındı. 12 Nisan 2025 saat 09:30’da Malatya İstasyonu’nda muayene randevunuz bulunmaktadır. Onay kodu: ABC1234.” Sonuç/Çıktı: Bu ajan, sürecin son çıktısını üretir: randevu onay bilgisi. Kullanıcıya tüm gerekli detaylar verilir. Eğer randevu alma aşamasında bir sorun çıkarsa (örneğin seçilen slot dolmuşsa), ajan durumu kullanıcıya bildirir ve gerekirse yeniden takvimden seçim yapması için Takvim Ajanına geri döner. Başarılı durumunda sohbeti nazikçe sonlandırır ve başka bir isteği olup olmadığını sorabilir.
5. İptal Ajanı (Ek Özellik)
Görevi: Kullanıcının mevcut bir TÜVTÜRK randevusunu iptal etmek istediğinde devreye girer. Bu ajan, yine kullanıcıdan gerekli tanımlayıcı bilgileri alarak (plaka, T.C. kimlik veya randevu referans numarası gibi) TÜVTÜRK sistemindeki randevu iptal işlemini gerçekleştirir. Çalışma Şekli: Süreç olarak, sistem ilk önce kullanıcının gerçekten bir randevusu olup olmadığını doğrulayabilir. Eğer Randevu Sorgulama Ajanı gibi bir ajanımız varsa onunla entegre çalışarak, verilen bilgilere göre aktif randevu detaylarını getirir. Sonrasında kullanıcıdan onay alarak iptal işlemini gerçekleştirir:
TÜVTÜRK web sitesinde randevu iptali genelde randevu referansı veya kimlik bilgileriyle yapılır. Scraper, ilgili iptal formunu doldurup gönderir.
İptal onayı alındığında, sistem bir başarı mesajı verir (örn: “Randevunuz iptal edilmiştir.”). Ajan bu mesajı yakalar ve kullanıcıya iletir.
Ajan, kullanıcıya iptal işleminin başarılı olduğunu, isterse yeni bir randevu alabileceğini belirten bir cevapla sohbeti sonuçlandırır.
Sonuç/Çıktı: Randevu iptal edildiğine dair kullanıcıya bir onay bilgisi sunulur. Bu ajan, diğer ajanlardan biraz farklı olarak başlangıçta kullanıcı isteğiyle (niyetiyle) devreye girer. Kullanıcı “randevumu iptal etmek istiyorum” dediğinde, orkestra bu ajana yönlenir ve gerekli işlemleri yapar.
6. Randevu Sorgulama Ajanı (Ek Özellik)
Görevi: Kullanıcının daha önceden almış olduğu bir randevunun detaylarını öğrenmek istemesi durumunda çalışır. Örneğin kullanıcı “Daha önce ne zaman randevu almıştım?” veya “Randevu bilgilerimi öğrenebilir miyim?” dediğinde, sistem bu ajana geçerek gerekli bilgileri toparlar. Çalışma Şekli: Yine kimlik ve araç bilgileri alındıktan sonra (zaten oturum devam ediyorsa sistemde mevcut olabilir), TÜVTÜRK’ün randevu sorgulama sayfasına istek atılır. Eğer halihazırda kayıtlı bir randevu varsa, tarih-saat ve yer bilgileri parse edilerek kullanıcıya iletilir. Eğer yoksa, kullanıcıya aktif bir randevusu olmadığı bilgisi verilir ve yeni randevu almak isteyip istemediği sorulabilir. Sonuç/Çıktı: Kullanıcıya mevcut randevusu varsa detaylar sunulur, yoksa olmadığını belirten bir mesaj gösterilir. Bu ajan, iptal ajanıyla birlikte de çalışabilir (örneğin önce sorgulayıp ardından iptale yönlendirme gibi).
7. Diyalog Yöneticisi / Orkestra Ajanı (Arka Plan Yönlendirme)
Görevi: Yukarıdaki ajanların ne zaman ve hangi sırayla devreye gireceğini belirleyen mekanizmadır. Aslında bu, tek başına bir ajan olmayıp ajan grafiği içinde tanımlanmış bir kontrol akışıdır. Kullanıcı mesajlarına ve sistemin o anki durumuna göre, doğru ajanın çağrılmasını sağlar. Örneğin:
Kullanıcı sohbetin başında niyetini belirtmediyse, ilk mesajında “Merhaba” gibi genel bir ifade varsa, diyalog yöneticisi kullanıcıdan hangi işlemi yapmak istediğini öğrenmek üzere bir yönlendirme yapar (randevu almak, iptal etmek, sorgulamak gibi seçenekler sunar).
Kullanıcının niyeti anlaşıldıktan sonra (niyet analizi veya kullanıcı seçimi ile), ilgili akışın başlangıç ajanını aktif hale getirir. Randevu alma akışı için Bilgi Toplama Ajanı, iptal için İptal Ajanı, sorgulama için Sorgulama Ajanı gibi.
Diyalog sırasında her ajanın işi bitince, sıradaki ajanın devreye girmesini sağlar. Ajanlar arası geçiş kuralları graph.py içinde tanımlıdır; diyalog yöneticisi bu kurallara uyarak akışı yönetir. Örneğin Bilgi Toplama -> Doğrulama -> Takvim -> Randevu şeklinde bir zincir izlenir. Eğer herhangi bir adımda sorun yaşanırsa (örneğin doğrulama hatası), graf üzerinde tanımlı geri dönüş yolunu takip ederek önceki ajana dönülür veya hata durumunu yönetecek bir alt akışa girilir.
Son olarak, işlem tamamlandığında, diyalog yöneticisi görüşmeyi sonlandırabilir veya kullanıcıya başka yardımcı olabileceği bir şey olup olmadığını sorarak gerekirse akışı yeniden başlatabilir.
Bu diyalog yönetimi, pratikte çoğunlukla graph.py içinde kurgulanmış bir durum makinesi (state machine) veya kural tabanlı yönlendirme olarak kodlanacaktır. Gelişmiş bir senaryoda, bu görev için ayrı bir LLM de kullanılabilir; örneğin bir süpervizör LLM ajanı tüm konuşmayı okuyup hangi ajana geçileceğine karar verebilir​
LANGCHAİN-Aİ.GİTHUB.İO
. Ancak mevcut proje kapsamımızda, akış büyük ölçüde önceden belirlenmiş olduğu için kural tabanlı ve deterministik bir graf yeterli olacaktır.
### Ajan Grafiği ve Bilgi Akışı
Ajanlar arasındaki etkileşim, tanımlı bir graf yapısı üzerinden gerçekleşir. Bu graf, her bir adımda hangi ajanın çağrılacağını ve olası geçişleri tanımlar. Bilgi akışı, ortak bir durum yapısı (memory/state) üzerinden sağlanır; böylece bir ajanın ürettiği çıktı veya aldığı bilgi, sonraki ajana girdi olarak aktarılabilir. Aşağıda randevu alma süreci için planlanan akış adımları listelenmiştir:
Başlangıç (Kullanıcı İsteği): Kullanıcı arayüzüne gelip bir mesaj gönderir. Örneğin “Aracım için muayene randevusu almak istiyorum” veya sadece “Merhaba” diyebilir.
Diyalog yöneticisi, kullanıcının niyetini anlamaya çalışır. Açıkça “randevu almak istiyorum” gibi bir ifade varsa doğrudan ilgili akışa yönlendirir, değilse kullanıcıya nasıl yardımcı olabileceğini sorup seçenekler sunar (randevu alma, iptal, sorgulama).
Kullanıcı randevu almayı seçtiğinde, graf üzerinde Bilgi Toplama Ajanı başlangıç düğümü olarak çağrılır.
Bilgi Toplama Ajanı > Doğrulama Ajanı: Bilgi Toplama Ajanı sırayla tüm gerekli bilgileri alır. Tüm bilgiler hazır olduğunda graf, Doğrulama Ajanına geçiş yapar.
Doğrulama Ajanı, aldığı bilgileri kontrol eder. Eğer bir tutarsızlık veya hata yoksa başarı durumunda graf üzerinde sonraki adıma yönlenir.
Hata Durumu: Doğrulamada bir hata çıkarsa (örn. plaka-tescil uyuşmadı), graf bu noktada geri dönüş kenarını takip ederek yeniden Bilgi Toplama Ajanı’na döner veya spesifik olarak hatalı bilgiyi tekrar sordurur. Kullanıcıdan düzeltme alındıktan sonra tekrar Doğrulama’ya geçilir. (Bu döngü, bilgiler doğru olana dek sürebilir.)
Doğrulama Ajanı > Takvim Ajanı: Bilgiler onaylandığında sistem, randevu takvimi adımına ilerler. Takvim Ajanı devreye girerek ilgili istasyon ve tarih aralığında müsait zamanları listeler.
Ajan grafiğinde bu geçiş, “doğrulama başarılı” durumuna bağlanmıştır. Takvim Ajanı, çalışması için gerekli parametreleri (istasyon, tarih tercihleri vs.) durum bilgisinden veya kullanıcıdan alır.
Takvim Ajanı > Kullanıcı Seçimi: Takvim Ajanı’nın sunduğu opsiyonlar kullanıcıya iletilir ve bu noktada sistem, bir süre kullanıcı cevabı bekler. Bu bir bekleme durumu gibi düşünülebilir. Kullanıcı, listelenen seçeneklerden birini seçtiğinde (örn. “12 Nisan 09:30’u istiyorum” diyerek veya listeden numarayla seçerek), bu yanıt yakalanır.
Eğer kullanıcı listedeki seçeneklerden memnun değilse, farklı istek belirtebilir (“daha geç bir tarih var mı?” gibi). Bu durumda graf, yine Takvim Ajanı’na dönebilir veya Takvim Ajanı içinde farklı bir alt akış tetiklenir (örneğin istenen tarih aralığı parametresi güncellenip yeniden listeleme yapılır).
Takvim Ajanı > Randevu Ajanı: Kullanıcı geçerli bir seçim yaptığında, graf Randevu Ajanına geçer ve seçilen randevu slotu ile birlikte gerekli tüm bilgiler ona iletilir.
Randevu Ajanı > Sonlandırma: Randevu Ajanı, arka planda randevuyu yaratmaya çalışır.
Başarılı olursa: Randevu detaylarını alır ve kullanıcıya iletir. Bu noktada işlem tamamlanmıştır. Graf, sürecin sonuna ulaşır (END durumuna). Kullanıcıya yardıma hazır olduğunu belirterek sohbeti sonlandırır veya yeni bir işlemi olup olmadığını sorar (isterse tekrar başlangıca dönülebilir).
Başarısız olursa: (Örneğin o slot seçilememişse) Ajan, başarısızlık durumunu kullanıcıya bildirir. Graf, uygun bir önceki adıma dönüş yapabilir. Büyük ihtimalle yine Takvim aşamasına dönüp güncel müsaitlikleri yeniden sorar ya da kullanıcıdan farklı bir seçim yapmasını ister. Ardından tekrar Randevu Ajanı denenir.
İptal ve Sorgulama Akışları: Kullanıcı başlangıçta randevu iptal veya mevcut randevuyu öğrenme talebiyle gelirse, graf farklı bir yol izler.
İptal için: Başlangıçtan sonra niyet belirlenince doğrudan İptal Ajanı çalışır. İptal için yine kimlik/araç bilgileri gerekebileceğinden, Bilgi Toplama Ajanı ile işbirliği yapabilir veya iptal ajanı kendi içinde bunları sorar. Ardından scraper ile iptal yapılır ve sonuç kullanıcıya iletilip sonlandırılır. İptal sonrasında kullanıcıya yeni bir randevu almak isteyip istemediği de sorulabilir (bir nevi tekrar başlangıca dönen bir kenar).
Sorgulama için: Benzer şekilde Randevu Sorgulama Ajanı çalışır; gerekirse bilgi alır, sorgular, sonucu verir. Bu ajan genellikle işlem sonunda ya biter ya da ardından iptal ya da yeni randevu işlemi önerisiyle başka akışlara dallanabilir.
Bu ajan grafini uygularken, kod seviyesinde graph.py içerisinde bir yönlendirme tablosu ya da durum makinesi kurgulanacaktır. Örneğin pseudo-kod olarak şöyle bir yapı olabilir:
python
Kopyala
Düzenle
# graph.py içinden basit bir akış tanımı örneği
graph = {
  "start": IntentAgent,            # ilk mesajı niyet analizine yönlendir
  ("IntentAgent", "randevu"): InfoAgent,    # niyet randevu ise Bilgi Toplama'ya git
  ("IntentAgent", "iptal"): CancelAgent,    # niyet iptal ise İptal Ajanı'na git
  ("IntentAgent", "sorgula"): QueryAgent,   # niyet sorgulama ise Sorgulama Ajanı'na git

  ("InfoAgent", "ready"): VerifyAgent,      # gerekli bilgiler tamam ise Doğrulama'ya git
  ("VerifyAgent", "success"): CalendarAgent,
  ("VerifyAgent", "fail"): InfoAgent,       # doğrulama hatası olursa tekrar bilgi al
  ("CalendarAgent", "date_selected"): AppointmentAgent,
  ("AppointmentAgent", "success"): END,     # randevu alındı, sona er
  ("AppointmentAgent", "fail"): CalendarAgent  # randevu alınamadıysa takvime geri dön
}
Yukarıdaki akışta "IntentAgent" bir diyalog başlatıcısı/niyet belirleyici olarak davranıyor. ("InfoAgent", "ready") ise Bilgi Toplama ajanı işini bitirince (ready) Doğrulama'ya geçileceğini belirtiyor. Bu yapı sayesinde, her ajanın olası çıktı durumlarına göre (success, fail, ready, date_selected gibi) bir sonraki adım tanımlanmış oluyor. Dependency injection yöntemi ile de, bu grafiğe her bir ajan için kullanılacak LLM veya araç nesneleri enjekte ediliyor; böylece ajanlar arası geçişler sabit kalsa da arkadaki model ve fonksiyonellik esnek kalıyor. Bilgi akışı boyunca, kullanıcı tarafından verilen bilgiler ve sistemin geçici verileri, ortak bir durum (state) objesinde tutulur ve gerektiğinde ajanlara aktarılır. Örneğin, Bilgi Toplama Ajanı plaka bilgisini aldıktan sonra bu state içine state["plaka"] = "34ABC12" olarak ekler; sonraki ajanlar bu state üzerinden plaka bilgisine erişebilir. Bu yaklaşım, her ajanın sadece kendi işine odaklanmasını, ancak gerektiğinde önceki adımlardan gelen verilere de ulaşabilmesini sağlar.
### LLM Entegrasyonu ve Esnek Tasarım
Projenin önemli bir tasarım hedefi, farklı görevler için farklı dil modellerini kullanabilme esnekliğidir. Her ajanın ihtiyacı olan dil işleme kapasitesi ve yeteneği farklı olabilir. Örneğin:
Bilgi Toplama Ajanı: Kullanıcıdan net bilgiler almak ve gerektiğinde hataları düzeltmek için güçlü bir doğal dil anlayışı gerektirir. Bu ajan için GPT-4 veya benzeri gelişmiş bir model kullanılabilir ki kullanıcı ifadelerini doğru anlasın ve yönlendirmeleri başarılı olsun.
Doğrulama Ajanı: Bu ajan daha çok kural ve format kontrolü yapar; belki dil modeline bile gerek kalmadan programatik kontrollerle işini halledebilir. Ancak, kullanıcıya hata mesajlarını nazikçe iletmek veya TÜVTÜRK’ten gelen hata yanıtlarını açıklamak için basit bir dil modeli (veya şablon cümleler) kullanılabilir.
Takvim ve Randevu Ajanları: Bu ajanlar, bir yandan kullanıcıya seçenekleri anlaşılır biçimde sunmak, diğer yandan onay almak gibi diyalog adımlarını yönetir. Takvim Ajanı belki liste formatında yanıt oluştururken Randevu Ajanı daha açıklayıcı cümlelerle onay verir. Bu rollere uygun ayrı model instance’ları veya ayrı prompt kalıpları tanımlanabilir.
Her bir ajanın arkasına farklı bir LLM bağlamak, model-agnostik bir mimari ile mümkün kılınacaktır. Yani, ajanlar arayüzlerini (girdi/çıktı formatlarını) standart tutarken, onlara hangi modelin güç verdiği kolayca değiştirilebilir olmalıdır. Projede bağımlılık enjeksiyonu (dependency injection) bu noktada devreye girer: Örneğin her ajan sınıfı, bir language_model parametresi alacak şekilde tasarlanır. graph.py içerisinde ajanlar oluşturulurken ilgili modele bağlanır:
python
Kopyala
Düzenle
# Ajanların yaratılması ve LLM enjeksiyonu
info_agent = InfoAgent(llm=OpenAI(model="gpt-4"))           # bilgi toplama için güçlü bir model
verify_agent = VerifyAgent(llm=None)                       # doğrulama için LLM gerekmeyebilir
calendar_agent = CalendarAgent(llm=OpenAI(model="gpt-3.5")) # takvim sunumu için orta seviye model
appointment_agent = AppointmentAgent(llm=OpenAI(model="gpt-4"))  # sonuç iletimi için iyi bir model
Bu şekilde, her bir ajanın hangi modelle çalışacağı merkezi olarak kontrol edilebilir. İleride bir modeli değiştirmek istersek (örneğin maliyet nedeniyle GPT-4 yerine açık kaynak bir modele geçmek gibi), sadece bu konfigürasyon değiştirilerek ajanın davranışı korunup model değiştirilmiş olur. PydanticAI gibi çerçeveler de tam bu esneklik için geliştirilmiştir; farklı LLM’lerle çalışabilen ve tip güvenli bir yapı sunarak model değişimlerinde minimum kod değişikliği gerektiren bir mimari önerir​
MEDİUM.COM
. Bu projenin yapısı da benzer şekilde model bağımlılıklarından ayrışık, gerektiğinde bir “ajan havuzu” içindeki herhangi bir aracı (LLM, API, kütüphane) kullanabilecek şekilde kurgulanacaktır. Esnek tasarımın bir diğer boyutu da, her ajanın birer araç (tool) gibi ele alınabilmesidir. Örneğin, orkestra eden bir üst model olsaydı, bu modelleri araç olarak çağırabilirdi​
MEDİUM.COM
. Bizim senaryomuzda bu çok gerekli değil, ancak tasarımımız yine de ajanların bağımsız test edilebilir ve birbirinden ayrık olmasına özen gösterecek. Her bir ajan, ilgili görevini tanımlayan arayüz metodlarına sahip olacak (örneğin InfoAgent.run(state) gibi bir metot, veya LangChain kullanılsa bir Tool arayüzü implemente edilebilir). Bu sayede, bir ajanın iç implementasyonunu (hangi LLM’i kullandığı, nasıl karar verdiği) diğer parçalara dokunmadan geliştirebilir veya değiştirebiliriz. Ayrıca, bir kısım ajanlarda LLM yerine klasik algoritmalar kullanmak da mümkündür. Örneğin doğrulama ajanı veya istasyon listesi çıkarma gibi işlemler kural tabanlı yapılabilir. Mimarimiz buna da olanak tanıyor, zira ajanlar sadece bir görev birimi olarak düşünülüyor, nasıl yaptıkları onların iç meselesi. Bir ajan ister LLM ile doğal dil anlasın, ister sabit kodlanmış kurallarla çalışsın, dışarıya karşı verdiği hizmet belli bir sözleşmeyle sabit olacak. Özetle, LLM entegrasyonu katmanında benimsediğimiz prensipler:
Gerekli yerde gerekli model: Her iş için en uygun kapasitede modeli kullan, tek bir modelle her şeyi yapmaya çalışma (hem kalite hem maliyet açısından). Bu, çok-ajanlı tasarımın getirdiği bir avantajdır​
K2VİEW.COM
.
Model bağımsız arayüz: Ajanların kodu, spesifik bir LLM’e bağlı olmayacak şekilde yaz (OpenAI API, HuggingFace Pipeline, vs. kolayca entegre edilebilir olsun).
Kolay değiştirme/deneme: Yeni bir model veya yöntem denemek istediğimizde ilgili ajana enjekte ederek hızlıca test edebiliriz. Örneğin ileride takvim bilgisini özetlemek için GPT-3.5 yerine daha özelleşmiş bir Türkçe model kullanmak istersek, CalendarAgent’e onu bağlayarak deneyebiliriz.
Hata toleransı: LLM’ler zaman zaman tutarsız çıktılar verebilir. Her ajanın çıktısı, mümkünse başka bir ajan veya kod bloğu tarafından doğrulanmalı. Örneğin InfoAgent, kullanıcının girdiği plaka bilgisini anlamakta zorlanırsa belki bir regex kontrolüyle yardıma ihtiyaç duyabilir; bu durumda model çıktısını post-processing ile sağlamlaştırmak gerekebilir. Bu da entegrasyonun bir parçasıdır.
### Scraper ve Veri İşleme Katmanı
TÜVTÜRK üzerinden randevu almak için sistemimizin, arka planda web sayfalarını otomatik olarak dolaşması ve formları doldurması gerekecek. Bu amaçla bir scraper ve ona bağlı veri işleme adımları tasarlanmıştır. Bu katman, aslında ajanların bir uzantısı gibi düşünülebilir; ajanlar karar verir veya kullanıcıdan veri alır, scraper ise gerçek işlemi yapar ve sonucu geri döndürür. Bu ayrım, özellikle web işlemlerinin başarısız olma ihtimaline karşı, ajanların sadece iş mantığına odaklanmasını ve web’den veri çekme detaylarının ayrı yönetilmesini sağlar. Scraper katmanında öngörülen bileşenler/servisler:
TÜVTÜRK Randevu Sorgu Servisi: Bu servis, plaka ve tescil no (ve gerekiyorsa T.C. kimlik) bilgisini TÜVTÜRK’ün randevu sorgulama giriş sayfasına gönderir. Amaç, bu bilgilerin geçerli olup olmadığını anlamaktır. Normalde TÜVTÜRK’ün web sitesinde kullanıcı bu bilgileri girip “Devam” der ve sistem arka planda bunları kontrol ederek randevu sayfasına geçirir. Scraper, aynı HTTP isteğini yaparak veya gerekiyorsa bir tarayıcı otomasyonu (Selenium gibi) ile bu adımı simüle eder. Gelen cevap başarılı ise, bir sonraki sayfanın HTML’i (istasyon ve takvim seçimi sayfası) alınır; eğer başarısızsa sunulan hata mesajı yakalanır. Bu sonuçlar doğrulama ajanına iletilecektir.
İstasyon Listesi / Seçimi Servisi: Eğer TÜVTÜRK sisteminde kullanıcının bir istasyon seçmesi gerekiyorsa (genelde plaka bazında değil, kullanıcıya tüm istasyonlar listelenir), scraper bu listeyi de çekebilir. Örneğin şehir seçilince ilçe/istasyon listesi gelir. Bu servis, gerekli durumlarda ilgili HTML dropdown listesinden istasyonları parse edip bir Python listesine dökebilir. Bilgi Toplama Ajanı bu listeyi kullanıcıya sunup seçim yaptırabilir. (Basitlik adına, başlangıçta kullanıcıdan metin olarak istasyon bilgisini alabiliriz ama ideal olan liste sunmaktır.)
Takvim (Müsait Randevu) Servisi: Belirli bir istasyon ve tarih için müsait randevuları çeken servistir. TÜVTÜRK’ün takvim sayfasında genelde takvim görünümü ve saat slotları olur. Scraper, bu sayfanın HTML’ini indirip içinde regex veya HTML parse (BeautifulSoup) ile müsait günleri ve saatleri ayrıştıracaktır. Bu veriyi yapılandırılmış bir formata (örneğin Python dict listesi: { "date": "2025-04-12", "times": ["09:30", "10:15", ...] }) dönüştürüp Takvim Ajanı’na verir. Ajan bu yapıyı alıp kullanıcıya uygun şekilde dilsel olarak sunar.
Randevu Onaylama Servisi: Kullanıcı bir randevu seçtikten sonra, o seçime ait formun gönderilmesi gerekir. Bu servis, arka planda ilgili form parametrelerini (genelde istasyon kodu, tarih ve saat, kullanıcı bilgileri vs.) TÜVTÜRK onay endpoint’ine yollar. Başarı durumunda dönen onay sayfasını yakalar. Bu sayfadan randevu detaylarını ve referans numarasını çeker. Örneğin RayHaber’de belirtildiği gibi TÜVTÜRK resmi sitesinde takvimden tarih seçilip onaylanarak işlem tamamlanır​
RAİLLYNEWS.COM
. Biz de bunu otomatikleştirip cevabı alacağız.
Randevu İptal Servisi: Ek özelliklerden iptal için, TÜVTÜRK’ün iptal sayfasına plaka ve referans numarası göndererek iptal işlemini yapan bir fonksiyon olacaktır. Onay mesajını yakalayıp döndürür.
Randevu Sorgulama Servisi: Plaka ve T.C. kimlik ile sisteme sorgu atıp mevcut aktif randevu var mı öğrenen bir fonksiyon. Eğer varsa, randevu tarih-saatini döndürür.
Teknoloji ve Araçlar: Bu scraping işlemleri için Python’un requests kütüphanesi basit durumlarda yeterli olabilir. Ancak, TÜVTÜRK’ün sitesi muhtemelen güvenlik için CAPTCHA veya diğer önlemlere sahip olabilir. İlk etapta, otomatize edilebilirlik test edilecek: eğer basitçe istek atılamıyorsa, bir headless browser (Selenium + Chrome Driver veya Playwright) kullanılabilir. Bu tabii ki biraz ağır ama gerekirse uygulanır. Proje başlangıcında, küçük bir scraper POC (proof of concept) yapılarak, gerekli HTTP isteklerinin ve parametrelerin ne olduğu belirlenecek. (Örneğin form alanı isimleri, cookie yönetimi, vs.) Scraper’dan gelen veriler genellikle HTML veya ham metin olacağından, bunların işlenip anlam çıkarılması gerekiyor. Bu işleme adımları:
HTML parse için BeautifulSoup veya XPath kullanılabilir.
Çekilen veriler Python veri yapılarına aktarılır (dict, list vs.), bu yapı ajanlara verilir.
Ajanlar bu ham veriyi ya direk kullanır ya da daha da özetleyip kullanıcıya gösterir. Örneğin Takvim Ajanı, available_slots listesi alır ve bunu cümle haline getirir.
Hata Yönetimi: Scraper katmanı, dış sistemle etkileşim kurduğu için hata ve istisnalara açık bir katmandır. Örneğin internet bağlantısı kopabilir, TÜVTÜRK sitesi bakımda olabilir, beklenmeyen bir HTML yapısı gelebilir vs. Bu durumlar için:
Her kritik fonksiyon try-except bloklarıyla donatılacak, hata durumunda anlaşılır mesajlar üretilecek.
Ajanlar, scraper’dan gelen hataya göre kullanıcıya durumu iletecek ve gerektiğinde yeniden denemek isteyip istemediğini soracak. (Örneğin “Şu an sistem cevap vermiyor, tekrar denememi ister misiniz?” gibi.)
Uzun vadede, scraper’ı sağlamlaştırmak için testler yazılacak ve site değişimlerinde güncelleme yapmak kolay olsun diye kod yapısı temiz tutulacak.
Özetle, scraper ve veri işleme katmanı, çok ajanlı sistemimizin TÜVTÜRK ile arasındaki köprüdür. Bu sayede kullanıcı sohbet ederken arka planda gerçek işlemler yapılabilecek. İlk versiyonda scraping kullanılacak olsa da, eğer TÜVTÜRK ileride bir API sunarsa veya farklı entegrasyon imkanı çıkarsa, mimarimiz bu katmanı değiştirip ajanları etkilemeden yeni sisteme geçiş yapabilecek esneklikte olacaktır.
### Kullanıcıyla Doğal Diyalog Planı
Sistemin başarısı, kullanıcıyla kurulan diyalogun kalitesine bağlı olacaktır. Amaç, resmi bir form doldurma deneyimini sohbet havasına sokarak kullanıcıyı yönlendirmek ve gerekli bilgileri toplamaktır. Bu bölümde, örnek bir diyalog akışı ve tasarlanacak diyalog yönetimi stratejisi anlatılmaktadır. Diyalog Akışı Örneği (Randevu Alma Senaryosu):
Karşılama ve Niyet Belirleme:
Bot: “Merhaba, TÜVTÜRK randevu asistanına hoş geldiniz. Size nasıl yardımcı olabilirim?”
(Bot, kullanıcının ne yapmak istediğini sorar. Kullanıcı doğrudan belirtmezse seçenek sunabilir.)
Kullanıcı: “Aracım için muayene randevusu almak istiyorum.”
(Bot, niyetin randevu almak olduğunu anlar.)
Bilgi Toplama Başlangıcı:
Bot: “Elbette, randevu alabilmem için bazı bilgilere ihtiyacım var. Öncelikle, araç plakanızı öğrenebilir miyim?”
Kullanıcı: “34 ABC 123”
Bot: “Teşekkürler. Araç tescil belgesi numaranızı da alabilir miyim? (Ruhsat üzerinde yazan belge no)”
Kullanıcı: “U123456”
Bot: “Harika, T.C. kimlik numaranızı da öğrenebilir miyim?”
Kullanıcı: “12345678901”
Bot: “İsminizi ve soyadınızı da yazabilir misiniz?”
Kullanıcı: “Ahmet Yılmaz”
Bot: “Son olarak, aracınızın muayenesi en son ne zamana kadar geçerli? (Tarihi gün/ay/yıl olarak yazabilirsiniz veya bilmiyorsanız 'bilmiyorum' diyebilirsiniz.)”
Kullanıcı: “30/06/2023”
(Bot burada temel bilgileri aldı. Son muayene geçerlilik tarihi geçmiş olabilir, bunu not eder ama esasen randevu almayı engellemez; sadece bilgilendirme için istenmiş olabilir.)
Bot: “Teşekkür ederim, tüm bilgileri aldım. Lütfen bir saniye, bilgilerinizi kontrol ediyorum...”
Bilgi Doğrulama ve İstasyon Seçimi:
(Bot arka planda doğrulama yapar, her şey uyumlu diyelim.)
Bot: “Bilgileriniz doğrulandı. Randevunuzu hangi TÜVTÜRK istasyonunda almak istersiniz? Örneğin Malatya Merkez istasyonu uygun mudur?”
Kullanıcı: “Evet, Malatya Merkez olsun.”
(Alternatif olarak bot, il-ilçe listesi sunabilir. Ancak basitlik için kullanıcı kendisi söyledi.)
Bot: “Malatya Merkez istasyonunu seçtiniz. Peki, sizin için uygun bir tarih aralığı var mı? Yoksa ilk müsait günü mü alayım?”
Kullanıcı: “Haftaya salı veya çarşamba uygun olabilir.”
Bot: “Anladım, 11 veya 12 Nisan tarihlerine bakalım...”
Müsait Tarih/Saat Sunumu:
(Bot, Takvim Ajanı ile 11-12 Nisan Malatya Merkez için müsaitlikleri çeker ve listelemeye hazırlanır.)
Bot: “Malatya Merkez istasyonu için müsait randevu saatleri şunlar:
11 Nisan 2025: 09:00, 09:45, 10:30, 14:00
12 Nisan 2025: 09:30, 10:15, 11:00, 15:15
Bu seçeneklerden birini tercih edebilirsiniz. Örneğin ‘11 Nisan 09:45’ diyebilirsiniz.”
Kullanıcı: “12 Nisan saat 09:30 uygun.”
Bot: “12 Nisan 2025 saat 09:30 seçildi. Sizin için bu randevuyu ayırtıyorum... Lütfen bekleyin.”
Randevu Onayı:
(Bot arka planda randevu oluşturur, onay döner.)
Bot: “Tebrikler! Randevunuz başarıyla alındı. İşte detaylar:
Tarih/Saat: 12/04/2025 - 09:30
İstasyon: Malatya Merkez TÜVTÜRK İstasyonu
Randevu No: ABC123456 (Bu numarayı not edebilirsiniz)
Muayene günü, lütfen araç ruhsatınızı ve gerekli belgeleri yanınızda bulundurunuz. Başka bir konuda yardımcı olmamı ister misiniz?”
Kullanıcı: “Teşekkürler, çok sağol.”
Bot: “Rica ederim. İyi günler dilerim!”
Bu akışta görüldüğü gibi sistem, tıpkı bir insan operatör gibi sırayla sorular sorup yanıtları alıyor, arada kontrol yapıp kullanıcıya seçenekler sunuyor ve sonunda işlemi tamamlıyor. Diyalog mümkün olduğunca yönlendirmeli tasarlandı; yani kullanıcı her adımda ne yapması gerektiğini anlıyor (hangi bilgiyi vermeli, neyi seçmeli). Yine de kullanıcı doğal dilde farklı bir yanıt verse bile (örneğin istasyon sorusuna “fark etmez” dese), LLM ajanın esnekliği sayesinde bu durum ele alınabilecektir (bot en yakın istasyonu önerebilir veya tekrar soruyu netleştirebilir). Dil ve Üslup: Botun Türkçe dil bilgisi kurallarına uygun, resmi ancak samimi bir üslup kullanması planlanmaktadır. TÜVTÜRK bir resmi hizmet olduğu için çok samimi bir dil yerine kibar bir resmiyet tercih edilir: “lütfen”, “teşekkürler”, “ister misiniz” gibi ifadelerle. Kullanıcı hata yaparsa nazikçe düzeltir (“TC numaranız 11 haneli olmalı, lütfen tekrar kontrol eder misiniz?” gibi). Ayrıca, gerektiğinde önemli uyarılar verir (randevuya geç kalmamak, gerekli belgeler vb.), çünkü bu gerçek bir hizmet. Bu bilgiler TÜVTÜRK’ün sitesindeki yönlendirmelere dayanarak da verilebilir (örneğin RayHaber’de geçen “randevu tamamen ücretsizdir, dolandırıcılara inanmayın” uyarısı gibi bilgileri bile bot sohbet sırasında aktarabilir kullanıcı faydası için​
RAİLLYNEWS.COM
). Çoklu Dönüt ve Anlama: Kullanıcı her zaman beklenen formatta cevap vermeyebilir. Bu durumda, LLM’in gücünden yararlanarak serbest metinden yapı çekmek gerekebilir. Örneğin kullanıcı plaka sorusuna “Plakam ‘34 ABC 123’ ” diye yanıt verebilir veya “Malatya’daki herhangi bir istasyon olur” diyebilir. Ajan, bu metinleri yorumlayıp gereken değişkenleri çıkarmalı (plaka = 34ABC123, istasyon = Malatya Merkez (herhangi dedi, o zaman Merkez seçilebilir) gibi). Bu, diyaloğun doğal kalması için kritik. Bu tür doğal dil anlama gereksinimleri, modelin Türkçe performansının iyi olmasını şart koşuyor; GPT-4 gibi modeller Türkçe’de bu işleri makul şekilde yapabildiği için tercih edilecek. Kontekst Yönetimi: Kullanıcıyla çok adımlı bir diyalog yürütüldüğünden, her adımda önceki verilen cevapların hatırlanması gerekir. Ajan grafiğimiz bir state ile bunu sağlıyor. Kullanıcı arada konudan saparsa veya farklı bir soru sorarsa (örneğin tam bilgileri girdikten sonra “bu arada muayene ücreti ne kadar?” gibi alakasız bir şey sorabilir), sistem bunu da ele almaya çalışmalı. Bu çok ajanlı mimaride böyle bir durum, belki geçici olarak diyaloğu ana akıştan çıkarıp bir bilgi yanıtı verip sonra kaldığı yere dönmek şeklinde çözülebilir. Bu ileri seviye bir özellik olsa da, LLM’lerin esnekliği sayesinde gerçekleştirilebilir: Orkestra, kullanıcının sorusunu fark edip bir Bilgi Ajanı (genel amaçlı Q&A) ile yanıtlayıp sonra kaldığı yere devam etmeyi kurgulayabilir. Sonuç olarak, diyalog planı kullanıcı deneyimini ön planda tutmaktadır. Kullanıcı herhangi bir teknik detayla uğraşmaz, sadece sorulara cevap verir ve seçimler yapar. Sistemin iç adımlarını fark etmez, sadece sonunda işinin hallolduğunu görür. Böylece TÜVTÜRK’ün web arayüzünde kendi başına boğuşmak yerine sohbet ederek randevusunu almış olur.
### Geliştirme Adımları (Yol Haritası)
Bu bölümde, projenin hayata geçirilmesi için adım adım bir plan sunulmaktadır. Her adımda hangi işler yapılacak, hangi bileşenlerin geliştirileceği belirtilmiştir. Bu sayede proje yönetimi daha kolay olacak ve sistematik bir şekilde ilerleme sağlanacaktır.
Ön Araştırma ve Kapsam Belirleme:
TÜVTÜRK randevu sisteminin manuel olarak incelenmesi: Web sitesinde randevu alma adımları nelerdir, hangi bilgiler istenir, istasyon ve tarih seçimi nasıl yapılır, muhtemel hata durumları nelerdir (örneğin yanlış bilgi girilince çıkan mesajlar).
Eğer mümkünse, tarayıcı geliştirici konsolundan form isteklerinin ve cevaplarının (network tab) incelenmesi. Bu sayede scraper için gerekli parametreler ve URL’ler belirlenecek.
Çok ajanlı mimariyle ilgili teknoloji seçimi: Python ile kendi basit çerçevemizi mi yazacağız, yoksa var olan bir kütüphane (LangChain, PydanticAI vs.) kullanacak mıyız kararının verilmesi. İlk etapta hafif bir kendi implementasyonumuz yeterli görünüyor.
Proje İskeletinin Oluşturulması:
Temel dizin ve dosya yapısının oluşturulması (bir sonraki bölümde ayrıntılı listelenmiştir).
graph.py içinde basit bir akış şemasının kodlanması (daha ajanlar dolu olmasa da, örnek bir başlangıç->bitiş akışı konabilir).
Ajan sınıflarının kabaca tanımlanması (her biri için bir Python sınıfı veya fonksiyonu, şimdilik pass geçilebilir). Örneğin InfoAgent, VerifyAgent vs. oluşturulur ki proje derli toplu dursun.
Streamlit arayüzünde basit bir chat iskeleti kurulması: Bir metin girdisi ve “Gönder” butonu, gönderilen metni şimdilik basitçe ekrana yansıtan bir prototip. Bu, entegrasyonun baştan sağlanması için önemlidir.
Scraper Katmanının Geliştirilmesi (POC):
Python istekleriyle TÜVTÜRK randevu sayfasına bağlanmayı deneyen küçük bir script yazılır. Örneğin scraper/test_tuvturk.py gibi bir dosyada sabit bir plaka/tescil ile istek atılıp cevap döndürülür. Eğer Cloudflare/CAPTCHA engeline takılmazsak devam edilir. Aksi halde Selenium gibi bir yöntemle POC tekrarlanır.
Başarılı olunduğunda, scraper için gerekli fonksiyonlar geliştirilir: fetch_stations(), fetch_available_slots(station, date_pref) ve book_appointment(details) vb. Henüz bunlar ajanlara bağlanmayacak, ama terminal çıktılarıyla çalıştığı doğrulanacak. Örneğin fetch_available_slots("Malatya Merkez", week=2) çağrısı yapıp sonuçları konsolda yazdırarak kontrol edilir.
Scraper geliştirmesi sırasında karşılaşılan zorluklar çözümlenir (gerekli header veya cookie ayarları vs. düzeltilir). Bu adımın sonunda sistemin arka kapılardan TÜVTÜRK’e erişebildiği netleşecektir.
Ajanların Uygulanması (Iterasyonlu):
Bu adımda her bir ajan teker teker ele alınıp kodlanacak ve test edilecektir.
Bilgi Toplama Ajanı: Önce basit haliyle, sabit bir sırayla soruları soran ve cevapları state’e kaydeden bir fonksiyon yazılır. İlk denemede LLM entegrasyonu olmadan, sabit promptlar ve string işlemleriyle çalışabilir (daha sonra LLM ile iyileştirilecek). Bu ajan Streamlit arayüzü ile bağlanıp test edilir: Kullanıcı chat’e girince arka arkaya sorular gelmeli ve verilen yanıtlar tutulmalı.
Doğrulama Ajanı: Basit format kontrolleri eklenir (regex ile plaka doğrulama gibi). Scraper entegrasyonu burada yapılır: info alınmışsa scraper.verify_info(plaka, tescil, tc) çağrısı entegre edilir. Bu fonksiyonun sonucu parse edilip ya hata ya da success olarak agenstan döndürülür. Test olarak, bilinen doğru bilgilerle akışın devam ettiği, yanlış bilgilerle Bilgi Toplama’ya geri döndüğü kontrol edilir.
Takvim Ajanı: Scraper’dan örnek müsait zaman verisi kullanarak (gerekirse sabit bir dummy veri ile) ajan geliştirilir. Bu ajan, kendisine bir liste verildiğinde bunu kullanıcıya mesaj olarak derleyip gönderebilmeli. İlk iterasyonda, “dummy slot list” kullanıp bunun kullanıcıya doğru biçimde iletildiğini doğrulayabiliriz. Sonra scraper bağlanır: slots = scraper.get_available_slots(station, prefs) ile gerçek veri çekilir, formatlanır, sunulur.
Randevu Ajanı: Bu ajan, kullanıcı seçiminden sonra devreye girecek. İlk aşamada, onu tetiklemek için elimizde bir seçim olması lazım. Bunu simüle etmek için, Takvim Ajanı’nın çıktısına kullanıcı tepkisini kendimiz vererek test edebiliriz. Randevu Ajanı, scraper.book(....) metodunu çağırır ve sonucunu döndürür. Bu sonuç içinden onay mesajını alıp kullanıcıya iletir. Başarı ve başarısızlık durumları test edilir.
İptal ve Sorgulama Ajanları: Temel akış çalıştıktan sonra bu ikisi eklenir. İptal ajanı, bilgi toplama ajanıyla benzer şekilde plaka vs. sorup scraper.cancel(...) çağırır, sonucu döndürür. Sorgulama ajanı da scraper.query(...) ile sonucu alıp kullanıcıya söyler. Bunlar ayrı diyalog başlangıçları olarak test edilir.
Her alt ajan geliştirildikten sonra, bunların entegrasyonu graph.py üzerinde yapılacak. Yani başlangıçtan sona kadar kesintisiz bir akış test edilecek. Bu testler sırasında, bir adımda elde edilen state’in sonraki adıma aktarıldığı, doğru ajanın doğru zamanda çağrıldığı incelenecek. Gerekirse graph.py mantığında düzeltmeler yapılacak.
LLM Entegrasyonu:
Ajanlar temel işlevlerini yerine getirir hale geldiğinde, bunların iletişim dilini ve esnekliğini iyileştirmek için LLM’ler entegre edilecek. Bu aşamada:
OpenAI API veya uygun bir yerel model kullanılacak şekilde ayarlar yapılır. (Not: Bu proje boyunca yer yer test etmek için OpenAI GPT-4 kullanılabilir, ancak canlıda sürekli kullanacaksak maliyet değerlendirmesi yapılır; belki GPT-3.5 yeterli olur. Alternatif olarak açık kaynak Türkçe modeller incelenir.)
Bilgi Toplama Ajanı için, her bir soru sorma işlemi prompt tabanlı hale getirilir. Örneğin ajan, state’de olmayan bir alan için bir dizi tanımlı prompt şablonuna sahip olabilir: “{alan} bilgisini sor” gibi. Bu prompt, LLM’e verilir ve modelin ürettiği soruyu kullanıcıya iletiriz. Böylece dil daha doğal hale gelebilir. (Basit bir yaklaşım olarak sabit cümleler de bırakılabilir, bu önem sırasına göre belirlenecek.)
Kullanıcıdan gelen serbest metin cevapların işlenmesinde LLM kullanılır. InfoAgent, bir yanıtı aldığında LLM ile bir “parse” yapabilir. Örneğin kullanıcı plaka ve tescili aynı mesajda verdiyse, LLM’e bu mesajı verip plakayı ve tescili ayırmasını isteyebiliriz. Ya da TC kimlik yazarken harf hatası varsa modelle düzeltme yaptırabiliriz. Bu gibi akıllı işlemler eklenecek.
Takvim ve Randevu ajanlarının, kullanıcıya cevap verirken daha zengin cümleler kurması LLM ile sağlanabilir. Örneğin onay mesajını süslü hale getirmek, ya da müsait tarihler listesine küçük açıklamalar eklemek gibi. Bu ince ayarlar prompt mühendisliği ile halledilecek.
LLM’lerin hallüsinasyon veya hata yapma riskine karşı, kritik yerlerde model çıktıları denetlenecek. Mesela Takvim Ajanı, asla listede olmayan bir tarihi uydurmamalı; bu yüzden model sadece verilen slotları listelemekle sınırlandırılacak (belki format restriksiyonu uygulanır). Bu test edilip ayarlanacak.
Streamlit Arayüz Geliştirmesi:
Projenin interaktif kullanımı için Streamlit arayüzü işlevsel hale getirilecek. Bu adımda:
Chatbot arayüzü iyileştirilir: Mesaj baloncukları, geçmiş mesajların tutulması, kaydırma vb. UX detayları halledilir. Streamlit’in state mekanizması kullanılarak kullanıcı oturumunun çok adımlı sohbeti muhafaza etmesi sağlanır. (Özellikle birden fazla kullanıcı aynı anda kullanabilsin istiyorsak, oturum bazlı state yönetimi düşünülmeli.)
Seçenek sunma durumlarında (örneğin istasyon listesi veya randevu saat listesi), bunları butonlar veya dropdown’lar olarak sunma imkanı araştırılır. Streamlit, sohbet sırasında seçim için bileşen eklemeye izin veriyorsa, kullanıcı deneyimi daha da geliştirilebilir (örneğin listeyi numaralandırmak yerine direkt buton olarak koymak). Bu teknik açıdan mümkün olmazsa, kullanıcıya yazıyla seçtirme yöntemi kalır.
Arayüzde ayrıca bir durum göstergesi veya loading spinner eklenir, çünkü scraper işlemleri birkaç saniye sürebilir. Kullanıcı “Lütfen bekleyin, randevunuz alınıyor...” gibi bir bildirim görmeli. Streamlit’te st.spinner vb. kullanılabilir.
Çok dilli destek ihtimaline karşı (belki İngilizce kullanıcı isterse gibi), ancak ilk etapta sadece Türkçe yeterli. Yine de metinlerin dilini kolay değiştirmek için sabit stringler bir yerde toplanabilir.
Test ve Hata Ayıklama:
Tüm modüller bir araya geldikten sonra, farklı senaryolar üzerinden uçtan uca test yapılır. Örneğin:
Mutlu path: Tüm bilgiler doğru, ilk sunulan tarih kabul edildi, randevu alındı.
Hatalı bilgi: Yanlış tescil no girildi, sistem tekrar sordu, sonra düzeldi.
Uygun slot bulunamadı: Kullanıcı çok yakın tarih istedi, dolu çıktı, sistem alternatif sordu.
İptal senaryosu: Kullanıcı önce randevu aldı, sonra iptal etmek istedi, vs.
Bu testler sırasında ortaya çıkan buglar giderilir. Özellikle ajan geçişlerinde state’in doğru taşınması, LLM çıktılarının beklenmedik cevaplar üretmesi (örneğin listelenen seçeneklerden farklı bir şey söylemesi) gibi durumlar yakından izlenecek. Gerekirse kural bazlı müdahaleler veya prompt düzeltmeleri yapılır.
Güvenlik testleri: Kötü niyetli girişler de düşünülmeli (SQL injection değil belki ama, kullanıcı alakasız ya da çok uzun metinler girerse ne olur). Sistem bunları makul şekilde karşılamalı, bozulmamalı.
Dokümantasyon ve Dizin Düzenlemesi:
Kod içi dokümantasyon (her fonksiyonun ne yaptığına dair docstring’ler) yazılır. Özellikle scraper fonksiyonlarının ne yaptığı ve hangi URL’lere hitap ettiği açıklanır (ileride site değişirse kolay güncelleme için).
Kullanım kılavuzu niteliğinde bir README hazırlanır: Projenin amacı, kurulumu, çalıştırma talimatları, ve bir örnek kullanım senaryosu anlatılır.
Dosya/dizin yapısı son haline göre README’de güncellenir.
Ayrıca, uzun vadeli gelişim önerileri, karşılaşılan sorunlar ve çözüm yöntemleri gibi notlar da belgelendirilir.
İyileştirmeler ve Ek Özellikler:
Zaman kalırsa veya sonraki sprintlerde, iptal ve sorgulama özellikleri tam entegre edilip son kullanıcıya sunulur. Bunların ayrı ayrı testleri yapılır.
Performans iyileştirmesi: Gereksiz API çağrıları veya yavaş noktalar optimize edilir. Örneğin her seferinde istasyon listesi çekiliyorsa bunu önbelleğe almak gibi.
LLM maliyeti değerlendirilir: Her sohbet için ne kadar token harcanıyor, bunu düşürmek için prompt optimizasyonu yapılır. Gerekirse bazı sabit yanıtlar koda alınır, LLM yerine kullanılır.
Sunum ve Geri Bildirim:
Proje, hedef kullanıcı kitlesine (bu bir şirket içi proje ise ilgili ekiplere, değilse küçük bir kullanıcı grubuna) demo edilir. Alınan geri bildirimlere göre düzeltmeler yapılır. Örneğin kullanıcılar belirli bir soruyu anlamadıysa o kısım yeniden yazılır.
Sistem gerçek ortamda test amaçlı birkaç randevu alır (gerekirse hemen iptal edilir bu randevular) ki canlı veride de çalıştığı görülsün.
Son olarak proje teslim edilir veya yayına alınır.
Bu yol haritası, her adımı mantıklı bir sırayla ele alarak projenin parça parça inşa edilmesini sağlayacaktır. Özellikle önce çekirdek işlevleri (randevu alabilme) çalışır hale getirip sonra iyileştirmeler eklemek, risk yönetimi açısından önemlidir. Her adım sonunda çalışan bir alt ürün (MVP) elde edip üzerine koyarak ilerlemek en sağlıklı yaklaşım olacaktır.
### Proje Dizin Yapısı ve Görev Dağılımı
Projenin düzenli ve ölçeklenebilir olması için dosya/dizin yapısı dikkatlice planlanmıştır. Aşağıda önerilen yapı ve her birimin sorumlulukları listelenmiştir:
bash
Kopyala
Düzenle
tuvturk_randevu_projesi/
├── README.md
├── requirements.txt
├── app.py                 # Streamlit uygulamasının ana dosyası
├── graph.py               # Ajan yönlendirme grafiği ve bağımlılık enjeksiyonu
├── agents/
│   ├── __init__.py
│   ├── info_agent.py      # Bilgi Toplama Ajanı implementasyonu
│   ├── verify_agent.py    # Doğrulama Ajanı implementasyonu
│   ├── calendar_agent.py  # Takvim Ajanı implementasyonu
│   ├── appointment_agent.py # Randevu Ajanı implementasyonu
│   ├── cancel_agent.py    # İptal Ajanı (ek özellik)
│   └── query_agent.py     # Sorgulama Ajanı (ek özellik)
├── services/
│   ├── __init__.py
│   ├── tuvturk_scraper.py # TÜVTÜRK web sayfalarını gezip veri çeken fonksiyonlar
│   └── utils.py           # Belki formatlama, tarih dönüştürme gibi yardımcı fonksiyonlar
├── data/
│   └── stations.json      # İstasyonların listesi ve kodları (scraper ile de çekilebilir)
├── tests/
│   ├── test_scraper.py    # Scraper fonksiyonları için birimler testleri
│   └── test_agents.py     # Ajanların mantığı için birimler testleri (örn doğrulama format testleri)
└── logs/
    └── app.log            # Uygulama logları (hata ayıklama için)
Açıklamalar ve görev dağılımları:
app.py: Streamlit uygulamasını çalıştıran ana modül. Burada kullanıcı arayüzü tanımlanır. Chatbotun arkaplanında graph.py ile tanımlanan ajan yapısı kullanılarak gelen kullanıcı mesajları uygun ajanlara yönlendirilir ve cevapları arayüzde gösterilir. app.py aynı zamanda oturum yönetimi, geçmiş konuşmaların tutulması gibi işleri de yapar.
graph.py: Çok ajanlı sistemin beyni diyebiliriz. Burada bir ajan grafiği tanımlanır; hangi ajanların örnekleri yaratılacak, bunlar hangi sırayla veya hangi koşullarda birbirini çağıracak belirlenir. Örneğin önce InfoAgent’i çağır, o bitince VerifyAgent’e git gibi kurallar burada kodlanır (önceki bölümde pseudo-kodunu verdik). Ayrıca her ajanın ihtiyaç duyduğu LLM veya servis nesneleri burada enjekte edilir. Örneğin info_agent = InfoAgent(llm=gpt4_model) gibi. Bu sayede ajanlar içerde direkt self.llm diyerek modeli kullanabilir hale gelir.
agents/*: Bu dizin altındaki her dosya bir ajanı temsil eder. Her ajan büyük olasılıkla bir sınıf olarak yazılacak. Ortak bir Agent arayüzü/soyut sınıfı tanımlamak iyi olabilir (agents/__init__.py içinde veya ayrı bir base_agent.py de tanımlanabilir). Bu sınıf, tüm ajanlarda bulunması gereken metodları (ör. run(state) veya step(...)) tanımlar. Alt ajanlar ise kendi özel davranışlarını uygular.
info_agent.py: Kullanıcıyla iletişim kurup verileri alan mantık. Muhtemelen burada hem bir diyalog state makinesi (hangi soruda olduğu vs.) yönetilecek, hem de LLM ile sorular sorulacak.
verify_agent.py: Bilgileri kontrol eden mantık. Scraper’ın doğrulama fonksiyonunu çağırır, hataları döndürür.
calendar_agent.py: Müsait randevuları getiren ve kullanıcıya sunan mantık. Scraper’ın takvim fonk.’unu kullanır.
appointment_agent.py: Randevuyu kesinleştiren mantık. Scraper’ın randevu al fonk.’unu çağırır, sonucu kullanıcıya iletir.
cancel_agent.py: Randevu iptal akışını yöneten mantık (opsiyonel ilk sürüm için).
query_agent.py: Randevu sorgulama akışını yöneten mantık (opsiyonel).
services/*: Ajanların harici işlemlerini yapmasını sağlayan servis fonksiyonları.
tuvturk_scraper.py: TÜVTÜRK’ün web sayfalarına istek atıp veri çeken fonksiyonlar. Örneğin def verify_vehicle(plaka, tescil) -> bool (doğrulama), def get_available_slots(station) -> list (takvim bilgisi), def make_reservation(details) -> dict (randevu onayı) gibi fonksiyonlar burada bulunur. Bu dosya tek başına çalıştırılabilir şekilde de yazılabilir (test amaçlı). Gerekirse alt fonksiyonlara ayrılabilir (çok karmaşık olursa).
utils.py: Ortak kullanılabilecek yardımcılar. Örneğin tarih formatlama (convert_date("12/04/2025") -> datetime.date(2025,4,12)), plaka normalizasyonu (boşluk ve harf boyutları düzeltme), string temizleme gibi. Ajanlar veya scraper bunları kullanabilir.
data/stations.json: TÜVTÜRK’ün istasyon ve şehir listesi. Scraper bunu web’den de çekebilir fakat sabit bir liste olarak da koyabiliriz (çok sık değişmez). Bu JSON içinde her şehirdeki istasyonlar ve kodları tutulabilir. Bilgi Toplama Ajanı, eğer kullanıcı şehir girerse buradan kod bulup Takvim Ajanı’na verebilir. Tamamen opsiyonel ama kullanışlı.
tests/*: Test kodları. Özellikle scraper fonksiyonlarını geliştirdikten sonra bozulmamasını sağlamak için bazı birim testler yazmak iyi olur. Örneğin test_scraper.py içinde örnek HTML dosyaları üzerinden get_available_slots fonksiyonunun parse’ının doğru yapıldığı test edilebilir. Ajan testlerinde ise, dummy bir LLM nesnesi verip (veya monkeypatch ile) belirli cevapları döndürmesi sağlanarak, ajanın akışı test edilir. Bu kısım isteğe bağlı ama uzun vadede güvenilirlik için önemli.
logs/app.log: Hata ayıklama ve izleme için log dosyası. Uygulama çalışırken kritik olaylar (randevu alındı, doğrulama başarısız vs.) bu log’a yazılabilir. Özellikle çok kullanıcılı kullanımda veya üretim ortamında sorunları teşhis için gerekli.
Bu yapıda, her bir dosya ve modül kendi sorumluluk alanına sahip olduğu için ekip içinde iş bölümü de kolaylaşır. Örneğin bir geliştirici sadece services/tuvturk_scraper.py üzerinde çalışıp veri çekme işini iyileştirirken, bir başkası agents/info_agent.py üzerinde diyalog akışını geliştirebilir. graph.py’de tanımlanan arayüz sayesinde, ikisi de uyumlu çalıştığı sürece sistem entegre olur. Görev Dağılımı Önerileri:
Ajan Geliştirme: Takımda dil işleme konusunda deneyimli biri, LLM prompt mühendisliği ve diyalog yönetimi kısmına odaklanıp agent modüllerini yazabilir.
Scraper Geliştirme: Web programcılığı veya tersine mühendislikte iyi olan biri, tarayıcı isteği analiz edip scraper fonksiyonlarını kodlayabilir.
Arayüz Geliştirme: Frontend yeteneği olan veya Streamlit tecrübesi olan biri, app.py ve arayüzün kullanıcı dostu olmasına odaklanabilir.
Test ve Entegrasyon: Bir kişi de tüm parçaların düzgün bağlandığını, graph.py’nin mantığının doğru olduğunu test edip, gerektiğinde düzenlemeler yapabilir.
Bu şekilde paralel ilerlemek de mümkün olacaktır.
### Uzun Vadeli Genişleme ve İyileştirme Önerileri
Projenin ilk sürümü temel işlevleri yerine getirdikten sonra, gelecekte eklenebilecek özellikler ve iyileştirmeler ile ilgili bazı öneriler:
Resmi Entegrasyon veya API Kullanımı: TÜVTÜRK ilerde bir açık API sunarsa, veya belki zaten kısıtlı da olsa bir web servis varsa, scraper yerine doğrudan API kullanımı daha sağlıklı olacaktır. Uzun vadede, sistemimizi bu API’ye geçirecek şekilde hazırlıklı tutmalıyız. Mimari olarak scraper katmanını soyut tuttuğumuz için, bu geçiş yalnızca services/tuvturk_api.py yazıp agent’ları oraya yönlendirmek şeklinde olabilir.
Çoklu Dil Desteği: Şu an sistem Türkçe odaklı, ancak Türkiye’de İngilizce konuşan araç sahipleri de olabilir (turistler vs.). Botun İngilizce de hizmet verebilmesi için LLM’in dil desteği avantaj; prompt’ları İngilizceye çevirmek yeterli olabilir. Uzun vadede dil seçimi opsiyonu sunulabilir.
Sesli Asistan Entegrasyonu: Streamlit arayüzü yerine veya yanı sıra bir sesli arayüz eklemek kullanıcı deneyimini artırabilir. Örneğin mobil uygulama veya web’de mikrofonla konuşarak bilgilerini verseler ve botun cevabını sesli duyabilseler güzel olur. Bu, speech-to-text ve text-to-speech API’lerinin entegrasyonunu gerektirir (Google, Azure veya open-source Kaldi vs. kullanılabilir).
Takvim Entegrasyonu: Kullanıcının onayıyla, alınan randevuyu kendi kişisel takvimine (Google Calendar, Outlook vb.) ekleme özelliği eklenebilir. Bu sayede kullanıcı randevuyu unutmaz, yaklaşınca hatırlatma alır. Bunu yapmak için randevu detaylarından ICS dosyası oluşturulup kullanıcıya verilebilir veya API entegrasyonuyla doğrudan takvimine işlenebilir.
Bildirim ve Hatırlatma: Randevu yaklaştığında (örneğin 1 gün önce) kullanıcının iletişim bilgileri varsa SMS veya e-posta hatırlatması gönderecek bir özellik düşünülebilir. Bu tabii ki ekstra iletişim verisi almayı gerektirir (telefon, email).
Daha Zeki Diyalog ve Konuşma: Şu anki diyalog nispeten kural bazlı ilerliyor. Gelecekte, botun kullanıcı niyetlerini daha derin anlaması, sohbeti esnek yönetmesi için çalışmalar yapılabilir. Örneğin kullanıcı aynı anda iki işlemek yapmak isterse (“dün aldığım randevuyu iptal edip yenisini alabilir miyiz?” gibi bir cümle), sistem bunu da çözümleyebilir hale gelebilir. Bu, multi-intent parsing ve daha gelişmiş bir diyalog yönetimi gerektirir​
İGORİZRAYLEVYCH.MEDİUM.COM
.
Veri Kaydı ve Raporlama: Sistemin kullanım verileri (kaç randevu alındı, en çok hangi şehir istendi, başarı/hata oranları) kaydedilip raporlanabilir. Bu bilgiler hem sistemin değerini gösterir hem de sorunlu noktaları ortaya çıkarır (örneğin bir istasyon için çok sık başarısız oluyorsa belki site yapısı farklıdır).
Ajanların Öğrenmesi ve Gelişimi: İlk etapta ajanlar sabit kurallarla çalışacak ancak zamanla biriken verilerle makine öğrenimi yaklaşımları eklenebilir. Örneğin, doğrulama ajanı hep belirli bir hatada başarısız oluyorsa (kullanıcılar tescil no yerine motor no giriyor diyelim), bu tespit edilip ajan proaktif uyarı verecek şekilde güncellenebilir. Bu sürekli iyileştirme döngüsü planlanabilir.
Daha Fazla Hizmet Entegrasyonu: TÜVTÜRK randevu dışında, araçla ilgili diğer işlemler de entegre edilebilir. Örneğin trafik sigortası yenileme hatırlatma, egzoz pulu randevusu, vb. Bot, ileride çok amaçlı bir araç asistanına genişleyebilir. Mimarimiz çok ajanlı olduğu için, yeni bir görev için yeni bir ajan ekleyip orkestra grafiğini genişleterek bunu yapabiliriz.
Kapasite ve Ölçeklendirme: Kullanıcı sayısı artarsa, sistemin birden fazla oturumu paralel yönetebilmesi gerekir. Şu an LLM çağrıları bulut üzerinden olduğu için ölçek sorunu pek olmaz, ancak Streamlit sunucusunun ve scraper’ın aynı anda birden çok isteği kaldırabilmesi önemli. Gerekirse queue mekanizması veya ayrı bir mikroservis (ör. scraper’ı ayrı bir web servisi yapıp istekleri orada sırala) kullanılabilir. Ayrıca, LLM maliyetlerini optimize etmek için caching stratejileri veya kullanıcı başına limitler konabilir.
Güvenlik ve Gizlilik: Uzun vadede, bu sistem gerçek kullanıcı verileri işleyeceği için KVKK kapsamında gizlilik önlemleri alınmalı. Örneğin T.C. kimlik numarası gibi veriler loglanmamalı, konuşma geçmişinde şifreli saklanmalı veya hiç saklanmamalı. Ayrıca, LLM prompt’larına gereksiz kişisel veri koymamaya dikkat edilmeli (OpenAI gibi servisler gönderilen verileri loglayabilir). Bu nedenle belki ileride on-premise bir LLM çözümüne geçmek veya kritik verileri maskelayıp göndermek düşünülebilir.
Kullanıcı Doğrulaması: Kötüye kullanımın önlenmesi için, özellikle iptal işlemlerinde, kullanıcının gerçekten o aracın sahibi olduğunu doğrulamak bir konu olabilir. Şu an bunu doğrulamanın tek yolu kimlik numarası vs. girmesi. Belki uzun vadede E-Devlet entegrasyonu gibi çok ileri fikirler akla gelebilir ama şimdilik bu not edilir.
Sonuç olarak, bu proje esnek mimarisi sayesinde büyümeye ve yeni özellikler eklenmesine uygundur. Temel modülerlik prensiplerine uyulduğundan, bir parçayı değiştirmek veya yeni bir parça eklemek, tüm sistemi silbaştan yazmayı gerektirmez. Çok ajanlı yapı da ölçeklendirme ve karmaşık işlere uyum sağlama konusunda avantaj sunar​
K2VİEW.COM
. İlk sürüm başarıyla kullanıma girdikten sonra, yukarıdaki fikirler sırasıyla değerlendirilebilir ve kullanıcı geri bildirimleri ışığında önceliklendirilerek hayata geçirilebilir.