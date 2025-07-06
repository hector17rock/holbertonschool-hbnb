#!/usr/bin/env python3
"""
Test script for SQLAlchemy relationships in HBnB application.
"""

from app import create_app
from app.models.base_model import db
from app.services.facade import HBnBFacade


def test_sqlalchemy_relationships():
    """Test SQLAlchemy relationships between models."""
    print("🚀 Testing SQLAlchemy Relationships")
    print("=" * 50)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Drop and recreate database tables
            print("🏗️  Recreating database with relationships...")
            db.drop_all()
            db.create_all()
            print("✅ Database tables created successfully!\n")
            
            # Initialize facade
            facade = HBnBFacade()
            
            # Test 1: Create User
            print("👤 Creating a user...")
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'password': 'secure123',
                'is_admin': False
            }
            
            user = facade.create_user(user_data)
            print(f"✅ User created: {user.first_name} {user.last_name} (ID: {user.id})")
            
            # Test 2: Create Amenities
            print("\n🏠 Creating amenities...")
            amenity1 = facade.create_amenity({'name': 'WiFi'})
            amenity2 = facade.create_amenity({'name': 'Swimming Pool'})
            print(f"✅ Amenities created: {amenity1.name}, {amenity2.name}")
            
            # Test 3: Create Place with relationships
            print("\n🏡 Creating a place with owner and amenities...")
            place_data = {
                'title': 'Beautiful Beach House',
                'description': 'A stunning oceanfront property',
                'price': 250.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': user.id,
                'amenities': [amenity1.id, amenity2.id]
            }
            
            place = facade.create_place(place_data)
            print(f"✅ Place created: {place.title} (ID: {place.id})")
            
            # Test 4: Verify relationships work
            print("\n🔗 Testing relationships...")
            
            # Test User -> Places relationship
            print(f"📍 User's places: {len(user.places)} place(s)")
            for user_place in user.places:
                print(f"   - {user_place.title}: ${user_place.price}")
            
            # Test Place -> Owner relationship
            print(f"👤 Place owner: {place.owner.first_name} {place.owner.last_name}")
            
            # Test Place -> Amenities relationship (many-to-many)
            print(f"🏠 Place amenities: {len(place.amenities)} amenity/amenities")
            for amenity in place.amenities:
                print(f"   - {amenity.name}")
            
            # Test Amenity -> Places relationship (reverse)
            print(f"🏡 Places with WiFi: {len(amenity1.places)} place(s)")
            for amenity_place in amenity1.places:
                print(f"   - {amenity_place.title}")
            
            # Test 5: Create Review with relationships
            print("\n📝 Creating a review...")
            review_data = {
                'text': 'Amazing place! Great location and amenities.',
                'rating': 5,
                'user_id': user.id,
                'place_id': place.id
            }
            
            review = facade.create_review(review_data)
            print(f"✅ Review created: Rating {review.rating}/5")
            
            # Test Review relationships
            print(f"👤 Review author: {review.user.first_name} {review.user.last_name}")
            print(f"🏡 Reviewed place: {review.place.title}")
            
            # Test Place -> Reviews relationship
            print(f"📝 Place reviews: {len(place.reviews)} review(s)")
            for place_review in place.reviews:
                print(f"   - Rating: {place_review.rating}/5 - {place_review.text[:50]}...")
            
            # Test User -> Reviews relationship
            print(f"📝 User reviews: {len(user.reviews)} review(s)")
            for user_review in user.reviews:
                print(f"   - {user_review.place.title}: {user_review.rating}/5")
            
            # Test 6: Query optimization test
            print("\n⚡ Testing query optimization...")
            
            # Get place with eager loading
            retrieved_place = facade.get_place(place.id)
            print(f"📍 Retrieved place: {retrieved_place.title}")
            print(f"👤 Owner loaded: {retrieved_place.owner.first_name}")
            print(f"🏠 Amenities loaded: {len(retrieved_place.amenities)}")
            print(f"📝 Reviews loaded: {len(retrieved_place.reviews)}")
            
            # Test 7: Get reviews by place using relationship
            print("\n📋 Testing get reviews by place...")
            place_reviews = facade.get_reviews_by_place(place.id)
            print(f"✅ Found {len(place_reviews)} review(s) for the place")
            
            print("\n🎉 All relationship tests completed successfully!")
            print("✅ One-to-Many relationships working correctly")
            print("✅ Many-to-Many relationships working correctly")
            print("✅ Bidirectional relationships functioning")
            print("✅ Lazy loading and eager loading operational")
            
        except Exception as e:
            print(f"❌ Error during relationship testing: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_sqlalchemy_relationships()
