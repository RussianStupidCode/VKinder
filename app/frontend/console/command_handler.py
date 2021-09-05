from app.core import config
from app.core.db.connect import session_sqlite, session_sql_db
from app.core.db_exchanger import DbExchanger
from app.core.vkinder import VkInder, VkReceiver
from app.frontend.console.utils import except_input_wrapper, get_user_input
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

        self._commands = {
            'gsu': self.get_suitable_users,
            'gcl': self.get_criteria_list,
            'exit': CommandHandler.exit,
            'sc': self._criteria_command.change_criterion
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
            for user in suitable_users:
                print(user)
        except StopIteration:
            self.is_need_get_user = True
            print('Не найдено подходящих пользователей. Измените критерии поиска')

    def get_criteria_list(self):
        print('Список критериев:')
        criteria = self.vkinder.criteria_info
        for key in criteria:
            print(f'\t{criteria[key]}')

    def main_loop(self):
        while True:
            command_name = get_user_input('Введите команду')
            if command_name not in self._commands:
                print('Неверная команда')
                continue

            command = self._commands[command_name]
            command()
