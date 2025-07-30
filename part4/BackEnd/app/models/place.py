from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign key to User (owner)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')

    def __init__(self, title="", description="", price=0, latitude=0.0,
                 longitude=0.0, owner=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        if owner:
            self.owner = owner

    @validates('title')
    def validate_title(self, key, title):
        """Validate title field"""
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title.strip()

    @validates('price')
    def validate_price(self, key, price):
        """Validate price field"""
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be positive")
        return float(price)

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validate latitude field"""
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return float(latitude)

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validate longitude field"""
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return float(longitude)

    # Methods to work with relationships
    def add_review(self, review):
        """Add review to place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove amenity from place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
