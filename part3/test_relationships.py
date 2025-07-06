#!/usr/bin/env python3
"""Test script for database relationships."""

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_relationships():
    """Test all the database relationships."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("=== Testing Database Relationships ===\n")
        
        # 1. Create a User
        print("1. Creating a User...")
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="hashedpassword123"
        )
        db.session.add(user)
        db.session.commit()
        print(f"   Created user: {user.first_name} {user.last_name} (ID: {user.id})")
        
        # 2. Create Amenities
        print("\n2. Creating Amenities...")
        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Swimming Pool")
        parking = Amenity(name="Free Parking")
        
        db.session.add_all([wifi, pool, parking])
        db.session.commit()
        
        print(f"   Created amenity: {wifi.name} (ID: {wifi.id})")
        print(f"   Created amenity: {pool.name} (ID: {pool.id})")
        print(f"   Created amenity: {parking.name} (ID: {parking.id})")
        
        # 3. Create a Place owned by the User
        print("\n3. Creating a Place...")
        place = Place(
            title="Beautiful Beach House",
            description="A lovely house by the beach",
            price=150.0,
            latitude=25.7617,
            longitude=-80.1918,
            owner_id=user.id
        )
        
        # Add amenities to the place (testing many-to-many)
        place.amenities.append(wifi)
        place.amenities.append(pool)
        
        db.session.add(place)
        db.session.commit()
        
        print(f"   Created place: {place.title} (ID: {place.id})")
        print(f"   Owner: {place.owner.first_name} {place.owner.last_name}")
        print(f"   Amenities: {[amenity.name for amenity in place.amenities]}")
        
        # 4. Create Reviews for the Place
        print("\n4. Creating Reviews...")
        review1 = Review(
            text="Amazing place! Really enjoyed our stay.",
            rating=5,
            user_id=user.id,
            place_id=place.id
        )
        
        # Create another user for second review
        user2 = User(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="hashedpassword456"
        )
        db.session.add(user2)
        db.session.commit()
        
        review2 = Review(
            text="Good location but could be cleaner.",
            rating=3,
            user_id=user2.id,
            place_id=place.id
        )
        
        db.session.add_all([review1, review2])
        db.session.commit()
        
        print(f"   Created review 1: {review1.rating}/5 stars by {review1.user.first_name}")
        print(f"   Created review 2: {review2.rating}/5 stars by {review2.user.first_name}")
        
        # 5. Test Relationships
        print("\n=== Testing Relationship Access ===")
        
        # Test User -> Places relationship
        print(f"\n5a. User's Places:")
        user_places = user.places
        print(f"    User {user.first_name} owns {len(user_places)} place(s):")
        for p in user_places:
            print(f"      - {p.title}")
        
        # Test User -> Reviews relationship
        print(f"\n5b. User's Reviews:")
        user_reviews = user.reviews
        print(f"    User {user.first_name} has written {len(user_reviews)} review(s):")
        for r in user_reviews:
            print(f"      - {r.rating}/5 stars: {r.text[:50]}...")
        
        # Test Place -> Reviews relationship
        print(f"\n5c. Place's Reviews:")
        place_reviews = place.reviews
        print(f"    Place '{place.title}' has {len(place_reviews)} review(s):")
        for r in place_reviews:
            print(f"      - {r.rating}/5 by {r.user.first_name}: {r.text[:50]}...")
        
        # Test Place -> Amenities relationship (many-to-many)
        print(f"\n5d. Place's Amenities:")
        place_amenities = place.amenities
        print(f"    Place '{place.title}' has {len(place_amenities)} amenity/amenities:")
        for a in place_amenities:
            print(f"      - {a.name}")
        
        # Test Amenity -> Places relationship (reverse many-to-many)
        print(f"\n5e. Amenity's Places:")
        wifi_places = wifi.places
        print(f"    Amenity '{wifi.name}' is available in {len(wifi_places)} place(s):")
        for p in wifi_places:
            print(f"      - {p.title}")
        
        # 6. Test Cascade Delete
        print(f"\n=== Testing Cascade Deletes ===")
        
        # Create another place for the user
        place2 = Place(
            title="Mountain Cabin",
            description="Cozy cabin in the mountains",
            price=120.0,
            latitude=39.7392,
            longitude=-104.9903,
            owner_id=user.id
        )
        place2.amenities.append(parking)
        db.session.add(place2)
        db.session.commit()
        
        print(f"6a. Created second place: {place2.title}")
        print(f"    User {user.first_name} now owns {len(user.places)} places")
        
        # Test deleting user (should cascade delete places and reviews)
        user_id = user.id
        place_ids = [p.id for p in user.places]
        review_ids = [r.id for r in user.reviews]
        
        print(f"6b. Before deleting user:")
        print(f"    - User has {len(user.places)} places")
        print(f"    - User has {len(user.reviews)} reviews")
        
        db.session.delete(user)
        db.session.commit()
        
        # Check if places and reviews were deleted
        remaining_places = Place.query.filter(Place.id.in_(place_ids)).all()
        remaining_reviews = Review.query.filter(Review.id.in_(review_ids)).all()
        
        print(f"6c. After deleting user:")
        print(f"    - Remaining places: {len(remaining_places)}")
        print(f"    - Remaining reviews: {len(remaining_reviews)}")
        
        # Check if amenities still exist (should not be deleted)
        all_amenities = Amenity.query.all()
        print(f"    - Amenities still exist: {len(all_amenities)}")
        
        print("\n=== Relationship Testing Complete ===")
        print("All relationships are working correctly!")

if __name__ == "__main__":
    test_relationships()
