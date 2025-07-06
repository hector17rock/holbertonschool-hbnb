#!/usr/bin/env python3
"""
Test script for SQLAlchemy models with facade.
This script tests the complete flow with Place, Review, Amenity, and User models
using SQLAlchemy repositories through the facade.
"""

from app.models.base_model import db
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app import create_app


def test_models_with_facade():
    """Test all models using the facade with SQLAlchemy repositories."""
    print("🚀 Testing SQLAlchemy Models with Facade")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Drop and recreate database tables
        print("🏗️  Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        print("✅ Database tables created successfully!\n")
        
        # Initialize facade
        facade = HBnBFacade()
        
        # Test User creation and operations
        print("🧪 Testing User model through facade...")
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'secure_password123',
            'is_admin': False
        }
        
        user = facade.create_user(user_data)
        print(f"✅ Created user: {user.first_name} {user.last_name} (ID: {user.id})")
        
        # Test getting user by email
        found_user = facade.get_user_by_email('john.doe@example.com')
        print(f"✅ Found user by email: {found_user.first_name} {found_user.last_name}")
        
        # Test password verification
        is_valid = user.verify_password('secure_password123')
        print(f"✅ Password verification: {'✓' if is_valid else '✗'}")
        
        # Test Amenity creation
        print("\n🧪 Testing Amenity model through facade...")
        amenity_data = {'name': 'WiFi'}
        amenity = facade.create_amenity(amenity_data)
        print(f"✅ Created amenity: {amenity.name} (ID: {amenity.id})")
        
        # Create another amenity
        amenity2_data = {'name': 'Swimming Pool'}
        amenity2 = facade.create_amenity(amenity2_data)
        print(f"✅ Created amenity: {amenity2.name} (ID: {amenity2.id})")
        
        # Test Place creation
        print("\n🧪 Testing Place model through facade...")
        place_data = {
            'title': 'Beautiful Beach House',
            'description': 'A stunning oceanfront property',
            'price': 250.0,
            'latitude': 34.0522,
            'longitude': -118.2437,
            'owner_id': user.id,
            'amenities': [amenity.id, amenity2.id]
        }
        
        place = facade.create_place(place_data)
        print(f"✅ Created place: {place.title} (ID: {place.id})")
        print(f"   Owner: {place.owner.first_name} {place.owner.last_name}")
        print(f"   Amenities: {[a.name for a in place.amenities]}")
        print(f"   Price: ${place.price}/night")
        
        # Test Review creation
        print("\n🧪 Testing Review model through facade...")
        review_data = {
            'text': 'Amazing place! Highly recommended.',
            'rating': 5,
            'user_id': user.id,
            'place_id': place.id
        }
        
        review = facade.create_review(review_data)
        print(f"✅ Created review: {review.id}")
        print(f"   Rating: {review.rating}/5")
        print(f"   Text: {review.text}")
        print(f"   User: {review.user.first_name} {review.user.last_name}")
        print(f"   Place: {review.place.title}")
        
        # Test retrieving all entities
        print("\n📋 Testing retrieval methods...")
        all_users = facade.get_all_users()
        all_places = facade.get_all_places()
        all_amenities = facade.get_all_amenities()
        all_reviews = facade.get_all_reviews()
        
        print(f"✅ Total users: {len(all_users)}")
        print(f"✅ Total places: {len(all_places)}")
        print(f"✅ Total amenities: {len(all_amenities)}")
        print(f"✅ Total reviews: {len(all_reviews)}")
        
        # Test updates
        print("\n🔄 Testing update operations...")
        
        # Update user
        update_data = {'first_name': 'Johnny'}
        updated_user = facade.update_user(user.id, update_data)
        print(f"✅ Updated user name: {updated_user.first_name}")
        
        # Update amenity
        amenity_update = {'name': 'High-Speed WiFi'}
        updated_amenity = facade.update_amenity(amenity.id, amenity_update)
        print(f"✅ Updated amenity: {updated_amenity.name}")
        
        # Update place
        place_update = {'title': 'Luxury Beach House', 'price': 300.0}
        updated_place = facade.update_place(place.id, place_update)
        print(f"✅ Updated place: {updated_place.title} - ${updated_place.price}")
        
        # Update review
        review_update = {'text': 'Absolutely fantastic place!', 'rating': 5}
        updated_review = facade.update_review(review.id, review_update)
        print(f"✅ Updated review: {updated_review.text}")
        
        # Test reviews by place
        place_reviews = facade.get_reviews_by_place(place.id)
        print(f"✅ Reviews for place '{place.title}': {len(place_reviews)}")
        
        # Test business logic validation
        print("\n🛡️  Testing business logic validation...")
        
        try:
            # Try to create place with non-existent owner
            invalid_place_data = {
                'title': 'Invalid Place',
                'price': 100.0,
                'latitude': 0.0,
                'longitude': 0.0,
                'owner_id': 'non-existent-id'
            }
            facade.create_place(invalid_place_data)
            print("❌ Should have failed with invalid owner")
        except ValueError as e:
            print(f"✅ Correctly rejected invalid owner: {e}")
        
        try:
            # Try to create review with invalid rating
            invalid_review_data = {
                'text': 'Bad review',
                'rating': 10,  # Invalid rating
                'user_id': user.id,
                'place_id': place.id
            }
            facade.create_review(invalid_review_data)
            print("❌ Should have failed with invalid rating")
        except ValueError as e:
            print(f"✅ Correctly rejected invalid rating: {e}")
        
        print("\n🎉 All facade tests completed successfully!")
        print(f"   Users created: {len(all_users)}")
        print(f"   Places created: {len(all_places)}")
        print(f"   Amenities created: {len(all_amenities)}")
        print(f"   Reviews created: {len(all_reviews)}")


if __name__ == "__main__":
    test_models_with_facade()
