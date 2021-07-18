from credentials import Credentials
from mailer import Mailer
from config import Config
from pathlib import Path

CONFIG_FILE = Path("config.json")


def main():
    config = Config(CONFIG_FILE)
    settings = config.get_config()
    mail_server = settings.get("credentials").get("server")
    mail_port = settings.get("credentials").get("port")
    mail_login = settings.get("credentials").get("login")
    mail_password = settings.get("credentials").get("password")
    mail_sender = settings.get("mail").get("sender")
    mail_recipients = settings.get("mail").get("recipients")
    mail_subject = settings.get("mail").get("subject")
    # mail_attachments = settings.get("directories").get("send_mail")
    mail_attachments = "config.py"
    mail_credentials = Credentials("mail", server=mail_server, port=mail_port, login=mail_login, password=mail_password)
    mailer = Mailer(mail_credentials)
    mailer.send_mail(mail_sender, mail_recipients, mail_subject, mail_attachments)


if __name__ == '__main__':
    main()
