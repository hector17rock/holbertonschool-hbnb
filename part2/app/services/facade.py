from app.persistence.repository import InMemoryRepository


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

    def get_user(self, use_id):
        """Retrieve a usr by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find usr by email."""
        return self.user_repo.get(user_id)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
