import os

import cherrypy

from bot import config
from bot.merger_bot import bot, db

filename = './webhookPayloads.txt'
if os.path.exists(filename):
    append_write = 'a'  # append if already exists
else:
    append_write = 'w'  # make a new file if not


class WebhookServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        # f = open(filename, append_write)
        # raw_body = cherrypy.request.body.read()
        raw_json = cherrypy.request.json
        # str_obj = json.dumps(raw_json)
        # f.write(str_obj + '\n')
        # f.close()
        assignees_array = raw_json['assignees']
        username_array = []
        for i in assignees_array:
            username_array.append(i['username'])
            print(i['username'])
            for receiver in db.token.find({'idGitLab': i['user_name']}):
                print(receiver)
                bot.send_message(chat_id=receiver['id'], text="Hello! A new merge request is waiting you!")
