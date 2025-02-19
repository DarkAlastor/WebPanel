import logging
from typing import Any, Dict, List, Optional

from sqlalchemy.sql import text

from src.app.utils.error_handlers import handle_db_helper_errors
from src.app.utils.profiler import profile_sql_execution

from .db_core import DatabaseCore
from .query_manager import QueryManager

logger = logging.getLogger("app_db_logger")


class DBHelperSQL:
    """
    Вспомогательный класс для работы с базой данных.

    Этот класс предоставляет методы для выполнения SQL-запросов с использованием
    компонентов `DatabaseCore` и `QueryManager`. Он инкапсулирует логику работы
    с сессиями и запросами, предоставляя удобный интерфейс для операций с базой данных.

    Основные методы:
    - execute_query: Выполнение SELECT-запросов.
    - execute_update: Выполнение INSERT, UPDATE или DELETE-запросов.
    """

    __slots__ = ("db_core", "query_manager")

    def __init__(self, db_core: DatabaseCore, query_manager: QueryManager):
        """
        Инициализация DBHelperSQL.

        :param db_core: Экземпляр DatabaseCore для управления сессиями базы данных.
        :param query_manager: Экземпляр QueryManager для управления SQL-запросами.
        """
        self.db_core = db_core
        self.query_manager = query_manager

    @profile_sql_execution
    @handle_db_helper_errors
    def execute_query(self, query_name: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Выполнить SELECT-запрос по имени.

        :param query_name: Имя запроса, зарегистрированного в QueryManager.
        :param params: Параметры для SQL-запроса (опционально).
        :return: Список строк результата в виде словарей.
        """
        with self.db_core.session_scope() as session:
            query = self.query_manager.get_query(query_name)
            result = session.execute(text(query), params or {})
            logger.debug(f"Запрос {query_name} успешно выполнено")
            return [row._asdict() for row in result]

    @profile_sql_execution
    @handle_db_helper_errors
    def execute_update(self, query_name: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Выполнить INSERT, UPDATE или DELETE-запрос по имени.

        :param query_name: Имя запроса, зарегистрированного в QueryManager.
        :param params: Параметры для SQL-запроса (опционально).
        """
        with self.db_core.session_scope() as session:
            query = self.query_manager.get_query(query_name)
            session.execute(text(query), params or {})
            logger.debug(f"Запрос {query_name} успешно выполнено")
            return True
