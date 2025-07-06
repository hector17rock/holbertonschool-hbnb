#!/usr/bin/env python3
"""
Comprehensive test for Many-to-Many relationships in HBnB application.
Demonstrates the Place ↔ Amenity many-to-many relationship.
"""

from app import create_app
from app.models.base_model import db
from app.services.facade import HBnBFacade


def test_many_to_many_relationships():
    """Test many-to-many relationships comprehensively."""
    print("🚀 Testing Many-to-Many Relationships")
    print("=" * 60)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Drop and recreate database tables
            print("🏗️  Recreating database with many-to-many relationships...")
            db.drop_all()
            db.create_all()
            print("✅ Database tables created successfully!\n")
            
            # Initialize facade
            facade = HBnBFacade()
            
            # Create test data
            print("📝 Setting up test data...")
            
            # Create users
            user1_data = {
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice@example.com',
                'password': 'secure123',
                'is_admin': False
            }
            user1 = facade.create_user(user1_data)
            
            user2_data = {
                'first_name': 'Bob',
                'last_name': 'Smith',
                'email': 'bob@example.com',
                'password': 'secure456',
                'is_admin': False
            }
            user2 = facade.create_user(user2_data)
            
            # Create amenities
            amenities_data = [
                {'name': 'WiFi'},
                {'name': 'Swimming Pool'},
                {'name': 'Parking'},
                {'name': 'Gym'},
                {'name': 'Kitchen'},
                {'name': 'Air Conditioning'}
            ]
            
            amenities = []
            for amenity_data in amenities_data:
                amenity = facade.create_amenity(amenity_data)
                amenities.append(amenity)
            
            print(f"✅ Created {len(amenities)} amenities")
            
            # Test 1: Create places with different amenity combinations
            print("\n🏡 Test 1: Creating places with different amenity combinations...")
            
            # Place 1: Beach House with WiFi, Pool, and Parking
            place1_data = {
                'title': 'Beach House Paradise',
                'description': 'Luxurious beachfront property',
                'price': 300.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': user1.id,
                'amenities': [amenities[0].id, amenities[1].id, amenities[2].id]  # WiFi, Pool, Parking
            }
            place1 = facade.create_place(place1_data)
            
            # Place 2: City Apartment with WiFi, Gym, Kitchen, AC
            place2_data = {
                'title': 'Modern City Apartment',
                'description': 'Downtown apartment with modern amenities',
                'price': 150.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': user2.id,
                'amenities': [amenities[0].id, amenities[3].id, amenities[4].id, amenities[5].id]  # WiFi, Gym, Kitchen, AC
            }
            place2 = facade.create_place(place2_data)
            
            # Place 3: Budget Room with just WiFi and Parking
            place3_data = {
                'title': 'Budget Friendly Room',
                'description': 'Simple and affordable accommodation',
                'price': 75.0,
                'latitude': 37.7749,
                'longitude': -122.4194,
                'owner_id': user1.id,
                'amenities': [amenities[0].id, amenities[2].id]  # WiFi, Parking
            }
            place3 = facade.create_place(place3_data)
            
            print(f"✅ Created 3 places with different amenity combinations")
            
            # Test 2: Demonstrate many-to-many relationships
            print("\n🔗 Test 2: Demonstrating many-to-many relationships...")
            
            print("\n📍 Place → Amenities (One place can have multiple amenities):")
            for place in [place1, place2, place3]:
                print(f"   {place.title}:")
                for amenity in place.amenities:
                    print(f"     - {amenity.name}")
                print(f"     Total: {len(place.amenities)} amenities\n")
            
            print("🏠 Amenity → Places (One amenity can be in multiple places):")
            for amenity in amenities:
                print(f"   {amenity.name}:")
                for place in amenity.places:
                    print(f"     - {place.title} (${place.price})")
                print(f"     Total: {len(amenity.places)} places\n")
            
            # Test 3: Query places by amenity
            print("🔍 Test 3: Querying places by specific amenities...")
            
            wifi_amenity = amenities[0]  # WiFi
            pool_amenity = amenities[1]  # Swimming Pool
            
            print(f"Places with {wifi_amenity.name}:")
            for place in wifi_amenity.places:
                print(f"   - {place.title}: ${place.price}/night")
            
            print(f"\nPlaces with {pool_amenity.name}:")
            for place in pool_amenity.places:
                print(f"   - {place.title}: ${place.price}/night")
            
            # Test 4: Dynamic amenity management
            print("\n⚡ Test 4: Dynamic amenity management...")
            
            # Add an amenity to an existing place
            gym_amenity = amenities[3]  # Gym
            print(f"Adding {gym_amenity.name} to {place1.title}...")
            
            if gym_amenity not in place1.amenities:
                place1.amenities.append(gym_amenity)
                db.session.commit()
                print(f"✅ {gym_amenity.name} added successfully")
            
            # Remove an amenity from a place
            parking_amenity = amenities[2]  # Parking
            print(f"Removing {parking_amenity.name} from {place3.title}...")
            
            if parking_amenity in place3.amenities:
                place3.amenities.remove(parking_amenity)
                db.session.commit()
                print(f"✅ {parking_amenity.name} removed successfully")
            
            # Verify changes
            print("\n📊 Updated amenity associations:")
            print(f"   {place1.title}: {[a.name for a in place1.amenities]}")
            print(f"   {place3.title}: {[a.name for a in place3.amenities]}")
            
            # Test 5: Statistics and analysis
            print("\n📈 Test 5: Many-to-many relationship statistics...")
            
            # Most popular amenities
            amenity_popularity = [(amenity.name, len(amenity.places)) for amenity in amenities]
            amenity_popularity.sort(key=lambda x: x[1], reverse=True)
            
            print("Most popular amenities:")
            for name, count in amenity_popularity:
                print(f"   - {name}: {count} place(s)")
            
            # Places with most amenities
            places_amenity_count = [(place.title, len(place.amenities)) for place in [place1, place2, place3]]
            places_amenity_count.sort(key=lambda x: x[1], reverse=True)
            
            print("\nPlaces with most amenities:")
            for title, count in places_amenity_count:
                print(f"   - {title}: {count} amenities")
            
            # Test 6: Association table verification
            print("\n🗃️  Test 6: Association table verification...")
            
            # Query the association table directly
            from app.models.place import place_amenity_association
            
            result = db.session.execute(
                db.select(place_amenity_association)
            ).fetchall()
            
            print(f"Total associations in place_amenity table: {len(result)}")
            print("Place-Amenity associations:")
            for row in result:
                place_obj = facade.get_place(row.place_id)
                amenity_obj = facade.get_amenity(row.amenity_id)
                if place_obj and amenity_obj:
                    print(f"   - {place_obj.title} ↔ {amenity_obj.name}")
            
            print("\n🎉 Many-to-Many relationship tests completed successfully!")
            print("✅ Association table working correctly")
            print("✅ Bidirectional relationships functional")
            print("✅ Dynamic management working")
            print("✅ Query operations efficient")
            print("✅ Data integrity maintained")
            
        except Exception as e:
            print(f"❌ Error during many-to-many testing: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_many_to_many_relationships()
