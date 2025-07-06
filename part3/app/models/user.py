from .base_model import BaseModel
from sqlalchemy import Column, String, Boolean


class User(BaseModel):
    """User model representing a user in the system."""
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    def __init__(self, first_name="", last_name="", email="",
                 password="", is_admin=False, **kwargs):
        """Initialize a User instance."""
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        # Note: places relationship will be added later
        # For now, we'll keep the list-based approach for compatibility
        if not hasattr(self, 'places'):
            self.places = []

    def add_place(self, place):
        """Add a place to this user's places."""
        if place and hasattr(place, 'owner') and place.owner == self:
            self.places.append(place)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
