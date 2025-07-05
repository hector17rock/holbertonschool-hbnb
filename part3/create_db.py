#!/usr/bin/env python3
"""
Simple database creation script that avoids circular imports.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Simple Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models after db is defined
from app.models.base_model import BaseModel
from app.models.user import User

def create_tables():
    """Create all database tables."""
    with app.app_context():
        print("🔧 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {tables}")

if __name__ == "__main__":
    create_tables()
