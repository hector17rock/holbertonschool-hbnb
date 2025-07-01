import os

class Config:
    """
    Base configuration class. Contains default configuration settings
    that are common to all environments.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    # Add more configuration settings that are common to all environments
    # For example: database URLs, API settings, etc.

class DevelopmentConfig(Config):
    """
    Development configuration. 
    Inherits from Config and adds development-specific settings.
    """
    DEBUG = True
    # Add development-specific settings here
    # For example: development database URL, debug tools, etc.

class ProductionConfig(Config):
    """
    Production configuration.
    Inherits from Config and adds production-specific settings.
    """
    DEBUG = False
    # Override the SECRET_KEY for production - must be set via environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Add production-specific settings here
    # For example: production database URL, logging settings, etc.

class TestingConfig(Config):
    """
    Testing configuration.
    Inherits from Config and adds testing-specific settings.
    """
    TESTING = True
    DEBUG = True
    # Add testing-specific settings here
    # For example: test database URL, disable CSRF, etc.

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
