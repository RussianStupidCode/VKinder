from app.vk_receiver.search_criteria import SexCriterion, RelationCriterion
from app.vk_receiver.utils import get_vk_user_age, get_vk_user_city


class VkUser:
    def __init__(self, vk_json_user_info, vk_session):
        self.__vk_session = vk_session
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

    @staticmethod
    def __extract_photo_properties(photo_json_info):
        return {
            'url': photo_json_info['sizes'][-1]['url'],
            'likes': photo_json_info['likes']['count']
        }

    def __set_most_popular_photo(self, max_count=3):
        params = {
            'owner_id': self.id,
            'extended': 1,
            'album_id': 'profile',
            'photo_sizes': 1,
            'count': 1000
        }
        photos = self.__vk_session.method('photos.get', values=params)['items']
        photos.sort(key=lambda x: x['likes']['count'], reverse=True)
        photos = photos[0:max_count]
        self.most_popular_photo = [VkUser.__extract_photo_properties(photo) for photo in photos]