import pytest
import os
from app.db.connect import session_sqlite
from app.core.db_exchanger import DbExchanger
from app.vk_receiver.vk_user import VkUser


@pytest.fixture
def session():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'test_sqlite3.db')
    Session = session_sqlite(db_path)
    session = Session()

    yield session

    session.close()
    if os.path.exists(db_path):
        os.remove(db_path)


def test_add_suitable_users(session):
    db = DbExchanger(session)
    user_1 = VkUser({'id': 121})
    user_2 = VkUser({'id': 11})
    photos = [{'url': 'dsgdfg'}]
    db.suitable_users_save(user_1, user_2, photos)
    person = db.get_person(user_2.id)

    assert len(person.photos) > 0
    assert person.photos[0]