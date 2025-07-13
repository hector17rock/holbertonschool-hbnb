"""
User-specific repository for handling user database operations.
"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository class for User entity with user-specific operations.
    """
    
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.
        
        Args:
            email (str): The email address to search for
            
        Returns:
            User: The user object if found, None otherwise
        """
        return self.model.query.filter_by(email=email).first()

    def get_users_by_admin_status(self, is_admin=False):
        """
        Retrieve users by admin status.
        
        Args:
            is_admin (bool): Whether to get admin users or regular users
            
        Returns:
            List[User]: List of users matching the admin status
        """
        return self.model.query.filter_by(is_admin=is_admin).all()

    def search_users_by_name(self, name_query):
        """
        Search users by first name or last name.
        
        Args:
            name_query (str): The name to search for
            
        Returns:
            List[User]: List of users matching the search query
        """
        return self.model.query.filter(
            (User.first_name.ilike(f'%{name_query}%')) | 
            (User.last_name.ilike(f'%{name_query}%'))
        ).all()

    def email_exists(self, email):
        """
        Check if an email already exists in the database.
        
        Args:
            email (str): The email to check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        return self.model.query.filter_by(email=email).first() is not None

    def get_admin_users(self):
        """
        Get all admin users.
        
        Returns:
            List[User]: List of admin users
        """
        return self.get_users_by_admin_status(is_admin=True)

    def get_regular_users(self):
        """
        Get all regular (non-admin) users.
        
        Returns:
            List[User]: List of regular users
        """
        return self.get_users_by_admin_status(is_admin=False)
