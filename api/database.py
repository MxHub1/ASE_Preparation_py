# api/database.py
import psycopg2

# Replace this with your PostgreSQL connection details
## DB_CONNECTION_STRING = "postgresql://username:password@localhost:5432/your_database"
## DB_CONNECTION_STRING = "postgresql://@localhost:5432/test_db"

def get_db_connection():
    # connection = psycopg2.connect(DB_CONNECTION_STRING)
    connection = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

    return connection