import pytest
from app.vk_receiver.vk_user import VkUser
from app.vk_receiver.receiver import VkReceiver


@pytest.fixture()
def user_info():
    yield {'first_name': 'Светочек', 'id': 19, 'last_name': 'Аленький', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '12.12', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}


@pytest.fixture()
def vk_session():
    yield VkReceiver().session


def test_extract_info(user_info, vk_session):
    user = VkUser(user_info, vk_session)

    assert user.first_name == user_info['first_name']
    assert user.last_name == user_info['last_name']
    assert user.gender == 'женщина'
    assert user.age is None
    assert user.city == user_info['city']['title']
    assert user.relation is None
    assert len(user.most_popular_photo) != 0