import json
import time
from base64 import b64decode, b64encode

import telebot
from pymongo import MongoClient

def encoderforone(word):
    enc = []
    for index, item in enumerate(word):
        key_c = key[index % len(key)]
        enc_c = chr(ord(item) + ord(key_c) % 256)
        enc.append(enc_c)
    return enc


def encoder(key, clear):
    enc = []
    enc1 = []
    if type(clear) == list:
        for word in clear:
            enc = encoderforone(word)
            enc1.append(b64encode("".join(enc).encode()).decode())
        return enc1
    else:
        for index, item in enumerate(clear):
            key_c = key[index % len(key)]
            enc_c = chr(ord(item) + ord(key_c) % 256)
            enc.append(enc_c)

        return b64encode("".join(enc).encode()).decode()


def decoder(key, enc):
    dec = []
    enc = b64decode(enc).decode()
    for index, item in enumerate(enc):
        key_c = key[index % len(key)]
        dec_c = chr((256 + ord(item) - ord(key_c)) % 256)
        dec.append(dec_c)

    return "".join(dec)


with open("./bot/bot_settings.json", "r") as f:
    data = json.load(f)

timer = time.localtime()

key = data['key']

telegram_token = data['telegram_token']
bot = telebot.TeleBot(telegram_token)
client = MongoClient(data['mongodb_url'])
db = client.mergebot

webhook_host = data['webhook_host']
webhook_port = data['webhook_port']
