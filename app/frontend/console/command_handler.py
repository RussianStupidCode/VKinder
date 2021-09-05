from app.core import config
from app.core.db.connect import session_sqlite, session_sql_db
from app.core.db_exchanger import DbExchanger
from app.core.vkinder import VkInder, VkReceiver
from app.frontend.console.utils import except_input_wrapper, get_user_input, type_input
from app.frontend.console.criteria_comnands import CriteriaCommandHandler
from app.core.vk_receiver.search_criteria import CriteriaManager
import sys


class CommandHandler:
    def __init__(self):
        self.vkinder = None
        self._criteria = CriteriaManager()
        self.session_maker_db = session_sqlite() if config.IS_SQLITE else session_sql_db()
        self.db_exchanger = DbExchanger(self.session_maker_db())
        self._criteria_command = CriteriaCommandHandler(self._criteria)

        self.is_need_get_user = True
        self.vk_users_generator = None
        self.viewed_users = []

        self._commands = {
            'gsu': self.get_suitable_users,
            'gcl': self.get_criteria_list,
            'exit': CommandHandler.exit,
            'sc': self._criteria_command.change_criterion,
            'afu': self.add_favorites_user,
            'gfu': self.get_favorites_user
        }

    @staticmethod
    def exit():
        sys.exit(1)

    @except_input_wrapper('Неверный токен')
    def set_vk_token(self):
        token = get_user_input('Введите токен')
        vk_receiver = VkReceiver(token)
        vk_receiver.raise_token()
        self.vkinder = VkInder(vk_receiver, self._criteria)
        print('Токен сохранен успешно')

    def get_suitable_users(self):
        if self.is_need_get_user:
            self.vk_users_generator = self.vkinder.get_vk_users_iterable(chunk_size=3)
            self.is_need_get_user = False

        try:
            suitable_users = next(self.vk_users_generator)
            self.viewed_users.extend(suitable_users)
            for user in suitable_users:
                print(user)
        except StopIteration:
            self.is_need_get_user = True
            print('Не найдено подходящих пользователей. Измените критерии поиска')

    def get_criteria_list(self):
        print('Список критериев:')
        criteria = self.vkinder.criteria_info
        for key, value in criteria.items():
            print(f'\t{value}')

    def add_favorites_user(self):
        user_id = type_input(int, 'Введите id пользователя')
        users = [user for user in self.viewed_users if user.id == user_id]
        if len(users) == 0:
            print('Пользователь с таким id вам не показывался')
            return

        self_user = self.vkinder.self_user_info
        favorite = self.db_exchanger.get_person(users[0].id)
        if favorite is not None:
            print('Пользователь уже добавлен в избранное')
            return
        self.db_exchanger.suitable_users_save(self_user, users[0])

    def get_favorites_user(self):
        self_user_id = self.vkinder.self_user_info.id
        favorites = self.db_exchanger.get_favorites(self_user_id)
        for user in favorites:
            print(user)

    def main_loop(self):
        while True:
            command_name = get_user_input('Введите команду')
            if command_name not in self._commands:
                print('Неверная команда')
                continue

            command = self._commands[command_name]
            command()
