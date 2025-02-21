import logging
from typing import Any, Dict

from dependency_injector.wiring import Provide
from flask import Flask
from flask_session import Session  # type: ignore
from flask_smorest import Api, Blueprint  # type: ignore

from src.app.core.context_processors import utility_routes
from src.app.core.di.di_app import AppContainer
from src.app.db.db_core import DatabaseCore
from src.app.utils.logger_decorators import log_routes

logger = logging.getLogger("app_logger")

# Инициализация контейнера приложения
container = AppContainer()
container.init_resources()
container.wire(modules=[__name__])


@log_routes
def create_app(
    flask_config: Dict[str, Any] = Provide[AppContainer.core.settings_flask].provider(),
    blp: Blueprint = Provide[AppContainer.view.v1_bp].provider(),
    db_core: DatabaseCore = Provide[AppContainer.db.db_core].provider(),
) -> Flask:
    """
    Создает и настраивает экземпляр Flask приложения.

    Параметры:
    ----------
    flask_config : Dict[str, Any]
        Конфигурация приложения, загружаемая из контейнера зависимостей.

    blp : Blueprint
        Blueprint для регистрации маршрутов приложения.

    Возвращает:
    ----------
    Flask:
        Конфигурированное Flask-приложение.
    """
    logger.info("=== Запуск создания приложения ===")

    # Инициализация приложения Flask
    app = Flask(__name__)

    # Конфигурация приложения
    logger.info("=== Инициализация приложения ===")
    app.config.from_mapping(flask_config)

    # Инициализация DatabaseCore
    logger.info("=== Инициализация базы данных ===")
    db_core.init_db(app=app)
    app.extensions["db_core"] = db_core

    # Создание или применение миграций
    with app.app_context():
        # Проверка наличия таблиц и их создание, если необходимо
        db_core.create_tables()

    # Инициализация сессий
    logger.info("=== Инициализация сессий ===")
    api = Api(app=app, spec_kwargs={"title": "WebSslPanel API"})

    Session(app)

    # Регистрация путей и контекстных процессоров
    logger.info("=== Регистрация путей ===")
    api.register_blueprint(blp)
    app.context_processor(lambda: utility_routes(app=app, blueprint_name="v1.main"))
    app.add_url_rule("/", endpoint="v1.main.index")

    # Возврат готового приложения
    return app


# Создание приложения
app = create_app()
