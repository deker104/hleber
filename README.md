# Хлебер-β [![Build Status](https://travis-ci.com/deker104/hleber.svg?branch=master)](https://travis-ci.com/deker104/hleber)

![Логотип Хлебер-β](./app/static/img/icon.png)

**Хлебер-β** (_хлебер-бетта_) - это приложение от студентов _Яндекс.Лицея_, созданное помочь людям, которые в период пандемии не могут самостоятельно выбраться на улицу и купить необходимые продукты и лекарства.
Для решения проблемы мы создали систему, связывающую нуждающихся людей с людьми, желающими им помочь.

**Хлебер-β** состоит из двух частей:
- Веб-сайт, на котором пользователь может зарегестрироваться как "клиент", чтобы оставить заказ, или как "волонтёр", чтобы получить удобные инструменты для исполнения этих закозов, например карта ближайших к дому клиента магазинов.
- Бот _ВКонтакте_, оповещающий клиентов и волонтёров об изменениях, связанных с их заказами.

## Запуск копии приложения

### Установка

- Сохраните копию ветки _master_ на компьютер.

- Создайте виртуальное окружение _Python_ и установите зависимости из `requirements.txt`.

- Задайте параметры приложения через переменные среды:

```
GEOCODER_KEY=<API-ключ Геокодера>
GEOSEARCH_KEY=<API-ключ Поиска по организациям>
VK_TOKEN=<токен группы-представителя бота ВКонтакте>
VK_GROUP_ID=<id группы-представителя>
VK_APP_ID=<id ВК-приложения сайта>
VK_SECRET_KEY=<секретный ключ ВК-приложения сайта>
```

- Вы можете сделать это созданием в корневой директории файла конфигурации `.env`.

- Запустите создание таблиц в БД:

```cmd
> flask db upgrade
```

### Запуск

- Запустите _Flask_-приложение.
    - Вы можете просто запустить `wsgi.py` как _Python_-скрипт _(рекомендовано для быстрой отладки)_;
    - Либо запустить его с помощью `gunicorn` или любого другого _WSGI_-сервера _(рекомендовано для стабильной работы)_:

```cmd
> gunicorn -b 0.0.0.0:8000 wsgi:app
```

- Параллельно запустите бота _ВКонтакте_ запуском `vk.py` в качестве _Python_-скрипта.

- _(не обязательно)_ Настройте доступ к Flask-приложению через какой-нибудь proxy-сервер (например _nginx_).
Это сильно улучшит производительно за счёт улучшенной параллелизации и отдельного обслуживания proxy-сервером статичных файлов.

### Обновление

- Загрузите на компьютер обновлённую ветку _master_.

- Обновите структуру таблиц в БД:

```cmd
> flask db upgrade
```

## Структура проекта

- `/app/` - модуль веб-сайта.
    - `/app/static/` - директория для статичных файлов.
    - `/app/templates/` - шаблоны веб-страниц (_Jinja2_).
- `/migrations/` - служебные файлы _alembic_.
- `/.env` - файл конфигурации, параметры из которого загружаются в переменные среды.
- `/Procfile` - файл, задающий процессы для запуска на сервере _Heroku_.
- `/requirements.txt` - файл с зависимостями проекта.

Описание ко всем неупомянутым файлам находится в их собственной документации.

## Используемые технологии

- _Heroku_ - хостинг всего веб-приложения, включая БД.
- _Flask_ - микро-фреймворк, используемый для создания веб-сайта.
- _SQLAlchemy*_ - библиотека ORM для доступа к БД.
    - _Alembic*_ - библиотека, позволяющая вносить правки в БД без потери данных.
- _WTForms*_ - библиотека для задания HTML-форм с помощью ООП.
- _Flask-Login_ - дополнение к Flask для удобной авторизации пользователей.
- _API Яндекс.Карт (в частности Static API, Geocoder и Поиск по организациям)_ - API рендера карт на странице и поиска объектов по адресу.
- _Bootstrap_ - CSS-фреймворк, отвечающий за всю красоту на нашем веб-сайте.
- _vk-api (python273)_ - библиотека для создания приложений на основе VK API.
- _pytest_ и _Travis CI_ - инструменты для автоматического тестирования приложения перед его загрузкой на сервер. 

_Модули, помеченые звёздочкой, подключены к Flask с помощью специальных дополнений._

## Планы по улучшению

- **Улучшение безопасности.**
Проект отпалирован не до конца, и всё ещё существуют некоторые проблемы с проверкой прав пользователей на посещение страниц.
- **JavaScript API карт.**
Статические карты, используемые в проекте, не являются лучшем решением для помощи волонтёрам.
Куда удобнее было бы использовать для этой цели отдельные виджеты с картами, однако на данный момент такой возможности нет.
- **Тестирование.**
Сейчас единственная функция, выполняемая CI, это проверка сборки проекта и его запуска.
Нам бы хотелось уметь в автоматическом режиме проверять работоспособность веб-страниц и БД.
- **Инструкция.**
Единственным способом разобраться с управлением на сайте является "метод тыка".
И пускай веб-сайт не обладает какой-то особо запутанной структурой, некоторым пользователям может быть сложно разобраться с ним самостоятельно.
