from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Ensure database and table exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()  # Run once when the app starts

# Route to Add Users (POST request)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json  # Get JSON data from request
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User added successfully'}), 201


# Route to Fetch All Users (GET request)
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify({'users': users})


# Vulnerable Search Users (GET request) - **Allows SQL Injection**
@app.route('/search')
def search():
    query = request.args.get('q', '')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # SQL Injection vulnerability: Direct string interpolation (f-string)
    cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{query}%'")  # This is insecure!
    results = cursor.fetchall()
    conn.close()

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)




















