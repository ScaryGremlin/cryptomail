class Credentials:
    """
    Класс реквизитов для авторизации
    """
    def __init__(self, api, **kwargs):
        """
        Конструктор
        :param kwargs: Данные авторизации
        """
        self.__api = api
        self.__smtp_server = kwargs.get("smtp_server")
        self.__smtp_port = kwargs.get("smtp_port")
        self.__imap_server = kwargs.get("imap_server")
        self.__imap_port = kwargs.get("imap_port")
        self.__login = kwargs.get("login")
        self.__password = kwargs.get("password")

    def get_credentials(self) -> dict:
        """
        Преобразовать ключ и токен в словарь данных авторизации
        :return: Словарь данных авторизации
        """
        if self.__api == "mail":
            return {
                "smtp": {"server": self.__smtp_server, "port": self.__smtp_port},
                "imap": {"server": self.__imap_server, "port": self.__imap_port},
                "login": self.__login,
                "password": self.__password
            }
