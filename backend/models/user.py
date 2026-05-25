from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(db.String(255), nullable=True)
    preferred_language: Mapped[str] = mapped_column(db.String(10), default='tr')
    skin_type: Mapped[Optional[str]] = mapped_column(db.String(50), nullable=True)
    
    otp_code: Mapped[Optional[str]] = mapped_column(db.String(6), nullable=True)
    otp_expires_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    last_login: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)
    
    analyses: Mapped[List["Analysis"]] = db.relationship('Analysis', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'avatar': self.avatar,
            'preferred_language': self.preferred_language,
            'skin_type': self.skin_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
