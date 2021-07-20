import email
import imaplib
import mimetypes
import smtplib
from datetime import datetime
from email.header import decode_header
from email.message import EmailMessage
from email.message import Message
from pathlib import Path
from typing import Union

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
        # CONFIG_FILE - путь к файлу конфигурации
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

    def __decode_name(self, string: str) -> Union[str, bytes]:
        """
        Преобразует имя из base64 в utf-8
        :param string: Текст, который необходимо преодразовать
        :return: Преобразованный в utf-8 текст
        """
        name = decode_header(string)[0][0]
        if isinstance(name, bytes):
            return name.decode("utf-8")
        return name

    def __get_attachments(self, message: Message, subdir: str):
        """
        Получить файл вложения и сохранить его в в поддиректорию с датой
        и временем получения вложения директорию {directories: {accept_attachments} }
        :param message: Необработанное сообщение электронной почты
        :param subdir: Поддиректория с именем "дата_время" для сохранения вложений одного письма
        """
        dir_accept_attachments = Path(self.__config.get("directories").get("accept_attachments")) / Path(subdir)
        if not dir_accept_attachments.exists():
            dir_accept_attachments.mkdir()
        for part in message.walk():
            if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                continue
            file_name = part.get_filename()
            if bool(file_name):
                file_path = dir_accept_attachments / Path(self.__decode_name(file_name))
                with open(file_path, "wb") as attachment_file:
                    attachment_file.write(part.get_payload(decode=True))

    def accept_mail(self):
        """
        Сохранить вложения всех непрочитанных собщений в почтовом ящике
        """
        mail_credentials = self.__credentials.get_credentials()
        imap_server = mail_credentials.get("imap").get("server")
        imap_port = mail_credentials.get("imap").get("port")
        imap_login = mail_credentials.get("login")
        imap_password = mail_credentials.get("password")

        with imaplib.IMAP4_SSL(imap_server, imap_port) as imap_connection:
            imap_connection.login(imap_login, imap_password)
            imap_connection.select("INBOX", readonly=True)
            # Получить все не прочитаные сообщения"
            response_search, all_uids_unseen_messages = imap_connection.uid("search", "SEEN")
            for uid in all_uids_unseen_messages[0].split():
                response_fetch, message_data = imap_connection.uid("fetch", uid, "RFC822")
                raw = email.message_from_bytes(message_data[0][1])
                # Получить все вложения сообщения и сохранить
                # в поддиректорию с датой и временем получения вложений
                # в директории {directories: {accept_attachments} }
                subdir_accept_attachments = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")
                self.__get_attachments(raw, subdir_accept_attachments)
