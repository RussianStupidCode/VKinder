from app.frontend.console import config
from app.core.db.connect import session_sqlite, session_sql_db
from app.core.db_exchanger import DbExchanger
from app.core.vkinder import VkInder, VkReceiver
from app.frontend.console.utils import except_input_wrapper, get_user_input


class CommandHandler:
    def __init__(self):
        self.vkinder = None
        self.session_maker_db = session_sqlite() if config.IS_SQLITE else session_sql_db()
        self.db_exchanger = DbExchanger(self.session_maker_db())

        self.is_need_get_user = True
        self.vk_users_generator = None

    @except_input_wrapper('Неверный токен')
    def set_vk_token(self):
        token = get_user_input('Введите токен')
        vk_receiver = VkReceiver(token)
        vk_receiver.raise_token()
        print('Токен сохранен успешно')
        self.vkinder = VkInder(vk_receiver)

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


if __name__ == "__main__":
    c = CommandHandler()
    c.set_vk_token()
    while True:
        input('qq:')
        c.get_suitable_users()