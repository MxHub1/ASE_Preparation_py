from flask import Flask, request, jsonify
import psycopg2
from marshmallow import Schema, fields, validate

app = Flask(__name__)

# Replace these with your PostgreSQL connection details
## DB_CONNECTION_STRING = "postgresql://username:password@localhost:5432/your_database"
DB_CONNECTION_STRING = "postgresql://@localhost:5432/database"

# Define a simple schema for validation
class ItemSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=50))
    quantity = fields.Int(required=True, validate=validate.Range(min=0))


# Establish a connection to PostgreSQL
def get_db_connection():
    connection = psycopg2.connect(DB_CONNECTION_STRING)
    return connection


# Endpoint to retrieve data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM your_table;')
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to store data
@app.route('/data', methods=['POST'])
def post_data():
    try:
        data = request.get_json()

        # Validate incoming JSON data
        schema = ItemSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Perform your business logic (e.g., store data in the database)
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO your_table (name, quantity) VALUES (%s, %s);',
                       (data['name'], data['quantity']))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Data stored successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)