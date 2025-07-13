# User Model Mapping Implementation

This document outlines the implementation of User entity mapping to SQLAlchemy model, including the BaseModel mapping, UserRepository implementation, and Facade integration.

## Overview

The User model mapping provides a complete database persistence layer for user management in the HBnB application. This implementation includes:

- BaseModel mapping to SQLAlchemy with common attributes
- User model mapping with validation and constraints
- UserRepository with specialized user operations
- Facade integration for seamless business logic
- Database initialization and testing

## Architecture

### 1. BaseModel Mapping (`app/models/base_model.py`)

The BaseModel serves as the foundation for all entities with common attributes:

```python
class BaseModel(db.Model):
    __abstract__ = True  # Prevents table creation for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Key Features:**
- **Abstract Model**: Uses `__abstract__ = True` to prevent table creation
- **UUID Primary Key**: Uses UUID strings for unique identification
- **Timestamps**: Automatic creation and update timestamps
- **Auto-update**: `onupdate` parameter automatically updates timestamps

### 2. User Model Mapping (`app/models/user.py`)

The User model extends BaseModel with user-specific attributes:

```python
class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

**Key Features:**
- **Table Name**: Explicit table name 'users'
- **Constraints**: NOT NULL and UNIQUE constraints
- **Validation**: SQLAlchemy validators for email and names
- **Password Hashing**: Bcrypt integration for secure passwords
- **Admin Flag**: Boolean field for role-based access

### 3. Data Validation

The User model includes comprehensive validation:

```python
@validates('email')
def validate_email(self, key, email):
    if '@' not in email:
        raise ValueError("Invalid email format")
    return email

@validates('first_name', 'last_name')
def validate_name(self, key, name):
    if not name or len(name.strip()) == 0:
        raise ValueError(f"{key} cannot be empty")
    if len(name) > 50:
        raise ValueError(f"{key} cannot exceed 50 characters")
    return name.strip()
```

**Validation Rules:**
- **Email**: Must contain '@' symbol
- **Names**: Cannot be empty, max 50 characters
- **Automatic Trimming**: Removes leading/trailing whitespace

### 4. UserRepository Implementation (`app/services/repositories/user_repository.py`)

The UserRepository provides specialized user operations:

```python
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
    def get_admin_users(self):
        return self.model.query.filter_by(is_admin=True).all()
    
    def search_users_by_name(self, name_query):
        return self.model.query.filter(
            (User.first_name.ilike(f'%{name_query}%')) | 
            (User.last_name.ilike(f'%{name_query}%'))
        ).all()
```

**Repository Methods:**
- **get_user_by_email()**: Find user by email address
- **get_admin_users()**: Get all admin users
- **get_regular_users()**: Get all non-admin users
- **search_users_by_name()**: Search by first or last name
- **email_exists()**: Check if email is already taken

### 5. Facade Integration

The facade has been updated to use UserRepository:

```python
class HBnBFacade:
    def __init__(self):
        if use_sqlalchemy:
            self.user_repo = UserRepository()
        else:
            self.user_repo = InMemoryRepository()
    
    def get_user_by_email(self, email):
        if hasattr(self.user_repo, 'get_user_by_email'):
            return self.user_repo.get_user_by_email(email)
        return self.user_repo.get_by_attribute('email', email)
```

**Benefits:**
- **Backward Compatibility**: Works with both SQLAlchemy and InMemory repositories
- **Optimized Queries**: Uses specific UserRepository methods when available
- **Seamless Integration**: No changes required in business logic

## Database Schema

### Users Table Structure

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Database Constraints

- **Primary Key**: `id` (UUID string)
- **Unique Constraint**: `email` (prevents duplicate emails)
- **NOT NULL**: `first_name`, `last_name`, `email`, `password`
- **Default Values**: `is_admin` (false), timestamps (current time)

## Usage Examples

### 1. Database Initialization

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()  # Creates users table
```

### 2. Creating Users

```python
# Through UserRepository
user_repo = UserRepository()
user = User(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    is_admin=False
)
user.hash_password("password123")
user_repo.add(user)

# Through Facade
facade = HBnBFacade()
user_data = {
    'first_name': 'Jane',
    'last_name': 'Smith',
    'email': 'jane@example.com',
    'password': 'password123',
    'is_admin': False
}
user = facade.create_user(user_data)
```

### 3. Querying Users

```python
# Find by email
user = user_repo.get_user_by_email('john@example.com')

# Get all admin users
admins = user_repo.get_admin_users()

# Search by name
results = user_repo.search_users_by_name('John')

# Check if email exists
exists = user_repo.email_exists('john@example.com')
```

### 4. Password Operations

```python
# Hash password
user.hash_password('new_password')

# Verify password
is_valid = user.verify_password('password123')
```

## Testing

### Automated Testing

Run the comprehensive test suite:

```bash
python3 test_user_model.py
```

**Test Coverage:**
- Model creation and validation
- Password hashing and verification
- Repository operations
- Facade integration
- Database persistence
- Constraint validation

### Manual API Testing

Initialize the database:

```bash
python3 init_db.py
```

Test API endpoints:

```bash
# Get admin token
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.com", "password": "adminpass123"}'

# Create user (admin required)
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Test", "last_name": "User", "email": "test@example.com", "password": "password123"}'

# Get all users
curl -X GET "http://127.0.0.1:5000/api/v1/users/"
```

## Error Handling

### Validation Errors

```python
# Invalid email
ValueError: Invalid email format

# Empty name
ValueError: first_name cannot be empty

# Name too long
ValueError: first_name cannot exceed 50 characters
```

### Database Errors

```python
# Duplicate email
IntegrityError: UNIQUE constraint failed: users.email

# Missing required field
IntegrityError: NOT NULL constraint failed: users.first_name
```

## Performance Considerations

### Database Indexes

The implementation includes appropriate indexes:
- **Primary Key Index**: On `id` column
- **Unique Index**: On `email` column
- **Consider Adding**: Index on `is_admin` for role-based queries

### Query Optimization

```python
# Efficient email lookup
User.query.filter_by(email=email).first()

# Case-insensitive search
User.query.filter(User.first_name.ilike(f'%{query}%'))

# Admin user filtering
User.query.filter_by(is_admin=True).all()
```

## Security Features

### Password Security

- **Bcrypt Hashing**: Uses bcrypt for secure password storage
- **Salt Generation**: Automatic salt generation per password
- **Hash Verification**: Secure password verification

### Data Validation

- **Input Sanitization**: Automatic trimming of whitespace
- **Length Limits**: Prevents buffer overflow attacks
- **Email Validation**: Basic format checking

### Database Security

- **Parameterized Queries**: SQLAlchemy ORM prevents SQL injection
- **Constraint Enforcement**: Database-level constraint validation
- **Unique Constraints**: Prevents duplicate user registration

## Migration Strategy

### From In-Memory to Database

1. **Environment Configuration**: Set `USE_SQLALCHEMY=true`
2. **Database Initialization**: Run `python3 init_db.py`
3. **API Testing**: Verify all endpoints work correctly
4. **Data Migration**: If needed, migrate existing data

### Future Enhancements

- **Database Migrations**: Implement Flask-Migrate for schema changes
- **Advanced Validation**: Add more sophisticated validation rules
- **Soft Deletes**: Implement soft delete functionality
- **Audit Logging**: Track user changes and activities

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Connection**: Check SQLAlchemy configuration
3. **Table Creation**: Verify database permissions
4. **Validation Errors**: Check input data format

### Debug Mode

Enable debug mode for detailed error messages:

```python
app = create_app()
app.config['DEBUG'] = True
```

## Conclusion

The User model mapping implementation provides:

- ✅ **Complete SQLAlchemy Integration**: Full database persistence
- ✅ **Robust Validation**: Comprehensive input validation
- ✅ **Secure Password Handling**: Bcrypt integration
- ✅ **Specialized Repository**: User-specific operations
- ✅ **Backward Compatibility**: Works with existing code
- ✅ **Comprehensive Testing**: Full test coverage
- ✅ **Production Ready**: Suitable for production deployment

The implementation follows best practices for:
- **Security**: Secure password handling and validation
- **Performance**: Optimized queries and proper indexing
- **Maintainability**: Clean code structure and separation of concerns
- **Extensibility**: Easy to extend with new features

This foundation is ready for extending to other models (Place, Review, Amenity) and implementing relationships between entities.
