from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, name="", description="", price=0, latitude=0.0,
                 longitude=0.0):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
