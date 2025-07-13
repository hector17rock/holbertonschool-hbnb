# Administrator Access Endpoints Guide

This guide explains the Role-Based Access Control (RBAC) implementation for administrator access in the HBnB API.

## Overview

Administrators have the highest level of privileges in the system and can:
- Create and modify user accounts
- Add and modify amenities
- Bypass ownership restrictions for places and reviews
- Perform all actions that regular users can do

## Administrator Permissions

### Admin-Only Endpoints

The following endpoints require administrator privileges:

1. **POST /api/v1/users/** - Create a new user
2. **PUT /api/v1/users/<user_id>** - Modify any user's details
3. **POST /api/v1/amenities/** - Add a new amenity
4. **PUT /api/v1/amenities/<amenity_id>** - Modify amenity details

### Admin Bypass Capabilities

Administrators can bypass ownership restrictions on:
- **PUT /api/v1/places/<place_id>** - Modify any place (not just owned ones)
- **PUT /api/v1/reviews/<review_id>** - Modify any review (not just authored ones)
- **DELETE /api/v1/reviews/<review_id>** - Delete any review (not just authored ones)

## Setting Up Admin Users

### Method 1: Using the Helper Script

Run the provided script to create test users:

```bash
python3 create_admin.py
```

This creates:
- Admin user: `admin@example.com` / `adminpass123`
- Regular user: `user@example.com` / `userpass123`

### Method 2: Manual Database Setup

If you have direct database access, you can manually set the `is_admin` flag to `True` for any user.

## Authentication

All admin endpoints require JWT authentication. The `is_admin` flag is included in the JWT token claims.

### Getting Admin Token

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "adminpass123"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Testing Admin Endpoints

### 1. Create a New User (Admin Only)

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "New",
    "last_name": "User",
    "email": "newuser@example.com",
    "password": "newpass123",
    "is_admin": false
  }'
```

**Expected Response (201):**
```json
{
  "id": "user-uuid",
  "first_name": "New",
  "last_name": "User",
  "email": "newuser@example.com"
}
```

**Regular User Attempt (403):**
```json
{
  "error": "Admin privileges required"
}
```

### 2. Modify User Details (Admin Only)

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/<user_id>" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updatedemail@example.com",
    "first_name": "Updated"
  }'
```

**Expected Response (200):**
```json
{
  "id": "user-uuid",
  "first_name": "Updated",
  "last_name": "User",
  "email": "updatedemail@example.com"
}
```

### 3. Add New Amenity (Admin Only)

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Swimming Pool"
  }'
```

**Expected Response (201):**
```json
{
  "id": "amenity-uuid",
  "name": "Swimming Pool",
  "created_at": "2023-07-13T10:00:00",
  "updated_at": "2023-07-13T10:00:00"
}
```

### 4. Modify Amenity (Admin Only)

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Amenity Name"
  }'
```

**Expected Response (200):**
```json
{
  "id": "amenity-uuid",
  "name": "Updated Amenity Name",
  "created_at": "2023-07-13T10:00:00",
  "updated_at": "2023-07-13T10:05:00"
}
```

### 5. Admin Bypass - Modify Any Place

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Admin Updated Place",
    "price": 199.99
  }'
```

**Expected Response (200):**
```json
{
  "id": "place-uuid",
  "title": "Admin Updated Place",
  "price": 199.99,
  "owner": {
    "id": "original-owner-id",
    "first_name": "Original",
    "last_name": "Owner",
    "email": "owner@example.com"
  }
}
```

### 6. Admin Bypass - Modify Any Review

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/<review_id>" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Admin updated review",
    "rating": 5
  }'
```

**Expected Response (200):**
```json
{
  "id": "review-uuid",
  "text": "Admin updated review",
  "rating": 5,
  "user_id": "original-reviewer-id",
  "place_id": "place-uuid"
}
```

### 7. Admin Bypass - Delete Any Review

```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<review_id>" \
  -H "Authorization: Bearer <admin_token>"
```

**Expected Response (200):**
```json
{
  "message": "Review deleted successfully"
}
```

## Error Responses

### 401 - Authentication Required
```json
{
  "msg": "Missing Authorization Header"
}
```

### 403 - Admin Privileges Required
```json
{
  "error": "Admin privileges required"
}
```

### 403 - Unauthorized Action (for ownership restrictions)
```json
{
  "error": "Unauthorized action"
}
```

### 400 - Email Already Registered
```json
{
  "error": "Email already registered"
}
```

### 404 - Resource Not Found
```json
{
  "error": "User not found"
}
```

## Implementation Details

### JWT Claims Structure
```json
{
  "sub": "user-uuid",
  "iat": 1623456789,
  "exp": 1623460389,
  "is_admin": true
}
```

### Admin Check Pattern
```python
from flask_jwt_extended import get_jwt

claims = get_jwt()
is_admin = claims.get('is_admin', False)
if not is_admin:
    return {'error': 'Admin privileges required'}, 403
```

### Ownership Bypass Pattern
```python
# Regular ownership check
if not is_admin and resource.owner.id != current_user:
    return {'error': 'Unauthorized action'}, 403
```

## Security Considerations

1. **Admin Token Security**: Admin tokens should be kept secure and have appropriate expiration times.
2. **Admin User Creation**: In production, admin users should be created through secure processes, not through the API.
3. **Audit Logging**: Consider implementing audit logs for admin actions.
4. **Principle of Least Privilege**: Only grant admin privileges when necessary.

## Testing Checklist

- [ ] Admin can create users
- [ ] Admin can modify any user
- [ ] Admin can create amenities
- [ ] Admin can modify amenities
- [ ] Admin can modify any place
- [ ] Admin can modify any review
- [ ] Admin can delete any review
- [ ] Regular users cannot access admin endpoints
- [ ] Regular users cannot bypass ownership restrictions
- [ ] Proper error messages for unauthorized access
- [ ] Email uniqueness validation works for admin operations

## Common Issues and Solutions

### Issue: "Admin privileges required" when using admin token
**Solution**: Verify the token contains the `is_admin` claim and it's set to `true`.

### Issue: 401 errors with valid tokens
**Solution**: Ensure the `Authorization: Bearer <token>` header is properly formatted.

### Issue: Cannot create admin user
**Solution**: Use the `create_admin.py` script or manually set the `is_admin` flag in the database.

### Issue: Email already registered errors
**Solution**: Check for existing users with the same email before creating new ones.
