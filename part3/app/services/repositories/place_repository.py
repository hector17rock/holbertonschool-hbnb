"""
Place-specific repository for handling place database operations.
"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """
    Repository class for Place entity with place-specific operations.
    """
    
    def __init__(self):
        super().__init__(Place)

    def get_places_by_price_range(self, min_price, max_price):
        """
        Retrieve places within a price range.
        
        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price
            
        Returns:
            List[Place]: List of places within the price range
        """
        return self.model.query.filter(
            Place.price >= min_price,
            Place.price <= max_price
        ).all()

    def get_places_by_location(self, latitude, longitude, radius=10):
        """
        Retrieve places within a geographical radius.
        
        Args:
            latitude (float): Center latitude
            longitude (float): Center longitude
            radius (float): Radius in kilometers (default: 10)
            
        Returns:
            List[Place]: List of places within the radius
        """
        # Simple bounding box calculation (for more precise results, use PostGIS)
        lat_offset = radius / 111.0  # Approximately 1 degree = 111 km
        lng_offset = radius / (111.0 * abs(latitude))  # Adjust for latitude
        
        return self.model.query.filter(
            Place.latitude >= latitude - lat_offset,
            Place.latitude <= latitude + lat_offset,
            Place.longitude >= longitude - lng_offset,
            Place.longitude <= longitude + lng_offset
        ).all()

    def search_places_by_title(self, title_query):
        """
        Search places by title.
        
        Args:
            title_query (str): The title to search for
            
        Returns:
            List[Place]: List of places matching the search query
        """
        return self.model.query.filter(
            Place.title.ilike(f'%{title_query}%')
        ).all()

    def get_places_above_price(self, min_price):
        """
        Get places above a minimum price.
        
        Args:
            min_price (float): Minimum price threshold
            
        Returns:
            List[Place]: List of places above the minimum price
        """
        return self.model.query.filter(Place.price >= min_price).all()

    def get_places_below_price(self, max_price):
        """
        Get places below a maximum price.
        
        Args:
            max_price (float): Maximum price threshold
            
        Returns:
            List[Place]: List of places below the maximum price
        """
        return self.model.query.filter(Place.price <= max_price).all()

    def get_places_ordered_by_price(self, ascending=True):
        """
        Get places ordered by price.
        
        Args:
            ascending (bool): Whether to sort in ascending order
            
        Returns:
            List[Place]: List of places ordered by price
        """
        if ascending:
            return self.model.query.order_by(Place.price.asc()).all()
        else:
            return self.model.query.order_by(Place.price.desc()).all()
