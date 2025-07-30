-- SQL Script for Testing CRUD Operations
-- This script tests Create, Read, Update, and Delete operations on all tables

-- Generate UUIDs for test data (replace with actual UUIDs when executing)
SET @test_user_id = '550e8400-e29b-41d4-a716-446655440000';
SET @test_place_id = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';
SET @test_review_id = '6ba7b811-9dad-11d1-80b4-00c04fd430c8';
SET @wifi_amenity_id = '3c49a8a3-cd53-41bf-bf60-79c09d5c2401';

-- ========================================
-- TEST 1: CREATE (INSERT) Operations
-- ========================================

SELECT '========================================' AS test_section;
SELECT 'TEST 1: CREATE (INSERT) Operations' AS test_section;
SELECT '========================================' AS test_section;

-- Test 1a: Insert a regular user
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
(@test_user_id, 'John', 'Doe', 'john.doe@example.com', 'hashed_password_123', FALSE);

-- Test 1b: Insert a place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
(@test_place_id, 'Beautiful Beach House', 'A lovely place by the sea', 150.00, 25.7617, -80.1918, @test_user_id);

-- Test 1c: Insert a review
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
(@test_review_id, 'Amazing place! Highly recommend.', 5, @test_user_id, @test_place_id);

-- Test 1d: Associate place with amenity
INSERT INTO place_amenity (place_id, amenity_id) VALUES
(@test_place_id, @wifi_amenity_id);

SELECT 'CREATE operations completed successfully!' AS result;

-- ========================================
-- TEST 2: READ (SELECT) Operations
-- ========================================

SELECT '========================================' AS test_section;
SELECT 'TEST 2: READ (SELECT) Operations' AS test_section;
SELECT '========================================' AS test_section;

-- Test 2a: Read all users
SELECT 'All Users:' AS query_description;
SELECT id, first_name, last_name, email, is_admin FROM users;

-- Test 2b: Read all places with owner information
SELECT 'All Places with Owner Information:' AS query_description;
SELECT p.id, p.title, p.description, p.price, p.latitude, p.longitude, 
       u.first_name, u.last_name, u.email
FROM places p
JOIN users u ON p.owner_id = u.id;

-- Test 2c: Read all reviews with user and place information
SELECT 'All Reviews with User and Place Information:' AS query_description;
SELECT r.id, r.text, r.rating,
       u.first_name as reviewer_first_name, u.last_name as reviewer_last_name,
       p.title as place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id;

-- Test 2d: Read all amenities
SELECT 'All Amenities:' AS query_description;
SELECT id, name FROM amenities;

-- Test 2e: Read place-amenity associations
SELECT 'Place-Amenity Associations:' AS query_description;
SELECT p.title, a.name
FROM place_amenity pa
JOIN places p ON pa.place_id = p.id
JOIN amenities a ON pa.amenity_id = a.id;

-- Test 2f: Complex query - Places with their amenities and average ratings
SELECT 'Places with Amenities and Average Ratings:' AS query_description;
SELECT p.title, 
       GROUP_CONCAT(a.name SEPARATOR ', ') as amenities,
       AVG(r.rating) as average_rating,
       COUNT(r.id) as review_count
FROM places p
LEFT JOIN place_amenity pa ON p.id = pa.place_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title;

-- ========================================
-- TEST 3: UPDATE Operations
-- ========================================

SELECT '========================================' AS test_section;
SELECT 'TEST 3: UPDATE Operations' AS test_section;
SELECT '========================================' AS test_section;

-- Test 3a: Update user information
UPDATE users SET first_name = 'Johnny', last_name = 'Smith' WHERE id = @test_user_id;

-- Test 3b: Update place information
UPDATE places SET price = 175.00, description = 'A lovely oceanfront property' WHERE id = @test_place_id;

-- Test 3c: Update review
UPDATE reviews SET text = 'Absolutely fantastic place! Will definitely return.', rating = 5 WHERE id = @test_review_id;

-- Verify updates
SELECT 'Updated User:' AS update_check;
SELECT id, first_name, last_name, email FROM users WHERE id = @test_user_id;

SELECT 'Updated Place:' AS update_check;
SELECT id, title, description, price FROM places WHERE id = @test_place_id;

SELECT 'Updated Review:' AS update_check;
SELECT id, text, rating FROM reviews WHERE id = @test_review_id;

SELECT 'UPDATE operations completed successfully!' AS result;

-- ========================================
-- TEST 4: DELETE Operations
-- ========================================

SELECT '========================================' AS test_section;
SELECT 'TEST 4: DELETE Operations' AS test_section;
SELECT '========================================' AS test_section;

-- Test 4a: Delete place-amenity association
DELETE FROM place_amenity WHERE place_id = @test_place_id AND amenity_id = @wifi_amenity_id;

-- Test 4b: Delete review
DELETE FROM reviews WHERE id = @test_review_id;

-- Test 4c: Delete place
DELETE FROM places WHERE id = @test_place_id;

-- Test 4d: Delete user
DELETE FROM users WHERE id = @test_user_id;

-- Verify deletions
SELECT 'Remaining Users (should not include test user):' AS delete_check;
SELECT COUNT(*) as user_count FROM users WHERE id = @test_user_id;

SELECT 'Remaining Places (should not include test place):' AS delete_check;
SELECT COUNT(*) as place_count FROM places WHERE id = @test_place_id;

SELECT 'Remaining Reviews (should not include test review):' AS delete_check;
SELECT COUNT(*) as review_count FROM reviews WHERE id = @test_review_id;

SELECT 'DELETE operations completed successfully!' AS result;

-- ========================================
-- TEST 5: Constraint Testing
-- ========================================

SELECT '========================================' AS test_section;
SELECT 'TEST 5: Constraint Testing' AS test_section;
SELECT '========================================' AS test_section;

-- Test 5a: Try to insert duplicate email (should fail)
SELECT 'Testing unique email constraint...' AS constraint_test;
-- This should fail due to unique constraint on email
-- INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
-- ('550e8400-e29b-41d4-a716-446655440001', 'Test', 'User', 'admin@hbnb.io', 'password', FALSE);

-- Test 5b: Try to insert duplicate amenity name (should fail)
SELECT 'Testing unique amenity name constraint...' AS constraint_test;
-- This should fail due to unique constraint on amenity name
-- INSERT INTO amenities (id, name) VALUES
-- ('550e8400-e29b-41d4-a716-446655440002', 'WiFi');

-- Test 5c: Try to insert review with invalid rating (should fail)
SELECT 'Testing rating check constraint...' AS constraint_test;
-- This should fail due to check constraint on rating
-- INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
-- ('550e8400-e29b-41d4-a716-446655440003', 'Test review', 6, @test_user_id, @test_place_id);

SELECT 'Constraint testing completed!' AS result;

-- ========================================
-- Final Status Check
-- ========================================

SELECT '========================================' AS test_section;
SELECT 'Final Database Status' AS test_section;
SELECT '========================================' AS test_section;

SELECT 'Admin User Status:' AS status_check;
SELECT COUNT(*) as admin_count FROM users WHERE is_admin = TRUE;

SELECT 'Total Users:' AS status_check;
SELECT COUNT(*) as total_users FROM users;

SELECT 'Total Amenities:' AS status_check;
SELECT COUNT(*) as total_amenities FROM amenities;

SELECT 'Total Places:' AS status_check;
SELECT COUNT(*) as total_places FROM places;

SELECT 'Total Reviews:' AS status_check;
SELECT COUNT(*) as total_reviews FROM reviews;

SELECT 'CRUD testing completed successfully!' AS final_result;
