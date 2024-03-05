from flask import Flask, request, jsonify
import requests
import psycopg2

app = Flask(__name__)

# Database setup
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id SERIAL PRIMARY KEY, name TEXT, age INTEGER)''')
conn.commit()

# API endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    user_list = []
    for user in users:
        user_list.append({'id': user[0], 'name': user[1], 'age': user[2]})
    return jsonify(user_list)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    if not name or not age:
        return jsonify({'error': 'Name and Age are required fields'}), 400
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    return jsonify({'message': 'User added successfully'}), 201

# Sending GET request to own API
@app.route('/send-get-request')
def send_get_request():
    response = requests.get('http://127.0.0.1:5000/api/users')
    return response.json()

# Sending POST request to own API
@app.route('/send-post-request')
def send_post_request():
    data = {'name': 'John', 'age': 30}
    response = requests.post('http://127.0.0.1:5000/api/users', json=data)
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(debug=True)