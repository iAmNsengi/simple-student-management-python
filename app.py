# app.py
from flask import Flask, request, jsonify, render_template
import mysql.connector
from functools import wraps
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'student_db')
}

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API_KEY must be set in .env file")

# Decorator to check API key from request body
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data = request.get_json()
            api_key = data.get('api_key') if data else None
            if not api_key:
                return jsonify({"message": "API key is required"}), 401
            if api_key != API_KEY:
                return jsonify({"message": "Invalid API key"}), 401
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Invalid request format"}), 400
    return decorated

# Database connection function
def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Initialize database from SQL file
def init_db():
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Read and execute SQL file
        with open('database/init.sql', 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/students', methods=['POST'])
@require_api_key
def register_student():
    data = request.json
    required_fields = ['name', 'age', 'grade']
    
    if not all(key in data for key in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        
        query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
        values = (data['name'], data['age'], data['grade'])
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Student registered successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/view', methods=['POST'])
@require_api_key
def get_students():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
        students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"students": students})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)