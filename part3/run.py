from app import create_app
import config

# Create app instance with development configuration
app = create_app(config.DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
