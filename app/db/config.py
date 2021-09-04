import os

SQLITE_PATH = os.path.join(os.path.dirname(__file__), '../..', 'sqlite3.db')

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': 'localhost',
    'port': '5432',
    'username': 'test_user',
    'password': '12345',
    'database': 'test_db'
}