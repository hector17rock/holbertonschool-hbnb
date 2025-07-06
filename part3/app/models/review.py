from .base_model import BaseModel
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import validates


class Review(BaseModel):
    """Review model representing a user's review of a place."""
    __tablename__ = 'reviews'

    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    
    # Foreign Keys
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)

    def __init__(self, text="", rating=0, **kwargs):
        """Initialize a Review instance."""
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate that rating is between 1 and 5."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    @property
    def comment(self):
        """Alias for text to maintain backward compatibility."""
        return self.text

    @comment.setter
    def comment(self, value):
        """Alias for text to maintain backward compatibility."""
        self.text = value
