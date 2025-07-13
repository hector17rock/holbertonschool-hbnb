from .base_model import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import validates


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name="", last_name="", email="", password="", is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if '@' not in email:
            raise ValueError("Invalid email format")
        return email

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """Validate name fields"""
        if not name or len(name.strip()) == 0:
            raise ValueError(f"{key} cannot be empty")
        if len(name) > 50:
            raise ValueError(f"{key} cannot exceed 50 characters")
        return name.strip()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
