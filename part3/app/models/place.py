from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title="", description="", price=0, latitude=0.0,
                 longitude=0.0, owner=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        # Note: owner relationship will be added later
        # Note: reviews and amenities relationships will be added later

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

    # Legacy compatibility methods (will be updated when relationships are added)
    def add_reviews(self, review):
        """Add review to place (placeholder for future relationship)"""
        # This will be implemented when relationships are added
        pass

    def add_amenity(self, amenity):
        """Add amenity to place (placeholder for future relationship)"""
        # This will be implemented when relationships are added
        pass
