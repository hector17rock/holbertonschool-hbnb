from .base_model import BaseModel
from sqlalchemy import Column, String, Float, Text


class Place(BaseModel):
    """Place model representing a place/property."""
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __init__(self, title="", description="", price=0.0, latitude=0.0,
                 longitude=0.0, **kwargs):
        """Initialize a Place instance."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        # Note: owner, reviews, and amenities relationships will be added later
        # For now, we'll keep the list-based approach for compatibility
        if not hasattr(self, 'reviews'):
            self.reviews = []
        if not hasattr(self, 'amenities'):
            self.amenities = []

    def add_reviews(self, review):
        """Add a review to this place."""
        if review and hasattr(review, 'place') and review.place == self:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    @property
    def name(self):
        """Alias for title to maintain backward compatibility."""
        return self.title

    @name.setter
    def name(self, value):
        """Alias for title to maintain backward compatibility."""
        self.title = value
