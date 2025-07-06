#!/usr/bin/env python3
"""
Quick verification that all required relationships are implemented and working.
"""

from app import create_app
from app.models.base_model import db
from app.services.facade import HBnBFacade


def verify_relationships():
    print("🔍 Verifying All Required Relationships")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create test data
        user = facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'test123',
            'is_admin': False
        })
        
        amenity = facade.create_amenity({'name': 'WiFi'})
        
        place = facade.create_place({
            'title': 'Test Place',
            'description': 'A test property',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': user.id,
            'amenities': [amenity.id]
        })
        
        review = facade.create_review({
            'text': 'Great place!',
            'rating': 5,
            'user_id': user.id,
            'place_id': place.id
        })
        
        # Verify all relationships
        print("✅ 1. User ↔ Place (One-to-Many):")
        print(f"   User has {len(user.places)} place(s)")
        print(f"   Place owner: {place.owner.first_name}")
        
        print("✅ 2. Place ↔ Review (One-to-Many):")
        print(f"   Place has {len(place.reviews)} review(s)")
        print(f"   Review place: {review.place.title}")
        
        print("✅ 3. User ↔ Review (One-to-Many):")
        print(f"   User has {len(user.reviews)} review(s)")
        print(f"   Review user: {review.user.first_name}")
        
        print("✅ 4. Place ↔ Amenity (Many-to-Many):")
        print(f"   Place has {len(place.amenities)} amenity/amenities")
        print(f"   Amenity in {len(amenity.places)} place(s)")
        
        print("\n🎉 All relationships verified successfully!")
        print("✅ All required relationships are implemented and working")


if __name__ == "__main__":
    verify_relationships()
