import json
import os

import cherrypy

from bot import config
from bot.merger_bot import bot

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
        assignees_array = []
        for i in raw_json['assignees']:
            assignees_array.append(i['username'])
        user_name = " ".join(assignees_array)
        bot.send_message(chat_id=87763438, text=user_name)
        return ''
