import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def mock_env():
    """
    Фикстура для подмены переменных окружения.

    Устанавливает необходимые переменные окружения для тестов, такие как путь к конфигурационному файлу
    и статус продакшена, чтобы обеспечить корректное поведение приложения в тестовой среде.
    """
    with patch.dict(
        os.environ,
        {
            "FLASK_CONFIG_PATH": "config/app_config.toml",
            "FLASK_STATUS_PROD_STAGES": "false",
        },
    ):
        yield


@pytest.fixture
def mock_toml_config():
    """
    Фикстура для корректного TOML-конфига для FlaskConfig.

    Возвращает словарь, имитирующий содержимое TOML-файла, используемого для настройки Flask,
    содержащий основные параметры конфигурации приложения.
    """
    return {
        "flask-config": {
            "DEBUG": True,
            "TESTING": False,
            "STATUS_PROD_STAGES": False,
            "APPLICATION_ROOT": "/",
            "PREFERRED_URL_SCHEME": "http",
            "STATIC_URL": "/static",
            "JSON_SORT_KEYS": True,
            "TEMPLATES_AUTO_RELOAD": True,
            "EXPLAIN_TEMPLATE_LOADING": False,
            "PROVIDE_AUTOMATIC_OPTIONS": True,
            "MAX_FORM_MEMORY_SIZE": 500000,
            "MAX_FORM_PARTS": 1000,
            "PROPAGATE_EXCEPTIONS": False,
            "TRAP_HTTP_EXCEPTIONS": False,
            "TRAP_BAD_REQUEST_ERRORS": False,
            "USE_X_SENDFILE": False,
            "SESSION_COOKIE_NAME": "session",
            "SESSION_COOKIE_HTTPONLY": True,
            "SESSION_COOKIE_SECURE": False,
            "SESSION_COOKIE_PARTITIONED": False,
            "MAX_COOKIE_SIZE": 4093,
            "SESSION_PERMANENT": True,
            "PERMANENT_SESSION_LIFETIME": 86400,
            "SESSION_REFRESH_EACH_REQUEST": False,
            "SESSION_KEY_PREFIX": "web_panel_session:",
            "SESSION_TYPE": "redis",
            "SESSION_USE_SIGNER": True,
            "SESSION_CACHE_SIZE": 100,
            "SESSION_POOL_TIMEOUT": 30,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_RECORD_QUERIES": False,
            "SQLALCHEMY_MAX_OVERFLOW": 10,
            "SQLALCHEMY_POOL_SIZE": 5,
            "SQLALCHEMY_POOL_RECYCLE": 3600,
            "SQLALCHEMY_CONFIG_PATH_INIT": "./config/db_config/config.yaml",
            "SQLALCHEMY_CONFIG_PATH_QUERIES_POSTGRESQL": "./config/db_config/queries_postgres.yaml",
            "API_TITLE": "WebSslPanel API Documentation",
            "API_VERSION": "0.0.1",
            "OPENAPI_VERSION": "3.0.3",
            "OPENAPI_URL_PREFIX": "/api-docs",
            "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
            "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        }
    }


@pytest.fixture
def valid_toml_config():
    """
    Фикстура для корректного TOML-конфига для LoggerConfig.

    Возвращает словарь, имитирующий секцию [flask-config-logger] в основном конфигурационном файле,
    содержащий пути к конфигурационным файлам логгера для разработки и продакшена.
    """
    return {
        "flask-config-logger": {
            "CONFIG_PATH_LOGGER_DEV": "config/logging_config_dev.yaml",
            "CONFIG_PATH_LOGGER_PROD": "config/logging_config_prod.yaml",
        }
    }


@pytest.fixture
def valid_yaml_config():
    """
    Фикстура для корректного YAML-конфига логгера.

    Возвращает словарь с параметрами логирования, который должен быть загружен из YAML-файла,
    содержащий уровень логирования и список обработчиков (handlers).
    """
    return {"level": "INFO", "handlers": ["console"]}


@pytest.fixture
def dummy_flask_config():
    """
    Фикстура для dummy данных FlaskConfig.

    Возвращает словарь с тестовыми данными для Flask-конфигурации, используемыми в тестах AppConfig.
    """
    return {"key": "flask_value"}


@pytest.fixture
def dummy_logger_config():
    """
    Фикстура для dummy данных LoggerConfig.

    Возвращает словарь, имитирующий данные конфигурации логгера, ожидаемые от метода model_dump(),
    с ключом CONFIG_LOGGER.
    """
    return {"CONFIG_LOGGER": {"level": "INFO", "handlers": ["console"]}}
