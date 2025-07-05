#!/usr/bin/env python3
"""
Database initialization script for HBnB project.
This script creates all database tables.
"""

from app import create_app, db
import config

def init_database():
    """Initialize the database and create all tables."""
    app = create_app(config.DevelopmentConfig)
    
    with app.app_context():
        print("🔧 Creating database tables...")
        
        # Import all models to ensure they are registered with SQLAlchemy
        from app.models.user import User
        from app.models.base_model import BaseModel
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print(f"✅ Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {tables}")

if __name__ == "__main__":
    init_database()
