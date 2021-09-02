import vk_api
from vk_receiver.group_scrapper import get_most_popular_groups

DEFAULT_VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
DEFAULT_VK_API_VERSION = 5.131

session = vk_api.VkApi(token=DEFAULT_VK_TOKEN)
api = session.get_api()
groups = get_most_popular_groups()
params = {'offset': 0, 'count': 2, 'q': groups[0]}
print(session.method('groups.search', values=params))