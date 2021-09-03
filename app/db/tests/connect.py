import pytest
import os
from app.db.connect import session_sqlite

@pytest.fixture
def session():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'test_sqlite3.db')
    Session = session_sqlite(db_path)
    session = Session()

    yield session

    session.close()
    if os.path.exists(db_path):
        os.remove(db_path)