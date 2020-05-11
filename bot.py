import telebot
from telebot import types
from pymongo import MongoClient
import time

with open("settings_for_bot.txt", "r") as f:
    file_lines = f.readlines()

timer = time.localtime()

bot = telebot.TeleBot(file_lines[0][:len(file_lines[0]) - 1])

client = MongoClient(file_lines[1][:len(file_lines[1])])
db = client.mergebot

F = 0
F1 = 0
F2 = 0


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global F1
    F1 = 1

    if (message.chat.username is None) and (db.token.count_documents({"id": message.chat.id}) == 0):
        inline_item2 = types.InlineKeyboardButton('Создание Username', url='https://telegram-rus.ru/nik')
        inline_bt2 = types.InlineKeyboardMarkup()
        inline_bt2.add(inline_item2)

        bot.send_message(message.chat.id, "У тебя нет никнейма в телеграме, "
                                          "мне приятнее обращаться к людям по никам, а не id."
                                          "Нажав на кнопку, ты узнаешь, как создать никнейм. "
                                          "Но если тебя все устраивает, я не настаиваю, моей работе это не помешает 🤔",
                         parse_mode="html", reply_markup=inline_bt2)

    if message.chat.username is None:
        name_user = str(message.chat.id)
    else:
        name_user = "@" + message.chat.username

    st = open('qaz/privet.webp', 'rb')
    bot.send_sticker(message.chat.id, st)

    if 5 <= timer[3] < 11:
        bot.send_message(message.chat.id,
                         "Доброе утро , " + name_user
                         + "! Какая же ты ранняя пташка, а я ведь мог и спать в это время 😅",
                         parse_mode="html")

    if 11 <= timer[3] < 17:
        bot.send_message(message.chat.id,
                         "Добрый день, " + name_user
                         + "! Как же ты вовремя я только вернулся с обеденного перекуса 🥘 А ты покушал?",
                         parse_mode="html")

    if 17 <= timer[3] < 23:
        bot.send_message(message.chat.id,
                         "Добрый вечер, " + name_user + "! Ого уже вечер, ты домой то не собираешься? 🌅",
                         parse_mode="html")

    if (timer[3] == 23) or (0 <= timer[3] < 5):
        bot.send_message(message.chat.id,
                         "Доброй ночи... добрая ночь... в общем, привет, " + name_user
                         + "! Ты чего не спишь, давай не засиживайся, спать - полезно 😴",
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

    elif db.token.count_documents({"id": message.chat.id}) > 1:
        bot.send_message(message.chat.id, "По твоему id в базе данных я нашел больше одного упоминания! "
                                          "Это ненормально, но твоей вины здесь нет."
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


@bot.message_handler(commands=['problem'])
def send_problem(message):
    global F
    F = 1

    st2 = open('qaz/problem.webp', 'rb')
    bot.send_sticker(message.chat.id, st2)

    bot.send_message(message.chat.id, "Ты уверен??? Если ты нашел ошибку... прости нас 😥", parse_mode="html")

    bot.send_message(message.chat.id, "Кратко опиши проблему, мы постараемся ее исправить в скором времени 😬\n",
                     parse_mode="html", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def dialog(message):
    global F1, F2, F

    if message.chat.username is None:
        name_user = str(message.chat.id)
    else:
        name_user = "@" + message.chat.username

    if message.chat.type == 'private':
        if (message.text == 'Ввод TOKEN') and (F1 == 1):
            F1 = 0
            F2 = 1

        elif F2 == 1:
            cursor3 = db.token.find_one({"id": message.chat.id})
            cur = []
            cursor4 = dict(cursor3)
            for j in cursor4["token"]:
                cur.append(j)
            cur.append(message.text)

            db.token.find_one_and_update({"id": message.chat.id}, {'$set': {"token": cur}})

            bot.send_message(message.chat.id, "Ваш TOKEN был успешно добавлен в нашу базу данных 🎉", parse_mode="html",
                             reply_markup=types.ReplyKeyboardRemove())
            F2 = 0
        elif F == 1:
            bot.send_message('538587223',
                             "Имя пользователя, оставившего комментарий: "
                             + name_user + "\nКомментарий: " + message.text,
                             parse_mode="html")
            F = 0
        else:
            bot.send_message(message.chat.id, 'Странно, такой команды нет...', parse_mode="html",
                             reply_markup=types.ReplyKeyboardRemove())
            F1 = 0
            F2 = 0


bot.polling()
