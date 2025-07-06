#!/usr/bin/env python3
"""
Simple test to verify place creation and basic attributes.
"""

from app import create_app
from app.services.facade import HBnBFacade


def test_place_details():
    """Test place details directly through facade."""
    app = create_app()
    
    with app.app_context():
        facade = HBnBFacade()
        
        # Get the place we created
        place_id = "db0b6055-a695-4303-800f-cb4361205b4c"
        place = facade.get_place(place_id)
        
        if place:
            print(f"Place ID: {place.id}")
            print(f"Title: {place.title}")
            print(f"Description: {place.description}")
            print(f"Price: ${place.price}")
            print(f"Location: ({place.latitude}, {place.longitude})")
            print(f"Created: {place.created_at}")
            print(f"Updated: {place.updated_at}")
            
            if hasattr(place, 'owner') and place.owner:
                print(f"Owner: {place.owner.first_name} {place.owner.last_name}")
            else:
                print("Owner: Not set (relationship not implemented)")
                
            if hasattr(place, 'amenities') and place.amenities:
                print(f"Amenities: {[a.name for a in place.amenities]}")
            else:
                print("Amenities: Not set (relationship not implemented)")
        else:
            print("Place not found")


if __name__ == "__main__":
    test_place_details()
