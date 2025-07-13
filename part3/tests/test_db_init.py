#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db

def test_db_initialization():
    """Test database initialization and table creation."""
    app = create_app()
    
    with app.app_context():
        print('Creating database tables...')
        db.create_all()
        print('Database tables created successfully!')
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f'Available tables: {tables}')
        
        # Check the place_amenity association table
        if 'place_amenity' in tables:
            print('Association table place_amenity created successfully!')
            columns = inspector.get_columns('place_amenity')
            print('  Columns in place_amenity:')
            for col in columns:
                print(f'    - {col["name"]} ({col["type"]})')
        
        # Check foreign key constraints
        for table_name in tables:
            if table_name != 'place_amenity':
                foreign_keys = inspector.get_foreign_keys(table_name)
                if foreign_keys:
                    print(f'Foreign keys in {table_name}:')
                    for fk in foreign_keys:
                        print(f'    - {fk["constrained_columns"]} -> {fk["referred_table"]}.{fk["referred_columns"]}')

if __name__ == '__main__':
    test_db_initialization()
