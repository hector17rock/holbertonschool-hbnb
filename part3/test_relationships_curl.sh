#!/bin/bash

# Test script for HBnB API relationships using cURL
# Make sure the Flask app is running on port 5001

BASE_URL="http://localhost:5001/api/v1"

echo "=== Testing HBnB API Relationships with cURL ==="

# Test 1: Create a User
echo -e "\n1. Creating a User..."
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }')

echo "Response: $USER_RESPONSE"
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "User ID: $USER_ID"

# Test 2: Create Amenities
echo -e "\n2. Creating Amenities..."

WIFI_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities" \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}')
echo "WiFi Response: $WIFI_RESPONSE"
WIFI_ID=$(echo "$WIFI_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

POOL_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities" \
  -H "Content-Type: application/json" \
  -d '{"name": "Swimming Pool"}')
echo "Pool Response: $POOL_RESPONSE"
POOL_ID=$(echo "$POOL_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

# Test 3: Create a Place
echo -e "\n3. Creating a Place..."
PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Beautiful Beach House\",
    \"description\": \"A lovely house by the beach\",
    \"price\": 150.0,
    \"latitude\": 25.7617,
    \"longitude\": -80.1918,
    \"owner_id\": \"$USER_ID\"
  }")

echo "Place Response: $PLACE_RESPONSE"
PLACE_ID=$(echo "$PLACE_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Place ID: $PLACE_ID"

# Test 4: Create a Review
echo -e "\n4. Creating a Review..."
REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Amazing place! Really enjoyed our stay.\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }")

echo "Review Response: $REVIEW_RESPONSE"

# Test 5: Get all users (should show the user we created)
echo -e "\n5. Getting all Users..."
curl -s -X GET "$BASE_URL/users" | head -c 500
echo -e "\n"

# Test 6: Get all places (should show owner information)
echo -e "\n6. Getting all Places..."
curl -s -X GET "$BASE_URL/places" | head -c 500
echo -e "\n"

# Test 7: Get all reviews (should show user and place relationships)
echo -e "\n7. Getting all Reviews..."
curl -s -X GET "$BASE_URL/reviews" | head -c 500
echo -e "\n"

# Test 8: Get specific user (should show related data)
echo -e "\n8. Getting specific User..."
curl -s -X GET "$BASE_URL/users/$USER_ID" | head -c 500
echo -e "\n"

# Test 9: Get specific place (should show related data)
echo -e "\n9. Getting specific Place..."
curl -s -X GET "$BASE_URL/places/$PLACE_ID" | head -c 500
echo -e "\n"

echo -e "\n=== API Testing Complete ==="

echo -e "\nNote: Run this script after starting the Flask app with:"
echo "python run.py"
