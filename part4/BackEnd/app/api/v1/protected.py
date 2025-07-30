from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected operations')

@api.route('')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Token required')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user_id = get_jwt_identity()  # Retrieve the user's id from the token
        claims = get_jwt()  # Get additional claims from the token
        
        return {
            'message': f'Hello, user {current_user_id}',
            'user_id': current_user_id,
            'is_admin': claims.get('is_admin', False)
        }, 200
