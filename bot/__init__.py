import cherrypy
import gitlab

from bot import config
from bot.merger_bot import bot, db


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
            ##########################################################################################

            for i in assignees_array:  # для каждого пользователя
                print(i['username'])
                private_key = db.token.find_one({'idGitLab': i['username']})  # достаем ключ авторизации пользователя
                print(private_key)

                # авторизуемся для каждого юзера по последнему токену TODO: оставить только один возможный токен
                print("Все токены юзера: " + private_key['token'][-1])
                gl = gitlab.Gitlab('https://git.iu7.bmstu.ru/', private_token=private_key['token'][-1])  # ['token'][-1]
                project = gl.projects.get(project_id)  # находим проект
                result = project.repository_compare(target_branch, source_branch)
                for receiver in db.token.find({'idGitLab': i['username']}):
                    # для каждого телеграм аккаунта, прикрепленного к этому юзеру
                    diff = str(file['diff']).replace("```", "")
                    for file in result['diffs']:
                        message = "Пользователь {0} отправил Вам " \
                                  "запрос на слитие веток {1} и {2} в проекте {3}" \
                                  "\n".format(author_name, target_branch, source_branch, project_name) \
                                  + "```" + diff + "```"
                        bot.send_message(chat_id=receiver['id'], text=message)
