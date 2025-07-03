from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

api = Namespace('protected', description='Protected operations')


@api.route('')
class Protected(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires JWT authentication"""
        # Get the identity from the JWT token
        current_user_identity = get_jwt_identity()

        # Parse the JSON string to get user data
        try:
            user_data = json.loads(current_user_identity)
            user_id = user_data.get('id')
            is_admin = user_data.get('is_admin')

            return {
                'message': f'Hello, user {user_id}',
                'user_id': user_id,
                'is_admin': is_admin
            }, 200

        except (json.JSONDecodeError, TypeError):
            return {'error': 'Invalid token format'}, 400
