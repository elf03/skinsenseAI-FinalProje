# SkinSense AI — Geliştirme Günlüğü (AI Günlüğü)

Bu günlük, Flask ile web uygulaması geliştirme dönem projesi kapsamında Yapay Zeka (AI) aracı ile yapılan çalışma oturumlarını belgelemektedir. Toplamda 7 oturum kaydedilmiştir.

---

## Oturum 1 — 15 Mayıs 2026 — 14:00 - 15:30

### Hedef
Projenin ana iskeletini oluşturmak ve GitHub yapısını kurmak.

### Kullandığım Mod ve Model
- Mod: Plan / Fast
- Model: Gemini 3 Pro
- Görünüm: Editor / Manager

### Verdiğim Promptlar
1. Cilt bakım analizi yapan bir site yapacağım. Kullanıcılar fotoğraf yükleyip veya anket çözüp rutin önerisi alacak. Bu proje için Flask ile nasıl bir klasör yapısı kurmalıyım?
2. Github için mantıklı bir .gitignore ve README.md taslağı oluştur.

### Ajanın Önerdiği Plan
Ajan, `backend` ve `frontend` olmak üzere projeyi iki ana klasöre ayırmayı önerdi. Backend tarafında Flask Blueprint yapısı kullanarak `routes`, `models` ve `services` klasörlerini oluşturmayı tavsiye etti.

### Plan'da Sorguladıklarım
- Başlangıçta frontend için React kullanmayı önerdi ancak ben "Vanilla HTML/CSS/JS (no framework) kullanmak istiyorum" diyerek karşı çıktım çünkü öğrenme eğrisi dönem projesi için çok uzundu.

### Üretilen Kodda Düzelttiklerim
- `app.py` oluşturulurken veritabanı adını `app.db` yapmıştı, proje bütünlüğü için `skinsense.db` olarak değiştirdim.

### Karşılaştığım Hatalar ve Çözümler
- Hata: İlk aşamada sanal ortam (venv) aktifleşmediği için Flask modülü bulunamadı.
- Çözüm: Terminalde `venv\Scripts\activate` komutunu çalıştırarak sanal ortamı aktif ettim.

### Bu Oturumdan Öğrendiğim
AI, projenin büyüklüğüne göre baştan sağlam bir mimari (Blueprint pattern vb.) kurmanın önemini gösterdi. Her şeyi tek bir `app.py` dosyasına yazmak yerine modüler yapının ileride işimi çok kolaylaştıracağını anladım.

### Sonraki Oturum İçin Notlar
- Veritabanı modellerini (User ve Analysis) tasarlayacağız.

---

## Oturum 2 — 17 Mayıs 2026 — 16:00 - 18:00

### Hedef
Veritabanı şemasını oluşturmak ve Flask-SQLAlchemy kurulumunu tamamlamak.

### Kullandığım Mod ve Model
- Mod: Plan
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. Kullanıcı kaydı ve cilt analizi sonuçlarını saklayacak veritabanı modellerini yaz (SQLAlchemy kullanarak).

### Ajanın Önerdiği Plan
Ajan; User, Analysis ve Product olmak üzere üç farklı tablo önerdi. `User` tablosunda cilt tipi tercihini ve dil seçeneğini, `Analysis` tablosunda ise AI sonuçlarını saklamayı planladı.

### Plan'da Sorguladıklarım
- Ajan ilişki kurarken `lazy='dynamic'` kullanmıştı, ancak ben dönen veriyi direkt frontend'e JSON basacağım için `lazy=True` olarak standart ilişkiye çevirmesini istedim.

### Üretilen Kodda Düzelttiklerim
- Sadece email ve şifre vardı, kullanıcının `preferred_language` ayarını manuel olarak modele ben ekledim.

### Karşılaştığım Hatalar ve Çözümler
- Hata: Terminalde Unicode hatası (emoji basarken crash) aldım.
- Çözüm: Ajanın yönlendirmesiyle `app.py` içerisine `sys.stdout` utf-8 encoding ekleyerek emoji hatalarını aştım.

### Bu Oturumdan Öğrendiğim
SQLAlchemy'de tablolar arası ilişkinin (Foreign Key ve Relationship) nasıl çalıştığını pekiştirdim. Özellikle JSON formatına dönüştürmek için modele eklediğimiz `to_dict()` fonksiyonu çok mantıklı bir yaklaşımdı.

### Sonraki Oturum İçin Notlar
- Auth (Kayıt, Giriş, Şifre Sıfırlama) endpoint'leri yapılacak.

---

## Oturum 3 — 20 Mayıs 2026 — 20:00 - 22:30

### Hedef
Sisteme giriş/çıkış ve OTP kodlu şifre sıfırlama mekanizmasını eklemek.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. Flask-JWT-Extended kullanarak /login, /register rotaları oluştur. Şifreyi unuttuysa mailine OTP kodu gelsin ve o kodla giriş yapsın.

### Ajanın Önerdiği Plan
Ajan, `auth.py` route'unu oluşturup şifrelerin bcrypt ile hashlendiği, giriş yapıldığında JWT token dönen güvenli bir sistem tasarladı. Mail gönderimi için ayrı bir `email_service.py` yazdı.

### Plan'da Sorguladıklarım
- Mail ayarlarında doğrudan şifremin kodda yer alması önerilmişti. Buna karşı çıktım, güvenlik sebebiyle bunları `.env` dosyasına almasını söyledim.

### Üretilen Kodda Düzelttiklerim
- E-posta servisi için Google'dan aldığım "App Password" sistemini kullanarak `.env` bilgilerini doldurdum.

### Karşılaştığım Hatalar ve Çözümler
- Hata: OTP doğrulama aşamasında "Token Has Expired" hatası alıyordum.
- Çözüm: JWT token süresini 15 dakikadan 24 saate (veya daha esnek bir süreye) çıkardık.

### Bu Oturumdan Öğrendiğim
Şifrelerin veritabanında düz metin (plain text) olarak saklanmasının ne kadar tehlikeli olduğunu ve `bcrypt` kütüphanesinin çalışma mantığını öğrendim.

### Sonraki Oturum İçin Notlar
- Frontend'e başlayacağız, renk paleti ve ana sayfayı kuracağız.

---

## Oturum 4 — 22 Mayıs 2026 — 10:00 - 12:00

### Hedef
Ana sayfa tasarımını oluşturmak ve UI/UX kararlarını netleştirmek.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. Tema açık renk olsun bej, toz pembe, mor, pembe renk seçenekleri olsun. Modern ve glassmorphism detaylı bir ana sayfa (index.html) tasarla.

### Ajanın Önerdiği Plan
Ajan, özel bir `main.css` dosyası içerisinde CSS variable'ları (değişkenleri) kullanarak renk paleti tasarladı. Ana sayfa için hero section, özellikler ve footer içeren bir yapı kurdu.

### Plan'da Sorguladıklarım
- Butonlardaki gölge çok sert görünüyordu, ajandan gölgeleri daha soft ve lila tonlarında yapmasını istedim.

### Üretilen Kodda Düzelttiklerim
- `index.html` içindeki İngilizce placeholder yazılarını kendim Türkçe'ye çevirdim ve menü linklerini düzenledim.

### Karşılaştığım Hatalar ve Çözümler
- Hata: Live Server'da açtığımda CSS dosyası yüklenmiyordu (404 Not Found).
- Çözüm: Dosya yollarını (href) kök dizin `/css/main.css` yerine bağıl `css/main.css` olarak düzelttim.

### Bu Oturumdan Öğrendiğim
CSS Değişkenleri (`:root`) kullanarak tüm sitenin renk temasını tek bir yerden yönetmenin projenin büyümesi durumunda ne kadar büyük bir avantaj sağladığını gördüm.

### Sonraki Oturum İçin Notlar
- Gemini API bağlantısını kurup, fotoğraf analizini kodlayacağız.

---

## Oturum 5 — 24 Mayıs 2026 — 13:00 - 15:30

### Hedef
Google Gemini Vision API kullanarak cilt analizini (fotoğraf üzerinden) yapmak.

### Kullandığım Mod ve Model
- Mod: Plan
- Model: Gemini 3 Pro
- Görünüm: Manager

### Verdiğim Promptlar
1. Kullanıcı selfie yüklesin veya kamerayla canlı fotoğraf çeksin. Bunu Gemini API'ye gönderip analiz (siyah nokta, akne, cilt tipi) yaptır.

### Ajanın Önerdiği Plan
Ajan, `gemini_service.py` adında bir dosya oluşturarak API'ye gidecek detaylı prompt'u (istem) belirledi. Sistem, kullanıcının fotoğrafını Base64'e çevirip Google'a göndererek JSON formatında analiz raporu dönüyordu.

### Plan'da Sorguladıklarım
- Gemini API bazen yavaş çalışıp Timeout atabiliyordu. Ajan'dan eğer API cevap vermezse projenin çökmemesi için mock (sahte) veri dönen bir fallback (yedek plan) fonksiyonu yazmasını istedim.

### Üretilen Kodda Düzelttiklerim
- Analiz anketindeki seçeneklere (Emoji'ler ve metinler) kendi cilt bakım bilgime dayanarak ufak eklemeler yaptım.

### Karşılaştığım Hatalar ve Çözümler
- Hata: Fotoğraf API'ye giderken "Payload Too Large" (Dosya çok büyük) hatası alındı.
- Çözüm: Frontend tarafında fotoğraf API'ye gönderilmeden önce canvas kullanılarak çözünürlüğü ve kalitesi düşürülerek (compress) gönderildi.

### Bu Oturumdan Öğrendiğim
Görsel işleme ve yapay zeka entegrasyonlarının sanıldığı kadar zor olmadığını, ancak yapay zekadan tutarlı JSON formatında cevap alabilmek için System Prompt'un çok dikkatli (ve sınırlandırıcı) yazılması gerektiğini öğrendim.

### Sonraki Oturum İçin Notlar
- İçerik kontrolü (Ingredient Check) sayfasını tasarlayacağız.

---

## Oturum 6 — 26 Mayıs 2026 — 15:00 - 17:30

### Hedef
Kullanıcının ürün içerik listesini kopyalayıp yapıştırdığında bunun güvenli olup olmadığını analiz eden sistemi yapmak.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. İçerik analizi sayfası yap. Kullanıcı ürünün içeriğini girecek (örn: Water, Glycerin, Sodium Lauryl Sulfate), sistem bunları "Güvenli, Dikkat Gerektiren, Zararlı" olarak kategorize edecek ve trafik ışığı (100 üzerinden puan) gibi skor verecek.

### Ajanın Önerdiği Plan
Ajan, `ingredient-check.html` isimli bir sayfa tasarladı. Kullanıcı veriyi girdiğinde, arka planda Gemini API'ye gidip her bir kimyasalın cilt için etkisini sordu ve skoru hesaplayıp frontend'e iletti.

### Plan'da Sorguladıklarım
- Sistemin her ürün sorgusunda baştan analiz yapması performans kaybı gibi geldi. "Ürünler veritabanında cache'lenebilir mi?" diye sorguladım, ajan da basit bir ürün veritabanı (Product tablosu) önerdi.

### Üretilen Kodda Düzelttiklerim
- Puanlama kısmındaki CSS kartlarında (score-good, score-bad vb.) arkaplan gradient renklerini kendi temamıza daha uygun olacak pastel tonlarla değiştirdim.

### Karşılaştığım Hatalar ve Çözümler
- Hata: İçerik analizi sonucu dönerken bazen metin uzunluğu sebebiyle UI patlıyordu.
- Çözüm: CSS'te `overflow-wrap: break-word` ekleyerek uzun içerik isimlerinin alt satıra geçmesini sağladım.

### Bu Oturumdan Öğrendiğim
Backend'den dönen karmaşık bir JSON verisini (kategorize edilmiş listeler) frontend tarafında dinamik olarak (JavaScript `map` fonksiyonları ile) HTML elementlerine dönüştürmenin mantığını iyice kavradım.

### Sonraki Oturum İçin Notlar
- Son rötuşlar (404 sayfası ve Dashboard ilerleme grafiği) yapılacak.

---

## Oturum 7 — 28 Mayıs 2026 — 19:00 - 20:30

### Hedef
Kullanıcı paneli (Dashboard) grafiklerini eklemek ve eksik olan sayfaları (404 vb.) tamamlamak.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. Chart.js kullanarak kullanıcının önceki analizlerine göre ilerlemesini gösteren bir grafik yap. Ayrıca olmayan bir sayfaya gidildiğinde çıkacak şık bir 404 sayfası oluştur.

### Ajanın Önerdiği Plan
Ajan `dashboard.html` içerisine Chart.js kütüphanesini CDN ile ekleyip, kullanıcının "nem" ve "akne" seviyelerini tarihe göre çizen bir grafik yazdı. Ardından animasyonlu bir `404.html` sayfası oluşturdu ve backend'e `@app.errorhandler(404)` yakalayıcısını ekledi.

### Plan'da Sorguladıklarım
- Grafikteki değerler sayısal değilse (Örn: Akne="Yok") nasıl çizileceğini sordum. Ajan JavaScript'te `"Yok": 0, "Orta": 55` gibi bir map (eşleştirme) objesi oluşturarak metinleri sayılara çevirme mantığını sundu.

### Üretilen Kodda Düzelttiklerim
- Chart.js varsayılan gri grid çizgileri çok keskindi. Onları sitemin renklerine uysun diye `rgba(203,153,197,0.1)` şeklinde lila alt tonlu yarı saydam yaptım.

### Karşılaştığım Hatalar ve Çözümler
- Hata: API'den hata döndüğünde sayfa bembeyaz kalıyordu.
- Çözüm: 404 ve 500 handler'larını JSON dönecek şekilde Flask içine (`app.py`) adapte ettim.

### Bu Oturumdan Öğrendiğim
Frontend'de bir veriyi kullanıcıya göstermeden önce ne olursa olsun işlemek ve şekillendirmek (data mapping) gerektiğini, ayrıca uygulamanın kullanıcı bilmedik bir yere gittiğinde patlamaması için hata yakalamanın (Error Handling) web geliştirmedeki kritik önemini öğrendim.
