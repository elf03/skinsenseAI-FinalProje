# SkinSense AI — Proje Notları

## Hızlı Başlangıç

### 1. Backend'i Başlat
```
start_backend.bat dosyasına çift tıklayın
VEYA:
cd backend
python app.py
```

### 2. Frontend'i Aç
`frontend/index.html` dosyasını tarayıcınızda açın.
**VS Code kullanıyorsanız**: Live Server ile açın (http://127.0.0.1:5500)

---

## API Adresi
http://localhost:5000

## Gemini API Anahtarı
1. https://aistudio.google.com adresine gidin
2. "Get API Key" butonuna tıklayın
3. `backend/.env` dosyasında `GEMINI_API_KEY=` satırına yapıştırın
4. Backend'i yeniden başlatın

**API anahtarı olmadan**: Demo modu çalışır, mock veriler kullanılır.

## Email Ayarları (Opsiyonel)
Şifre sıfırlama kodu gerçek email göndermek için:
1. Gmail hesabınızda "App Password" oluşturun
2. `backend/.env` dosyasına doldurun
3. **Yoksa**: OTP kodu backend console'una yazdırılır

---

## Sayfalar
| Sayfa | Açıklama |
|-------|----------|
| index.html | Ana sayfa |
| auth.html | Giriş / Kayıt |
| analysis.html | Cilt analizi |
| results.html | Analiz sonuçları |
| dashboard.html | Kullanıcı paneli |
| history.html | Geçmiş + karşılaştırma |
| ingredient-check.html | İçerik analizi |
