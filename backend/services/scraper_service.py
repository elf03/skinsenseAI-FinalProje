import requests
from bs4 import BeautifulSoup
import time
import random
from models.analysis import Product, db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
}


def _safe_get(url: str, timeout: int = 10) -> BeautifulSoup | None:
    try:
        time.sleep(random.uniform(1, 2))
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, 'lxml')
    except Exception as e:
        logger.error(f"Request hatası ({url}): {e}")
    return None


def scrape_bioderma() -> list[dict]:
    """Bioderma Türkiye ürünlerini çek."""
    products = []
    base_url = "https://www.bioderma.com.tr"
    
    categories = [
        ("/cilt-bakimi/yuz-temizleme", "cleanser"),
        ("/cilt-bakimi/nemlendirici", "moisturizer"),
        ("/gunes/gunes-kremleri", "sunscreen"),
    ]
    
    for path, category in categories:
        try:
            soup = _safe_get(base_url + path)
            if not soup:
                continue
            
            product_cards = soup.select('.product-item, .product-card, [class*="product"]')[:10]
            
            for card in product_cards:
                try:
                    name_el = card.select_one('h2, h3, .product-name, [class*="name"]')
                    price_el = card.select_one('.price, [class*="price"]')
                    img_el = card.select_one('img')
                    link_el = card.select_one('a')
                    
                    if not name_el:
                        continue
                    
                    name = name_el.get_text(strip=True)
                    if not name or len(name) < 3:
                        continue
                    
                    products.append({
                        'brand': 'Bioderma',
                        'name': name,
                        'category': category,
                        'price': price_el.get_text(strip=True) if price_el else None,
                        'image_url': img_el.get('src') or img_el.get('data-src') if img_el else None,
                        'product_url': base_url + link_el.get('href') if link_el and link_el.get('href', '').startswith('/') else (link_el.get('href') if link_el else None),
                        'skin_types': 'Normal,Karma,Yağlı,Kuru,Hassas',
                        'concerns': category
                    })
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"Bioderma scraping hatası: {e}")
    
    return products


def scrape_cerave() -> list[dict]:
    """CeraVe Türkiye ürünlerini çek."""
    products = []
    base_url = "https://www.cerave.com.tr"
    
    categories = [
        ("/temizleyiciler", "cleanser"),
        ("/nemlendirici-kremler", "moisturizer"),
        ("/gunes-kremleri", "sunscreen"),
    ]
    
    for path, category in categories:
        try:
            soup = _safe_get(base_url + path)
            if not soup:
                continue
            
            product_cards = soup.select('.product-item, [class*="product-card"]')[:10]
            
            for card in product_cards:
                try:
                    name_el = card.select_one('h2, h3, .product-name, [class*="title"]')
                    price_el = card.select_one('.price, [class*="price"]')
                    img_el = card.select_one('img')
                    link_el = card.select_one('a')
                    
                    if not name_el:
                        continue
                    
                    name = name_el.get_text(strip=True)
                    if not name or len(name) < 3:
                        continue
                    
                    products.append({
                        'brand': 'CeraVe',
                        'name': name,
                        'category': category,
                        'price': price_el.get_text(strip=True) if price_el else None,
                        'image_url': img_el.get('src') or img_el.get('data-src') if img_el else None,
                        'product_url': base_url + link_el.get('href') if link_el and link_el.get('href', '').startswith('/') else (link_el.get('href') if link_el else None),
                        'skin_types': 'Normal,Karma,Kuru,Hassas',
                        'concerns': category
                    })
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"CeraVe scraping hatası: {e}")
    
    return products


def load_fallback_products() -> list[dict]:
    """Scraping başarısız olursa statik ürün veritabanı kullan."""
    return [
        # BIODERMA
        {"brand": "Bioderma", "name": "Sébium Foaming Gel", "category": "cleanser", "price": "245 TL",
         "image_url": "https://www.bioderma.com.tr/sites/default/files/styles/product_page/public/product_images/sebium-gel-moussant.png",
         "product_url": "https://www.bioderma.com.tr", "skin_types": "Yağlı,Karma", "concerns": "akne,gözenek,yağlanma"},
        {"brand": "Bioderma", "name": "Hydrabio Légère Crème", "category": "moisturizer", "price": "380 TL",
         "image_url": "https://www.bioderma.com.tr/sites/default/files/styles/product_page/public/product_images/hydrabio-creme-legere.png",
         "product_url": "https://www.bioderma.com.tr", "skin_types": "Normal,Karma,Kuru", "concerns": "nem,kuruluk"},
        {"brand": "Bioderma", "name": "Photoderm MAX SPF 50+", "category": "sunscreen", "price": "450 TL",
         "image_url": "https://www.bioderma.com.tr/sites/default/files/styles/product_page/public/product_images/photoderm-max-spf50.png",
         "product_url": "https://www.bioderma.com.tr", "skin_types": "Normal,Karma,Yağlı,Kuru,Hassas", "concerns": "güneş koruması"},
        {"brand": "Bioderma", "name": "Sensibio H2O Micellar Water", "category": "cleanser", "price": "320 TL",
         "image_url": "https://www.bioderma.com.tr/sites/default/files/styles/product_page/public/product_images/sensibio-h2o.png",
         "product_url": "https://www.bioderma.com.tr", "skin_types": "Hassas,Normal,Karma", "concerns": "makyaj temizleme,hassasiyet"},
        {"brand": "Bioderma", "name": "Pigmentbio Daily Care SPF 50+", "category": "sunscreen", "price": "520 TL",
         "image_url": "https://www.bioderma.com.tr/sites/default/files/styles/product_page/public/product_images/pigmentbio-daily-care.png",
         "product_url": "https://www.bioderma.com.tr", "skin_types": "Normal,Karma,Kuru", "concerns": "leke,güneş koruması"},
        {"brand": "Bioderma", "name": "Atoderm Intensive Baume", "category": "moisturizer", "price": "410 TL",
         "image_url": "https://www.bioderma.com.tr/sites/default/files/styles/product_page/public/product_images/atoderm-intensive-baume.png",
         "product_url": "https://www.bioderma.com.tr", "skin_types": "Kuru,Hassas", "concerns": "nem,kuruluk,hassasiyet"},
        
        # CERAVE
        {"brand": "CeraVe", "name": "Foaming Facial Cleanser", "category": "cleanser", "price": "290 TL",
         "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/foaming-facial-cleanser/700x875/cerave_foamingfacialcleanser_16oz_front-700x875-us.jpg",
         "product_url": "https://www.cerave.com.tr", "skin_types": "Normal,Yağlı,Karma", "concerns": "temizlik,gözenek,yağlanma"},
        {"brand": "CeraVe", "name": "Moisturizing Cream", "category": "moisturizer", "price": "350 TL",
         "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/moisturizing-cream/700x875/cerave_moisturizingcream_front-700x875-us.jpg",
         "product_url": "https://www.cerave.com.tr", "skin_types": "Kuru,Normal,Hassas", "concerns": "nem,kuruluk"},
        {"brand": "CeraVe", "name": "Hydrating Facial Cleanser", "category": "cleanser", "price": "275 TL",
         "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/hydrating-facial-cleanser/700x875/cerave_hydratingfacialcleanser_front-700x875-us.jpg",
         "product_url": "https://www.cerave.com.tr", "skin_types": "Kuru,Normal,Hassas", "concerns": "nem,hassasiyet"},
        {"brand": "CeraVe", "name": "AM Facial Moisturizing Lotion SPF 30", "category": "sunscreen", "price": "395 TL",
         "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/am-facial-moisturizing-lotion-spf-30/700x875/cerave_amfacialmoisturizinglotion_front-700x875-us.jpg",
         "product_url": "https://www.cerave.com.tr", "skin_types": "Normal,Karma,Yağlı", "concerns": "güneş koruması,nem"},
        {"brand": "CeraVe", "name": "Resurfacing Retinol Serum", "category": "serum", "price": "480 TL",
         "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/resurfacing-retinol-serum/700x875/cerave_resurfacingretinolserum_front-700x875-us.jpg",
         "product_url": "https://www.cerave.com.tr", "skin_types": "Normal,Karma,Yağlı", "concerns": "leke,gözenek,yaşlanma"},
        {"brand": "CeraVe", "name": "SA Smoothing Cream", "category": "moisturizer", "price": "340 TL",
         "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/sa-smoothing-cream/700x875/cerave_sasmoothing_cream_front-700x875-us.jpg",
         "product_url": "https://www.cerave.com.tr", "skin_types": "Kuru,Normal", "concerns": "peeling,kuruluk"},
        
        # LA ROCHE-POSAY
        {"brand": "La Roche-Posay", "name": "Effaclar Gel Moussant", "category": "cleanser", "price": "310 TL",
         "image_url": "https://www.laroche-posay.com.tr/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-lrp-master-catalog/default/product_images/large/3337875545365.jpg",
         "product_url": "https://www.laroche-posay.com.tr", "skin_types": "Yağlı,Karma", "concerns": "akne,yağlanma,gözenek"},
        {"brand": "La Roche-Posay", "name": "Effaclar DUO(+)", "category": "moisturizer", "price": "520 TL",
         "image_url": "https://www.laroche-posay.com.tr/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-lrp-master-catalog/default/product_images/large/3337875545372.jpg",
         "product_url": "https://www.laroche-posay.com.tr", "skin_types": "Yağlı,Karma", "concerns": "akne,sivilce,yağlanma"},
        {"brand": "La Roche-Posay", "name": "Anthelios UV Mune 400 SPF50+", "category": "sunscreen", "price": "580 TL",
         "image_url": "https://www.laroche-posay.com.tr/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-lrp-master-catalog/default/product_images/large/3337875796962.jpg",
         "product_url": "https://www.laroche-posay.com.tr", "skin_types": "Normal,Karma,Yağlı,Kuru,Hassas", "concerns": "güneş koruması"},
        {"brand": "La Roche-Posay", "name": "Toleriane Hydrating Gentle Cleanser", "category": "cleanser", "price": "295 TL",
         "image_url": "https://www.laroche-posay.com.tr/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-lrp-master-catalog/default/product_images/large/3337872413652.jpg",
         "product_url": "https://www.laroche-posay.com.tr", "skin_types": "Hassas,Kuru,Normal", "concerns": "hassasiyet,nem"},
        {"brand": "La Roche-Posay", "name": "Mela B3 Serum", "category": "serum", "price": "650 TL",
         "image_url": "https://www.laroche-posay.com.tr/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-lrp-master-catalog/default/product_images/large/3337875797693.jpg",
         "product_url": "https://www.laroche-posay.com.tr", "skin_types": "Normal,Karma,Kuru,Yağlı", "concerns": "leke,cilt tonu eşitsizliği"},
        {"brand": "La Roche-Posay", "name": "Cicaplast Baume B5+", "category": "moisturizer", "price": "440 TL",
         "image_url": "https://www.laroche-posay.com.tr/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-lrp-master-catalog/default/product_images/large/3337875796887.jpg",
         "product_url": "https://www.laroche-posay.com.tr", "skin_types": "Hassas,Kuru,Normal", "concerns": "hassasiyet,onarım,kızarıklık"},
    ]


def sync_products_to_db():
    """Ürünleri veritabanına kaydet (scraping veya fallback)."""
    # Önce scraping dene
    products = []
    
    try:
        products += scrape_bioderma()
        logger.info(f"Bioderma: {len(products)} ürün scraped")
    except Exception as e:
        logger.error(f"Bioderma scraping başarısız: {e}")
    
    try:
        cerave_products = scrape_cerave()
        products += cerave_products
        logger.info(f"CeraVe: {len(cerave_products)} ürün scraped")
    except Exception as e:
        logger.error(f"CeraVe scraping başarısız: {e}")
    
    # Scraping yeterli ürün getirmediyse fallback kullan
    if len(products) < 5:
        logger.info("Scraping yetersiz, fallback ürün veritabanı kullanılıyor")
        products = load_fallback_products()
    
    # DB'ye kaydet
    saved = 0
    for p in products:
        try:
            existing = Product.query.filter_by(brand=p['brand'], name=p['name']).first()
            if existing:
                for key, val in p.items():
                    setattr(existing, key, val)
                existing.scraped_at = datetime.utcnow()
            else:
                product = Product(**p)
                db.session.add(product)
            saved += 1
        except Exception as e:
            logger.error(f"Ürün kaydı hatası: {e}")
    
    db.session.commit()
    logger.info(f"{saved} ürün veritabanına kaydedildi")
    return saved


def get_recommended_products(skin_type: str = None, concerns: list = None, category: str = None) -> list:
    """Cilt tipine ve sorunlarına göre ürün öner."""
    query = Product.query
    
    if skin_type:
        query = query.filter(Product.skin_types.like(f'%{skin_type}%'))
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.all()
    
    if concerns:
        scored = []
        for p in products:
            score = 0
            p_concerns = (p.concerns or '').lower()
            for concern in concerns:
                if concern.lower() in p_concerns:
                    score += 1
            scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        products = [p for _, p in scored]
    
    return [p.to_dict() for p in products[:12]]
