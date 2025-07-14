# HBnB Database Entity-Relationship Diagram

## Main Database Schema

```mermaid
erDiagram
    USERS {
        string id PK "UUID Primary Key"
        string first_name "NOT NULL"
        string last_name "NOT NULL"
        string email "UNIQUE NOT NULL"
        string password "NOT NULL (bcrypt hashed)"
        boolean is_admin "DEFAULT FALSE"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    PLACES {
        string id PK "UUID Primary Key"
        string title "NOT NULL"
        text description "NULLABLE"
        decimal price "NOT NULL"
        float latitude "NOT NULL"
        float longitude "NOT NULL"
        string owner_id FK "NOT NULL"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    REVIEWS {
        string id PK "UUID Primary Key"
        text text "NOT NULL"
        int rating "NOT NULL CHECK (1-5)"
        string user_id FK "NOT NULL"
        string place_id FK "NOT NULL"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    AMENITIES {
        string id PK "UUID Primary Key"
        string name "UNIQUE NOT NULL"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    PLACE_AMENITY {
        string place_id FK "PRIMARY KEY"
        string amenity_id FK "PRIMARY KEY"
    }
    
    %% Relationships
    USERS ||--o{ PLACES : "owns (owner_id)"
    USERS ||--o{ REVIEWS : "writes (user_id)"
    PLACES ||--o{ REVIEWS : "has (place_id)"
    PLACES ||--o{ PLACE_AMENITY : "has (place_id)"
    AMENITIES ||--o{ PLACE_AMENITY : "belongs_to (amenity_id)"
```

## Relationship Explanations

### One-to-Many Relationships

1. **USERS → PLACES** (One-to-Many)
   - A user can own multiple places
   - Each place has exactly one owner
   - Foreign Key: `places.owner_id` → `users.id`

2. **USERS → REVIEWS** (One-to-Many)
   - A user can write multiple reviews
   - Each review is written by exactly one user
   - Foreign Key: `reviews.user_id` → `users.id`

3. **PLACES → REVIEWS** (One-to-Many)
   - A place can have multiple reviews
   - Each review is for exactly one place
   - Foreign Key: `reviews.place_id` → `places.id`

### Many-to-Many Relationships

1. **PLACES ↔ AMENITIES** (Many-to-Many)
   - A place can have multiple amenities
   - An amenity can be available in multiple places
   - Junction Table: `place_amenity` with composite primary key
   - Foreign Keys: `place_amenity.place_id` → `places.id`, `place_amenity.amenity_id` → `amenities.id`

## Database Constraints

- **Primary Keys**: All tables use UUID format for primary keys
- **Foreign Keys**: All references include `ON DELETE CASCADE`
- **Unique Constraints**: 
  - `users.email` (unique email addresses)
  - `amenities.name` (unique amenity names)
  - `reviews(user_id, place_id)` (one review per user per place)
- **Check Constraints**: 
  - `reviews.rating` must be between 1 and 5
- **NOT NULL Constraints**: All required fields are enforced
