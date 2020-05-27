import json

with open("./bot/bot_settings.json", "r") as f:
    data = json.load(f)

user_name = data["object_attributes"]["assignee_id"]


bot.send_message(message.chat.id, user_name)
