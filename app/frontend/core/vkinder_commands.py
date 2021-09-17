from app.core import config
from app.core.db.connect import session_sqlite, session_sql_db
from app.core.db_exchanger import DbExchanger
from app.core.vkinder import VkInder, VkReceiver
from app.core.vk_receiver.search_criteria import (CriteriaManager,
                                                  AgeCriterion,
                                                  SexCriterion,
                                                  CityCriterion,
                                                  RelationCriterion)


class VkinderCommands:
    def __init__(self):
        self.vkinder = None
        self._criteria = CriteriaManager()
        self.session_maker_db = session_sqlite() if config.IS_SQLITE else session_sql_db()
        self.db_exchanger = DbExchanger(self.session_maker_db())

        self.is_need_get_user = True
        self.vk_users_generator = None
        self.viewed_users = {}  # список уже показанных пользователей

    def is_new_user_search(self, user_id):
        self_user_id = self.vkinder.self_user_info.id
        return self_user_id != user_id

    @property
    def session(self):
        return self.vkinder.session

    @property
    def main_user_id(self):
        return self.vkinder.self_user_info.id

    def _refresh_suitable_user(self, user_id):
        favorites_user_id = [user.id for user in self.db_exchanger.get_favorites(user_id)]
        self.vk_users_generator = self.vkinder.get_vk_users_iterable(3, favorites_user_id)

    def set_vk_token(self, token):
        vk_receiver = VkReceiver(token)
        vk_receiver.raise_token()
        self.vkinder = VkInder(vk_receiver, self._criteria)

    def change_main_user(self, user_id):
        if not self.is_new_user_search(user_id):
            return

        self.vkinder.set_main_user(user_id)
        self.is_need_get_user = True  # надо получать пользователей заного (обнулить генератор)
        self.vkinder.reset_save_users_id()

    def get_suitable_users(self, user_id) -> list:
        """Возвращает подходящих пользователей """

        if self.is_need_get_user or self.is_new_user_search(user_id):
            self.change_main_user(user_id)
            self._refresh_suitable_user(user_id)
            self.is_need_get_user = False

        try:
            suitable_users = next(self.vk_users_generator)
            if user_id not in self.viewed_users:
                self.viewed_users[user_id] = []
            self.viewed_users[user_id].extend(suitable_users)
            return suitable_users
        except StopIteration:
            self.is_need_get_user = True
        return []

    def get_criteria_list(self, user_id) -> dict:
        self.vkinder.set_main_user(user_id)
        return self.vkinder.criteria_info

    def add_favorites_user(self, user_id, favorites_id):
        self.vkinder.set_main_user(user_id)
        self_user = self.vkinder.self_user_info

        users = [user for user in self.viewed_users[user_id] if user.id == favorites_id]
        if len(users) == 0:
            return

        self.db_exchanger.suitable_users_save(self_user, users[0])

    def get_favorites_user(self, user_id) -> list:
        favorites = self.db_exchanger.get_favorites(user_id)
        return favorites

    def set_criteria(self, name, value, is_required, weight):
        if name == 'age':
            criterion = AgeCriterion(min_age=value[0], max_age=value[1], is_required=is_required, weight=weight)
        else:
            criterion_class = self._criteria.criteria_class[name]
            print(name, value, is_required, weight)
            criterion = criterion_class(value, weight, is_required)
        self._criteria.change_criterion(name, criterion)

