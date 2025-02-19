import logging
from typing import Any, Dict

from dependency_injector.wiring import Provide
from flask import Flask
from flask_migrate import Migrate

from src.app.core.di.di_app import AppContainer
from src.app.db.db_core import DatabaseCore

logger = logging.getLogger("migrate_logger")

# Инициализация контейнера
container = AppContainer()
container.init_resources()
container.wire(modules=[__name__])


def create_migrate_app(
    flask_config: Dict[str, Any] = Provide[AppContainer.core.settings_flask].provider(),
    db_core: DatabaseCore = Provide[AppContainer.db.db_core].provider(),
) -> Flask:
    """
    Создает Flask-приложение только для работы с миграциями.
    """
    logger.info("=== Запуск приложения для миграций ===")

    app = Flask(__name__)

    # Подгружаем конфиг
    flask_config = container.core.settings_flask()
    app.config.from_mapping(flask_config)

    # Настраиваем базу
    db_core: DatabaseCore = container.db.db_core()
    db_core.init_app(app=app)
    app.extensions["db_core"] = db_core

    # Инициализируем миграции
    Migrate(app, db_core.engine)

    return app


app = create_migrate_app()
