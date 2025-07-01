import os
from app import create_app

# Get configuration name from environment variable or default to 'development'
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
