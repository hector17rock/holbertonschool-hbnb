from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
import json

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user'),
    'is_admin': fields.Boolean(description='Whether the user is an admin',
                               default=False)
})

# Define the user response model (excludes password for security)
user_response_model = api.model('UserResponse', {
    'id': fields.String(required=True,
                        description='Unique identifier of the user'),
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email} for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user"""
        # Check if there are any existing users
        existing_users = facade.get_all_users()
        
        # If there are no users yet, allow creation of first admin user
        if len(existing_users) == 0:
            user_data = api.payload
            # Ensure first user is an admin
            user_data['is_admin'] = True
        else:
            # For subsequent users, require admin authentication
            from flask_jwt_extended import verify_jwt_in_request
            try:
                verify_jwt_in_request()
                current_user_identity = get_jwt_identity()
                current_user = json.loads(current_user_identity)
                if not current_user.get('is_admin'):
                    return {'error': 'Admin privileges required'}, 403
            except:
                return {'error': 'Admin privileges required'}, 403
            
            user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real
        # validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'message': 'User successfully created'}, 201


@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by id"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, user_id):
        """Update a user's information"""
        current_user_identity = get_jwt_identity()
        current_user = json.loads(current_user_identity)
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Update user details
        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
