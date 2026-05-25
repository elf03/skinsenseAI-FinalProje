from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from .user import db
from datetime import datetime
import json

class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=False)
    
    analysis_type: Mapped[str] = mapped_column(db.String(20), nullable=False)  # 'photo' or 'questionnaire'
    photo_path: Mapped[Optional[str]] = mapped_column(db.String(255), nullable=True)
    
    skin_type: Mapped[Optional[str]] = mapped_column(db.String(50), nullable=True)
    moisture_level: Mapped[Optional[int]] = mapped_column(db.Integer, nullable=True)
    acne_level: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    sensitivity: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    blackheads: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    pores: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    oiliness: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    redness: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    dark_spots: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    dark_circles: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    tone_evenness: Mapped[Optional[str]] = mapped_column(db.String(20), nullable=True)
    
    ai_comments: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    recommended_ingredients: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    morning_routine: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    evening_routine: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    
    raw_response: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    
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
    
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(db.String(100), nullable=False)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(db.String(100), nullable=True)  # cleanser, serum, moisturizer, sunscreen
    description: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    price: Mapped[Optional[str]] = mapped_column(db.String(50), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(db.String(500), nullable=True)
    product_url: Mapped[Optional[str]] = mapped_column(db.String(500), nullable=True)
    ingredients: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    skin_types: Mapped[Optional[str]] = mapped_column(db.String(255), nullable=True)  # comma-separated
    concerns: Mapped[Optional[str]] = mapped_column(db.String(255), nullable=True)    # comma-separated
    
    scraped_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    
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
