# HBnB Application Tests

This directory contains all test files for the HBnB application. The tests are organized by functionality and testing approach.

## Test File Organization

### Core Model Tests
- `test_models.py` - Basic model functionality tests
- `test_sqlalchemy_models.py` - SQLAlchemy model integration tests
- `test_db_user.py` - Database user model specific tests

### API Endpoint Tests
- `test_api.py` - General API endpoint tests
- `test_user_endpoints.py` - User-specific API endpoint tests
- `test_amenity_creation.py` - Amenity creation API tests
- `test_place_registration.py` - Place registration API tests
- `test_reviews_api.py` - Review API endpoint tests
- `test_put_endpoint.py` - Update (PUT) endpoint tests
- `test_update_review.py` - Review update functionality tests

### Integration Tests
- `test_app_integration.py` - Full application integration tests
- `test_facade_sqlalchemy.py` - Facade layer with SQLAlchemy tests

### CRUD Operation Tests
- `test_facade_crud.py` - Facade CRUD operations
- `test_place_details.py` - Place detail retrieval tests
- `test_review_crud.py` - Review CRUD operations

### Example Files
- `example_get_reviews.py` - Example review retrieval implementations
- `example_review_api.py` - Example review API usage
- `example_update_review.py` - Example review update implementations

## Running Tests

### Individual Test Files
To run a specific test file:
```bash
python tests/test_models.py
python tests/test_facade_sqlalchemy.py
python tests/test_app_integration.py
```

### All Tests
To run all tests in the directory:
```bash
python -m pytest tests/
```

### Test Categories

#### Unit Tests
- Model validation tests
- Business logic tests
- Individual component tests

#### Integration Tests
- Database integration
- API endpoint integration
- Full application workflow tests

#### CRUD Tests
- Create operations
- Read operations
- Update operations
- Delete operations

## Test Coverage

### ✅ Covered Areas
- User model and authentication
- Amenity CRUD operations
- Place CRUD operations
- Review CRUD operations
- SQLAlchemy model integration
- Database persistence
- Business logic validation
- API endpoint functionality
- JWT authentication

### 🔄 Areas for Expansion
- Relationship testing (when implemented)
- Performance testing
- Error handling edge cases
- Security testing
- Load testing

## Test Environment

- **Database**: SQLite (development.db)
- **Framework**: Flask with SQLAlchemy
- **Authentication**: JWT tokens
- **API Format**: RESTful JSON API

## Notes

- Tests may require database initialization before running
- Some tests require the Flask application to be running
- Integration tests may create/modify test data
- Clean up test data between test runs for consistent results
