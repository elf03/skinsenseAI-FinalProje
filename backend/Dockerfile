FROM python:3.11-slim

WORKDIR /app

# Kurulum için gerekli sistem paketleri (Bcrypt vb. için)
RUN apt-get update && apt-get install -y build-essential gcc

# Python bağımlılıklarını kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm backend kodlarını kopyala
COPY . .

# Flask portunu aç
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "app.py"]
