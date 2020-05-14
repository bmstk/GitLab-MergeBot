import cherrypy
from bot import WebhookServer, config, bot

app = cherrypy.tree.mount(WebhookServer(), '/')

if __name__ == '__main__':
    bot.remove_webhook()
    sleep(2)
    bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

    cherrypy.config.update({
        'server.socket_host': config.WEBHOOK_HOST,
        'server.socket_port': config.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': config.WEBHOOK_SSL_PRIV,
    })

    # Run the application using CherryPy's HTTP Web Server
    cherrypy.quickstart(WebhookServer())
