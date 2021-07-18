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
        self.__server = kwargs.get("server")
        self.__port = kwargs.get("port")
        self.__login = kwargs.get("login")
        self.__password = kwargs.get("password")

    def get_credentials(self) -> dict:
        """
        Преобразовать ключ и токен в словарь данных авторизации
        :return: Словарь данных авторизации
        """
        if self.__api == "mail":
            return {
                "server": self.__server,
                "port": self.__port,
                "login": self.__login,
                "password": self.__password
            }
