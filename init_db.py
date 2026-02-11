"""
Database initialization script
Run this script separately if you need to reset or initialize the database
"""
import sqlite3

DB_PATH = 'users.db'

def init_database():
    """Initialize the database with users table and sample data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing table if you want to start fresh
    # cursor.execute('DROP TABLE IF EXISTS users')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample users
    sample_users = ['toms', 'alice', 'bob', 'charlie', 'david']
    
    for username in sample_users:
        try:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            print(f"Added user: {username}")
        except sqlite3.IntegrityError:
            print(f"User {username} already exists, skipping...")
    
    conn.commit()
    
    # Display all users
    cursor.execute('SELECT id, username, created_at FROM users')
    users = cursor.fetchall()
    
    print("\n--- Current Users in Database ---")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Created: {user[2]}")
    
    conn.close()
    print("\nDatabase initialization completed!")

if __name__ == '__main__':
    init_database()
