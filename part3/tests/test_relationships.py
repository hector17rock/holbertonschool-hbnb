#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade

def test_relationships():
    """Test all entity relationships using the facade."""
    app = create_app()
    
    with app.app_context():
        # Initialize the database
        db.create_all()
        
        # Create facade instance
        facade = HBnBFacade()
        
        print("=== Testing Entity Relationships ===\n")
        
        # 1. Create a user (owner)
        print("1. Creating a user...")
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        user = facade.create_user(user_data)
        print(f"   User created: {user.first_name} {user.last_name} (ID: {user.id})")
        
        # 2. Create another user (reviewer)
        print("\n2. Creating another user (reviewer)...")
        reviewer_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123'
        }
        reviewer = facade.create_user(reviewer_data)
        print(f"   Reviewer created: {reviewer.first_name} {reviewer.last_name} (ID: {reviewer.id})")
        
        # 3. Create amenities
        print("\n3. Creating amenities...")
        amenity1_data = {'name': 'WiFi'} 
        amenity1 = facade.create_amenity(amenity1_data)
        print(f"   Amenity created: {amenity1.name} (ID: {amenity1.id})")
        
        amenity2_data = {'name': 'Swimming Pool'}
        amenity2 = facade.create_amenity(amenity2_data)
        print(f"   Amenity created: {amenity2.name} (ID: {amenity2.id})")
        
        # 4. Create a place with amenities
        print("\n4. Creating a place with amenities...")
        place_data = {
            'title': 'Beautiful Beach House',
            'description': 'A wonderful place by the beach',
            'price': 150.0,
            'latitude': 25.7617,
            'longitude': -80.1918,
            'owner_id': user.id,
            'amenities': [amenity1.id, amenity2.id]
        }
        place = facade.create_place(place_data)
        print(f"   Place created: {place.title} (ID: {place.id})")
        print(f"   Owner: {place.owner.first_name} {place.owner.last_name}")
        print(f"   Amenities: {[amenity.name for amenity in place.amenities]}")
        
        # 5. Create a review
        print("\n5. Creating a review...")
        review_data = {
            'user_id': reviewer.id,
            'place_id': place.id,
            'rating': 5,
            'text': 'Absolutely amazing place! Highly recommend.'
        }
        review = facade.create_review(review_data)
        print(f"   Review created: Rating {review.rating}/5 (ID: {review.id})")
        print(f"   Reviewer: {review.user.first_name} {review.user.last_name}")
        print(f"   Place: {review.place.title}")
        print(f"   Review text: {review.text}")
        
        # 6. Test relationships - User to Places
        print("\n6. Testing User -> Places relationship...")
        user_places = user.places
        print(f"   User {user.first_name} owns {len(user_places)} place(s):")
        for p in user_places:
            print(f"     - {p.title}")
        
        # 7. Test relationships - User to Reviews
        print("\n7. Testing User -> Reviews relationship...")
        user_reviews = reviewer.reviews
        print(f"   User {reviewer.first_name} has written {len(user_reviews)} review(s):")
        for r in user_reviews:
            print(f"     - {r.rating}/5 stars for {r.place.title}")
        
        # 8. Test relationships - Place to Reviews
        print("\n8. Testing Place -> Reviews relationship...")
        place_reviews = place.reviews
        print(f"   Place {place.title} has {len(place_reviews)} review(s):")
        for r in place_reviews:
            print(f"     - {r.rating}/5 stars by {r.user.first_name} {r.user.last_name}")
        
        # 9. Test relationships - Place to Amenities (Many-to-Many)
        print("\n9. Testing Place -> Amenities relationship...")
        place_amenities = place.amenities
        print(f"   Place {place.title} has {len(place_amenities)} amenity/amenities:")
        for a in place_amenities:
            print(f"     - {a.name}")
        
        # 10. Test relationships - Amenity to Places (Many-to-Many reverse)
        print("\n10. Testing Amenity -> Places relationship...")
        amenity_places = amenity1.places
        print(f"   Amenity {amenity1.name} is available in {len(amenity_places)} place(s):")
        for p in amenity_places:
            print(f"     - {p.title}")
        
        # 11. Test adding more amenities to a place
        print("\n11. Testing adding more amenities to place...")
        amenity3_data = {'name': 'Air Conditioning'}
        amenity3 = facade.create_amenity(amenity3_data)
        place.add_amenity(amenity3)
        db.session.commit()
        
        updated_place = facade.get_place(place.id)
        print(f"   Updated place {updated_place.title} now has {len(updated_place.amenities)} amenities:")
        for a in updated_place.amenities:
            print(f"     - {a.name}")
        
        print("\n=== All relationship tests completed successfully! ===")

if __name__ == '__main__':
    test_relationships()
