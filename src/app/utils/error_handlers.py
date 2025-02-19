import logging
from functools import wraps
from typing import Any, Callable, Optional

from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            ProgrammingError, SQLAlchemyError)

# Инициализация логера для базы данных
logger = logging.getLogger("app_db_logger")


def handle_error_for_database(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для обработки ошибок, возникающих при работе с базой данных.

    Этот декоратор применяется к методам, выполняющим SQL-запросы через ORM или напрямую.
    Он перехватывает ошибки SQLAlchemy и другие исключения, логирует их и выбрасывает снова,
    позволяя системе корректно обрабатывать сбои в базе данных.

    :param func: Функция, выполняющая операцию с базой данных.
    :return: Обернутая функция, перехватывающая ошибки базы данных.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных в {func.__name__}: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Непредвиденная ошибка в {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper


def handle_db_helper_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для обработки ошибок в `DBHelperSQL`.

    Этот декоратор предназначен для обработки ошибок, возникающих при выполнении SQL-запросов
    в `DBHelperSQL`. Он логирует ошибки и добавляет контекст запроса и параметры.

    Если ошибка происходит в методе обновления (`execute_update`), он возвращает `False`,
    в противном случае — пустой список `[]`.

    :param func: Функция, выполняющая SQL-запрос.
    :return: Обернутая функция с обработкой ошибок.
    """

    @wraps(func)
    def wrapper(
        self: Any,
        query_name: str,
        params: Optional[dict] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        try:
            return func(self, query_name, params, *args, **kwargs)

        except OperationalError:
            logger.critical(
                f"Ошибка подключения к БД при выполнении '{query_name}', params: {params}",
                exc_info=True,
            )
            return False if "update" in func.__name__ else []

        except IntegrityError:
            logger.warning(
                f"Ошибка целостности данных в '{query_name}', params: {params}",
                exc_info=True,
            )
            return False if "update" in func.__name__ else []

        except ProgrammingError:
            logger.error(
                f"Ошибка SQL-синтаксиса в '{query_name}', params: {params}",
                exc_info=True,
            )
            return False if "update" in func.__name__ else []

        except DataError:
            logger.warning(f"Ошибка типа данных в '{query_name}', params: {params}", exc_info=True)
            return False if "update" in func.__name__ else []

        except SQLAlchemyError:
            logger.error(
                f"Общая ошибка SQLAlchemy в '{query_name}', params: {params}",
                exc_info=True,
            )
            return False if "update" in func.__name__ else []

        except Exception as e:
            logger.error(
                f"Непредвиденная ошибка в '{query_name}', params: {params}: {e}",
                exc_info=True,
            )
            return False if "update" in func.__name__ else []

    return wrapper
