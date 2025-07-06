from .base_model import BaseModel
from sqlalchemy import Column, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship


# Association table for many-to-many relationship between Place and Amenity
place_amenity_association = Table(
    'place_amenity', BaseModel.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place model representing a place/property."""
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # ForeignKey and relationship
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    reviews = relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = relationship('Amenity', secondary=place_amenity_association, lazy='subquery',
                             backref='places', cascade='all')

    def __init__(self, title="", description="", price=0.0, latitude=0.0,
                 longitude=0.0, **kwargs):
        """Initialize a Place instance."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

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
