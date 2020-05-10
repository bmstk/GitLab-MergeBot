import telebot
from telebot import types
import time

timer = time.localtime()

bot = telebot.TeleBot("951724945:AAGPfKwEp9vM44KXnbr0RsFsRGh1xuiHhc4")

@bot.message_handler(commands = ['start'])
def send_welcome(message):

        st = open('qaz/privet.webp', 'rb')
        bot.send_sticker(message.chat.id, st)

        if 5 <= timer[3] < 11:
                bot.send_message(message.chat.id, "Доброе утро ☀️, @" + message.chat.username + "! Какая же ты ранняя пташка, а я ведь мог и спать в это время 😅", parse_mode = "html")

        if 11 <= timer[3] < 17:
                bot.send_message(message.chat.id, "Добрый день, @" + message.chat.username + "! Как же ты вовремя я только вернулся с обеденного перекуса 🥘 А ты покушал?", parse_mode = "html")

        if 17 <= timer[3] < 23:
                bot.send_message(message.chat.id, "Добрый вечер, @" + message.chat.username + "! Ого уже вечер, ты домой то не собираешься? 🌅", parse_mode = "html")

        if 23 <= timer[3] < 5:
                bot.send_message(message.chat.id, "Доброй ночи... добрая ночь... в общем, привет, @" + message.chat.username + "! Ты чего не спишь, давай не засиживайся, спать - полезно 😴", parse_mode = "html")
                
bot.polling()

while True:
        pass
