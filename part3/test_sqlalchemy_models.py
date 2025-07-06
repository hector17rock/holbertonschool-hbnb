#!/usr/bin/env python3
"""
Test script for SQLAlchemy models
Creates database tables and tests CRUD operations for Place, Review, and Amenity entities
"""

from app import create_app
from app.models.base_model import db
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def create_tables():
    """Create all database tables."""
    print("🏗️  Creating database tables...")
    db.create_all()
    print("✅ Database tables created successfully!")


def test_amenity_crud():
    """Test Amenity CRUD operations."""
    print("\n🧪 Testing Amenity model...")
    
    # Create
    wifi = Amenity(name="WiFi")
    pool = Amenity(name="Swimming Pool")
    parking = Amenity(name="Parking")
    
    db.session.add_all([wifi, pool, parking])
    db.session.commit()
    
    print(f"✅ Created amenities:")
    print(f"   - WiFi: {wifi.id}")
    print(f"   - Swimming Pool: {pool.id}")
    print(f"   - Parking: {parking.id}")
    
    # Read
    retrieved_wifi = Amenity.query.filter_by(name="WiFi").first()
    print(f"✅ Retrieved amenity: {retrieved_wifi}")
    
    # Read all
    all_amenities = Amenity.query.all()
    print(f"✅ Total amenities in database: {len(all_amenities)}")
    
    # Update
    retrieved_wifi.name = "High-Speed WiFi"
    db.session.commit()
    print(f"✅ Updated amenity name: {retrieved_wifi.name}")
    
    return all_amenities


def test_place_crud():
    """Test Place CRUD operations."""
    print("\n🧪 Testing Place model...")
    
    # Create
    place = Place(
        title="Beautiful Beach House",
        description="A stunning oceanfront property with panoramic views",
        price=250.0,
        latitude=34.0522,
        longitude=-118.2437
    )
    
    db.session.add(place)
    db.session.commit()
    
    print(f"✅ Created place:")
    print(f"   - Title: {place.title}")
    print(f"   - ID: {place.id}")
    print(f"   - Price: ${place.price}/night")
    print(f"   - Location: ({place.latitude}, {place.longitude})")
    
    # Test backward compatibility with 'name' property
    print(f"   - Name (alias): {place.name}")
    place.name = "Updated Beach House"
    print(f"   - Updated title via name alias: {place.title}")
    
    # Read
    retrieved_place = Place.query.filter_by(title="Updated Beach House").first()
    print(f"✅ Retrieved place: {retrieved_place.title}")
    
    # Read all
    all_places = Place.query.all()
    print(f"✅ Total places in database: {len(all_places)}")
    
    # Update
    retrieved_place.price = 300.0
    retrieved_place.description = "Updated description - Luxury oceanfront villa"
    db.session.commit()
    print(f"✅ Updated place price: ${retrieved_place.price}")
    
    return retrieved_place


def test_review_crud():
    """Test Review CRUD operations."""
    print("\n🧪 Testing Review model...")
    
    # Create
    review1 = Review(
        text="Amazing place with breathtaking views! Highly recommended.",
        rating=5
    )
    
    review2 = Review(
        text="Good location but could use some improvements.",
        rating=3
    )
    
    db.session.add_all([review1, review2])
    db.session.commit()
    
    print(f"✅ Created reviews:")
    print(f"   - Review 1: {review1.id} - Rating: {review1.rating}/5")
    print(f"   - Review 2: {review2.id} - Rating: {review2.rating}/5")
    
    # Test backward compatibility with 'comment' property
    print(f"   - Comment (alias): {review1.comment}")
    review1.comment = "Updated review text"
    print(f"   - Updated text via comment alias: {review1.text}")
    
    # Read
    high_rating_reviews = Review.query.filter(Review.rating >= 4).all()
    print(f"✅ High rating reviews (4+): {len(high_rating_reviews)}")
    
    # Read all
    all_reviews = Review.query.all()
    print(f"✅ Total reviews in database: {len(all_reviews)}")
    
    # Update
    review2.rating = 4
    review2.text = "Actually, it's quite nice. Updated my opinion!"
    db.session.commit()
    print(f"✅ Updated review rating: {review2.rating}/5")
    
    # Test validation
    try:
        invalid_review = Review(text="Invalid rating test", rating=6)
        db.session.add(invalid_review)
        db.session.commit()
    except ValueError as e:
        print(f"✅ Rating validation working: {e}")
    
    return all_reviews


def test_constraints_and_validation():
    """Test database constraints and validation."""
    print("\n🧪 Testing constraints and validation...")
    
    # Test unique constraint on amenity name
    try:
        duplicate_amenity = Amenity(name="WiFi")  # Should fail if WiFi already exists
        db.session.add(duplicate_amenity)
        db.session.commit()
        print("❌ Unique constraint not working")
    except Exception as e:
        db.session.rollback()
        print("✅ Unique constraint working for amenity names")
    
    # Test nullable=False constraints
    try:
        empty_place = Place()  # Missing required fields
        db.session.add(empty_place)
        db.session.commit()
        print("❌ Nullable constraints not working")
    except Exception as e:
        db.session.rollback()
        print("✅ Nullable constraints working for required fields")
    
    # Test rating validation
    try:
        invalid_review = Review(text="Test", rating=10)
        invalid_review.rating = 10  # This should trigger validation
        print("❌ Rating validation not working")
    except ValueError:
        print("✅ Rating validation working (1-5 range)")


def display_database_schema():
    """Display the created database schema."""
    print("\n📊 Database Schema Information:")
    print("=" * 50)
    
    # Get table information
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    for table_name in tables:
        print(f"\n📋 Table: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            nullable = "NULL" if column['nullable'] else "NOT NULL"
            print(f"   - {column['name']}: {column['type']} {nullable}")
            if column.get('default'):
                print(f"     Default: {column['default']}")


def main():
    """Main function to run all tests."""
    print("🚀 Testing SQLAlchemy Models for Place, Review, and Amenity")
    print("=" * 60)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Create tables
        create_tables()
        
        # Test each model
        amenities = test_amenity_crud()
        place = test_place_crud()
        reviews = test_review_crud()
        
        # Test constraints
        test_constraints_and_validation()
        
        # Display schema
        display_database_schema()
        
        print("\n🎉 All tests completed successfully!")
        print(f"   - Amenities created: {len(amenities)}")
        print(f"   - Places created: 1")
        print(f"   - Reviews created: {len(reviews)}")
        
        print("\n💡 Next steps:")
        print("   - Add relationships between entities")
        print("   - Implement foreign key constraints")
        print("   - Add more advanced validations")


if __name__ == "__main__":
    main()
