# HBnB Database Relationship Types Diagram

## Relationship Types Visualization

```mermaid
erDiagram
    USER {
        string id PK
        string email UK
        string first_name
        string last_name
        boolean is_admin
    }
    
    PLACE {
        string id PK
        string title
        decimal price
        string owner_id FK
    }
    
    REVIEW {
        string id PK
        int rating
        string user_id FK
        string place_id FK
    }
    
    AMENITY {
        string id PK
        string name UK
    }
    
    PLACE_AMENITY {
        string place_id FK
        string amenity_id FK
    }
    
    %% One-to-Many Relationships
    USER ||--o{ PLACE : "ONE user OWNS many places"
    USER ||--o{ REVIEW : "ONE user WRITES many reviews"
    PLACE ||--o{ REVIEW : "ONE place HAS many reviews"
    
    %% Many-to-Many Relationship
    PLACE ||--o{ PLACE_AMENITY : "ONE place HAS many amenities"
    AMENITY ||--o{ PLACE_AMENITY : "ONE amenity BELONGS TO many places"
```

## Relationship Cardinality Explanation

### Mermaid.js Relationship Notation

| Notation | Meaning | Description |
|----------|---------|-------------|
| `||--o{` | One-to-Many | One entity relates to many entities |
| `}o--||` | Many-to-One | Many entities relate to one entity |
| `||--||` | One-to-One | One entity relates to exactly one entity |
| `}o--o{` | Many-to-Many | Many entities relate to many entities |

### Our Database Relationships

1. **USER ||--o{ PLACE** (One-to-Many)
   - **Left side (||)**: One user
   - **Right side (o{)**: Many places
   - **Meaning**: One user can own multiple places

2. **USER ||--o{ REVIEW** (One-to-Many)
   - **Left side (||)**: One user
   - **Right side (o{)**: Many reviews
   - **Meaning**: One user can write multiple reviews

3. **PLACE ||--o{ REVIEW** (One-to-Many)
   - **Left side (||)**: One place
   - **Right side (o{)**: Many reviews
   - **Meaning**: One place can have multiple reviews

4. **PLACE ||--o{ PLACE_AMENITY** (One-to-Many)
   - **Left side (||)**: One place
   - **Right side (o{)**: Many place_amenity records
   - **Meaning**: One place can have multiple amenities

5. **AMENITY ||--o{ PLACE_AMENITY** (One-to-Many)
   - **Left side (||)**: One amenity
   - **Right side (o{)**: Many place_amenity records
   - **Meaning**: One amenity can belong to multiple places

## Many-to-Many Relationship Breakdown

The **PLACE ↔ AMENITY** many-to-many relationship is implemented using a junction table:

```mermaid
erDiagram
    PLACE {
        string id PK
        string title
    }
    
    AMENITY {
        string id PK
        string name
    }
    
    PLACE_AMENITY {
        string place_id FK
        string amenity_id FK
    }
    
    PLACE ||--o{ PLACE_AMENITY : "place_id"
    AMENITY ||--o{ PLACE_AMENITY : "amenity_id"
```

### How Many-to-Many Works

1. **Direct Relationship**: PLACE ↔ AMENITY (Many-to-Many)
2. **Implementation**: Through junction table PLACE_AMENITY
3. **Breakdown**: 
   - PLACE → PLACE_AMENITY (One-to-Many)
   - AMENITY → PLACE_AMENITY (One-to-Many)
4. **Result**: A place can have multiple amenities, and an amenity can belong to multiple places

## Foreign Key Constraints

```mermaid
erDiagram
    USERS {
        string id PK "Primary Key"
    }
    
    PLACES {
        string id PK "Primary Key"
        string owner_id FK "→ USERS.id"
    }
    
    REVIEWS {
        string id PK "Primary Key"
        string user_id FK "→ USERS.id"
        string place_id FK "→ PLACES.id"
    }
    
    PLACE_AMENITY {
        string place_id FK "→ PLACES.id"
        string amenity_id FK "→ AMENITIES.id"
    }
    
    AMENITIES {
        string id PK "Primary Key"
    }
    
    USERS ||--o{ PLACES : "owner_id"
    USERS ||--o{ REVIEWS : "user_id"
    PLACES ||--o{ REVIEWS : "place_id"
    PLACES ||--o{ PLACE_AMENITY : "place_id"
    AMENITIES ||--o{ PLACE_AMENITY : "amenity_id"
```

## Unique Constraints

```mermaid
erDiagram
    USERS {
        string id PK
        string email UK "UNIQUE"
        string first_name
        string last_name
    }
    
    AMENITIES {
        string id PK
        string name UK "UNIQUE"
    }
    
    REVIEWS {
        string id PK
        string user_id FK
        string place_id FK
        int rating
        string text
    }
    
    USERS ||--o{ REVIEWS : "user_id"
    PLACE ||--o{ REVIEWS : "place_id"
    
    %% Unique constraint on combination
    REVIEWS : "UNIQUE(user_id, place_id)"
```

### Unique Constraint Types

1. **Single Column Unique**: `users.email`, `amenities.name`
2. **Composite Unique**: `reviews(user_id, place_id)` - One review per user per place
3. **Primary Key Unique**: All `id` fields are unique by definition
