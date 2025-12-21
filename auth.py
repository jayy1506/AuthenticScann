from flask import Blueprint, request, jsonify
import sqlite3
import hashlib
import os

# Create the uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

auth_bp = Blueprint('auth', __name__)

# Initialize database when the blueprint is created
init_db()

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    # Hash the password
    password_hash = hash_password(password)
    
    # Store user in database
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Username or email already exists'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing email or password'}), 400
    
    # Hash the provided password
    password_hash = hash_password(password)
    
    # Check credentials
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username FROM users
        WHERE email = ? AND password_hash = ?
    ''', (email, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user': {
                'id': user[0],
                'username': user[1]
            }
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401