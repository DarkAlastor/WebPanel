import time
from unittest.mock import patch

import pytest
from flask import Flask
from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            ProgrammingError, SQLAlchemyError)

from src.app.utils.error_handlers import (handle_db_helper_errors,
                                          handle_error_for_database)
from src.app.utils.logger_decorators import log_routes
from src.app.utils.profiler import profile_sql_execution


# ================== Для тестов test_profiler ==================
@pytest.fixture
def mock_logger():
    """
    Фикстура для мокирования логгера.
    """
    with patch("src.app.utils.profiler.logger") as mock_log:
        yield mock_log


@pytest.fixture
def fast_query():
    """
    Тестовая функция, эмулирующая быстрый SQL-запрос (< 1 сек).
    """
    mock_self = object()  # Используем пустой объект для имитации self

    @profile_sql_execution
    def query_func(self, query_name):
        return "fast_result"

    return lambda query_name: query_func(mock_self, query_name)


@pytest.fixture
def slow_query():
    """
    Тестовая функция, эмулирующая медленный SQL-запрос (> 1 сек).
    """
    mock_self = object()

    @profile_sql_execution
    def query_func(self, query_name):
        time.sleep(1.2)  # Искусственно замедляем запрос
        return "slow_result"

    return lambda query_name: query_func(mock_self, query_name)


@pytest.fixture
def query_with_args():
    """
    Тестовая функция, принимающая SQL-запрос через args.
    """
    mock_self = object()

    @profile_sql_execution
    def query_func(self, query_name, query):
        return f"executed {query}"

    return lambda query_name, query: query_func(mock_self, query_name, query)


@pytest.fixture
def query_with_kwargs():
    """
    Тестовая функция, принимающая SQL-запрос через kwargs.
    """
    mock_self = object()

    @profile_sql_execution
    def query_func(self, query_name, **kwargs):
        return f"executed {kwargs.get('query', 'unknown')}"

    return lambda query_name, **kwargs: query_func(mock_self, query_name, **kwargs)


# ================== Для тестов test_logger_decorators ==================
@pytest.fixture
def sample_app() -> Flask:
    """
    Фикстура, создающая тестовое Flask-приложение с одним тестовым маршрутом.
    """
    app = Flask("test_app")

    @app.route("/hello")
    def hello():
        return "Hello, world!"

    return app


@pytest.fixture
def decorated_app(sample_app) -> callable:
    """
    Фикстура, создающая функцию, возвращающую Flask-приложение,
    декорированное декоратором log_routes.
    """

    @log_routes
    def create_app() -> Flask:
        """Создает тестовое Flask-приложение."""
        return sample_app

    return create_app


# ================== Для тестов handlerr error for db ==================
@pytest.fixture
def dummy_success():
    """
    Фикстура, возвращающая функцию, обёрнутую декоратором handle_error_for_database,
    которая отрабатывает без ошибок.
    """

    @handle_error_for_database
    def func(*args, **kwargs):
        return "success"

    return func


@pytest.fixture
def dummy_sqlalchemy_error():
    """
    Фикстура, возвращающая функцию, обёрнутую декоратором handle_error_for_database,
    которая генерирует SQLAlchemyError.
    """

    @handle_error_for_database
    def func(*args, **kwargs):
        raise SQLAlchemyError("sqlalchemy error")

    return func


@pytest.fixture
def dummy_generic_error():
    """
    Фикстура, возвращающая функцию, обёрнутую декоратором handle_error_for_database,
    которая генерирует обычное исключение.
    """

    @handle_error_for_database
    def func(*args, **kwargs):
        raise ValueError("generic error")

    return func


# ================== Для тестов db_helper ==================


# Фикстуры для корректного выполнения
@pytest.fixture
def dummy_helper_success_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            return "query_success"

    return Dummy()


@pytest.fixture
def dummy_helper_success_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            return "update_success"

    return Dummy()


# Фикстуры для OperationalError
@pytest.fixture
def dummy_helper_operational_error_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            raise OperationalError("op error", None, None)

    return Dummy()


@pytest.fixture
def dummy_helper_operational_error_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            raise OperationalError("op error", None, None)

    return Dummy()


# Фикстуры для IntegrityError
@pytest.fixture
def dummy_helper_integrity_error_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            raise IntegrityError("integrity error", None, None)

    return Dummy()


@pytest.fixture
def dummy_helper_integrity_error_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            raise IntegrityError("integrity error", None, None)

    return Dummy()


# Фикстуры для ProgrammingError
@pytest.fixture
def dummy_helper_programming_error_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            raise ProgrammingError("programming error", None, None)

    return Dummy()


@pytest.fixture
def dummy_helper_programming_error_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            raise ProgrammingError("programming error", None, None)

    return Dummy()


# Фикстуры для DataError
@pytest.fixture
def dummy_helper_data_error_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            raise DataError("data error", None, None)

    return Dummy()


@pytest.fixture
def dummy_helper_data_error_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            raise DataError("data error", None, None)

    return Dummy()


# Фикстуры для SQLAlchemyError
@pytest.fixture
def dummy_helper_sqlalchemy_error_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            raise SQLAlchemyError("sqlalchemy error")

    return Dummy()


@pytest.fixture
def dummy_helper_sqlalchemy_error_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            raise SQLAlchemyError("sqlalchemy error")

    return Dummy()


# Фикстуры для Generic Exception


@pytest.fixture
def dummy_helper_generic_error_query():
    class Dummy:
        @handle_db_helper_errors
        def execute_query(self, query_name, params=None, *args, **kwargs):
            raise Exception("generic error")

    return Dummy()


@pytest.fixture
def dummy_helper_generic_error_update():
    class Dummy:
        @handle_db_helper_errors
        def execute_update(self, query_name, params=None, *args, **kwargs):
            raise Exception("generic error")

    return Dummy()
