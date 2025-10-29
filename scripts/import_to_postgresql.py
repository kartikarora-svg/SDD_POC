#!/usr/bin/env python3
"""
Import data from JSON export into PostgreSQL database.
Usage: python scripts/import_to_postgresql.py
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.database import SessionLocal, engine
from app.models import Base
from sqlalchemy import text

INPUT_FILE = "sqlite_export.json"

def import_data():
    """Import data from JSON export."""
    if not Path(INPUT_FILE).exists():
        print(f"Error: Export file '{INPUT_FILE}' not found.")
        print("Run 'python scripts/export_sqlite_data.py' first.")
        return
    
    print(f"Reading data from {INPUT_FILE}...")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        export_data = json.load(f)
    
    print(f"Found {len(export_data)} tables to import")
    
    # Verify PostgreSQL connection
    if not settings.DATABASE_URL.startswith("postgresql"):
        print("Error: DATABASE_URL must be set to PostgreSQL connection string")
        print("Update your .env file with: DATABASE_URL=postgresql://...")
        return
    
    print(f"Connecting to PostgreSQL: {settings.DATABASE_URL.split('@')[1]}")
    
    # Create all tables
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Import data table by table
        for table_name, rows in export_data.items():
            if not rows:
                print(f"  Skipping {table_name} (no data)")
                continue
            
            print(f"  Importing {table_name}...", end=" ")
            
            # Get column names
            columns = list(rows[0].keys())
            
            # Prepare bulk insert
            placeholders = ', '.join([f':{col}' for col in columns])
            column_list = ', '.join(columns)
            
            insert_sql = f"""
                INSERT INTO {table_name} ({column_list})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
            """
            
            # Execute bulk insert
            try:
                result = db.execute(text(insert_sql), rows)
                db.commit()
                print(f"✓ ({len(rows)} rows)")
            except Exception as e:
                print(f"✗ Error: {e}")
                db.rollback()
                # Try row-by-row for debugging
                success_count = 0
                for row in rows:
                    try:
                        db.execute(text(insert_sql), row)
                        db.commit()
                        success_count += 1
                    except:
                        db.rollback()
                        continue
                print(f"  Imported {success_count}/{len(rows)} rows (some failed)")
        
        print(f"\n✓ Import complete!")
        
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_data()

