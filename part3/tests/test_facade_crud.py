#!/usr/bin/env python3
"""
Test CRUD operations directly through the facade.
"""

from app import create_app
from app.services.facade import HBnBFacade


def test_facade_crud():
    """Test CRUD operations directly through facade."""
    app = create_app()
    
    with app.app_context():
        facade = HBnBFacade()
        
        print("🧪 Testing Facade CRUD Operations")
        print("=" * 40)
        
        # Test Place update
        print("\n📝 Testing Place Update...")
        place_id = "db0b6055-a695-4303-800f-cb4361205b4c"
        update_data = {
            "title": "Luxury Beach House",
            "price": 350.0
        }
        
        updated_place = facade.update_place(place_id, update_data)
        if updated_place:
            print(f"✅ Place updated successfully")
            print(f"   New title: {updated_place.title}")
            print(f"   New price: ${updated_place.price}")
        else:
            print("❌ Failed to update place")
        
        # Test getting all places
        print("\n📋 Testing Get All Places...")
        places = facade.get_all_places()
        print(f"✅ Found {len(places)} place(s)")
        for place in places:
            print(f"   - {place.title}: ${place.price}")
        
        # Test getting all amenities
        print("\n📋 Testing Get All Amenities...")
        amenities = facade.get_all_amenities()
        print(f"✅ Found {len(amenities)} amenity/amenities")
        for amenity in amenities:
            print(f"   - {amenity.name}")
        
        # Test getting all users
        print("\n📋 Testing Get All Users...")
        users = facade.get_all_users()
        print(f"✅ Found {len(users)} user(s)")
        for user in users:
            print(f"   - {user.first_name} {user.last_name}: {user.email}")


if __name__ == "__main__":
    test_facade_crud()
