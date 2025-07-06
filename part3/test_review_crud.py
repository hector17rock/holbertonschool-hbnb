#!/usr/bin/env python3
"""
Test Review CRUD operations directly through the facade.
"""

from app import create_app
from app.services.facade import HBnBFacade


def test_review_crud():
    """Test Review CRUD operations directly through facade."""
    app = create_app()
    
    with app.app_context():
        facade = HBnBFacade()
        
        print("🧪 Testing Review CRUD Operations")
        print("=" * 40)
        
        # Create a review
        print("\n➕ Creating a review...")
        review_data = {
            "text": "Amazing place! The location is perfect and amenities are great.",
            "rating": 5,
            "user_id": "8a58fa44-c571-42e9-bd90-063b8352c71b",  # Admin user
            "place_id": "db0b6055-a695-4303-800f-cb4361205b4c"  # Beach house
        }
        
        try:
            review = facade.create_review(review_data)
            print(f"✅ Review created successfully")
            print(f"   Review ID: {review.id}")
            print(f"   Rating: {review.rating}/5")
            print(f"   Text: {review.text}")
            review_id = review.id
            
        except Exception as e:
            print(f"❌ Failed to create review: {e}")
            return
        
        # Read all reviews
        print("\n📋 Getting all reviews...")
        reviews = facade.get_all_reviews()
        print(f"✅ Found {len(reviews)} review(s)")
        for review in reviews:
            print(f"   - Rating: {review.rating}/5")
            print(f"     Text: {review.text[:50]}...")
        
        # Read specific review
        print(f"\n👁️  Getting specific review {review_id}...")
        review = facade.get_review(review_id)
        if review:
            print(f"✅ Review found")
            print(f"   ID: {review.id}")
            print(f"   Rating: {review.rating}/5")
            print(f"   Text: {review.text}")
            print(f"   Created: {review.created_at}")
        else:
            print("❌ Review not found")
        
        # Update review
        print(f"\n📝 Updating review {review_id}...")
        update_data = {
            "text": "Absolutely fantastic place! Highly recommended for families.",
            "rating": 5
        }
        
        try:
            updated_review = facade.update_review(review_id, update_data)
            if updated_review:
                print(f"✅ Review updated successfully")
                print(f"   New text: {updated_review.text}")
                print(f"   Updated: {updated_review.updated_at}")
            else:
                print("❌ Failed to update review")
        except Exception as e:
            print(f"❌ Failed to update review: {e}")
        
        # Delete review
        print(f"\n🗑️  Deleting review {review_id}...")
        try:
            success = facade.delete_review(review_id)
            if success:
                print(f"✅ Review deleted successfully")
                
                # Verify deletion
                deleted_review = facade.get_review(review_id)
                if deleted_review:
                    print("❌ Review still exists after deletion")
                else:
                    print("✅ Review deletion confirmed")
            else:
                print("❌ Failed to delete review")
        except Exception as e:
            print(f"❌ Failed to delete review: {e}")


if __name__ == "__main__":
    test_review_crud()
