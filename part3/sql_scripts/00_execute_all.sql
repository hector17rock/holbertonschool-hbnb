-- Master SQL Script for HBnB Database Setup and Testing
-- This script executes all database setup and testing scripts in the correct order

-- ========================================
-- STEP 1: Database Schema Creation
-- ========================================

SELECT '========================================' AS step;
SELECT 'STEP 1: Creating Database Schema' AS step;
SELECT '========================================' AS step;

-- Execute table creation script
SOURCE 01_create_tables.sql;

-- ========================================
-- STEP 2: Initial Data Insertion
-- ========================================

SELECT '========================================' AS step;
SELECT 'STEP 2: Inserting Initial Data' AS step;
SELECT '========================================' AS step;

-- Execute initial data insertion script
SOURCE 02_insert_initial_data.sql;

-- ========================================
-- STEP 3: CRUD Operations Testing
-- ========================================

SELECT '========================================' AS step;
SELECT 'STEP 3: Testing CRUD Operations' AS step;
SELECT '========================================' AS step;

-- Execute CRUD testing script
SOURCE 03_test_crud_operations.sql;

-- ========================================
-- FINAL STATUS
-- ========================================

SELECT '========================================' AS final_status;
SELECT 'All scripts executed successfully!' AS final_status;
SELECT '========================================' AS final_status;

-- Display final database status
SELECT 'Final Database Summary:' AS summary;
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM users WHERE is_admin = TRUE) as admin_users,
    (SELECT COUNT(*) FROM places) as total_places,
    (SELECT COUNT(*) FROM reviews) as total_reviews,
    (SELECT COUNT(*) FROM amenities) as total_amenities,
    (SELECT COUNT(*) FROM place_amenity) as place_amenity_associations;
