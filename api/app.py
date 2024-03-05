# api/routes.py
import logging
from flask import Flask, request, jsonify
from database import get_db_connection
from schemas import ItemSchema

app = Flask(__name__)

# Define a simple schema for validation
schema = ItemSchema()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint to retrieve data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        
        logger.info(f"Received GET request.")
        
        connection = get_db_connection()
        cursor = connection.cursor()

        logger.info(f"Built DB Connection")

        cursor.execute('SELECT * FROM public.user;')
        data = cursor.fetchall()

        logger.info(f"Fetched Data {data}")

        cursor.close()
        connection.close()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New endpoint to retrieve data by ID
@app.route('/data/<int:item_id>', methods=['GET'])
def get_data_by_id(item_id):
    try:

        logger.info(f"Received GET request for User ID {item_id}.")

        connection = get_db_connection()
        cursor = connection.cursor()

        logger.info(f"Built DB Connection")

        cursor.execute('SELECT * FROM public.user WHERE id = %s;', (item_id,))
        data = cursor.fetchone()

        logger.info(f"Fetched Data {data}")

        cursor.close()
        connection.close()

        if not data:
            return jsonify({'error': 'Item not found'}), 404

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to store data
@app.route('/data', methods=['POST'])
def post_data():
    try:
        data = request.get_json()

        logger.info(f"Received POST request. Data: {data}")

        # Validate incoming JSON data
        errors = schema.validate(data)
        if errors:
            logger.warning(f"Validation failed for request. Errors: {errors}")
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Perform your business logic (e.g., store data in the database)
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO public.user (id, name, age) VALUES (%s, %s, %s);',
                       (data['id'], data['name'], data['age']))

        connection.commit()
        cursor.close()
        connection.close()

        logger.info("Data stored successfully.")
        return jsonify({'message': 'Data stored successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8080, debug=True)