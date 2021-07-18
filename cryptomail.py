from credentials import Credentials
from mailer import Mailer
from config import Config
from pathlib import Path

CONFIG_FILE = Path("config.json")


def main():
    config = Config(CONFIG_FILE)
    settings = config.get_config()
    smtp_server = settings.get("credentials").get("smtp_server")
    smtp_port = settings.get("credentials").get("smtp_port")
    imap_server = settings.get("credentials").get("imap_server")
    imap_port = settings.get("credentials").get("imap_port")
    mail_login = settings.get("credentials").get("login")
    mail_password = settings.get("credentials").get("password")
    mail_sender = settings.get("mail").get("sender")
    mail_recipients = settings.get("mail").get("recipients")
    mail_subject = settings.get("mail").get("subject")
    # mail_attachments = settings.get("directories").get("send_mail")
    mail_attachments = "config.py"
    smtp_credentials = Credentials("mail", server=smtp_server, port=smtp_port, login=mail_login, password=mail_password)
    imap_credentials = Credentials("mail", server=imap_server, port=imap_port, login=mail_login, password=mail_password)
    mail_sender = Mailer(smtp_credentials)
    mail_acceptor = Mailer(imap_credentials)
    # mailer.send_mail(mail_sender, mail_recipients, mail_subject, mail_attachments)
    mail_acceptor.accept_mail()

if __name__ == '__main__':
    main()
