import json
import time

import telebot
from pymongo import MongoClient

with open("./bot/bot_settings.json", "r") as f:
    data = json.load(f)

timer = time.localtime()

bot = telebot.TeleBot(data['telegram_token'])
client = MongoClient(data['mongodb_url'])
db = client.mergebot
