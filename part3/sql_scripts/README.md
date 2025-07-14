# HBnB Database SQL Scripts

This directory contains SQL scripts for creating and testing the HBnB database schema.

## Files Overview

- `00_execute_all.sql` - Master script that executes all other scripts in order
- `01_create_tables.sql` - Creates all database tables and relationships
- `02_insert_initial_data.sql` - Inserts initial data (admin user and amenities)
- `03_test_crud_operations.sql` - Tests CRUD operations on all tables
- `generate_uuids.py` - Python script to generate UUIDs and hashed passwords
- `README.md` - This documentation file

## Database Schema

### Tables Created

1. **users** - User information with authentication
2. **places** - Property listings with location and pricing
3. **reviews** - User reviews for places
4. **amenities** - Available amenities for places
5. **place_amenity** - Many-to-many relationship between places and amenities

### Relationships

- **User → Places** (One-to-Many): A user can own multiple places
- **User → Reviews** (One-to-Many): A user can write multiple reviews
- **Place → Reviews** (One-to-Many): A place can have multiple reviews
- **Place ↔ Amenities** (Many-to-Many): Places can have multiple amenities

### Constraints

- **Foreign Keys**: Proper referential integrity between tables
- **Unique Constraints**: Email addresses and amenity names must be unique
- **Check Constraints**: Review ratings must be between 1 and 5
- **Composite Unique**: Users can only review each place once

## Initial Data

### Admin User
- **ID**: `36c9050e-ddd3-4c3b-9731-9f487208bbc1` (fixed as specified)
- **Email**: `admin@hbnb.io`
- **Password**: `admin1234` (hashed with bcrypt)
- **Name**: Admin HBnB
- **Role**: Administrator

### Initial Amenities
- WiFi
- Swimming Pool
- Air Conditioning

## Usage Instructions

### Method 1: Execute All Scripts at Once

```bash
# Connect to your MySQL database
mysql -u your_username -p your_database_name

# Execute the master script
source /path/to/sql_scripts/00_execute_all.sql
```

### Method 2: Execute Scripts Individually

```bash
# Connect to MySQL
mysql -u your_username -p your_database_name

# Execute scripts in order
source /path/to/sql_scripts/01_create_tables.sql
source /path/to/sql_scripts/02_insert_initial_data.sql
source /path/to/sql_scripts/03_test_crud_operations.sql
```

### Method 3: Execute from Command Line

```bash
# Create database and tables
mysql -u your_username -p your_database_name < 01_create_tables.sql

# Insert initial data
mysql -u your_username -p your_database_name < 02_insert_initial_data.sql

# Test CRUD operations
mysql -u your_username -p your_database_name < 03_test_crud_operations.sql
```

## Generating New UUIDs

If you need to generate new UUIDs for testing or additional data:

```bash
cd sql_scripts
python generate_uuids.py
```

This script will generate:
- Fresh UUIDs for amenities
- A new bcrypt hash for the admin password
- Ready-to-use SQL INSERT statements

## Testing Database Functionality

The `03_test_crud_operations.sql` script performs comprehensive testing:

### CREATE Operations
- Inserts test users, places, reviews, and amenities
- Tests many-to-many relationships

### READ Operations
- Selects data from all tables
- Tests JOIN operations across related tables
- Demonstrates complex queries with aggregations

### UPDATE Operations
- Updates records in all tables
- Verifies data integrity after updates

### DELETE Operations
- Removes test data
- Verifies cascade delete operations

### Constraint Testing
- Tests unique constraints
- Validates check constraints
- Ensures foreign key integrity

## Expected Results

After running all scripts, you should have:

1. **Database Schema**: All tables created with proper relationships
2. **Initial Data**: Admin user and 3 amenities inserted
3. **Verified Functionality**: All CRUD operations working correctly
4. **Data Integrity**: All constraints and relationships enforced

## Database Summary

The final database will contain:
- 1 admin user (initially)
- 3 amenities (WiFi, Swimming Pool, Air Conditioning)
- 0 places (initially)
- 0 reviews (initially)
- 0 place-amenity associations (initially)

## Verification Queries

To verify the database is set up correctly:

```sql
-- Check admin user
SELECT * FROM users WHERE is_admin = TRUE;

-- Check amenities
SELECT * FROM amenities ORDER BY name;

-- Check table structure
DESCRIBE users;
DESCRIBE places;
DESCRIBE reviews;
DESCRIBE amenities;
DESCRIBE place_amenity;

-- Check foreign key constraints
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_SCHEMA = 'your_database_name'
AND REFERENCED_TABLE_NAME IS NOT NULL;
```

## Notes

- All UUIDs are in standard UUID4 format (36 characters)
- Passwords are hashed using bcrypt with salt rounds
- Timestamps are automatically managed by the database
- All foreign key constraints include `ON DELETE CASCADE` for data consistency
- The database is designed to work with both MySQL and compatible databases

## Troubleshooting

If you encounter issues:

1. **Permission Errors**: Ensure your MySQL user has CREATE, INSERT, UPDATE, DELETE privileges
2. **UUID Format**: Some databases may require different UUID handling
3. **Constraint Violations**: Check that foreign key references exist before inserting data
4. **Password Hashing**: Ensure bcrypt library is available for password generation

For additional help, refer to the MySQL documentation or contact your database administrator.
