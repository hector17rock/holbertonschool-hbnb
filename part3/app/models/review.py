from .base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, user=None, place=None, rating=0, text=""):
        super().__init__()
        # Note: user and place relationships will be added later
        self.rating = rating
        self.text = text
        # For backward compatibility, also set comment
        self.comment = text

    @validates('text')
    def validate_text(self, key, text):
        """Validate text field"""
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 1000:
            raise ValueError("Review text cannot exceed 1000 characters")
        return text.strip()

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate rating field"""
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    # Backward compatibility property
    @property
    def comment(self):
        """Backward compatibility property for comment"""
        return self.text

    @comment.setter
    def comment(self, value):
        """Backward compatibility setter for comment"""
        self.text = value
