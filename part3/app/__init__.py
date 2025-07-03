from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# Initialize Bcrypt instance
bcrypt = Bcrypt()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_class (str): The configuration class to use.
                           Defaults to "config.DevelopmentConfig".
    
    Returns:
        Flask: Configured Flask application instance with all plugins initialized.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    
    # Initialize Flask-RESTX API
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    
    return app
