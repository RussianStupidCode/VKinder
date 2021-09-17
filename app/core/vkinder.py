from app.core.vk_receiver import VkReceiver
from app.core.vk_receiver import VkUser
from app.core.vk_receiver.user_refiner import refined_users
from app.core.vk_receiver.search_criteria import AgeCriterion, CityCriterion, SexCriterion
import math


class VkInder:
    def __init__(self, vk_receiver, criteria):
        self._user = VkUser(vk_receiver.get_user_json_info())  # пользователь для которого осуществляется подбор
        self._vk_receiver = vk_receiver
        self._criteria = criteria
        VkInder.set_criteria_for_user(self._criteria, self._user)
        self._save_user_id = set()  # id пользователей, которые уже получались в сессии

    def reset_save_users_id(self):
        self._save_user_id = set()

    @property
    def session(self):
        return self._vk_receiver.session

    @staticmethod
    def set_criteria_for_user(criteria, user: VkUser):
        info = user.json_info
        age = info.get('age', None)
        if age is not None:
            criteria.change_criterion('age', AgeCriterion(age - 5, age + 5, 1, is_required=True))

        city = info.get('city')
        if city is not None:
            criteria.change_criterion('city', CityCriterion(city['title'], 1, is_required=True))

        sex = info.get('sex')
        if sex is not None:
            sex = 2 if sex == 1 else 1
            criteria.change_criterion('sex', SexCriterion(sex, 1, is_required=True))

        return criteria

    @property
    def self_user_info(self):
        return self._user

    def set_main_user(self, user_id):
        if user_id == self.self_user_info.id:
            return
        user_json_info = self._vk_receiver.get_user_json_info(user_id)
        self._user = VkUser(user_json_info)
        VkInder.set_criteria_for_user(self._criteria, self._user)

    @property
    def criteria_info(self):
        return self._criteria.criteria

    @property
    def saving_user_id(self) -> set:
        return self._save_user_id

    def get_no_repeat_user(self, user_json_info, favorites_user_id=[]):
        """
        очистка запрошенных пользователей от тех, которые уже были запрошены ранее
        и избранных пользователем
        """
        result = [user for user in user_json_info if user['id'] not in self._save_user_id]
        result = [user for user in result if user['id'] not in favorites_user_id]
        self._save_user_id.update([u['id'] for u in result])
        return result

    def get_user_json_list(self, favorites_user_id=[]) -> list:
        params = self._criteria.return_vk_params()
        params['city'] = self._vk_receiver.get_city_id(params['city'])
        user_json_info = self._vk_receiver.get_suitable_peoples(**params)['items']
        return self.get_no_repeat_user(user_json_info, favorites_user_id)

    def get_vk_user_list(self, favorites_user_id=[]) -> (list, int):
        return refined_users(self.get_user_json_list(favorites_user_id), criteria=self._criteria)

    def get_vk_users_iterable(self, chunk_size=10, favorites_user_id=[]):
        """генератор для итерации по подходящим пользователям"""

        collection = self.get_vk_user_list(favorites_user_id)[0]
        count = math.ceil(len(collection) / chunk_size)
        split_collection = [collection[i * chunk_size: (i + 1) * chunk_size] for i in range(count)]
        for users in split_collection:
            for user in users:
                user.photos = self._vk_receiver.get_most_popular_photo(user.id)
            yield users
