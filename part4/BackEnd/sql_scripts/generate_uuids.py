#!/usr/bin/env python3

import uuid
import bcrypt

def generate_uuids():
    """Generate UUIDs for initial data."""
    print("Generated UUIDs for initial data:")
    print("=" * 50)
    
    # Fixed admin UUID as specified
    admin_id = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"
    print(f"Admin User ID: {admin_id}")
    
    # Generate UUIDs for amenities
    amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
    amenity_uuids = {}
    
    print("\nAmenity UUIDs:")
    for amenity in amenities:
        amenity_uuid = str(uuid.uuid4())
        amenity_uuids[amenity] = amenity_uuid
        print(f"{amenity}: {amenity_uuid}")
    
    # Generate bcrypt hash for admin password
    password = 'admin1234'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"\nHashed password for admin: {hashed_password}")
    
    return admin_id, amenity_uuids, hashed_password

if __name__ == '__main__':
    admin_id, amenity_uuids, hashed_password = generate_uuids()
    
    # Generate SQL INSERT statements
    print("\n" + "=" * 50)
    print("SQL INSERT Statements:")
    print("=" * 50)
    
    # Admin user insert
    print("-- Insert Admin User")
    print(f"INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES")
    print(f"('{admin_id}', 'Admin', 'HBnB', 'admin@hbnb.io', '{hashed_password}', TRUE);")
    
    # Amenities insert
    print("\n-- Insert Amenities")
    print("INSERT INTO amenities (id, name) VALUES")
    amenity_values = []
    for amenity, uuid_val in amenity_uuids.items():
        amenity_values.append(f"('{uuid_val}', '{amenity}')")
    print(",\n".join(amenity_values) + ";")
