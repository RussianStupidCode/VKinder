from app.core.vk_receiver import VkReceiver
from app.core.vk_receiver import VkUser
from app.core.vk_receiver.user_refiner import refined_users
from app.core.vk_receiver.search_criteria import CriteriaManager, Criterion
import math


class VkInder:
    def __init__(self, vk_receiver, criteria):
        self._user = VkUser(vk_receiver.get_user_json_info())
        self._vk_receiver = vk_receiver
        self._criteria = criteria
        self._save_user_id = set()  # id пользователей, которые уже получались в сессии

    def change_criterion(self, name, criterion: Criterion):
        self._criteria.possible_criteria[name] = criterion

    @property
    def self_user_info(self):
        return self._user

    def set_criteria(self, criteria: dict):
        self._criteria.possible_criteria = criteria

    @property
    def criteria_info(self):
        return self._criteria.criteria

    @property
    def saving_user_id(self) -> set:
        return self._save_user_id

    def get_no_repeat_user(self, user_json_info):
        """
        очистка запрошенных пользователей от тех, которые уже были запрошены ранее
        """
        result = [user for user in user_json_info if user['id'] not in self._save_user_id]
        self._save_user_id.update([u['id'] for u in result])
        return result

    def get_user_json_list(self) -> list:
        params = self._criteria.return_vk_params()
        params['city'] = self._vk_receiver.get_city_id(params['city'])
        user_json_info = self._vk_receiver.get_suitable_peoples(**params)['items']
        return self.get_no_repeat_user(user_json_info)

    def get_vk_user_list(self) -> (list, int):
        return refined_users(self.get_user_json_list(), criteria=self._criteria)

    def get_vk_users_iterable(self, chunk_size=10):
        """генератор для итерации по подходящим пользователям"""

        collection = self.get_vk_user_list()[0]
        count = math.ceil(len(collection) / chunk_size)
        split_collection = [collection[i * chunk_size: (i + 1) * chunk_size] for i in range(count)]
        for users in split_collection:
            for user in users:
                user.photos = self._vk_receiver.get_most_popular_photo(user.id)
            yield users
