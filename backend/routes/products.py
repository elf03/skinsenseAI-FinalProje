from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.analysis import Product
from services.scraper_service import get_recommended_products, sync_products_to_db
from models.user import User

products_bp = Blueprint('products', __name__)


@products_bp.route('/recommend', methods=['GET'])
def recommend():
    skin_type = request.args.get('skin_type')
    concerns_str = request.args.get('concerns', '')
    category = request.args.get('category')
    
    concerns = [c.strip() for c in concerns_str.split(',') if c.strip()] if concerns_str else []
    
    # JWT opsiyonel - giriş yapılmışsa kullanıcının cilt tipini kullan
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id and not skin_type:
            user = User.query.get(int(user_id))
            if user and user.skin_type:
                skin_type = user.skin_type
    except Exception:
        pass
    
    products = get_recommended_products(skin_type=skin_type, concerns=concerns, category=category)
    
    # Ürün yoksa fallback yükle
    if not products:
        sync_products_to_db()
        products = get_recommended_products(skin_type=skin_type, concerns=concerns, category=category)
    
    return jsonify({'products': products, 'skin_type': skin_type, 'count': len(products)}), 200


@products_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if not q:
        return jsonify({'products': [], 'total': 0, 'pages': 0}), 200
    
    pagination = Product.query.filter(
        (Product.name.like(f'%{q}%')) | 
        (Product.brand.like(f'%{q}%')) |
        (Product.description.like(f'%{q}%'))
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200


@products_bp.route('/sync', methods=['POST'])
@jwt_required()
def sync():
    """Admin: Ürünleri yeniden scrape et."""
    count = sync_products_to_db()
    return jsonify({'message': f'{count} ürün senkronize edildi.'}), 200


@products_bp.route('/brands', methods=['GET'])
def get_brands():
    brands = db.session.query(Product.brand).distinct().all()
    return jsonify({'brands': [b[0] for b in brands]}), 200


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': [
        {'id': 'cleanser', 'name_tr': 'Temizleyici', 'name_en': 'Cleanser', 'icon': '🧼'},
        {'id': 'serum', 'name_tr': 'Serum', 'name_en': 'Serum', 'icon': '✨'},
        {'id': 'moisturizer', 'name_tr': 'Nemlendirici', 'name_en': 'Moisturizer', 'icon': '💧'},
        {'id': 'sunscreen', 'name_tr': 'Güneş Kremi', 'name_en': 'Sunscreen', 'icon': '☀️'},
        {'id': 'toner', 'name_tr': 'Tonik', 'name_en': 'Toner', 'icon': '💦'},
        {'id': 'eye_cream', 'name_tr': 'Göz Kremi', 'name_en': 'Eye Cream', 'icon': '👁️'},
    ]}), 200


from models.analysis import db
