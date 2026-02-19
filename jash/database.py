import sqlite3
import os
from datetime import datetime

DATABASE_NAME = 'portfolio.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create visitors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            count INTEGER NOT NULL DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Initialize visitor count if not exists
    cursor.execute('SELECT COUNT(*) FROM visitors')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO visitors (count) VALUES (0)')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def add_contact(name, email, message):
    """Add a new contact message"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
            (name, email, message)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding contact: {e}")
        return False

def get_all_contacts():
    """Get all contact messages"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_visitor_count():
    """Get current visitor count"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT count FROM visitors WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def increment_visitor_count():
    """Increment and return visitor count"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE visitors SET count = count + 1, last_updated = ? WHERE id = 1',
        (datetime.now(),)
    )
    conn.commit()
    new_count = get_visitor_count()
    conn.close()
    return new_count

if __name__ == '__main__':
    init_database()
    print("Database setup complete!")
