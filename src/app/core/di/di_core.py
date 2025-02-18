import logging.config

from dependency_injector import containers, providers
from pydantic_settings import BaseSettings

from src.app.core.config import AppConfig


class CoreContainer(containers.DeclarativeContainer):
    """
    Контейнер зависимостей для настройки и получения конфигурации и логирования.

    Этот контейнер используется для организации зависимостей приложения, таких как конфигурация, логирование
    и настройки для Flask-приложения, с помощью библиотеки `dependency_injector`.

    Attributes:
        config: Провайдер для конфигурации приложения.
        logging_config: Провайдер для настройки конфигурации логгера.
        settings_flask: Провайдер для настройки Flask-приложения.
    """

    # Определяем провайдер для получения конфигурации
    config: providers.Singleton[AppConfig] = providers.Singleton(AppConfig)

    # Настраиваем конфиг для логгера
    logging_config: providers.Resource[None] = providers.Resource(
        logging.config.dictConfig,
        config=config.provided().logging_config_app.get("CONFIG_LOGGER"),
    )

    # Определяем настройки для flask-приложения
    settings_flask: providers.Singleton[BaseSettings] = providers.Singleton(lambda: CoreContainer.config().flask_config)
