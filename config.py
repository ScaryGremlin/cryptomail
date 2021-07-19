import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


class Config:
    """
    Класс получения настроек из конфигурационного файла
    """
    def __init__(self, path_to_config_file):
        """
        Конструктор
        :param path_to_config_file: Путь к конфигурационному файлу
        """
        self.__path_to_config_file = path_to_config_file

    def get_config(self) -> dict:
        """
        Получение конфигурационных данных в виде словаря
        :return: Словарь конфигурационных данных
        """
        with open(self.__path_to_config_file, "r") as config_file:
            settings = json.load(config_file)
            return settings
