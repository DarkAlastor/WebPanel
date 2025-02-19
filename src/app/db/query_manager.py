import logging
from typing import Dict

import yaml

logger = logging.getLogger("app_db_logger")


class QueryManager:
    """
    Класс для управления SQL-запросами.

    Позволяет загружать, регистрировать и получать SQL-запросы из YAML-файла.
    Подходит для работы с динамическими или статическими запросами, разделёнными на категории.
    """

    def __init__(self, file_path_query_yaml: str) -> None:
        """
        Инициализация QueryManager.

        :param file_path_query_yaml: Путь к YAML-файлу с SQL-запросами.
        """
        self.file_path_query_yaml = file_path_query_yaml
        self.queries: Dict[str, str] = {}  # Словарь зарегистрированных запросов

    @classmethod
    def from_yaml(cls, file_path_query_yaml: str) -> "QueryManager":
        """
        Фабричный метод для создания и инициализации QueryManager.

        :param file_path_query_yaml: Путь к YAML-файлу с SQL-запросами.
        :return: Инициализированный экземпляр QueryManager.
        """
        instance = cls(file_path_query_yaml)
        instance._register_queries()
        return instance

    def _load_queries_from_yaml(self) -> Dict[str, Dict[str, str]]:
        """
        Загрузка запросов из YAML-файла.

        :return: Словарь запросов, загруженных из файла.
        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если структура YAML некорректна.
        """
        try:
            with open(self.file_path_query_yaml, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                if not isinstance(data, dict):
                    raise ValueError(f"Некорректный формат YAML в {self.file_path_query_yaml}: ожидается словарь.")
                return data
        except FileNotFoundError:
            logger.error(f"Файл {self.file_path_query_yaml} не найден.")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Ошибка чтения YAML из файла {self.file_path_query_yaml}: {e}")
            raise

    def _register_queries(self) -> None:
        """
        Регистрирует SQL-запросы из YAML-файла.

        Загружает запросы из файла и добавляет их в локальный словарь `queries`.

        :raises ValueError: Если запрос с одинаковым именем уже существует.
        """
        try:
            queries = self._load_queries_from_yaml()
            for category, query_dict in queries.items():
                if not isinstance(query_dict, dict):
                    raise ValueError(f"Категория '{category}' должна содержать словарь запросов.")
                for name, query in query_dict.items():
                    if not isinstance(query, str):
                        raise ValueError(f"Запрос '{name}' в категории '{category}' должен быть строкой.")
                    if name in self.queries:
                        raise ValueError(f"Запрос с именем '{name}' уже зарегистрирован.")
                    self.queries[name] = query
                    logger.debug(f"Запрос '{name}' успешно зарегистрирован.")
        except Exception as e:
            logger.error(f"Ошибка при регистрации запросов: {e}")
            raise

    def get_query(self, name: str) -> str:
        """
        Получить SQL-запрос по имени.

        :param name: Имя зарегистрированного SQL-запроса.
        :return: SQL-запрос в виде строки.
        :raises ValueError: Если запрос с указанным именем не найден.
        """
        query = self.queries.get(name)
        if query is None:
            logger.error(f"Запрос с именем '{name}' не найден.")
            raise ValueError(f"Запрос с именем '{name}' не найден.")
        return query

    def list_queries(self) -> Dict[str, str]:
        """
        Возвращает список всех зарегистрированных запросов.

        :return: Словарь зарегистрированных запросов.
        """
        logger.debug("Получение списка всех зарегистрированных запросов.")
        return self.queries
