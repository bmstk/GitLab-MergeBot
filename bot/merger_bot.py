import json
import time

import telebot
from pymongo import MongoClient

with open("./bot/bot_settings.json", "r") as f:
    data = json.load(f)

timer = time.localtime()

telegram_token = data['telegram_token']
bot = telebot.TeleBot(telegram_token)
client = MongoClient(data['mongodb_url'])
db = client.mergebot

webhook_host = data['webhook_host']
webhook_port = data['webhook_port']
