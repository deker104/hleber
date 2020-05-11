from random import randint

from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll

from app import create_app
from app.models import User
from config import Config

__doc__ = """Модуль бота ВКонтакте"""


class VkApiGroup(VkApi):
    """Предназначен для авторизации с токеном группы.
    Увеличивает частоту обращений к API с 3 до 20 в секунду.
    Взято здесь: https://github.com/python273/vk_api/commit/c6f3f72
    """
    RPS_DELAY = 1 / 20.0


vk = VkApi(token=Config.VK_TOKEN)
vk_api = vk.get_api()
upload = VkUpload(vk)
long_poll = VkBotLongPoll(vk, Config.VK_GROUP_ID)

MAX_RANDOM = 2**64


def send_message(**kwargs):
    """Упрощённая отправка сообщений: можно забыть о достающем random_id"""
    random_id = randint(0, MAX_RANDOM)
    vk_api.messages.send(random_id=random_id, **kwargs)


def main():
    print('VkBot started')
    for event in long_poll.listen():
        user = User.query.get(event.from_id)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
