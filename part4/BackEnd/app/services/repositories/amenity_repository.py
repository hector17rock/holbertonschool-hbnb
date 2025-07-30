"""
Amenity-specific repository for handling amenity database operations.
"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """
    Repository class for Amenity entity with amenity-specific operations.
    """
    
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """
        Retrieve an amenity by name.
        
        Args:
            name (str): The name of the amenity
            
        Returns:
            Amenity: The amenity object if found, None otherwise
        """
        return self.model.query.filter_by(name=name).first()

    def search_amenities_by_name(self, name_query):
        """
        Search amenities by name.
        
        Args:
            name_query (str): The name to search for
            
        Returns:
            List[Amenity]: List of amenities matching the search query
        """
        return self.model.query.filter(
            Amenity.name.ilike(f'%{name_query}%')
        ).all()

    def amenity_exists(self, name):
        """
        Check if an amenity with the given name exists.
        
        Args:
            name (str): The name to check
            
        Returns:
            bool: True if amenity exists, False otherwise
        """
        return self.model.query.filter_by(name=name).first() is not None

    def get_amenities_ordered_by_name(self, ascending=True):
        """
        Get amenities ordered by name.
        
        Args:
            ascending (bool): Whether to sort in ascending order
            
        Returns:
            List[Amenity]: List of amenities ordered by name
        """
        if ascending:
            return self.model.query.order_by(Amenity.name.asc()).all()
        else:
            return self.model.query.order_by(Amenity.name.desc()).all()

    def get_amenities_starting_with(self, prefix):
        """
        Get amenities whose names start with a specific prefix.
        
        Args:
            prefix (str): The prefix to search for
            
        Returns:
            List[Amenity]: List of amenities starting with the prefix
        """
        return self.model.query.filter(
            Amenity.name.ilike(f'{prefix}%')
        ).all()

    def get_amenities_containing(self, substring):
        """
        Get amenities whose names contain a specific substring.
        
        Args:
            substring (str): The substring to search for
            
        Returns:
            List[Amenity]: List of amenities containing the substring
        """
        return self.search_amenities_by_name(substring)

    def get_recent_amenities(self, limit=10):
        """
        Get the most recently created amenities.
        
        Args:
            limit (int): Maximum number of amenities to return
            
        Returns:
            List[Amenity]: List of recent amenities
        """
        return self.model.query.order_by(
            Amenity.created_at.desc()
        ).limit(limit).all()
