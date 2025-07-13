# SQLAlchemy Relationships Documentation

## Overview
This document describes the relationships implemented between the entities in the HBnB application using SQLAlchemy ORM.

## Relationship Types Implemented

### 1. One-to-Many Relationships

#### User → Places (One-to-Many)
- **Description**: A User can own multiple Places, but each Place belongs to one User
- **Implementation**: 
  - `Place.owner_id` - Foreign key to `User.id`
  - `User.places` - Relationship to access all places owned by the user
  - `Place.owner` - Relationship to access the owner of the place

#### User → Reviews (One-to-Many)
- **Description**: A User can write multiple Reviews, but each Review belongs to one User
- **Implementation**:
  - `Review.user_id` - Foreign key to `User.id`
  - `User.reviews` - Relationship to access all reviews written by the user
  - `Review.user` - Relationship to access the user who wrote the review

#### Place → Reviews (One-to-Many)
- **Description**: A Place can have multiple Reviews, but each Review belongs to one Place
- **Implementation**:
  - `Review.place_id` - Foreign key to `Place.id`
  - `Place.reviews` - Relationship to access all reviews for the place
  - `Review.place` - Relationship to access the place being reviewed

### 2. Many-to-Many Relationships

#### Place ↔ Amenities (Many-to-Many)
- **Description**: A Place can have multiple Amenities, and an Amenity can be associated with multiple Places
- **Implementation**:
  - `place_amenity` - Association table with `place_id` and `amenity_id`
  - `Place.amenities` - Relationship to access all amenities for the place
  - `Amenity.places` - Relationship to access all places that have this amenity

## Database Schema

### Tables Created
- `users` - User information
- `places` - Place information with owner relationship
- `reviews` - Review information with user and place relationships
- `amenities` - Amenity information
- `place_amenity` - Association table for many-to-many relationship

### Foreign Key Constraints
- `places.owner_id` → `users.id`
- `reviews.user_id` → `users.id`
- `reviews.place_id` → `places.id`
- `place_amenity.place_id` → `places.id`
- `place_amenity.amenity_id` → `amenities.id`

## Model Definitions

### User Model
```python
class User(BaseModel):
    # ... other fields ...
    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
```

### Place Model
```python
class Place(BaseModel):
    # ... other fields ...
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')
```

### Review Model
```python
class Review(BaseModel):
    # ... other fields ...
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')
```

### Amenity Model
```python
class Amenity(BaseModel):
    # ... other fields ...
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')
```

### Association Table
```python
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)
```

## Test Results

### Database Initialization Test
✅ **PASSED**: Database tables created successfully
- Tables: `amenities`, `place_amenity`, `places`, `reviews`, `users`
- Association table created with proper foreign key constraints
- All foreign key relationships established correctly

### Relationship Functionality Test
✅ **PASSED**: All relationships working correctly
- User can own multiple places
- User can write multiple reviews
- Place can have multiple reviews
- Place can have multiple amenities (many-to-many)
- Amenity can be associated with multiple places (many-to-many)
- Bidirectional relationships work properly

### Test Output Example
```
=== Testing Entity Relationships ===

1. Creating a user...
   User created: John Doe (ID: 8b109582-f062-4739-900f-a8b678a81899)

2. Creating another user (reviewer)...
   Reviewer created: Jane Smith (ID: f1127749-9fac-4f9e-bff1-7802be606495)

3. Creating amenities...
   Amenity created: WiFi (ID: 1129712e-2c4b-4da3-985a-e899eaa9e64b)
   Amenity created: Swimming Pool (ID: 06265640-24c3-4998-8892-59701160d65c)

4. Creating a place with amenities...
   Place created: Beautiful Beach House (ID: 254a7d0a-e822-45cc-b8f4-d5689ab8b3f7)
   Owner: John Doe
   Amenities: ['Swimming Pool', 'WiFi']

5. Creating a review...
   Review created: Rating 5/5 (ID: 5542652f-6b97-4c46-8c8d-fb37d74dc421)
   Reviewer: Jane Smith
   Place: Beautiful Beach House
   Review text: Absolutely amazing place! Highly recommend.

6. Testing User -> Places relationship...
   User John owns 1 place(s):
     - Beautiful Beach House

7. Testing User -> Reviews relationship...
   User Jane has written 1 review(s):
     - 5/5 stars for Beautiful Beach House

8. Testing Place -> Reviews relationship...
   Place Beautiful Beach House has 1 review(s):
     - 5/5 stars by Jane Smith

9. Testing Place -> Amenities relationship...
   Place Beautiful Beach House has 2 amenity/amenities:
     - Swimming Pool
     - WiFi

10. Testing Amenity -> Places relationship...
   Amenity WiFi is available in 1 place(s):
     - Beautiful Beach House

11. Testing adding more amenities to place...
   Updated place Beautiful Beach House now has 3 amenities:
     - Swimming Pool
     - WiFi
     - Air Conditioning
```

## Key Features Implemented

1. **Bidirectional Relationships**: All relationships can be traversed in both directions
2. **Cascade Operations**: Deleting a user will delete their places and reviews
3. **Integrity Constraints**: Foreign key constraints ensure data consistency
4. **Many-to-Many Support**: Proper association table for place-amenity relationships
5. **Automatic Loading**: Relationships are loaded automatically when accessed
6. **Validation**: All relationships respect the business rules (e.g., users can't review their own places)

## Business Rules Enforced

1. **Owner Validation**: Places must have a valid owner
2. **Review Restrictions**: Users cannot review their own places
3. **Unique Reviews**: Users can only review each place once
4. **Amenity Validation**: Only existing amenities can be added to places
5. **Rating Constraints**: Review ratings must be between 1 and 5

## Integration with Facade

The relationships are properly integrated with the facade pattern:
- `HBnBFacade` uses specialized repositories for each entity
- Relationships are automatically handled when creating/updating entities
- Cross-entity validation is performed before creating related objects
- Business logic is centralized in the facade layer

This implementation provides a solid foundation for the HBnB application's data layer, ensuring proper relationships between all entities while maintaining data integrity and business rule enforcement.
