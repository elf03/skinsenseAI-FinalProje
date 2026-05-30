import google.generativeai as genai
import os
import json
import base64
from PIL import Image
import io

def configure_gemini():
    api_key = os.getenv('GEMINI_API_KEY', '')
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False


def analyze_skin_photo(image_data: bytes) -> dict:
    """Selfie fotoğrafını Gemini Vision ile analiz et."""
    if not configure_gemini():
        return _mock_analysis_result()
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        img = Image.open(io.BytesIO(image_data))
        
        prompt = """Sen bir uzman dermatoloji AI asistanısın. Bu selfie fotoğrafını analiz et ve aşağıdaki formatta JSON döndür.
        
Lütfen yalnızca JSON döndür, başka metin ekleme:

{
  "skin_type": "Normal|Yağlı|Kuru|Karma|Hassas",
  "moisture_level": 0-100,
  "acne_level": "Yok|Hafif|Orta|Yüksek",
  "sensitivity": "Düşük|Orta|Yüksek",
  "blackheads": "Yok|Az|Orta|Çok",
  "pores": "Küçük|Orta|Büyük",
  "oiliness": "Kuru|Normal|Hafif Yağlı|Yağlı",
  "redness": "Yok|Hafif|Orta|Yüksek",
  "dark_spots": "Yok|Az|Orta|Çok",
  "dark_circles": "Yok|Hafif|Belirgin",
  "tone_evenness": "Eşit|Hafif Eşitsiz|Eşitsiz",
  "ai_comments": [
    "Kişisel yorum 1 (Türkçe, samimi ve bilgilendirici)",
    "Kişisel yorum 2",
    "Kişisel yorum 3"
  ],
  "recommended_ingredients": [
    {"name": "İçerik adı", "benefit": "Faydası", "icon": "💧"},
    ...
  ],
  "morning_routine": [
    {"step": 1, "product_type": "Temizleyici", "recommendation": "Nazik köpük temizleyici", "reason": "Neden?", "icon": "🧼"},
    ...
  ],
  "evening_routine": [
    {"step": 1, "product_type": "Çift Temizleme", "recommendation": "Misellar su + Temizleyici", "reason": "Neden?", "icon": "🌙"},
    ...
  ]
}

Analiz yaparken dikkatli ol ve fotoğrafta görüneni gerçekçi şekilde değerlendir. AI yorumları için kişisel, motivasyonu artıran cümleler yaz örneğin: "Cildin bugün biraz yorgun görünüyor, daha fazla su içmeyi dene!" gibi."""

        response = model.generate_content([prompt, img])
        
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()
        
        result = json.loads(text)
        return result
        
    except Exception as e:
        print(f"Gemini fotoğraf analizi hatası: {e}")
        return _mock_analysis_result()


def analyze_questionnaire(answers: dict) -> dict:
    """Questionnaire yanıtlarından cilt analizi yap."""
    if not configure_gemini():
        return _mock_analysis_result()
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Sen bir uzman dermatoloji AI asistanısın. Kullanıcının cilt anketi yanıtlarına göre analiz yap.

Anket yanıtları:
{json.dumps(answers, ensure_ascii=False, indent=2)}

Aşağıdaki formatta yalnızca JSON döndür:

{{
  "skin_type": "Normal|Yağlı|Kuru|Karma|Hassas",
  "moisture_level": 0-100,
  "acne_level": "Yok|Hafif|Orta|Yüksek",
  "sensitivity": "Düşük|Orta|Yüksek",
  "blackheads": "Yok|Az|Orta|Çok",
  "pores": "Küçük|Orta|Büyük",
  "oiliness": "Kuru|Normal|Hafif Yağlı|Yağlı",
  "redness": "Yok|Hafif|Orta|Yüksek",
  "dark_spots": "Yok|Az|Orta|Çok",
  "dark_circles": "Yok|Hafif|Belirgin",
  "tone_evenness": "Eşit|Hafif Eşitsiz|Eşitsiz",
  "ai_comments": [
    "Kişisel yorum 1 (Türkçe, samimi ve pratik önerileri içeren)",
    "Kişisel yorum 2",
    "Kişisel yorum 3"
  ],
  "recommended_ingredients": [
    {{"name": "İçerik adı", "benefit": "Faydası", "icon": "💧"}},
    ...
  ],
  "morning_routine": [
    {{"step": 1, "product_type": "Temizleyici", "recommendation": "Örnek ürün tipi", "reason": "Neden?", "icon": "🧼"}},
    ...
  ],
  "evening_routine": [
    {{"step": 1, "product_type": "Çift Temizleme", "recommendation": "Misellar su + Temizleyici", "reason": "Neden?", "icon": "🌙"}},
    ...
  ]
}}"""

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()
        
        result = json.loads(text)
        return result
        
    except Exception as e:
        print(f"Gemini questionnaire analizi hatası: {e}")
        return _mock_analysis_result()


def analyze_ingredients(product_name: str, ingredients_text: str, skin_type: str = None) -> dict:
    """Ürün içeriklerini analiz et."""
    if not configure_gemini():
        return _mock_ingredient_result(product_name)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        skin_context = f"Kullanıcının cilt tipi: {skin_type}" if skin_type else ""
        
        prompt = f"""Sen bir kozmetik kimyacısı ve dermatoloji uzmanısın. Aşağıdaki ürün içeriklerini analiz et.

Ürün: {product_name}
{skin_context}
İçerikler: {ingredients_text}

Aşağıdaki formatta yalnızca JSON döndür:

{{
  "overall_score": 0-100,
  "overall_verdict": "Temiz|Dikkatli Kullan|Sorunlu",
  "summary": "Genel özet (2-3 cümle)",
  "safe_ingredients": [
    {{"name": "İçerik", "benefit": "Faydası", "icon": "✅"}}
  ],
  "caution_ingredients": [
    {{"name": "İçerik", "concern": "Dikkat noktası", "icon": "⚠️"}}
  ],
  "harmful_ingredients": [
    {{"name": "İçerik", "reason": "Neden zararlı", "icon": "❌"}}
  ],
  "skin_compatibility": "Bu ürün {skin_type if skin_type else 'genel'} cilt tipi için uyumlu mu? Açıkla.",
  "recommendation": "Kullanmalı mıyım? Kesin öneri ver."
}}"""

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()
        
        return json.loads(text)
        
    except Exception as e:
        print(f"Gemini içerik analizi hatası: {e}")
        return _mock_ingredient_result(product_name)


def _mock_analysis_result() -> dict:
    """Gemini API yoksa demo sonuç döner."""
    return {
        "skin_type": "Karma",
        "moisture_level": 62,
        "acne_level": "Hafif",
        "sensitivity": "Orta",
        "blackheads": "Az",
        "pores": "Orta",
        "oiliness": "Hafif Yağlı",
        "redness": "Hafif",
        "dark_spots": "Az",
        "dark_circles": "Hafif",
        "tone_evenness": "Hafif Eşitsiz",
        "ai_comments": [
            "🌟 Cildin genel olarak sağlıklı görünüyor! T-bölgeni biraz daha özenle temizle.",
            "💧 Nem seviyeni artırmak için gün içinde daha fazla su içmeyi dene — cildin teşekkür edecek!",
            "🌙 Uyku düzenin cildini doğrudan etkiliyor. 7-8 saat uyku, en iyi cilt bakım ürününden daha etkili!"
        ],
        "recommended_ingredients": [
            {"name": "Niasinamid", "benefit": "Gözenek küçültür, yağ dengesini sağlar", "icon": "⚗️"},
            {"name": "Hyaluronik Asit", "benefit": "Derin nem sağlar, cilt bariyerini güçlendirir", "icon": "💧"},
            {"name": "Salisilik Asit", "benefit": "Gözenekleri temizler, akneyi önler", "icon": "🔬"},
            {"name": "C Vitamini", "benefit": "Leke açar, cilt tonunu eşitler", "icon": "✨"},
            {"name": "Çay Ağacı Yağı", "benefit": "Antibakteriyel, akne karşıtı", "icon": "🌿"}
        ],
        "morning_routine": [
            {"step": 1, "product_type": "Temizleyici", "recommendation": "Nazik köpük temizleyici", "reason": "Geceyi geçiren bakterileri temizler", "icon": "🧼"},
            {"step": 2, "product_type": "Tonik", "recommendation": "Niasinamid tonik", "reason": "Gözenekleri sıkılaştırır", "icon": "💦"},
            {"step": 3, "product_type": "Serum", "recommendation": "C Vitamini Serum", "reason": "Leke açar, antioksidan koruma sağlar", "icon": "✨"},
            {"step": 4, "product_type": "Nemlendirici", "recommendation": "Hafif jel nemlendirici", "reason": "Yağlanmadan nem dengesi sağlar", "icon": "🫧"},
            {"step": 5, "product_type": "Güneş Kremi", "recommendation": "SPF 50+ hafif formül", "reason": "UV hasarından ve lekelerden korur", "icon": "☀️"}
        ],
        "evening_routine": [
            {"step": 1, "product_type": "Çift Temizleme", "recommendation": "Misellar su + Temizleyici", "reason": "Makyaj ve güneş kremini tam temizler", "icon": "🌙"},
            {"step": 2, "product_type": "Tonik", "recommendation": "BHA tonik (haftada 2-3 kez)", "reason": "Gözenek temizliği sağlar", "icon": "💦"},
            {"step": 3, "product_type": "Tedavi Serumu", "recommendation": "Niasinamid veya Retinol", "reason": "Hücre yenilenmesini hızlandırır", "icon": "🔬"},
            {"step": 4, "product_type": "Göz Kremi", "recommendation": "Kafein içerikli göz kremi", "reason": "Göz altı morluklarını azaltır", "icon": "👁️"},
            {"step": 5, "product_type": "Gece Kremi", "recommendation": "Besleyici nemlendirici", "reason": "Uyku sırasında cilt onarımını destekler", "icon": "🌛"}
        ]
    }


def _mock_ingredient_result(product_name: str) -> dict:
    """Demo içerik analiz sonucu."""
    return {
        "overall_score": 78,
        "overall_verdict": "Dikkatli Kullan",
        "summary": f"'{product_name}' genel olarak güvenli bir formüle sahip. Birkaç dikkat edilmesi gereken içerik mevcut ancak çoğu kişi için sorun yaratmaz.",
        "safe_ingredients": [
            {"name": "Hyaluronic Acid", "benefit": "Nem sağlar", "icon": "✅"},
            {"name": "Glycerin", "benefit": "Nemlendirici, cilde dost", "icon": "✅"},
            {"name": "Niacinamide", "benefit": "Gözenek küçültür, aydınlatır", "icon": "✅"}
        ],
        "caution_ingredients": [
            {"name": "Parfum/Fragrance", "concern": "Hassas ciltlerde iritan olabilir", "icon": "⚠️"}
        ],
        "harmful_ingredients": [],
        "skin_compatibility": "Karma cilt tipi için genel olarak uyumlu. Hassas bölgelerinizde dikkatli kullanın.",
        "recommendation": "Kullanabilirsiniz, ancak parfüm içerdiği için hassas cildiniz varsa yüz bölgesinde patch test yapın."
    }
