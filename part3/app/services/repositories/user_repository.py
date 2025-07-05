from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Get user by email address."""
        return self.model.query.filter_by(email=email).first()

    def get_admin_users(self):
        """Get all admin users."""
        return self.model.query.filter_by(is_admin=True).all()

    def get_regular_users(self):
        """Get all non-admin users."""
        return self.model.query.filter_by(is_admin=False).all()

    def email_exists(self, email):
        """Check if email already exists in the database."""
        return self.model.query.filter_by(email=email).first() is not None

    def create_user(self, user_data):
        """Create a new user with validation."""
        # Check if email already exists
        if self.email_exists(user_data['email']):
            raise ValueError("Email already exists")

        # Create user instance
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )

        # Add to database
        self.add(user)
        return user
