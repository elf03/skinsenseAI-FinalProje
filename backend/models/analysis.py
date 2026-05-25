from .user import db
from datetime import datetime
import json

class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    analysis_type = db.Column(db.String(20), nullable=False)  # 'photo' or 'questionnaire'
    photo_path = db.Column(db.String(255), nullable=True)
    
    skin_type = db.Column(db.String(50), nullable=True)
    moisture_level = db.Column(db.Integer, nullable=True)
    acne_level = db.Column(db.String(20), nullable=True)
    sensitivity = db.Column(db.String(20), nullable=True)
    blackheads = db.Column(db.String(20), nullable=True)
    pores = db.Column(db.String(20), nullable=True)
    oiliness = db.Column(db.String(20), nullable=True)
    redness = db.Column(db.String(20), nullable=True)
    dark_spots = db.Column(db.String(20), nullable=True)
    dark_circles = db.Column(db.String(20), nullable=True)
    tone_evenness = db.Column(db.String(20), nullable=True)
    
    ai_comments = db.Column(db.Text, nullable=True)
    recommended_ingredients = db.Column(db.Text, nullable=True)
    morning_routine = db.Column(db.Text, nullable=True)
    evening_routine = db.Column(db.Text, nullable=True)
    
    raw_response = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_type': self.analysis_type,
            'photo_path': self.photo_path,
            'skin_type': self.skin_type,
            'moisture_level': self.moisture_level,
            'acne_level': self.acne_level,
            'sensitivity': self.sensitivity,
            'blackheads': self.blackheads,
            'pores': self.pores,
            'oiliness': self.oiliness,
            'redness': self.redness,
            'dark_spots': self.dark_spots,
            'dark_circles': self.dark_circles,
            'tone_evenness': self.tone_evenness,
            'ai_comments': json.loads(self.ai_comments) if self.ai_comments else [],
            'recommended_ingredients': json.loads(self.recommended_ingredients) if self.recommended_ingredients else [],
            'morning_routine': json.loads(self.morning_routine) if self.morning_routine else [],
            'evening_routine': json.loads(self.evening_routine) if self.evening_routine else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)  # cleanser, serum, moisturizer, sunscreen
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    product_url = db.Column(db.String(500), nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    skin_types = db.Column(db.String(255), nullable=True)  # comma-separated
    concerns = db.Column(db.String(255), nullable=True)    # comma-separated
    
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'product_url': self.product_url,
            'skin_types': self.skin_types.split(',') if self.skin_types else [],
            'concerns': self.concerns.split(',') if self.concerns else [],
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None
        }
