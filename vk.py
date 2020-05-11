from random import randint

from flask import url_for
from vk_api import VkApi, VkUpload

__doc__ = """Модуль Flask-дополнения бота ВКонтакте"""

MAX_RANDOM = 2**64


class VkApiGroup(VkApi):
    """Предназначен для авторизации с токеном группы.
    Увеличивает частоту обращений к API с 3 до 20 в секунду.
    Взято здесь: https://github.com/python273/vk_api/commit/c6f3f72
    """
    RPS_DELAY = 1 / 20.0


class VkBot:
    """Flask-дополнение бота ВКонтакте"""
    def __init__(self, app=None):
        self.token = None
        self.group_id = None
        self.vk = None
        self.api = None
        self.upload = None
        self.long_poll = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.token = app.config.get('VK_TOKEN')
        self.group_id = app.config.get('VK_GROUP_ID')
        self.vk = VkApiGroup(token=self.token)
        self.api = self.vk.get_api()
        self.upload = VkUpload(self.vk)

    def send_message(self, **kwargs):
        """Упрощённая отправка сообщений: можно забыть о достающем random_id"""
        random_id = randint(0, MAX_RANDOM)
        self.api.messages.send(random_id=random_id, **kwargs)

    def notify(self, message, to_user):
        if not to_user or not to_user.notify:
            return
        self.send_message(user_id=to_user.id, message=message)

    def notify_change(self, from_user, to_user, order):
        """Оповещение об изменении заказа"""
        message = \
            f"Клиент {from_user.first_name} {from_user.last_name} изменил параметры заказа.\n\n" \
            f"Ссылка на заказ: {url_for('orders.about', id=order.id, _external=True)}"
        self.notify(message, to_user)

    def notify_delete(self, from_user, to_user):
        """Оповещение об удалении заказа"""
        message = \
            f"Клиент {from_user.first_name} {from_user.last_name} удалил свой заказ." \
            f"Вы были автоматически освобождены от его выполнения.\n\n" \
            f"Список активных заказов: {url_for('orders.taken', _external=True)}"
        self.notify(message, to_user)

    def notify_client_confirm(self, from_user, to_user, order):
        """Оповещение о подтверждении заказа клиентом"""
        message = \
            f"Клиент {from_user.first_name} {from_user.last_name} подтвердил выполнение заказа.\n\n" \
            f"Ссылка на заказ: {url_for('orders.about', id=order.id, _external=True)}"
        self.notify(message, to_user)

    def notify_volunteer_confirm(self, from_user, to_user):
        """Оповещение о завершении заказа волонтёром"""
        message = \
            f"Волонтёр {from_user.first_name} {from_user.last_name} отметил заказ как выполненый.\n\n" \
            f"Список ваших заказов: {url_for('orders.given', _external=True)}"
        self.notify(message, to_user)
