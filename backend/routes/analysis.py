from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, db
from models.analysis import Analysis
from services.gemini_service import analyze_skin_photo, analyze_questionnaire
import os
import json
import base64
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@analysis_bp.route('/photo', methods=['POST'])
@jwt_required()
def analyze_photo():
    user_id = int(get_jwt_identity())
    
    if 'photo' not in request.files:
        # Base64 olarak da gelebilir
        data = request.get_json()
        if not data or 'photo_base64' not in data:
            return jsonify({'error': 'Fotoğraf gerekli.'}), 400
        
        image_data = base64.b64decode(data['photo_base64'].split(',')[-1])
    else:
        image_data = request.files['photo'].read()
    
    # Fotoğrafı kaydet
    photo_filename = f"{user_id}_{int(datetime.utcnow().timestamp())}.jpg"
    photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
    with open(photo_path, 'wb') as f:
        f.write(image_data)
    
    # Gemini analizi
    result = analyze_skin_photo(image_data)
    
    # Veritabanına kaydet
    analysis = Analysis(
        user_id=user_id,
        analysis_type='photo',
        photo_path=photo_path,
        skin_type=result.get('skin_type'),
        moisture_level=result.get('moisture_level'),
        acne_level=result.get('acne_level'),
        sensitivity=result.get('sensitivity'),
        blackheads=result.get('blackheads'),
        pores=result.get('pores'),
        oiliness=result.get('oiliness'),
        redness=result.get('redness'),
        dark_spots=result.get('dark_spots'),
        dark_circles=result.get('dark_circles'),
        tone_evenness=result.get('tone_evenness'),
        ai_comments=json.dumps(result.get('ai_comments', []), ensure_ascii=False),
        recommended_ingredients=json.dumps(result.get('recommended_ingredients', []), ensure_ascii=False),
        morning_routine=json.dumps(result.get('morning_routine', []), ensure_ascii=False),
        evening_routine=json.dumps(result.get('evening_routine', []), ensure_ascii=False),
        raw_response=json.dumps(result, ensure_ascii=False)
    )
    db.session.add(analysis)
    
    # Kullanıcının cilt tipini güncelle
    user = User.query.get(user_id)
    if user:
        user.skin_type = result.get('skin_type')
    
    db.session.commit()
    
    return jsonify({'analysis': analysis.to_dict()}), 201


@analysis_bp.route('/questionnaire', methods=['POST'])
@jwt_required()
def analyze_questionnaire_route():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    answers = data.get('answers', {})
    
    if not answers:
        return jsonify({'error': 'Anket yanıtları gerekli.'}), 400
    
    result = analyze_questionnaire(answers)
    
    analysis = Analysis(
        user_id=user_id,
        analysis_type='questionnaire',
        skin_type=result.get('skin_type'),
        moisture_level=result.get('moisture_level'),
        acne_level=result.get('acne_level'),
        sensitivity=result.get('sensitivity'),
        blackheads=result.get('blackheads'),
        pores=result.get('pores'),
        oiliness=result.get('oiliness'),
        redness=result.get('redness'),
        dark_spots=result.get('dark_spots'),
        dark_circles=result.get('dark_circles'),
        tone_evenness=result.get('tone_evenness'),
        ai_comments=json.dumps(result.get('ai_comments', []), ensure_ascii=False),
        recommended_ingredients=json.dumps(result.get('recommended_ingredients', []), ensure_ascii=False),
        morning_routine=json.dumps(result.get('morning_routine', []), ensure_ascii=False),
        evening_routine=json.dumps(result.get('evening_routine', []), ensure_ascii=False),
        raw_response=json.dumps(result, ensure_ascii=False)
    )
    db.session.add(analysis)
    
    user = User.query.get(user_id)
    if user:
        user.skin_type = result.get('skin_type')
    
    db.session.commit()
    
    return jsonify({'analysis': analysis.to_dict()}), 201


@analysis_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    pagination = Analysis.query.filter_by(user_id=user_id).order_by(Analysis.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'analyses': [a.to_dict() for a in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200


@analysis_bp.route('/latest', methods=['GET'])
@jwt_required()
def get_latest():
    user_id = int(get_jwt_identity())
    analysis = Analysis.query.filter_by(user_id=user_id).order_by(Analysis.created_at.desc()).first()
    if not analysis:
        return jsonify({'analysis': None}), 200
    return jsonify({'analysis': analysis.to_dict()}), 200


@analysis_bp.route('/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis(analysis_id):
    user_id = int(get_jwt_identity())
    analysis = Analysis.query.filter_by(id=analysis_id, user_id=user_id).first()
    if not analysis:
        return jsonify({'error': 'Analiz bulunamadı.'}), 404
    return jsonify({'analysis': analysis.to_dict()}), 200


@analysis_bp.route('/photo/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis_photo(analysis_id):
    user_id = int(get_jwt_identity())
    analysis = Analysis.query.filter_by(id=analysis_id, user_id=user_id).first()
    if not analysis or not analysis.photo_path:
        return jsonify({'error': 'Fotoğraf bulunamadı.'}), 404
    
    try:
        with open(analysis.photo_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        return jsonify({'photo': f'data:image/jpeg;base64,{img_data}'}), 200
    except Exception:
        return jsonify({'error': 'Fotoğraf okunamadı.'}), 500
