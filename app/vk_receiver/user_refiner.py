from app.vk_receiver.search_criteria import CriteriaManager
from app.vk_receiver.utils import get_vk_user_age, get_vk_user_city
from app.vk_receiver.vk_user import VkUser


def get_user_info(vk_json_user_info) -> dict:
    user_info = {
        'city': get_vk_user_city(vk_json_user_info.get('city', None)),
        'age': get_vk_user_age(vk_json_user_info.get('bdate', None)),
        'sex': vk_json_user_info.get('sex', None),
        'relation': vk_json_user_info.get('relation', None),
    }

    return user_info


def user_suit_value(vk_json_user_info, criteria: CriteriaManager) -> float:
    """возвращает итоговый вес пользователя если 0, то не подходит"""

    result = 0
    if not vk_json_user_info.get('can_access_closed', False):
        return 0

    user_info = get_user_info(vk_json_user_info)

    # Проверка если пользователь не подходит по любому обязательному критерию
    for key, value in user_info.items():
        if criteria.possible_criteria[key].is_required and user_info[key] <= 0:
            return 0
        else:
            result += criteria.possible_criteria[key].get_weight(value)

    # если все критерии необязательны и не было совпадений ни по 1 критерию, то вес будет единичный
    if criteria.is_all_criteria_not_required() and result <= 0:
        return 1

    return result


def refined_users(vk_session, vk_json_users_info: list, max_refined=100, criteria=CriteriaManager()):
    refined_list = []
    last_user_index = 0

    for idx, user in enumerate(vk_json_users_info):
        if user_suit_value(user, criteria):
            refined_list.append(VkUser(user, vk_session))
            last_user_index = idx

        if len(refined_list) >= max_refined:
            break

    return refined_list, last_user_index


if __name__ == "__main__":
    from app.vk_receiver.receiver import VkReceiver
    user = {'count': 15722105, 'items': [{'first_name': 'Светочек', 'id': 19, 'last_name': 'Аленький', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '12.12', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Анна', 'id': 78, 'last_name': 'Руднева', 'can_access_closed': False, 'is_closed': True, 'sex': 1, 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Луиза', 'id': 150, 'last_name': 'Левиева', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '24.4', 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1}, {'first_name': 'Екатерина', 'id': 177, 'last_name': 'Абраменко', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '23.4', 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1, 'interests': '', 'relation': 0}, {'first_name': 'Юля', 'id': 531, 'last_name': 'Шильниковская', 'can_access_closed': False, 'is_closed': True, 'sex': 1, 'bdate': '30.6', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Никита', 'id': 559, 'last_name': 'Куликов', 'can_access_closed': True, 'is_closed': False, 'sex': 2, 'has_photo': 1, 'interests': '', 'relation': 0}, {'first_name': 'Василий', 'id': 628, 'last_name': 'Ефанов', 'can_access_closed': True, 'is_closed': False, 'sex': 2, 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1}, {'first_name': 'Marisabell', 'id': 706, 'last_name': 'Pinashkina', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '11.6', 'city': {'id': 1, 'title': 'Москва'}, 'has_photo': 1}, {'first_name': 'Антонина', 'id': 761, 'last_name': 'Сердюкова', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '18.4.1987', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}, {'first_name': 'Юлия', 'id': 885, 'last_name': 'Смирнова', 'can_access_closed': True, 'is_closed': False, 'sex': 1, 'bdate': '9.8.1990', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'has_photo': 1}]}
    refined, l = refined_users(VkReceiver(), user['items'])
    print(len(refined), l)