# Mermaid Syntax Test

## Test 1: Basic Entity Definition (Fixed)
```mermaid
erDiagram
    TEST_ENTITY {
        string id PK "Primary Key"
        string name UK "Unique Key"
        string foreign_id FK "Foreign Key"
    }
```

## Test 2: Simple Relationship
```mermaid
erDiagram
    USER {
        string id PK
        string email UK
        string name
    }
    
    PLACE {
        string id PK
        string title
        string owner_id FK
    }
    
    USER ||--o{ PLACE : "owns"
```

## Test 3: Complex Relationships
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
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    
    %% Many-to-Many Relationship
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "belongs_to"
```

## Syntax Validation

All diagrams above should now render correctly in:
- GitHub/GitLab markdown
- Mermaid Live Editor
- VS Code with Mermaid extension

The key fixes were:
1. Adding `erDiagram` declaration at the start of each diagram
2. Fixing entity name references to be consistent
3. Ensuring proper indentation and syntax
