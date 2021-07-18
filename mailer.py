import mimetypes
import smtplib
from email.message import EmailMessage

from credentials import Credentials


class Mailer:
    """
    Класс работы с электронной почтой
    """
    def __init__(self, credentials: Credentials):
        """
        Конструктор
        :param credentials: Реквизиты для входа
        """
        self.__credentials = credentials

    def send_mail(self, sender: str, recipients: list, subject: str, attachment: str):
        """
        Отправить сообщение электронной почты
        :param sender: Отправитель письма
        :param recipients: Список получателей письма
        :param subject: Тема письма
        :param attachment: Файл для отправки
        """
        email_message = EmailMessage()
        email_message["Subject"] = subject
        email_message["To"] = recipients
        email_message["From"] = sender
        email_message.preamble = "You will not see this in a MIME-aware mail reader. \n"

        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        with open(attachment, 'rb') as attached_file:
            email_message.add_attachment(attached_file.read(), maintype=maintype, subtype=subtype, filename=attachment)

        mail_credentials = self.__credentials.get_credentials()
        mail_server = mail_credentials.get("server")
        mail_port = mail_credentials.get("port")
        mail_login = mail_credentials.get("login")
        mail_password = mail_credentials.get("password")
        with smtplib.SMTP_SSL(mail_server, mail_port) as smtp_server:
            smtp_server.login(mail_login, mail_password)
            smtp_server.send_message(email_message)

    def accept_mail(self):
        pass


