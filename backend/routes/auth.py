from models.user import User, db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
import random
import string
from datetime import datetime, timedelta
from services.email_service import send_otp_email

import os
import time

auth_bp = Blueprint('auth', __name__)

UPLOAD_AVATAR_FOLDER = 'uploads/avatars'
os.makedirs(UPLOAD_AVATAR_FOLDER, exist_ok=True)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name or not email or not password:
        return jsonify({'error': 'Tüm alanlar zorunludur.', 'error_en': 'All fields are required.'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Şifre en az 6 karakter olmalıdır.', 'error_en': 'Password must be at least 6 characters.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Bu email zaten kayıtlı.', 'error_en': 'Email already registered.'}), 409

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(name=name, email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Email veya şifre hatalı.', 'error_en': 'Invalid email or password.'}), 401

    user.last_login = datetime.utcnow()
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    user = User.query.filter_by(email=email).first()
    if not user:
        # Güvenlik için kullanıcı bulunamasa da başarılı mesaj dön
        return jsonify({'message': 'OTP kodu gönderildi.', 'message_en': 'OTP code sent if email exists.'}), 200

    otp = ''.join(random.choices(string.digits, k=6))
    user.otp_code = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    # Email gönder (email servisi yoksa console'a yaz)
    sent = send_otp_email(user.email, user.name, otp)
    
    response = {'message': 'OTP kodu email adresinize gönderildi.', 'message_en': 'OTP code sent to your email.'}
    if not sent:
        # Geliştirme modunda kodu direkt dön
        response['dev_otp'] = otp
    
    return jsonify(response), 200


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Kullanıcı bulunamadı.', 'error_en': 'User not found.'}), 404

    if not user.otp_code or user.otp_code != otp:
        return jsonify({'error': 'Geçersiz OTP kodu.', 'error_en': 'Invalid OTP code.'}), 400

    if datetime.utcnow() > user.otp_expires_at:
        return jsonify({'error': 'OTP süresi doldu.', 'error_en': 'OTP code expired.'}), 400

    # OTP temizle
    user.otp_code = None
    user.otp_expires_at = None
    user.last_login = datetime.utcnow()
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    new_password = data.get('password', '')

    if len(new_password) < 6:
        return jsonify({'error': 'Şifre en az 6 karakter olmalıdır.'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Kullanıcı bulunamadı.'}), 404

    user.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Şifre başarıyla güncellendi.'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Kullanıcı bulunamadı.'}), 404
    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name'].strip()
    if 'preferred_language' in data:
        user.preferred_language = data['preferred_language']
    
    
    db.session.commit()
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/upload-avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    user_id = int(get_jwt_identity())
    
    if 'avatar' not in request.files:
        return jsonify({'error': 'Fotoğraf yüklenmedi.'}), 400
        
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi.'}), 400
        
    if file:
        ext = file.filename.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            return jsonify({'error': 'Sadece resim formatları desteklenir.'}), 400
            
        filename = f"avatar_{user_id}_{int(time.time())}.{ext}"
        filepath = os.path.join(UPLOAD_AVATAR_FOLDER, filename)
        file.save(filepath)
        
        user = User.query.get(user_id)
        # /uploads/avatars/<filename> URL path
        user.avatar = f"/uploads/avatars/{filename}"
        db.session.commit()
        
        return jsonify({'message': 'Avatar başarıyla güncellendi.', 'avatar_url': user.avatar, 'user': user.to_dict()}), 200
