import logging
import time
from functools import wraps
from typing import Any, Callable

# Логгер для профилирования SQL-запросов
logger = logging.getLogger("app_db_profiler_logger")


def profile_sql_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для измерения времени выполнения SQL-запросов.

    Логирует время выполнения функции, переданной в качестве аргумента,
    что позволяет отслеживать производительность запросов к базе данных.

    :param func: Функция, выполняющая SQL-запрос.
    :return: Обернутая функция, измеряющая и логирующая время выполнения.
    """

    @wraps(func)
    def wrapper(self, query_name: str, *args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(self, query_name, *args, **kwargs)  # Выполнение оригинальной функции
        execution_time = time.time() - start_time

        # Определяем уровень логирования
        log_level = logging.WARNING if execution_time > 1.0 else logging.INFO

        logger.log(log_level, f"SQL Query `{query_name}` executed in {execution_time:.4f} sec")
        return result

    return wrapper
