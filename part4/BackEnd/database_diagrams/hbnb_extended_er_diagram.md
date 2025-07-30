# HBnB Extended Database Entity-Relationship Diagram

## Extended Database Schema with Booking System

```mermaid
erDiagram
    USERS {
        string id PK "UUID Primary Key"
        string first_name "NOT NULL"
        string last_name "NOT NULL"
        string email "UNIQUE NOT NULL"
        string password "NOT NULL (bcrypt hashed)"
        boolean is_admin "DEFAULT FALSE"
        string phone "NULLABLE"
        date date_of_birth "NULLABLE"
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
        int max_guests "DEFAULT 1"
        int bedrooms "DEFAULT 1"
        int bathrooms "DEFAULT 1"
        boolean available "DEFAULT TRUE"
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
        string category "NULLABLE"
        text description "NULLABLE"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    PLACE_AMENITY {
        string place_id FK "PRIMARY KEY"
        string amenity_id FK "PRIMARY KEY"
    }
    
    BOOKINGS {
        string id PK "UUID Primary Key"
        string user_id FK "NOT NULL"
        string place_id FK "NOT NULL"
        date check_in_date "NOT NULL"
        date check_out_date "NOT NULL"
        int guests "NOT NULL"
        decimal total_price "NOT NULL"
        string status "DEFAULT 'pending'"
        text special_requests "NULLABLE"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    PAYMENTS {
        string id PK "UUID Primary Key"
        string booking_id FK "NOT NULL"
        decimal amount "NOT NULL"
        string payment_method "NOT NULL"
        string status "DEFAULT 'pending'"
        string transaction_id "NULLABLE"
        timestamp payment_date "NULLABLE"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    MESSAGES {
        string id PK "UUID Primary Key"
        string sender_id FK "NOT NULL"
        string receiver_id FK "NOT NULL"
        string booking_id FK "NULLABLE"
        text message "NOT NULL"
        boolean is_read "DEFAULT FALSE"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    %% Core Relationships
    USERS ||--o{ PLACES : "owns (owner_id)"
    USERS ||--o{ REVIEWS : "writes (user_id)"
    PLACES ||--o{ REVIEWS : "has (place_id)"
    PLACES ||--o{ PLACE_AMENITY : "has (place_id)"
    AMENITIES ||--o{ PLACE_AMENITY : "belongs_to (amenity_id)"
    
    %% Extended Relationships
    USERS ||--o{ BOOKINGS : "makes (user_id)"
    PLACES ||--o{ BOOKINGS : "booked_for (place_id)"
    BOOKINGS ||--|| PAYMENTS : "paid_via (booking_id)"
    USERS ||--o{ MESSAGES : "sends (sender_id)"
    USERS ||--o{ MESSAGES : "receives (receiver_id)"
    BOOKINGS ||--o{ MESSAGES : "related_to (booking_id)"
```

## Additional Relationships in Extended Schema

### New One-to-Many Relationships

4. **USERS → BOOKINGS** (One-to-Many)
   - A user can make multiple bookings
   - Each booking is made by exactly one user
   - Foreign Key: `bookings.user_id` → `users.id`

5. **PLACES → BOOKINGS** (One-to-Many)
   - A place can have multiple bookings
   - Each booking is for exactly one place
   - Foreign Key: `bookings.place_id` → `places.id`

6. **USERS → MESSAGES (Sender)** (One-to-Many)
   - A user can send multiple messages
   - Each message has exactly one sender
   - Foreign Key: `messages.sender_id` → `users.id`

7. **USERS → MESSAGES (Receiver)** (One-to-Many)
   - A user can receive multiple messages
   - Each message has exactly one receiver
   - Foreign Key: `messages.receiver_id` → `users.id`

8. **BOOKINGS → MESSAGES** (One-to-Many)
   - A booking can have multiple related messages
   - Each message can be related to zero or one booking
   - Foreign Key: `messages.booking_id` → `bookings.id`

### One-to-One Relationships

9. **BOOKINGS → PAYMENTS** (One-to-One)
   - Each booking has exactly one payment
   - Each payment is for exactly one booking
   - Foreign Key: `payments.booking_id` → `bookings.id`

## Business Rules in Extended Schema

### Booking Constraints
- Check-in date must be before check-out date
- Booking dates cannot overlap for the same place
- Number of guests cannot exceed place's maximum capacity
- Users cannot book their own places

### Payment Constraints
- Payment amount must match booking total price
- Payment status must be one of: 'pending', 'completed', 'failed', 'refunded'
- Payment date is required when status is 'completed'

### Message Constraints
- Sender and receiver must be different users
- Messages related to bookings must involve the booking's user or place owner

## Status Enums

### Booking Status
- `pending`: Awaiting confirmation
- `confirmed`: Booking confirmed
- `cancelled`: Booking cancelled
- `completed`: Stay completed

### Payment Status
- `pending`: Payment not yet processed
- `completed`: Payment successful
- `failed`: Payment failed
- `refunded`: Payment refunded

## Extended Entity Purposes

### BOOKINGS Table
- Manages reservation system
- Tracks booking details and status
- Links users to places with dates
- Stores pricing and guest information

### PAYMENTS Table
- Handles payment processing
- Links to booking for financial tracking
- Stores transaction details
- Supports different payment methods

### MESSAGES Table
- Enables communication between users
- Supports booking-related discussions
- Maintains message history
- Tracks read/unread status
