from app.vk_receiver.group_scrapper import get_most_popular_groups
import vk_api

DEFAULT_VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
DEFAULT_VK_API_VERSION = 5.131


class VkReceiver:
    def __init__(self, token=DEFAULT_VK_TOKEN):
        self.__vk_session = vk_api.VkApi(token=token)
        self.__most_popular_group = get_most_popular_groups()[0]
        self.__is_valid = self.__is_token_valid()

    @property
    def search_fields(self):
        return ['sex', 'bdate', ' has_photo', 'interests', 'relation', 'city']

    @property
    def is_valid(self):
        return self.__is_valid

    def __is_token_valid(self):
        try:
            self.__vk_session.method('users.get')
            return True
        except vk_api.exceptions.ApiError:
            return False

    def __get_group_id(self, group_name):
        group = self.__vk_session.method('groups.search', values={'q': group_name})
        return group['items'][0]['id']

    def get_suitable_peoples_id(self, offset=0, max_count=10, **parametrs):
        group_id = self.__get_group_id(self.__most_popular_group)
        params = {
            **parametrs,
            'fields': ",".join(self.search_fields),
            'group_id': group_id,
            'count': max_count,
            'offset': offset
        }
        return self.__vk_session.method('groups.getMembers', values=params)


if __name__ == "__main__":
    session = VkReceiver()
    params = {}
    print(session.get_suitable_peoples_id(**params))