from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DB_PATH = 'users.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with users table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample users if table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        sample_users = ['toms', 'alice', 'bob', 'charlie']
        for username in sample_users:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

@app.route('/api/verify', methods=['GET', 'POST'])
def verify_user():
    """
    Verify if user exists in database by checking username in header
    Expected header: X-Username or Username
    Returns: 200 if user exists, 404 if not found, 400 if header missing
    """
    # Try to get username from different possible header names
    username = request.headers.get('X-Username') or request.headers.get('Username')
    
    if not username:
        return jsonify({
            'error': 'Username header missing',
            'message': 'Please provide username in X-Username or Username header'
        }), 400
    
    # Check if user exists in database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'success': True,
            'message': f'User {username} exists',
            'username': username
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': f'User {username} not found',
            'username': username
        }), 404

@app.route('/api/users', methods=['GET'])
def list_users():
    """List all users in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, created_at FROM users')
    users = cursor.fetchall()
    conn.close()
    
    users_list = [{'id': user['id'], 'username': user['username'], 'created_at': user['created_at']} for user in users]
    
    return jsonify({
        'success': True,
        'count': len(users_list),
        'users': users_list
    }), 200

@app.route('/api/users', methods=['POST'])
def add_user():
    """Add a new user to the database"""
    data = request.get_json()
    
    if not data or 'username' not in data:
        return jsonify({
            'error': 'Username is required',
            'message': 'Please provide username in request body'
        }), 400
    
    username = data['username']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'User {username} added successfully',
            'username': username
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({
            'error': 'User already exists',
            'message': f'User {username} already exists in database'
        }), 409

@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    """Delete an existing user from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({
            'success': False,
            'message': f'User {username} not found'
        }), 404

    # Delete user
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'User {username} deleted successfully'
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with visual database viewer"""
    return render_template('index.html')

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'User Verification API',
        'endpoints': {
            '/': 'Visual database viewer',
            '/api/verify': 'Verify user exists (requires X-Username header)',
            '/api/users': 'GET: List all users, POST: Add new user',
            '/api/info': 'This API information'
        },
        'usage': 'Send GET request to /api/verify with X-Username header'
    }), 200



if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run the Flask app
    print("Starting Flask API server...")
    print("API will be available at http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
