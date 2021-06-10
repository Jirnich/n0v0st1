
# 1. Что это?

[n0v0st1](https://t.me/n0v0st1_bot)

Это небольшой телеграм-бот для чтения и поиска новостей.

# 2. Какие библиотеки нужны?

* newsapi-python      0.2.6
* newspaper3k         0.2.8
* pyTelegramBotAPI    3.7.4
* python-telegram-bot 13.6
* telebot             0.0.4

# 3. Как с этим работать?

Бот задеплоин на Heroku напрямую с Github, поэтому в коде указаны и токен самого бота, и ключ newsapi.
Если нужна проверка на своем боте, необходимо делать следующее:

1. При помощи бота [BotFather](https://telegram.me/botfather) создайте нового бота и получите токен.
2. Введите свой токен в следующую строку в `main.py`:

```python
TOKEN = 'token'  # token = токен вашего бота
```
3. Создайте аккаунт на [newsapi.org](https://newsapi.org/) и получите newsapi ключ.
4. Введите свой ключ в следующую строку в `newsfeed.py`:

```python
KEY = 'key'  # key = ваш ключ newsapi
```

5. Бот готов исполнять свой долг. Запустите `main.py`, чтобы бот стартовал.






By Financial University