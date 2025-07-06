#!/usr/bin/env python3
"""
Database initialization script for HBnB application.
This script initializes the database and creates all tables.
"""

from app import create_app
from app.models.base_model import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def init_database():
    """Initialize the database and create all tables."""
    print("🚀 Initializing HBnB Database")
    print("=" * 40)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Drop existing tables (for clean start)
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            print("✅ Existing tables dropped successfully")
            
            # Create all tables
            print("🏗️  Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Print table information
            print("\n📋 Database Schema Information:")
            print("-" * 40)
            
            # Get table names
            tables = db.metadata.tables.keys()
            print(f"📊 Total tables created: {len(tables)}")
            
            for table_name in sorted(tables):
                table = db.metadata.tables[table_name]
                print(f"\n📋 Table: {table_name}")
                for column in table.columns:
                    nullable = "NULL" if column.nullable else "NOT NULL"
                    primary_key = "PRIMARY KEY" if column.primary_key else ""
                    unique = "UNIQUE" if column.unique else ""
                    constraints = " ".join(filter(None, [nullable, primary_key, unique]))
                    print(f"   - {column.name}: {column.type} {constraints}")
            
            print(f"\n🎉 Database initialization completed successfully!")
            print(f"📍 Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
        except Exception as e:
            print(f"❌ Error during database initialization: {e}")
            raise


if __name__ == "__main__":
    init_database()
