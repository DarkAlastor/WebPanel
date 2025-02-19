from typing import Optional

from flask import session

# Импорт интерфейса для менеджера сессий
from src.app.repository.interface.isession_repo import ISessionManager


class RepositoryFlaskSessionManager(ISessionManager):
    """
    Менеджер сессий для Flask, реализующий интерфейс ISessionManager.

    Этот класс отвечает за взаимодействие с сессией в Flask-приложении.
    Он предоставляет методы для работы с данными, сохраненными в сессии,
    используя Flask's встроенный объект `session`.

    Основные методы:
    - set(key: str, value: str) -> None: Сохраняет значение в сессии по указанному ключу.
    - get(key: str) -> str: Возвращает значение из сессии по указанному ключу.
    - exists(key: str) -> bool: Проверяет, существует ли значение в сессии по указанному ключу.
    """

    def set(self, key: str, value: str) -> None:
        """
        Сохраняет значение в сессии по указанному ключу.

        :param key: Ключ для сохранения данных.
        :param value: Значение для сохранения.
        """
        session[key] = value

    def get(self, key: str) -> Optional[str]:
        """
        Получает значение из сессии по указанному ключу.

        :param key: Ключ для получения данных.
        :return: Значение из сессии по ключу.
        """
        value = session.get(key)
        return value if isinstance(value, str) else None

    def exists(self, key: str) -> bool:
        """
        Проверяет, существует ли значение в сессии по указанному ключу.

        :param key: Ключ для проверки.
        :return: True, если значение существует, иначе False.
        """
        return key in session
