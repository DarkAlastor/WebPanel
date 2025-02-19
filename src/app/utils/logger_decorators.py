import logging
from functools import wraps
from typing import Any, Callable, Dict, Tuple

from flask import Flask

# Инициализация логера для веб-приложения
logger = logging.getLogger("web_panel")


def log_routes(func: Callable[..., Flask]) -> Callable[..., Flask]:
    """
    Декоратор для логирования всех маршрутов в приложении Flask.

    Этот декоратор перебирает все маршруты, зарегистрированные в Flask-приложении,
    и выводит их в лог. Логируются путь и endpoint для каждого маршрута.

    :param func: Функция, которая возвращает экземпляр Flask-приложения.
    :return: Обёрнутая функция, которая логирует маршруты.
    """

    @wraps(func)
    def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Flask:
        """
        Обёртка, которая вызывает исходную функцию и логирует маршруты приложения.

        :param args: Аргументы, передаваемые в исходную функцию.
        :param kwargs: Ключевые аргументы, передаваемые в исходную функцию.
        :return: Экземпляр Flask-приложения.
        """
        app = func(*args, **kwargs)
        # Логируем все маршруты приложения
        for rule in app.url_map.iter_rules():
            logger.info(f"Route: {rule}, Endpoint: {rule.endpoint}")
        return app

    return wrapper
