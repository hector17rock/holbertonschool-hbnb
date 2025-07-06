from .base_model import BaseModel
from sqlalchemy import Column, String


class Amenity(BaseModel):
    """Amenity model representing a place amenity."""
    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name="", **kwargs):
        """Initialize an Amenity instance."""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        """String representation of the Amenity."""
        return f"<Amenity(id='{self.id}', name='{self.name}')>"

    def __str__(self):
        """Human-readable string representation."""
        return self.name
