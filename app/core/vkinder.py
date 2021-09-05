from app.vk_receiver.receiver import VkReceiver
from app.vk_receiver.vk_user import VkUser
from app.vk_receiver.user_refiner import refined_users
from app.vk_receiver.search_criteria import CriteriaManager, Criterion


class VkInder:
    def __init__(self, vk_receiver=VkReceiver(), criteria=CriteriaManager()):
        self._user = VkUser(vk_receiver.get_user_json_info())
        self._vk_receiver = vk_receiver
        self._criteria = criteria
        self._save_user_id = set()  # id пользователей, которые уже получались в сессии

    def change_criterion(self, name, criterion: Criterion):
        self._criteria.possible_criteria[name] = criterion

    @property
    def saving_user_id(self) -> set:
        return self._save_user_id

    def get_no_repeat_user(self, user_json_info):
        result = [user for user in user_json_info if user['id'] not in self._save_user_id]
        self._save_user_id.update([u['id'] for u in result])
        return result

    def get_user_json_list(self) -> list:
        params = self._criteria.return_vk_params()
        params['city'] = self._vk_receiver.get_city_id(params['city'])['items'][0]['id']
        user_json_info = self._vk_receiver.get_suitable_peoples(**params)['items']
        return self.get_no_repeat_user(user_json_info)

    def get_vk_user_list(self) -> (list, int):
        return refined_users(self.get_user_json_list(), criteria=self._criteria)
