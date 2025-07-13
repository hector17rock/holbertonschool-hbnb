from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationships
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def __init__(self, name=""):
        super().__init__()
        self.name = name

    @validates('name')
    def validate_name(self, key, name):
        """Validate name field"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        return name.strip()
