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
    if not vk_json_user_info.get('can_access_closed', 0):
        return 0

    # фото обязательно!!!
    if not vk_json_user_info.get('has_photo', 0):
        return 0

    user_info = get_user_info(vk_json_user_info)

    # Проверка если пользователь не подходит по любому обязательному критерию
    for key, value in user_info.items():
        weight_criterion = criteria.possible_criteria[key].get_weight(value)

        if criteria.possible_criteria[key].is_required and weight_criterion <= 0:
            return 0
        else:
            result += weight_criterion

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
