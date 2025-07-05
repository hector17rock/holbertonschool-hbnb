from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import json

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new amenity"""
        current_user_identity = get_jwt_identity()
        current_user = json.loads(current_user_identity)
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        
        # Validate required fields
        if not amenity_data or 'name' not in amenity_data:
            return {'error': 'Missing required field: name'}, 400
        
        # Validate name is not empty
        if not amenity_data['name'].strip():
            return {'error': 'Name cannot be empty'}, 400
        
        try:
            # Create the amenity using the facade
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [
                {
                    'id': amenity.id,
                    'name': amenity.name,
                    'created_at': amenity.created_at.isoformat(),
                    'updated_at': amenity.updated_at.isoformat()
                }
                for amenity in amenities
            ], 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            
            return {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat(),
                'updated_at': amenity.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user_identity = get_jwt_identity()
        current_user = json.loads(current_user_identity)
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        
        # Validate required fields
        if not amenity_data or 'name' not in amenity_data:
            return {'error': 'Missing required field: name'}, 400
        
        # Validate name is not empty
        if not amenity_data['name'].strip():
            return {'error': 'Name cannot be empty'}, 400
        
        # Check if amenity exists
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        try:
            # Update the amenity using the facade
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat(),
                'updated_at': updated_amenity.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400
