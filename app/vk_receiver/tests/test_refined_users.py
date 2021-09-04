import pytest
from app.vk_receiver.receiver import VkReceiver
from app.vk_receiver.user_refiner import refined_users, user_suit_value
from app.vk_receiver.search_criteria import CriteriaManager, CityCriterion


@pytest.fixture()
def criteria():
    return CriteriaManager()


@pytest.fixture()
def users_info():
    yield {'count': 15722105, 'items': [{'first_name': 'Светочек', 'id': 19, 'last_name': 'Аленький', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '12.12', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Анна', 'id': 78, 'last_name': 'Руднева', 'can_access_closed': False, 'is_closed': True, 'sex': 1, 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Луиза', 'id': 150, 'last_name': 'Левиева', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '24.4', 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1}, {'first_name': 'Екатерина', 'id': 177, 'last_name': 'Абраменко', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '23.4', 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1, 'interests': '', 'relation': 0}, {'first_name': 'Юля', 'id': 531, 'last_name': 'Шильниковская', 'can_access_closed': False, 'is_closed': True, 'sex': 1, 'bdate': '30.6', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Никита', 'id': 559, 'last_name': 'Куликов', 'can_access_closed': True, 'is_closed': False, 'sex': 2, 'has_photo': 1, 'interests': '', 'relation': 0}, {'first_name': 'Василий', 'id': 628, 'last_name': 'Ефанов', 'can_access_closed': True, 'is_closed': False, 'sex': 2, 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1}, {'first_name': 'Marisabell', 'id': 706, 'last_name': 'Pinashkina', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '11.6', 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1}, {'first_name': 'Антонина', 'id': 761, 'last_name': 'Сердюкова', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '18.4.1987', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Юлия', 'id': 885, 'last_name': 'Смирнова', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '9.8.1990', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}]}


def test_refined_users(users_info, criteria):
    refined, last_index = refined_users(users_info['items'], criteria=criteria)
    assert len(refined) == 8
    assert last_index == 9
    assert refined[0].id == 19


def test_user_suit_value(users_info, criteria: CriteriaManager):
    criteria.possible_criteria['city'] = CityCriterion('Санкт-Петербург', 10, True)
    value = user_suit_value(users_info['items'][0], criteria)
    assert value >= 10
