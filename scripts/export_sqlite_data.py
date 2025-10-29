#!/usr/bin/env python3
"""
Export data from SQLite database to JSON format for migration.
Usage: python scripts/export_sqlite_data.py
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Database file
SQLITE_DB = "finalytics.db"
OUTPUT_FILE = "sqlite_export.json"

def export_table(cursor, table_name):
    """Export a single table to a list of dictionaries."""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            row_dict = {}
            for col, val in zip(columns, row):
                # Handle datetime conversion
                if isinstance(val, str) and ('_at' in col or 'created' in col):
                    try:
                        # Try to parse as datetime
                        datetime.fromisoformat(val.replace('Z', '+00:00'))
                        row_dict[col] = val
                    except:
                        row_dict[col] = val
                else:
                    row_dict[col] = val
            data.append(row_dict)
        
        return data
    except sqlite3.OperationalError as e:
        print(f"Warning: Could not export table '{table_name}': {e}")
        return []

def main():
    """Main export function."""
    if not Path(SQLITE_DB).exists():
        print(f"Error: SQLite database '{SQLITE_DB}' not found.")
        return
    
    print(f"Exporting data from {SQLITE_DB}...")
    
    # Connect to SQLite database
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Found tables: {', '.join(tables)}")
    
    # Export data
    export_data = {}
    for table in tables:
        print(f"  Exporting {table}...", end=" ")
        data = export_table(cursor, table)
        export_data[table] = data
        print(f"({len(data)} rows)")
    
    # Close connection
    conn.close()
    
    # Write to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"\n✓ Export complete! Data saved to {OUTPUT_FILE}")
    print(f"  Total tables: {len(tables)}")
    print(f"  Total rows: {sum(len(rows) for rows in export_data.values())}")

if __name__ == "__main__":
    main()

