from random import randint

from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll

from config import VK_TOKEN
from config import VK_GROUP_ID

vk = VkApi(token=VK_TOKEN)
vk_api = vk.get_api()
upload = VkUpload(vk)
long_poll = VkBotLongPoll(vk, VK_GROUP_ID)

MAX_RANDOM = 2**64


def send_message(**kwargs):
    random_id = randint(0, MAX_RANDOM)
    vk_api.messages.send(random_id=random_id, **kwargs)


if __name__ == '__main__':
    print('VkBot started')
    for event in long_poll.listen():
        pass
