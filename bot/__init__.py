import cherrypy
import gitlab
from telebot import types

from bot import config
from bot.merger_bot import bot, db, encoder, decoder
from wsgi import key


class WebhookServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        # raw_body = cherrypy.request.body.read()
        raw_json = cherrypy.request.json  # получаем вебхук
        if raw_json['object_kind'] == 'merge_request':  # если вебхук вызван мержреквестом
            print(raw_json)

            # Парсинг вебхука ########################################################################
            assignees_array = raw_json['assignees']  # находим всем юзеров, заасаненных к мержреквесту
            project_name = raw_json['project']['name']  # название проекта
            project_id = raw_json['project']['id']  # id проекта
            source_branch = raw_json['object_attributes']['source_branch']  # ветка, которую сливаем
            target_branch = raw_json['object_attributes']['target_branch']  # ветка, в которую сливаем
            author_name = raw_json['user']['name']  # имя автора merge request
            merge_request_url = raw_json['object_attributes']['url']  # адрес страницы merge request
            mg_title = raw_json['object_attributes']['title']  # заголовок мерд реквеста
            action = raw_json['object_attributes']['action']  # действие
            ##########################################################################################

            for i in assignees_array:  # для каждого пользователя
                private_key = db.token.find_one(
                    {'idGitLab': encoder(key, i['username'])})  # достаем ключ авторизации пользователя

                # авторизуемся для каждого юзера по последнему токену TODO: оставить только один возможный токен
                gl = gitlab.Gitlab('https://git.iu7.bmstu.ru/',
                                   private_token=decoder(key, private_key['token'][-1]))  # ['token'][-1]
                project = gl.projects.get(project_id)  # находим проект
                result = project.repository_compare(target_branch, source_branch)
                for receiver in db.token.find(encoder(key, {'idGitLab': i['username']})):
                    # для каждого телеграм аккаунта, прикрепленного к этому юзеру
                    for i, file in enumerate(result['diffs']):
                        print(action)
                        if action == 'open':
                            diff = "```" + str(file['diff']).replace("```", "\`\`\`") + "```"
                            message = "Пользователь {0} отправил Вам " \
                                      "запрос на слитие веток {1} и {2} " \
                                      "в проекте {3}\n".format(author_name, target_branch,
                                                               source_branch,
                                                               project_name).replace("_", "\_")
                            bot.send_message(chat_id=receiver['id'], text=message + diff, parse_mode="markdown")

                        if action == 'update' and i <= 3:
                            message = "В Merge Request {0} произошло новое событие.".format(mg_title)
                            bot.send_message(chat_id=receiver['id'], text=message)
                        if action == 'update' and i > 3:
                            message = "А так же еще {0} изменений".format(len(file['diff']) - 3)
                            bot.send_message(chat_id=receiver['id'], text=message)
                            break
                        if action == 'close':
                            message = "Merge request {0} был закрыт.".format(mg_title)
                            bot.send_message(chat_id=receiver['id'], text=message)

                    inline_item1 = types.InlineKeyboardButton('Merge Request', url=merge_request_url)
                    inline_bt1 = types.InlineKeyboardMarkup()
                    inline_bt1.add(inline_item1)

                    bot.send_message(chat_id=receiver['id'],
                                     text="Более подробную информацию о мерж реквесте можно узнать, перейдя по ссылке.",
                                     reply_markup=inline_bt1)
