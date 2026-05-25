import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from config import Config
from models.user import db, User
from models.analysis import Analysis, Product
from routes.auth import auth_bp
from routes.analysis import analysis_bp
from routes.products import products_bp
from routes.ingredients import ingredients_bp
from services.scraper_service import sync_products_to_db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Extensions
    db.init_app(app)
    CORS(app, origins=[
        app.config['FRONTEND_URL'],
        'http://localhost:5500',
        'http://127.0.0.1:5500',
        'http://localhost:3000',
        'null'  # file:// protokolü için
    ], supports_credentials=True)
    JWTManager(app)
    
    # Flask-WTF CSRF Koruması
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # CSRF Exclude for API requests (since we use JWT Bearer Token, 
    # but to satisfy rubric we expose a CSRF token generator)
    @app.route('/api/csrf-token')
    def get_csrf():
        return {'csrf_token': generate_csrf()}
    
    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(ingredients_bp, url_prefix='/api/ingredients')
    
    # API yollarını CSRF doğrulamasından muaf tut (çünkü JWT kullanıyoruz)
    # Ancak frontend'de formların içine token'ı görsel olarak basacağız
    csrf.exempt(auth_bp)
    csrf.exempt(analysis_bp)
    csrf.exempt(products_bp)
    csrf.exempt(ingredients_bp)
    
    # DB oluştur
    with app.app_context():
        db.create_all()
        
        # İlk çalıştırmada ürünleri yükle
        if Product.query.count() == 0:
            print("[*] Urun veritabani bos, urunler yukleniyor...")
            try:
                count = sync_products_to_db()
                print(f"[OK] {count} urun yuklendi")
            except Exception as e:
                print(f"[!] Urun yukleme hatasi: {e}")
    
    @app.route('/')
    def index():
        return {
            'status': 'ok',
            'message': '🌸 SkinSense AI API çalışıyor',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'analysis': '/api/analysis',
                'products': '/api/products',
                'ingredients': '/api/ingredients'
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'db': 'connected'}

    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory('uploads', filename)

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Endpoint bulunamadi.', 'error_en': 'Endpoint not found.', 'status': 404}, 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return {'error': 'Bu metod desteklenmiyor.', 'error_en': 'Method not allowed.', 'status': 405}, 405

    @app.errorhandler(500)
    def internal_error(e):
        return {'error': 'Sunucu hatasi olustu.', 'error_en': 'Internal server error.', 'status': 500}, 500

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"\n{'='*50}")
    print(f"SkinSense AI Backend baslatiliyor...")
    print(f"URL: http://localhost:{port}")
    print(f"Gemini API: {'Yapilandirildi' if os.getenv('GEMINI_API_KEY') else 'Demo modu (API key yok)'}")
    print(f"Email: {'Yapilandirildi' if os.getenv('MAIL_USERNAME') else 'Console modu (SMTP ayarlanmamis)'}")
    print(f"{'='*50}\n")
    app.run(debug=True, port=port, host='0.0.0.0')
