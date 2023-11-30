# Tg API

![PyPI - Downloads](https://img.shields.io/pypi/dm/tg_api)
![PyPI - License](https://img.shields.io/pypi/l/tg_api)

Библиотека Tg API упрощает работу с веб-API Telegram. Она предоставляет тонкую обёртку над веб API Telegram и библиотекой [HTTPX](https://www.python-httpx.org/). Библиотека Tg API добавляет к обычным возможностям HTTPX свои схемы данных и удобные часто используемые функции, но не мешает, при необходимости, спускаться ниже на уровень HTTP-запросов.

Пример отправки пользователю текстового сообщения:

```py
from tg_api import SyncTgClient, SendMessageRequest


with SyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=tg_chat_id, text='Message proofs high level usage.')
    tg_request.send()
```

## Ключевые возможности библиотеки

Ключевые возможности библиотеки Tg API:

- Поддержка синхронных и асинхронных запросов к API
- Shortcuts для часто используемых запросов
- Лёгкий доступ к боту из любого места в коде
- Наглядные схемы данных для всех типов запросов и ответов API
- Аннотация типов для удобства работы с IDE
- Простое низкоуровневое API для кастомизации запросов к API
- Набор инструментов для удобной работы с исключениями

## Как установить

Библиотека доступна на PyPI:

```shell
$ python -m pip install tg-api
```

## Документация

Документация доступна на Read the Docs: [https://tg-api.readthedocs.io/en/latest/](https://tg-api.readthedocs.io/en/latest/).

<a name="contributing"></a>
## Разработчикам библиотеки Tg API

Инструкции и справочная информация для разработчиков библиотеки Tg API собраны в отдельном документе [CONTRIBUTING.md](CONTRIBUTING.md).
