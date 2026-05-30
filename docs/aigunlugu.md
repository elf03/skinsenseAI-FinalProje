# SkinSense AI — Geliştirme Günlüğü (AI Günlüğü)

Bu günlük, Flask ile web uygulaması geliştirme dönem projesi kapsamında Yapay Zeka (AI) aracı ile yapılan çalışma oturumlarını belgelemektedir. Toplamda 8 oturum kaydedilmiştir.

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
AI, projenin büyüklüğüne göre baştan sağlam bir mimari kurmanın önemini gösterdi.

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

### Karşılaştığım Hatalar ve Çözümler
- Hata: Terminalde Unicode hatası (emoji basarken crash) aldım.
- Çözüm: Ajanın yönlendirmesiyle `app.py` içerisine `sys.stdout` utf-8 encoding ekleyerek emoji hatalarını aştım.

---

## Oturum 3 — 20 Mayıs 2026 — 20:00 - 22:30

### Hedef
Sisteme giriş/çıkış ve OTP kodlu şifre sıfırlama mekanizmasını eklemek.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. Flask-JWT-Extended kullanarak /login, /register rotaları oluştur. Şifreyi unuttuysa mailine OTP kodu gelsin.

### Ajanın Önerdiği Plan
Ajan, `auth.py` route'unu oluşturup şifrelerin bcrypt ile hashlendiği güvenli bir sistem tasarladı. Mail gönderimi için ayrı bir `email_service.py` yazdı.

### Üretilen Kodda Düzelttiklerim
- E-posta servisi için Google'dan aldığım "App Password" sistemini kullanarak `.env` bilgilerini doldurdum.

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

### Karşılaştığım Hatalar ve Çözümler
- Hata: Live Server'da açtığımda CSS dosyası yüklenmiyordu (404 Not Found).
- Çözüm: Dosya yollarını (href) kök dizin `/css/main.css` yerine bağıl `css/main.css` olarak düzelttim.

---

## Oturum 5 — 24 Mayıs 2026 — 13:00 - 15:30

### Hedef
Google Gemini Vision API kullanarak cilt analizini (fotoğraf üzerinden) yapmak.

### Kullandığım Mod ve Model
- Mod: Plan
- Model: Gemini 3 Pro
- Görünüm: Manager

### Verdiğim Promptlar
1. Kullanıcı selfie yüklesin veya kamerayla canlı fotoğraf çeksin. Bunu Gemini API'ye gönderip analiz yaptır.

### Karşılaştığım Hatalar ve Çözümler
- Hata: Fotoğraf API'ye giderken "Payload Too Large" (Dosya çok büyük) hatası alındı.
- Çözüm: Frontend tarafında fotoğraf API'ye gönderilmeden önce canvas kullanılarak çözünürlüğü düşürüldü.

---

## Oturum 6 — 26 Mayıs 2026 — 15:00 - 17:30

### Hedef
Kullanıcının ürün içerik listesini kopyalayıp yapıştırdığında bunun güvenli olup olmadığını analiz eden sistemi yapmak.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. İçerik analizi sayfası yap. Kullanıcı ürünün içeriğini girecek, sistem bunları "Güvenli, Dikkat Gerektiren, Zararlı" olarak kategorize edecek.

### Üretilen Kodda Düzelttiklerim
- Puanlama kısmındaki CSS kartlarında (score-good, score-bad vb.) arkaplan gradient renklerini kendi temamıza daha uygun olacak pastel tonlarla değiştirdim.

---

## Oturum 7 — 29 Mayıs 2026 — 19:00 - 20:30

### Hedef
Kullanıcı paneli (Dashboard) grafiklerini eklemek ve eksik olan sayfaları (404 vb.) tamamlamak.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. Chart.js kullanarak kullanıcının önceki analizlerine göre ilerlemesini gösteren bir grafik yap. Ayrıca olmayan bir sayfaya gidildiğinde çıkacak şık bir 404 sayfası oluştur.

### Plan'da Sorguladıklarım
- Grafikteki değerler sayısal değilse (Örn: Akne="Yok") nasıl çizileceğini sordum. Ajan JavaScript'te eşleştirme (mapping) mantığını sundu.

---

## Oturum 8 — 30 Mayıs 2026 — 16:00 - 18:30

### Hedef
Yapay Zeka kodundaki mantık hatasını düzeltmek, Profil Sayfasını eklemek ve projeyi teslimata (Docker) hazırlamak.

### Kullandığım Mod ve Model
- Mod: Fast
- Model: Gemini 3 Pro
- Görünüm: Editor

### Verdiğim Promptlar
1. "Profil sayfası tasarla ve avatar yükleme sistemini kur."
2. **(Hata Düzeltme Prompt'u):** "Profil fotoğrafı ekleniyor ama `api.js` dosyasındaki menü kodlarını eksik yazmışsın. Navbar'da hala ismimin baş harfi çıkıyor. Sadece ilk harfi alan kodu sil ve eğer kullanıcının avatarı varsa sağ üstte resmi gösterecek şekilde `initNavbar` fonksiyonunu baştan yaz."

### Üretilen Kodda Düzelttiklerim / Ajanı Yönlendirmem
- Ajan avatar yükleme rotasını backend'de doğru kurmasına rağmen frontend'de (Navbar'da) güncellemeyi unutmuştu. Benim bu uyarım üzerine hatasını fark edip `api.js` kodlarını yeniden yazdı. Bu sayede sadece kopyala-yapıştır yapmadığımı, kodun çalışma mantığını anlayıp yapay zekayı denetleyebildiğimi test etmiş oldum.

### Bu Oturumdan Öğrendiğim
Yapay zekanın backend tarafında çok başarılı kod yazsa da, bazen frontend'deki detayları (UI güncellemelerini) atlayabildiğini gördüm. Yazılım geliştirirken son kontrolün her zaman insanda (bende) olması gerektiğini öğrendim.
