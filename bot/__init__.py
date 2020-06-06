import os

import cherrypy
import gitlab

from bot import config
from bot.merger_bot import bot, db

filename = './webhookPayloads.txt'
if os.path.exists(filename):
    append_write = 'a'  # append if already exists
else:
    append_write = 'w'  # make a new file if not

"""
Класс сервера, обеспечивающего работу бэкэнда
"""
class WebhookServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        # f = open(filename, append_write)
        # raw_body = cherrypy.request.body.read()
        raw_json = cherrypy.request.json  # получаем вебхук
        # str_obj = json.dumps(raw_json)
        # f.write(str_obj + '\n')
        # f.close()
        if raw_json['object_kind'] == 'merge_request':  # если вебхук вызван мержреквестом
            print(raw_json)
            assignees_array = raw_json['assignees']  # находим всем юзеров, заасаненных к мержреквесту
            for i in assignees_array:  # для каждого пользователя
                print(i['username'])
                private_key = db.token.find_one({'idGitLab': i['username']}) # достаем ключ авторизации пользователя
                # авторизуемся для каждого юзера по последнему токену TODO: оставить только один возможный токен
                gl = gitlab.Gitlab('https://git.iu7.bmstu.ru/', private_token=private_key['token'][-1])
                project = gl.projects.get(raw_json['project']['id'])  # находим проект
                print(project.mergerequests.list(state='merged', order_by='updated_at'), raw_json['object_attributes']['iid'])
                mr = project.mergerequests.get(raw_json['object_attributes']['iid'])  # находим МР
                for receiver in db.token.find({'idGitLab': i['username']}):
                    # для каждого телеграм аккаунта, прикрепленного к этому юзеру
                    print(receiver)
                    bot.send_message(chat_id=receiver['id'],
                                     text=("Hello! A new merge request is waiting you! \n" + mr.diffs.list()))
                    # шлем юзеру гит див

