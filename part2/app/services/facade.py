from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create new usr and store in the repo."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a usr by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find usr by email."""
        users = self.user_repo.get_all()
        for user in users:
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.update(user_id, user_data)
            return user
        return None

    def create_amenity(self, amenity_data):
        """Create a new amenity and store in the repository."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
