from dependency_injector import containers, providers

from src.app.db.db_core import DatabaseCore
from src.app.db.db_helper import DBHelperSQL
from src.app.db.query_manager import QueryManager


class DbContainer(containers.DeclarativeContainer):
    """
    Контейнер зависимостей для работы с базой данных.

    Этот контейнер отвечает за настройку и управление зависимостями,
    связанными с базой данных. Он предоставляет компоненты для работы с
    основной логикой базы данных (DatabaseCore), управления SQL-запросами
    (QueryManager) и вспомогательные методы для работы с базой (DBHelperSQL).

    Основные атрибуты:
    - db_core: Singleton-провайдер для DatabaseCore. Основной компонент для работы с БД.
    - query_manager: Singleton-провайдер для QueryManager. Используется для управления SQL-запросами.
    - db_helper: Singleton-провайдер для DBHelperSQL. Вспомогательный класс для выполнения операций с БД.
    """

    core = providers.DependenciesContainer()

    # Singleton-провайдер для DatabaseCore
    db_core: providers.Singleton[DatabaseCore] = providers.Singleton(DatabaseCore)

    # Singleton-провайдер для QueryManager
    query_manager: providers.Singleton[QueryManager] = providers.Singleton(
        QueryManager.from_yaml,
        file_path_query_yaml="./config/db_config/queries_postgres.yaml",  # тут нужно подправить хардкод
    )

    # Singleton-провайдер для DBHelperSQL
    db_helper: providers.Singleton[DBHelperSQL] = providers.Singleton(
        DBHelperSQL, db_core=db_core, query_manager=query_manager
    )
