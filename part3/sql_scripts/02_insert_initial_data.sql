-- SQL Script for HBnB Initial Data Insertion
-- This script inserts the required initial data into the database

-- Insert Admin User
-- Fixed ID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1
-- Email: admin@hbnb.io
-- Password: admin1234 (hashed with bcrypt)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$NaZIdJCjuhBVkgeBLuEvbueKEfmLXNXVw.Tj7dq0dt6KLoK/bjrZW', TRUE);

-- Insert Initial Amenities
-- Generated UUIDs for each amenity
INSERT INTO amenities (id, name) VALUES
('3c49a8a3-cd53-41bf-bf60-79c09d5c2401', 'WiFi'),
('ede3f26b-8078-4e34-ac00-c6929daf9a99', 'Swimming Pool'),
('d717859a-5555-4897-b6da-9c11d0799560', 'Air Conditioning');

-- Verify initial data insertion
SELECT 'Initial data inserted successfully!' AS status;

-- Display inserted data
SELECT 'Admin User:' AS section;
SELECT id, first_name, last_name, email, is_admin, created_at FROM users WHERE is_admin = TRUE;

SELECT 'Initial Amenities:' AS section;
SELECT id, name, created_at FROM amenities ORDER BY name;
