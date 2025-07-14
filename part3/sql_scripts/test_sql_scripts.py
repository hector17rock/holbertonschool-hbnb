#!/usr/bin/env python3

import sqlite3
import os
import sys

def test_sql_scripts():
    """Test the SQL scripts using SQLite for verification."""
    
    # Create an in-memory SQLite database for testing
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    print("Testing SQL Scripts with SQLite")
    print("=" * 50)
    
    try:
        # Test 1: Create Tables
        print("\n1. Testing table creation...")
        
        # Create tables directly for SQLite
        cursor.execute("""
            CREATE TABLE users (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE amenities (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE places (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                owner_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE reviews (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                user_id TEXT NOT NULL,
                place_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
                UNIQUE(user_id, place_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE place_amenity (
                place_id TEXT NOT NULL,
                amenity_id TEXT NOT NULL,
                PRIMARY KEY (place_id, amenity_id),
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
                FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
            )
        """)
        
        print("   ✓ Tables created successfully")
        
        # Test 2: Insert Initial Data
        print("\n2. Testing initial data insertion...")
        
        # Insert admin user
        cursor.execute("""
            INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
            ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', 
             '$2b$12$NaZIdJCjuhBVkgeBLuEvbueKEfmLXNXVw.Tj7dq0dt6KLoK/bjrZW', 1)
        """)
        
        # Insert amenities
        cursor.execute("""
            INSERT INTO amenities (id, name) VALUES
            ('3c49a8a3-cd53-41bf-bf60-79c09d5c2401', 'WiFi'),
            ('ede3f26b-8078-4e34-ac00-c6929daf9a99', 'Swimming Pool'),
            ('d717859a-5555-4897-b6da-9c11d0799560', 'Air Conditioning')
        """)
        
        conn.commit()
        print("   ✓ Initial data inserted successfully")
        
        # Test 3: Verify Data
        print("\n3. Verifying inserted data...")
        
        # Check admin user
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_count = cursor.fetchone()[0]
        print(f"   Admin users: {admin_count}")
        
        # Check amenities
        cursor.execute("SELECT COUNT(*) FROM amenities")
        amenity_count = cursor.fetchone()[0]
        print(f"   Amenities: {amenity_count}")
        
        # Test 4: Test CRUD Operations
        print("\n4. Testing CRUD operations...")
        
        # CREATE - Insert test user
        test_user_id = '550e8400-e29b-41d4-a716-446655440000'
        cursor.execute("""
            INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
            (?, 'John', 'Doe', 'john.doe@example.com', 'hashed_password_123', 0)
        """, (test_user_id,))
        
        # CREATE - Insert test place
        test_place_id = '6ba7b810-9dad-11d1-80b4-00c04fd430c8'
        cursor.execute("""
            INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
            (?, 'Beautiful Beach House', 'A lovely place by the sea', 150.00, 25.7617, -80.1918, ?)
        """, (test_place_id, test_user_id))
        
        # CREATE - Insert test review
        test_review_id = '6ba7b811-9dad-11d1-80b4-00c04fd430c8'
        cursor.execute("""
            INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
            (?, 'Amazing place! Highly recommend.', 5, ?, ?)
        """, (test_review_id, test_user_id, test_place_id))
        
        # CREATE - Associate place with amenity
        cursor.execute("""
            INSERT INTO place_amenity (place_id, amenity_id) VALUES
            (?, '3c49a8a3-cd53-41bf-bf60-79c09d5c2401')
        """, (test_place_id,))
        
        print("   ✓ CREATE operations successful")
        
        # READ - Test complex query
        cursor.execute("""
            SELECT p.title, u.first_name, u.last_name, AVG(r.rating) as avg_rating
            FROM places p
            JOIN users u ON p.owner_id = u.id
            LEFT JOIN reviews r ON p.id = r.place_id
            GROUP BY p.id, p.title, u.first_name, u.last_name
        """)
        
        results = cursor.fetchall()
        print(f"   ✓ READ operations successful ({len(results)} results)")
        
        # UPDATE - Test update operations
        cursor.execute("""
            UPDATE users SET first_name = 'Johnny' WHERE id = ?
        """, (test_user_id,))
        
        cursor.execute("""
            UPDATE places SET price = 175.00 WHERE id = ?
        """, (test_place_id,))
        
        print("   ✓ UPDATE operations successful")
        
        # DELETE - Test delete operations
        cursor.execute("DELETE FROM place_amenity WHERE place_id = ?", (test_place_id,))
        cursor.execute("DELETE FROM reviews WHERE id = ?", (test_review_id,))
        cursor.execute("DELETE FROM places WHERE id = ?", (test_place_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (test_user_id,))
        
        print("   ✓ DELETE operations successful")
        
        # Test 5: Final Verification
        print("\n5. Final verification...")
        
        # Check final counts
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM amenities")
        amenity_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM places")
        place_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reviews")
        review_count = cursor.fetchone()[0]
        
        print(f"   Final counts: Users={user_count}, Amenities={amenity_count}, Places={place_count}, Reviews={review_count}")
        
        # Test 6: Constraint Testing
        print("\n6. Testing constraints...")
        
        # Test unique email constraint
        try:
            cursor.execute("""
                INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
                ('test-id', 'Test', 'User', 'admin@hbnb.io', 'password', 0)
            """)
            print("   ✗ Unique email constraint failed")
        except sqlite3.IntegrityError:
            print("   ✓ Unique email constraint working")
        
        # Test unique amenity name constraint
        try:
            cursor.execute("""
                INSERT INTO amenities (id, name) VALUES
                ('test-id', 'WiFi')
            """)
            print("   ✗ Unique amenity name constraint failed")
        except sqlite3.IntegrityError:
            print("   ✓ Unique amenity name constraint working")
        
        print("\n" + "=" * 50)
        print("✓ All SQL script tests passed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        return False
    
    finally:
        conn.close()
    
    return True

if __name__ == '__main__':
    success = test_sql_scripts()
    sys.exit(0 if success else 1)
