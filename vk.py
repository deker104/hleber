from random import randint

from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll

try:
    with open('token.txt', 'r') as f:
        token, group_id = [i.strip() for i in f.readlines()]
except FileNotFoundError:
    raise ImportError

vk = VkApi(token=token)
vk_api = vk.get_api()
upload = VkUpload(vk)
long_poll = VkBotLongPoll(vk, group_id)

MAX_RANDOM = 2**64


def send_message(**kwargs):
    random_id = randint(0, MAX_RANDOM)
    vk_api.messages.send(random_id=random_id, **kwargs)


if __name__ == '__main__':
    print('VkBot started')
    for event in long_poll.listen():
        pass
