from app.frontend.core.utils import except_input_wrapper, get_user_input
from app.frontend.core.vkinder_commands import VkinderCommands
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import re
from random import randrange
from app.core.vk_receiver.search_criteria import CriteriaManager
import json

DEFAULT_VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class VkBot:
    def __init__(self):
        self.vkinder = VkinderCommands()
        self.group_session = None
        self.longpoll = None
        self.vkinder.set_vk_token(DEFAULT_VK_TOKEN)
        self._commands = {
            'найти': self.get_suitable_user,
            'критерии': self.print_criteria,
            'фавориты': self.get_favorites,
            'сохранить': self.add_favorites,
            'установить': self.set_criteria,
            'команды': self.print_command_list
        }

    def print_command_list(self, user_id, text):
        self.write_msg(user_id, "\n".join([key for key in self._commands]))

    @except_input_wrapper('Неверный токен')
    def set_user_token(self):
        """нужен для методов, которые требуют ключ пользователя"""
        token = get_user_input('Введите токен пользователя')
        self.vkinder.set_vk_token(token)

    @except_input_wrapper('Неверный токен')
    def set_group_token(self):
        token = get_user_input('Введите токен группы')
        self.group_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.group_session)
        print('токен сохранен успешно')

    def write_msg(self, user_id, message):
        self.group_session.method('messages.send',
                                  {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    @staticmethod
    def _users_to_str(users):
        result = []
        for user in users:
            users_photos = "\n\t".join([p['url'] for p in user.photos])
            user_msg = f"Id пользователя: https://vk.com/id{user.id}\n\tСписок фото: {users_photos}"
            result.append(user_msg)
        return "\n\n".join(result)

    def get_suitable_user(self, user_id, text):
        users = self.vkinder.get_suitable_users(user_id)
        if len(users) == 0:
            message = "Не найдено подходящих пользователей"
        else:
            message = self._users_to_str(users)
        self.write_msg(user_id, message)

    def print_criteria(self, user_id, text):
        criteria = self.vkinder.get_criteria_list(user_id)
        message = []
        for key, value in criteria.items():
            message.append(f'{value}')
        self.write_msg(user_id, "\n".join(message))

    def execute_command(self, user_id, text):
        try:
            for key, value in self._commands.items():
                if key in text:
                    value(user_id, text)
        except:
            self.write_msg(user_id, f"Ошибка при исполнении команды {text}")

    def get_favorites(self, user_id, text):
        favorites = self.vkinder.get_favorites_user(user_id)
        if len(favorites) == 0:
            message = "Нет избранных пользователей"
        else:
            message = self._users_to_str(favorites)
        self.write_msg(user_id, message)

    def add_favorites(self, user_id, text):
        favorites_id = int(text.split()[1])
        try:
            self.vkinder.add_favorites_user(user_id, favorites_id)
            message = f"Пользователь добавлен успешно {favorites_id}"
        except:
            message = f"ошибка при добавлении пользователя {favorites_id}"
        self.write_msg(user_id, message)

    def set_criteria(self, user_id, text):
        text = " ".join(text.split()[1:])  # избавиться от первого слова

        criterion_name = re.search('(.+):.*', text).group(1).lower()
        criterion_name = CriteriaManager.criteria_mapper[criterion_name]
        if criterion_name == 'age':
            values = re.search('(.+): от (\d+) до (\d+).*', text)
            value = (values.group(2), values.group(3))
        elif criterion_name == 'city':
            value = text.split()[1]
        else:
            value = int(text.split()[1])
        is_required = True if re.search(r'\bобязат.*', text) else False
        print(is_required)
        weight = float(text.split()[-1])

        self.vkinder.set_criteria(criterion_name, value, is_required, weight)
        self.write_msg(user_id, 'Критерий установлен успешно')
        self.print_criteria(user_id, text)

    def listen(self):
        print('началась прослушка')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    self.execute_command(event.user_id, event.text)




