import vk_api

DEFAULT_VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
DEFAULT_VK_API_VERSION = 5.131


class VkReceiver:
    def __init__(self, token=DEFAULT_VK_TOKEN):
        self.__vk_session = vk_api.VkApi(token=token)
        self.__is_valid = self.__is_token_valid()

    @property
    def session(self):
        return self.__vk_session

    @property
    def search_fields(self):
        return ['sex', 'bdate', 'has_photo', 'interests', 'relation', 'city']

    def raise_token(self):
        self.__vk_session.method('users.get')

    @property
    def is_valid(self):
        return self.__is_valid

    def __is_token_valid(self):
        try:
            self.raise_token()
            return True
        except vk_api.exceptions.ApiError:
            return False

    def __get_group_id(self, group_name):
        group = self.__vk_session.method('groups.search', values={'q': group_name})
        return group['items'][0]['id']

    def get_peoples_in_group(self, offset=0, max_count=1000, group_id=1, **parameters):
        """
        метод для выборки из групп, позволяет обойти ограаничение в первые 1000 пользователей
        проблема в необходимости самостоятельного отбора по критериям
        такой подход очень медленный от его использования пока отказался
        """
        params = {
            **parameters,
            'fields': ",".join(self.search_fields),
            'group_id': group_id,
            'count': max_count,
            'offset': offset
        }
        return self.__vk_session.method('groups.getMembers', values=params)

    def get_suitable_peoples(self, offset=0, max_count=1000, **parameters):
        params = {
            **parameters,
            'fields': ",".join(self.search_fields),
            'count': max_count,
            'offset': offset
        }
        return self.__vk_session.method('users.search', values=params)

    def get_city_id(self, name):
        cities = self.__vk_session.method('database.getCities', values={'q': name.lower(), 'country_id': 1})
        return cities['items'][0]['id']

    def get_all_photos(self, user_id):
        params = {
            'owner_id': user_id,
            'extended': 1,
            'album_id': 'profile',
            'photo_sizes': 1,
            'offset': 0,
            'count': 1000
        }
        all_photos = []
        photos = self.__vk_session.method('photos.get', values=params)['items']

        while len(photos) > 0:
            all_photos.extend(photos)
            params['offset'] += params['count']
            photos = self.__vk_session.method('photos.get', values=params)['items']

        return all_photos

    @staticmethod
    def __extract_photo_properties(photo_json_info):
        return {
            'url': photo_json_info['sizes'][-1]['url'],
            'likes': photo_json_info['likes']['count']
        }

    def get_most_popular_photo(self, user_id, max_count=3):
        photos = self.get_all_photos(user_id)
        photos.sort(key=lambda x: x['likes']['count'], reverse=True)
        photos = photos[0:max_count]
        return [VkReceiver.__extract_photo_properties(photo) for photo in photos]

    def get_user_json_info(self, user_id=None):
        params = {'fields': ",".join(self.search_fields)}
        if user_id:
            params['user_ids'] = [user_id]
        return self.__vk_session.method('users.get', values=params)[0]


