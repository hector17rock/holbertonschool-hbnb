# SQLAlchemy Integration Guide

This document outlines the implementation of SQLAlchemy integration for the HBnB project, replacing the in-memory repository with a database-backed persistence layer.

## Overview

The SQLAlchemy integration provides a robust, production-ready persistence layer using the Repository pattern. The implementation maintains backward compatibility with the existing in-memory repository while adding support for database persistence.

## Architecture

### Repository Pattern
- **Abstract Repository Interface**: Defines the contract for all repository implementations
- **InMemoryRepository**: Original in-memory implementation for testing
- **SQLAlchemyRepository**: New database-backed implementation

### Facade Pattern
- **HBnBFacade**: Business logic layer that uses repositories
- **Configurable Repository Selection**: Environment-based repository choice

## Files Modified/Created

### 1. Configuration (`config.py`)
```python
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 2. App Initialization (`app/__init__.py`)
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Initialize SQLAlchemy
    db.init_app(app)
```

### 3. Repository Implementation (`app/persistence/repository.py`)
```python
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model
    
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
    
    # ... other CRUD methods
```

### 4. Facade Refactoring (`app/services/facade.py`)
```python
class HBnBFacade:
    def __init__(self):
        use_sqlalchemy = os.getenv('USE_SQLALCHEMY', 'true').lower() == 'true'
        
        if use_sqlalchemy:
            self.user_repo = SQLAlchemyRepository(User)
            # ... other repositories
        else:
            self.user_repo = InMemoryRepository()
            # ... other repositories
```

## Dependencies

### Added to requirements.txt:
```
sqlalchemy
flask-sqlalchemy
```

## Configuration Options

### Environment Variables
- `USE_SQLALCHEMY`: Set to 'false' to use in-memory repositories (default: 'true')

### Database Configuration
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disable object modification tracking

## SQLAlchemy Repository Features

### CRUD Operations
- **Create**: `add(obj)` - Adds object to database
- **Read**: `get(obj_id)` - Retrieves object by ID
- **Update**: `update(obj_id, data)` - Updates object with new data
- **Delete**: `delete(obj_id)` - Removes object from database

### Query Methods
- **get_all()**: Retrieves all objects
- **get_by_attribute(attr_name, attr_value)**: Finds object by attribute

### Transaction Management
- Automatic commit on successful operations
- Session management handled by Flask-SQLAlchemy

## Usage Examples

### Creating a User
```python
facade = HBnBFacade()
user_data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john@example.com',
    'password': 'password123'
}
user = facade.create_user(user_data)
```

### Querying Users
```python
# Get user by ID
user = facade.get_user(user_id)

# Get user by email
user = facade.get_user_by_email('john@example.com')

# Get all users
users = facade.get_all_users()
```

### Updating a User
```python
user_data = {
    'first_name': 'Jane',
    'email': 'jane@example.com'
}
updated_user = facade.update_user(user_id, user_data)
```

## Migration Strategy

### From In-Memory to SQLAlchemy
1. **Phase 1**: SQLAlchemy repository implementation ✅
2. **Phase 2**: Model mapping (next task)
3. **Phase 3**: Database initialization
4. **Phase 4**: Full testing and validation

### Backward Compatibility
- Environment variable controls repository selection
- Existing API endpoints remain unchanged
- Same business logic in facade layer

## Testing Strategy

### Current Status
- **Repository Implementation**: Complete
- **Facade Integration**: Complete
- **Database Testing**: Pending model mapping

### Test Scenarios
1. **Repository Selection**: Test both SQLAlchemy and InMemory modes
2. **CRUD Operations**: Verify all operations work correctly
3. **Transaction Handling**: Test commit/rollback scenarios
4. **Error Handling**: Test database connection failures

## Next Steps

### Model Mapping (Next Task)
1. Map User model to SQLAlchemy
2. Map Place model to SQLAlchemy
3. Map Review model to SQLAlchemy
4. Map Amenity model to SQLAlchemy
5. Define relationships between models

### Database Initialization
1. Create database tables
2. Set up migrations
3. Seed initial data
4. Test full integration

## Error Handling

### Database Connection Issues
- Fallback to in-memory repository if configured
- Proper error messages for connection failures
- Transaction rollback on errors

### Session Management
- Automatic session handling via Flask-SQLAlchemy
- Proper cleanup on request completion
- Connection pooling for performance

## Performance Considerations

### Query Optimization
- Use appropriate indexes
- Implement lazy loading for relationships
- Consider query caching for read-heavy operations

### Connection Management
- Connection pooling configured
- Proper session cleanup
- Monitor connection usage

## Security Considerations

### Database Security
- Use parameterized queries (SQLAlchemy ORM handles this)
- Validate all input data
- Implement proper access controls

### Data Integrity
- Use database constraints
- Implement proper transaction boundaries
- Handle concurrent access properly

## Configuration Examples

### Development Environment
```python
# config.py
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
```

### Production Environment
```python
# config.py
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
```

### Testing Environment
```python
# Set environment variable for testing
export USE_SQLALCHEMY=false

# Or use in-memory SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Database Connection**: Check database URI configuration
3. **Model Mapping**: Wait for next task to complete model mapping
4. **Transaction Issues**: Verify commit/rollback logic

### Debug Mode
- Enable Flask debug mode for detailed error messages
- Check SQLAlchemy echo for query debugging
- Monitor database logs for connection issues

## Future Enhancements

### Database Features
- Migration support with Flask-Migrate
- Database indexing for performance
- Connection pooling optimization
- Read replicas for scaling

### Repository Features
- Pagination support
- Advanced filtering
- Bulk operations
- Caching layer

## Conclusion

The SQLAlchemy integration provides a solid foundation for database persistence while maintaining the existing API structure. The implementation is ready for model mapping and database initialization in the next phase of development.

Key benefits:
- ✅ Production-ready database support
- ✅ Backward compatibility maintained
- ✅ Flexible repository selection
- ✅ Proper transaction management
- ✅ Ready for model mapping

The next task will focus on mapping the existing models to SQLAlchemy, which will enable full database functionality.
