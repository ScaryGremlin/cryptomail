import base64
import email
import imaplib
import mimetypes
import smtplib
from email.message import EmailMessage
from email.message import Message
from pathlib import Path

from config import CONFIG_FILE
from config import Config
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
        self.__config = Config(CONFIG_FILE).get_config()

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
        smtp_server = mail_credentials.get("smtp").get("server")
        smtp_port = mail_credentials.get("smtp").get("port")
        smtp_login = mail_credentials.get("login")
        smtp_password = mail_credentials.get("password")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp_connection:
            smtp_connection.login(smtp_login, smtp_password)
            smtp_connection.send_message(email_message)

    def __get_attachments(self, message: Message):
        """
        Получить файл вложения и сохранить его в директорию {directories: {accept_attachments} }
        """
        dir_accept_attachments = self.__config.get("directories").get("accept_attachments")
        for part in message.walk():
            if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                continue
            file_name = part.get_filename()
            transfer_encoding = part.get_all('Content-Transfer-Encoding')
            if transfer_encoding and transfer_encoding[0] == 'base64':
                filename_parts = file_name.split('?')
                print(filename_parts)
                file_name = base64.b64decode(filename_parts[3]).decode(filename_parts[1])
            if bool(file_name):
                file_path = Path(dir_accept_attachments) / Path(file_name)
                with open(file_path, "wb") as attachment_file:
                    attachment_file.write(part.get_payload(decode=True))

    def accept_mail(self):
        """
        Сохранить вложения всех непрочитанных собщений в почтовом ящике
        :return:
        """
        mail_credentials = self.__credentials.get_credentials()
        imap_server = mail_credentials.get("imap").get("server")
        imap_port = mail_credentials.get("imap").get("port")
        imap_login = mail_credentials.get("login")
        imap_password = mail_credentials.get("password")

        with imaplib.IMAP4_SSL(imap_server, imap_port) as imap_connection:
            imap_connection.login(imap_login, imap_password)
            imap_connection.select("INBOX", readonly=True)
            # Получить все сообщения с пометкой "не прочитано"
            response_search, all_uids_unseen_messages = imap_connection.uid("search", "SEEN")
            for uid in all_uids_unseen_messages[0].split():
                response_fetch, message_data = imap_connection.uid("fetch", uid, "RFC822")
                raw = email.message_from_bytes(message_data[0][1])
                self.__get_attachments(raw)
