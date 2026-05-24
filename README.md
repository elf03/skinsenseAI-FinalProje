# 🌸 SkinSense AI

## Projenin Amacı
SkinSense AI, kullanıcıların cilt tiplerini analiz eden ve onlara kişiselleştirilmiş cilt bakım rutinleri ile ürün önerileri (Bioderma, CeraVe, La Roche-Posay vb.) sunan yapay zeka destekli bir platformdur. Google Gemini API kullanarak kullanıcı selfie'leri üzerinden görsel analiz yapar veya detaylı anketlerle cilt durumu (akne, nem, hassasiyet) tespiti sağlar. Ayrıca, kullanıcıların mevcut ürünlerinin içerik listelerini analiz ederek güvenli, dikkat edilmesi gereken veya zararlı maddeleri belirleyip cilde uygunluğunu raporlar.

## Kullanılan Teknolojiler
* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended
* **Yapay Zeka:** Google Generative AI (Gemini 1.5 Pro / Flash)
* **Veri Toplama:** BeautifulSoup4, Requests (Web Scraping)
* **Frontend:** Vanilla HTML/CSS/JS, Chart.js (Grafikler)
* **Veritabanı:** SQLite
* **Tasarım:** Özel CSS Design System (Glassmorphism, Değişkenler)

## Kurulum Adımları
1. **Sanal Ortam Oluşturma ve Aktifleştirme:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Bağımlılıkların Yüklenmesi:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment (.env) Dosyasını Oluşturma:**
   `backend` klasöründe bulunan `.env.example` dosyasını kopyalayarak `.env` olarak adlandırın veya yeni bir dosya oluşturup aşağıdaki değişkenleri doldurun:
   ```env
   SECRET_KEY=skinsense-gizli-anahtar
   JWT_SECRET_KEY=skinsense-jwt-anahtari
   DATABASE_URL=sqlite:///skinsense.db
   GEMINI_API_KEY=sizin_gemini_api_keyiniz
   # Opsiyonel - Şifre sıfırlama mailleri için:
   MAIL_USERNAME=test@gmail.com
   MAIL_PASSWORD=gmail_uygulama_sifresi
   ```
4. **Veritabanını Başlatma:**
   ```bash
   flask db init
   flask db upgrade
   ```
   *(Not: Uygulama `python app.py` ile ilk kez çalıştığında veritabanını ve varsayılan başlangıç ürünlerini otomatik olarak da oluşturur.)*

## Geliştirme Komutları

* **Geliştirme Sunucusunu Çalıştırma:**
  ```bash
  flask run --debug
  ```
  *(Alternatif olarak proje dizinindeki `start_backend.bat` dosyasını kullanabilirsiniz)*

* **Veritabanı Şeması Değişikliklerini Uygulama (Migration):**
  Modellerde bir değişiklik yaptıktan sonra:
  ```bash
  flask db migrate -m "degisiklik_aciklamasi"
  flask db upgrade
  ```

* **Testleri Çalıştırma:**
  ```bash
  pytest
  ```
