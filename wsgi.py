import threading

import cherrypy
import gitlab
from gitlab import Gitlab
from telebot import types

from bot import WebhookServer, config
from bot.merger_bot import db, timer, bot

app = cherrypy.tree.mount(WebhookServer(), '/')

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': config.WEBHOOK_HOST,
        'server.socket_port': config.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': config.WEBHOOK_SSL_PRIV,
    })

    server_thread = threading.Thread(target=cherrypy.quickstart, args=(WebhookServer(),))
    bot_thread = threading.Thread(target=bot.polling)
    server_thread.start()
    bot_thread.start()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if (message.chat.username is None) and (db.token.count_documents({"id": message.chat.id}) == 0):
        inline_item2 = types.InlineKeyboardButton('Создание Username', url='https://telegram-rus.ru/nik')
        inline_bt2 = types.InlineKeyboardMarkup()
        inline_bt2.add(inline_item2)

        bot.send_message(message.chat.id, "У тебя нет никнейма в телеграме, "
                                          "мне приятнее обращаться к людям по никам, а не id. "
                                          "Нажав на кнопку, ты узнаешь, как создать никнейм. "
                                          "Но если тебя все устраивает, я не настаиваю, моей работе это не помешает 🤔",
                         parse_mode="html", reply_markup=inline_bt2)

    if message.chat.username is None:
        name_user = str(message.chat.id)
    else:
        name_user = "@" + message.chat.username

    st = open('static/privet.webp', 'rb')
    bot.send_sticker(message.chat.id, st)

    if 5 <= timer[3] < 11:
        bot.send_message(message.chat.id,
                         "Доброе утро , " + name_user +
                         "! Какая же ты ранняя пташка, а я ведь мог и спать в это время 😅",
                         parse_mode="html")

    if 11 <= timer[3] < 17:
        bot.send_message(message.chat.id,
                         "Добрый день, " + name_user +
                         "! Как же ты вовремя я только вернулся с обеденного перекуса 🥘 А ты покушал?",
                         parse_mode="html")

    if 17 <= timer[3] < 23:
        bot.send_message(message.chat.id,
                         "Добрый вечер, " + name_user + "! Ого уже вечер, ты домой то не собираешься? 🌅",
                         parse_mode="html")

    if (timer[3] == 23) or (0 <= timer[3] < 5):
        bot.send_message(message.chat.id,
                         "Доброй ночи... добрая ночь... в общем, привет, " + name_user +
                         "! Ты чего не спишь, давай не засиживайся, спать - полезно 😴",
                         parse_mode="html")

    if db.token.count_documents({"id": message.chat.id}) == 1:
        cursor = db.token.find_one({"id": message.chat.id})
        cur = []
        cursor1 = dict(cursor)
        for j in cursor1['token']:
            cur.append(j)
            cur.append('\n')
        token_string = ' '.join(cur)

        bot.send_message(message.chat.id, "По твоему id в базе данных я нашел следующие TOKEN: " + token_string,
                         parse_mode="html")

        item1 = types.KeyboardButton("Ввод TOKEN")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1)

        bot.send_message(message.chat.id, "Хочешь добавить TOKEN - жми на кнопочку ", parse_mode="html",
                         reply_markup=markup)

        bot.register_next_step_handler(message, process_step_1)

    elif db.token.count_documents({"id": message.chat.id}) > 1:
        bot.send_message(message.chat.id, "По твоему id в базе данных я нашел больше одного упоминания! "
                                          "Это ненормально, но твоей вины здесь нет. "
                                          "Напиши /problem и опиши этот случай "
                                          "(можешь перекопировать текст моего сообщения). Извини за неудобства 😬",
                         parse_mode="html")

    elif db.token.count_documents({"id": message.chat.id}) == 0:
        db.token.insert_one({"id": message.chat.id, "token": []})

        inline_item1 = types.InlineKeyboardButton('Как получить TOKEN', url='https://git.iu7.bmstu.ru/')
        inline_bt1 = types.InlineKeyboardMarkup()
        inline_bt1.add(inline_item1)

        item1 = types.KeyboardButton("Ввод TOKEN")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1)

        bot.send_message(message.chat.id, name_user + ", ты у нас впервые, твой id был удачно записан в базу данных.",
                         parse_mode="html", reply_markup=markup)

        bot.send_message(message.chat.id,
                         "Теперь давай добавим TOKEN. Если ты не знаешь, где его найти, нажми на кнопочку ",
                         parse_mode="html", reply_markup=inline_bt1)

        bot.register_next_step_handler(message, process_step_1)


def process_step_1(message):
    if message.text == 'Ввод TOKEN':
        bot.register_next_step_handler(message, process_step_2)
    else:
        bot.send_message(message.chat.id, 'Странно, такой команды нет...', parse_mode="html",
                         reply_markup=types.ReplyKeyboardRemove())


def process_step_2(message):
    # TODO: отрефакторить этот кусок кода
    cursor3 = db.token.find_one({"id": message.chat.id})
    cur = []
    cursor4 = dict(cursor3)
    for j in cursor4["token"]:
        cur.append(j)
    cur.append(message.text)
    #####

    try:
        gl = Gitlab('https://git.iu7.bmstu.ru/', private_token=' '.join(cur))
        gl.auth()
        username = gl.user.username
        db.token.find_one_and_update({"id": message.chat.id}, {'$set': {"token": cur, "idGitLab": username}})

        bot.send_message(message.chat.id,
                         "Ваш TOKEN был успешно добавлен в нашу базу данных 🎉",
                         parse_mode="html",
                         reply_markup=types.ReplyKeyboardRemove())

    except gitlab.GitlabAuthenticationError:
        bot.send_message(message.chat.id,
                         "Произошла ошибка при авторизации в GitLab. Проверьте правильность токена",
                         parse_mode="html")


@bot.message_handler(commands=['problem'])
def send_problem(message):
    st2 = open('static/problem.webp', 'rb')
    bot.send_sticker(message.chat.id, st2)

    bot.send_message(message.chat.id, "Ты уверен??? Если ты нашел ошибку... прости нас 😥", parse_mode="html")

    bot.send_message(message.chat.id, "Кратко опиши проблему, мы постараемся ее исправить в скором времени 😬\n",
                     parse_mode="html", reply_markup=types.ReplyKeyboardRemove())

    bot.register_next_step_handler(message, process_step_3)


def process_step_3(message):
    if message.chat.username is None:
        name_user = str(message.chat.id)
    else:
        name_user = "@" + message.chat.username

    bot.send_message('538587223',
                     "Имя пользователя, оставившего комментарий: " + name_user + "\nКомментарий: " + message.text,
                     parse_mode="html")


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id,
                     "К сожалению, я не знаю, что мне ответить 😓\nНапиши / , чтобы увидеть доступные команды",
                     parse_mode="html")
