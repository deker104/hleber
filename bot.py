from flask import url_for
from vk_api.bot_longpoll import VkBotLongPoll

from app import bot
from app import create_app
from app import db
from app.models import User

__doc__ = "Основной скрипт бота"


def main():
    long_poll = VkBotLongPoll(bot.vk, bot.group_id)
    print('VkBot started')
    for event in long_poll.listen():
        user = User.query.get(event.message.from_id)
        message = None
        keyboard = None
        if user is None:
            message = \
                f"Ваш профиль не зарегестрирован на сайте.\n" \
                f"Перейдите по ссылке чтобы зарегестрироваться: " \
                f"{url_for('auth.login')}"
        elif not user.notify:
            user.notify = True
            db.session.add(user)
            message = \
                "Уведомления включены.\n" \
                "Для отключения уведомлений напишите \"Отключить\""
        elif 'отключить' in event.message.text.lower():
            user.notify = False
            db.session.add(user)
            message = \
                "Уведомления отключены.\n" \
                "Для включения уведомлений напишите любое сообщение."
        db.session.commit()
        if message is not None:
            bot.send_message(
                peer_id=event.message.peer_id,
                message=message,
                keyboard=keyboard
            )


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
