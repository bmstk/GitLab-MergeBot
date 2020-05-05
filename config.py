API_TOKEN = "850657102:AAEQJOc9kAXjzQNXNh1fqjUsEgZZTXapJdk"


WEBHOOK_HOST = '64.227.126.203'
WEBHOOK_PORT = 80  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './SSL/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './SSL/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % API_TOKEN
