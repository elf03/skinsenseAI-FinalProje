from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from services.gemini_service import analyze_ingredients
from models.user import User

ingredients_bp = Blueprint('ingredients', __name__)


@ingredients_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_name = data.get('product_name', 'Bilinmeyen Ürün')
    ingredients_text = data.get('ingredients', '').strip()
    
    if not ingredients_text:
        return jsonify({'error': 'İçerik listesi gerekli.'}), 400
    
    # Kullanıcının cilt tipini al (opsiyonel)
    skin_type = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            user = User.query.get(int(user_id))
            if user:
                skin_type = user.skin_type
    except Exception:
        pass
    
    result = analyze_ingredients(product_name, ingredients_text, skin_type)
    return jsonify({'analysis': result}), 200


@ingredients_bp.route('/check-ingredient', methods=['POST'])
def check_single():
    """Tek bir içeriği hızlıca kontrol et."""
    data = request.get_json()
    ingredient = data.get('ingredient', '').strip()
    
    if not ingredient:
        return jsonify({'error': 'İçerik adı gerekli.'}), 400
    
    # Bilinen zararlı içerikler listesi
    harmful = ['sodium lauryl sulfate', 'parabens', 'formaldehyde', 'triclosan', 
                'oxybenzone', 'petrolatum', 'butylated hydroxyanisole']
    caution = ['fragrance', 'parfum', 'alcohol denat', 'methylisothiazolinone',
                'cocamidopropyl betaine', 'propylene glycol']
    
    ing_lower = ingredient.lower()
    
    status = 'safe'
    message_tr = 'Bu içerik genel olarak güvenli kabul edilmektedir.'
    message_en = 'This ingredient is generally considered safe.'
    
    for h in harmful:
        if h in ing_lower:
            status = 'harmful'
            message_tr = 'Bu içerik potansiyel olarak zararlı olabilir. Dikkatli kullanın.'
            message_en = 'This ingredient may be potentially harmful. Use with caution.'
            break
    
    if status == 'safe':
        for c in caution:
            if c in ing_lower:
                status = 'caution'
                message_tr = 'Bu içerik hassas ciltlerde iritan olabilir.'
                message_en = 'This ingredient may be irritating for sensitive skin.'
                break
    
    return jsonify({'ingredient': ingredient, 'status': status, 
                    'message_tr': message_tr, 'message_en': message_en}), 200
