from app.vk_receiver.search_criteria import SexCriterion, RelationCriterion
from app.vk_receiver.utils import get_vk_user_age, get_vk_user_city


class VkUser:
    def __init__(self, vk_json_user_info, user_weight=1):
        self.__user_info = vk_json_user_info
        self.user_weight = user_weight
        self.__set_info()

    @staticmethod
    def create_user(**kwargs):
        user = VkUser
        user.id = kwargs['id']
        user.first_name = kwargs.get('first_name', None)
        user.last_name = kwargs.get('last_name', None)
        user.city = kwargs.get('city', None)
        user.age = kwargs.get('age', None)
        user.relation = kwargs.get('relation', None)
        user.gender = kwargs.get('gender', None)
        user.url = f"https://vk.com/id{user.id}"

    def __set_info(self):
        self.first_name = self.__user_info.get('first_name', None)
        self.last_name = self.__user_info.get('last_name', None)
        self.id = self.__user_info.get('id', None)
        self.url = f'https://vk.com/id{self.id}'
        self.interests = self.__user_info.get('interests', None)

        gender = self.__user_info.get('sex', None)
        self.gender = SexCriterion.possible_values.get(gender, None)

        self.age = get_vk_user_age(self.__user_info.get('bdate', None))
        self.city = get_vk_user_city(self.__user_info.get('city', None))

        relation = self.__user_info.get('relation', None)
        self.relation = RelationCriterion.possible_values.get(relation, None)

