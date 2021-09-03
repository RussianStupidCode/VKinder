from app.vk_receiver.search_criteria import SexCriterion, RelationCriterion
from app.vk_receiver.utils import get_vk_user_age, get_vk_user_city


class VkUser:
    def __init__(self, vk_json_user_info, vk_session):
        self.__user_info = vk_json_user_info
        self.__set_info()

    def __set_info(self):
        self.first_name = self.__user_info.get('first_name', None)
        self.last_name = self.__user_info.get('last_name', None)
        self.id = self.__user_info['id']
        self.url = f'https://vk.com/id{self.id}'

        gender = self.__user_info['sex']
        self.gender = SexCriterion.possible_values.get(gender, None)

        self.age = get_vk_user_age(self.__user_info.get('bdate', None))
        self.city = get_vk_user_city(self.__user_info.get('city', None))

        relation = self.__user_info.get('relation', None)
        self.relation = RelationCriterion.possible_values.get(relation, None)

        self.__set_most_popular_photo()

    def __set_most_popular_photo(self, max_count=3):
        pass
