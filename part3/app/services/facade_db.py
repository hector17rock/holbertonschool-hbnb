from app.services.repositories.user_repository import UserRepository
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()

    # User operations
    def create_user(self, user_data):
        """Create new user and store in the database."""
        return self.user_repo.create_user(user_data)

    def get_user(self, user_id):
        """Retrieve a user by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find user by email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.user_repo.get(user_id)
        if user:
            # Hash password if provided
            if 'password' in user_data:
                user.hash_password(user_data['password'])
                # Remove password from user_data to avoid storing it twice
                user_data_copy = user_data.copy()
                del user_data_copy['password']
                user_data = user_data_copy
            
            self.user_repo.update(user_id, user_data)
            return user
        return None

    def get_admin_users(self):
        """Get all admin users."""
        return self.user_repo.get_admin_users()

    def get_regular_users(self):
        """Get all regular users."""
        return self.user_repo.get_regular_users()

    # Placeholder methods for other entities (to be implemented later)
    def create_amenity(self, amenity_data):
        """Create a new amenity - placeholder for now."""
        raise NotImplementedError("Amenity operations not yet implemented with SQLAlchemy")

    def get_amenity(self, amenity_id):
        """Get amenity by ID - placeholder for now."""
        raise NotImplementedError("Amenity operations not yet implemented with SQLAlchemy")

    def get_all_amenities(self):
        """Get all amenities - placeholder for now."""
        raise NotImplementedError("Amenity operations not yet implemented with SQLAlchemy")

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity - placeholder for now."""
        raise NotImplementedError("Amenity operations not yet implemented with SQLAlchemy")

    def create_place(self, place_data):
        """Create a new place - placeholder for now."""
        raise NotImplementedError("Place operations not yet implemented with SQLAlchemy")

    def get_place(self, place_id):
        """Get place by ID - placeholder for now."""
        raise NotImplementedError("Place operations not yet implemented with SQLAlchemy")

    def get_all_places(self):
        """Get all places - placeholder for now."""
        raise NotImplementedError("Place operations not yet implemented with SQLAlchemy")

    def update_place(self, place_id, place_data):
        """Update place - placeholder for now."""
        raise NotImplementedError("Place operations not yet implemented with SQLAlchemy")

    def create_review(self, review_data):
        """Create a new review - placeholder for now."""
        raise NotImplementedError("Review operations not yet implemented with SQLAlchemy")

    def get_review(self, review_id):
        """Get review by ID - placeholder for now."""
        raise NotImplementedError("Review operations not yet implemented with SQLAlchemy")

    def get_all_reviews(self):
        """Get all reviews - placeholder for now."""
        raise NotImplementedError("Review operations not yet implemented with SQLAlchemy")

    def get_reviews_by_place(self, place_id):
        """Get reviews by place - placeholder for now."""
        raise NotImplementedError("Review operations not yet implemented with SQLAlchemy")

    def update_review(self, review_id, review_data):
        """Update review - placeholder for now."""
        raise NotImplementedError("Review operations not yet implemented with SQLAlchemy")

    def delete_review(self, review_id):
        """Delete review - placeholder for now."""
        raise NotImplementedError("Review operations not yet implemented with SQLAlchemy")
