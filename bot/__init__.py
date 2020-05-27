import json
import os

import cherrypy
import simplejson as simplejson

from bot import config

filename = './webhookPayloads.txt'
if os.path.exists(filename):
    append_write = 'a'  # append if already exists
else:
    append_write = 'w'  # make a new file if not


class WebhookServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        f = open(filename, append_write)
        # raw_body = cherrypy.request.body.read()
        raw_json = cherrypy.request.json
        str_obj = json.dumps(raw_json)
        f.write(str_obj + '\n')
        f.close()
        with open("./bot/bot_settings.json", "r") as f:
            data = json.load(f)
        user_name = data["object_attributes"]["assignee_id"]
        bot.send_message(message.chat.id, user_name)
        return ''
