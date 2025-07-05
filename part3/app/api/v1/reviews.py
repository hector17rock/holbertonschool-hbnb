from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import json

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Forbidden - Cannot review own place or '
                       'already reviewed')
    def post(self):
        """Register a new review"""
        # Get current user identity from JWT token
        current_user_identity = get_jwt_identity()
        current_user_data = json.loads(current_user_identity)
        current_user_id = current_user_data['id']

        review_data = api.payload

        # Override user_id with authenticated user
        review_data['user_id'] = current_user_id

        try:
            # Check if place exists and user is not the owner
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404

            # Users cannot review their own places
            if place.owner.id == current_user_id:
                return {'error': 'You cannot review your own place'}, 400

            # Check if user has already reviewed this place
            existing_reviews = facade.get_all_reviews()
            for review in existing_reviews:
                if (review.user.id == current_user_id and
                        review.place.id == review_data['place_id']):
                    return {'error':
                            'You have already reviewed this place'}, 400
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.comment,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.comment,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            } for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.comment,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Forbidden - Can only modify own reviews')
    def put(self, review_id):
        """Update a review's information"""
        # Get current user identity from JWT token
        current_user_identity = get_jwt_identity()
        current_user_data = json.loads(current_user_identity)
        current_user_id = current_user_data['id']

        review_data = api.payload

        try:
            # Check if review exists
            existing_review = facade.get_review(review_id)
            if not existing_review:
                return {'error': 'Review not found'}, 404

            # Check if current user is the author of the review
            if existing_review.user.id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            # Override user_id to ensure it stays the same
            review_data['user_id'] = current_user_id

            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {
                'id': updated_review.id,
                'text': updated_review.comment,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Forbidden - Can only delete own reviews')
    def delete(self, review_id):
        """Delete a review"""
        # Get current user identity from JWT token
        current_user_identity = get_jwt_identity()
        current_user_data = json.loads(current_user_identity)
        current_user_id = current_user_data['id']

        try:
            # Check if review exists
            existing_review = facade.get_review(review_id)
            if not existing_review:
                return {'error': 'Review not found'}, 404

            # Check if current user is the author of the review
            if existing_review.user.id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            # Delete the review using the facade
            success = facade.delete_review(review_id)
            if success:
                return {'message': 'Review deleted successfully'}, 200
            else:
                return {'error': 'Review not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass
