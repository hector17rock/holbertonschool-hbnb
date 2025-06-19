import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the update_at timestamp whenever the object is modified."""
        self.update_at = datetime.now()

    def update(self, data):
        """Update the atributes of the object based of a provied dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(slef, key, value)
        self.save()
