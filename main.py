import logging
import telebot
import nltk

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters)

from newsfeed import get_newsfeed, get_searchfeed, summarise
nltk.download('punkt')Ы

def main():
    """Погнали."""

    # настройка сборки логов
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # создаем Updater и указываем в нем токен нашего бота
    # также установим "use_context = True", чтобы получать обратные вызовы на основе нового контекста.
    TOKEN = '1846215057:AAF3U-vIr6gI4RGrcAlh_QXPMMSXv3eVG8E'  # токен нашего бота

    updater = Updater(token=TOKEN, use_context=True)

    # диспетчер для обработчиков
    dp = updater.dispatcher

    # инициируем следующие обработчики

    # обработчик команд
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('search', news_search))
    dp.add_handler(CommandHandler('help', help_menu))

    # обработчик сообщений
    dp.add_handler(MessageHandler(Filters.command, fallback))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # обработчик обратных вызовов
    dp.add_handler(CallbackQueryHandler(news_bulletin, pattern='^\d$'))
    dp.add_handler(CallbackQueryHandler(news_bulletin, pattern='^main$'))

    # запускаем бота
    updater.start_polling()
    print('Бот живет и вам советует.')
    updater.idle()


def start(update, context):
    """Команда: /start. Отправляем пользователю топ новостей"""

    # получаем адреса и заголовки новостей для этого топа
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='Получаем Ваши новости...')
    newsfeed = get_newsfeed()

    # сохраняем url и заголовки для пользователя
    user_data = context.user_data
    ids = [1, 2, 3, 4, 5]
    for i, news in zip(ids, newsfeed):
        user_data[i] = news

    # отправляем новостной топ
    user_data = context.user_data
    titles = [title for (key, (num, url, title)) in user_data.items()]
    message = "*Вот топ-5 новостей на данный момент: *\n"
    message += f"\n1️⃣ {titles[0]}\n\n2️⃣ {titles[1]}\n\n3️⃣ {titles[2]}\n\n4️⃣ {titles[3]}\n\n5️⃣ {titles[4]}"

    keyboard = [[InlineKeyboardButton('Читать 1-ю', callback_data='1'),
                 InlineKeyboardButton('Читать 2-ю', callback_data='2')],
                [InlineKeyboardButton('Читать 3-ю', callback_data='3'),
                 InlineKeyboardButton('Читать 4-ю', callback_data='4')],
                [InlineKeyboardButton('Читать 5-ю', callback_data='5'),
                 InlineKeyboardButton('Мечта', url='https://i2.paste.pics/CR4BJ.png')]]

    context.bot.send_message(chat_id=update.message.chat.id,
                             text=message,
                             reply_markup=InlineKeyboardMarkup(keyboard),
                             parse_mode=ParseMode.MARKDOWN)


def news_bulletin(update, context):
    """Отображение новостного меню"""

    user_data = context.user_data
    query = update.callback_query
    callback = query.data

    if callback == 'main':  # пользователь нажимает кнопку "вернуться к новостям", чтобы вернуться к новостям

        # создаем сообщение главного меню
        titles = [title for (key, (num, url, title)) in user_data.items()]
        message = "*Вот топ-5 новостей на данный момент: *\n"
        message += f"\n1️⃣ {titles[0]}\n\n2️⃣ {titles[1]}\n\n3️⃣ {titles[2]}\n\n4️⃣ {titles[3]}\n\n5️⃣ {titles[4]}"

        # кнопки в главном меню
        keyboard = [[InlineKeyboardButton('Читать 1-ю', callback_data='1'),
                     InlineKeyboardButton('Читать 2-ю', callback_data='2')],
                    [InlineKeyboardButton('Читать 3-ю', callback_data='3'),
                     InlineKeyboardButton('Читать 4-ю', callback_data='4')],
                    [InlineKeyboardButton('Читать 5-ю', callback_data='5'),
                     InlineKeyboardButton('Мечта', url='https://i2.paste.pics/CR4BJ.png')]]

        # отправляй наше главное меню
        query.edit_message_text(text=message,
                                reply_markup=InlineKeyboardMarkup(keyboard),
                                parse_mode=ParseMode.MARKDOWN)

    else:  # пользователь кликает "читать", идем в под-меню
        callback_num = int(query.data)

        # получает конкретный текст
        story = user_data[callback_num]
        (num, url, title) = story

        # создаем сообщение для этого текста
        summary = summarise(url)
        message = '*{}*\n\n'.format(title.upper())
        message += summary
        message += '\n\nЧитать новость полностью [тутъ]({})'.format(url)

        # встроенные кнопки для под-меню
        if callback_num == 1:  # для первой новости
            keyboard_first = [[InlineKeyboardButton('—', callback_data='nil'),
                               InlineKeyboardButton('Следующая', callback_data='2')],
                              [InlineKeyboardButton('Вернуться к новостям', callback_data='main')]]
            query.edit_message_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard_first),
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)

        elif callback_num == 5:  # для последней новости
            keyboard_last = [[InlineKeyboardButton('Предыдущая', callback_data='4'),
                              InlineKeyboardButton('—', callback_data='nil')],
                             [InlineKeyboardButton('Вернуться к новостям', callback_data='main')]]
            query.edit_message_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard_last),
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)

        else:  # для остальных новостей
            prev_story = callback_num - 1
            next_story = callback_num + 1
            keyboard_mid = [[InlineKeyboardButton('Предыдущая', callback_data='{}'.format(prev_story)),
                             InlineKeyboardButton('Следующая', callback_data='{}'.format(next_story))],
                            [InlineKeyboardButton('Вернуться к новостям', callback_data='main')]]
            query.edit_message_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard_mid),
                                    parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)


def news_search(update, context):
    """команда: /search."""

    user_input = update.message.text

    # предложения пользователю ввести нужный ему поисковый запрос
    if user_input == '/search':
        update.message.reply_text(text='Отправьте мне поисковый запрос cледующим образом: `/search <ваш поисковый запрос>`',
                                  parse_mode=ParseMode.MARKDOWN)

    # если пользователь ввел поисковый запрос
    elif user_input.startswith('/search '):
        search_query = list(user_input.partition(' '))[2].strip()
        update.message.reply_text(text='Ищем...')

        # получение результатов поиска
        search = get_searchfeed(query=search_query)

        if search is not None:  # если поиск был успешен
            message = '*Результаты по запросу "{}":*\n\n'.format(search_query)
            for result in search:
                (num, url, title) = result
                message += '{}. {} [Читать]({})\n\n'.format(num, title, url)

            context.bot.send_message(chat_id=update.message.chat.id,
                                     text=message,
                                     parse_mode=ParseMode.MARKDOWN,
                                     disable_web_page_preview=True)

        else:  # если поиск безуспешен
            message = '0 результатов по запросу "{}".'.format(search_query)
            context.bot.send_message(chat_id=update.message.chat.id, text=message)


def help_menu(update, context):
    """коменда: /help."""

    # меню команды help
    message = "Вот команды, что я понимаю:\n"
    message += "`/start`: отправить топ-5 новостей\n"
    message += "`/search`: поиск новости по слову или фразе"

    context.bot.send_message(chat_id=update.message.chat.id, text=message, parse_mode=ParseMode.MARKDOWN,)


def echo(update, context):
    """Бот повторяет ввод пользователя, если пользователь пытается заговорить с ботом 😛"""

    context.bot.send_message(chat_id=update.message.chat.id,
                             text=update.message.text+' 😛')


def fallback(update, context):
    """Сообщение, если была введена неизвестная команда. Команда: /unknown command."""

    context.bot.send_message(chat_id=update.message.chat.id, text="Извините, я таким командам не обучен.")


if __name__ == '__main__':
    main()
