import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import toml
import yaml
from dotenv import load_dotenv
from pydantic import Field, TypeAdapter
from pydantic.v1 import PydanticValueError
from pydantic_settings import BaseSettings
from redis import Redis

# Загружаем переменные из .env
load_dotenv()

# Получаем путь к корню
project_root = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[3]))


class LoggerConfig(BaseSettings):
    """
    Класс конфигурации логирования для Flask приложения.

    Этот класс наследуется от Pydantic BaseSettings и используется для загрузки
    и валидации настроек логирования, которые могут быть извлечены из конфигурационного
    файла TOML и YAML. В зависимости от стадии приложения (например, разработка или продакшн),
    выбираются различные конфигурации логирования.

    Атрибуты:
        CONFIG_LOGGER (Optional[dict]): Конфигурация логирования. Может быть None, если конфигурация не найдена.
    """

    CONFIG_LOGGER: Optional[Dict[str, Any]] = None  # Конфигурация логирования по умолчанию None

    @classmethod
    def from_yaml(cls) -> "LoggerConfig":
        """
        Загружает конфигурацию логирования для приложения из TOML и YAML файлов
        в зависимости от стадии (разработка или продакшн).

        Метод сначала проверяет переменную окружения для определения стадии приложения
        и затем загружает путь к YAML файлу с конфигурацией логирования. Если путь найден,
        конфигурация загружается из YAML файла и возвращается как часть экземпляра класса LoggerConfig.
        Если конфигурация не найдена или произошла ошибка, возвращается пустой словарь.

        :return: Экземпляр класса LoggerConfig с загруженной конфигурацией логирования.
        :raises FileNotFoundError: Если не удается найти конфигурационный файл (TOML или YAML).
        :raises PydanticValueError: Если данные в конфигурационном файле не проходят валидацию.
        :raises Exception: Если возникает другая ошибка при загрузке конфигурации.
        """
        try:
            # Задаем переменные
            stages = "CONFIG_PATH_LOGGER_DEV"
            config_toml_path = project_root.joinpath(os.getenv("FLASK_CONFIG_PATH", "config/app_config.toml"))
            # Используем адаптер для преобразования строки в bool
            is_prod_stage = TypeAdapter(bool).validate_python(os.getenv("FLASK_STATUS_PROD_STAGES", False))
            # Проверяем какой у нас STATUS_PROD_STAGES
            if is_prod_stage:
                stages = "CONFIG_PATH_LOGGER_PROD"
            # Загружаем toml файл
            with open(config_toml_path, "r") as file:
                config_data = toml.load(file)

            # Извлечение конфигурации для логера из секции [flask-config-logger]
            logger_config_yaml_path = config_data.get("flask-config-logger", {}).get(stages, None)

            # Загружаем конфигурацию
            if logger_config_yaml_path:
                with open(project_root.joinpath(logger_config_yaml_path), "r") as file:
                    config_yaml = yaml.safe_load(file)
                    return cls(CONFIG_LOGGER=config_yaml)
            return cls(CONFIG_LOGGER={})

        except FileNotFoundError:  # Файл не найдет
            return cls(CONFIG_LOGGER={})
        except PydanticValueError:  # Ошибка валидации
            return cls(CONFIG_LOGGER={})
        except Exception:  # Любые другие ошибки
            return cls(CONFIG_LOGGER={})


class FlaskConfig(BaseSettings):
    """
    Класс конфигурации для Flask приложения.

    Этот класс предоставляет полную настройку для работы Flask-приложения,
    включая параметры разработки, тестирования, сессий, базы данных, логирования и
    управления файлами cookie. Конфигурация загружается из `.env` и TOML-файлов.

    Основные параметры:
    - Настройки окружения (`DEBUG`, `TESTING`, `STATUS_PROD_STAGES`).
    - Конфигурация хоста и шаблонов (`TRUSTED_HOSTS`, `SERVER_NAME`, `APPLICATION_ROOT`).
    - Параметры работы с сессиями (`SECRET_KEY`, `SESSION_TYPE`, `SESSION_REDIS`, и др.).
    - Настройки базы данных SQLAlchemy (`SQLALCHEMY_DATABASE_URI`, `SQLALCHEMY_TRACK_MODIFICATIONS`, и др.).
    - Управление файлами (`MAX_CONTENT_LENGTH`, `USE_X_SENDFILE`).
    - Конфигурация логирования.

    Ключевые особенности:
    - **Динамическая загрузка**: Конфигурация загружается из переменных окружения и TOML-файлов.
    - **Безопасность**: Поддержка безопасной работы с сессиями и cookie.
    - **Гибкость**: Поддерживает как режим разработки, так и режим продакшн.

    Методы:
    - `from_toml(cls)`: Загружает настройки из TOML-файла. Используется для централизованного управления конфигурацией.

    Пример использования:
        config = FlaskConfig.from_toml()
    """

    # ==== Настройки для dev и prod stages из .env ====
    DEBUG: bool = os.getenv("FLASK_STATUS_DEBUG", False)
    TESTING: bool = os.getenv("FLASK_STATUS_TESTING", False)
    STATUS_PROD_STAGES: bool = os.getenv("FLASK_STATUS_PROD_STAGES", False)

    WTF_CSRF_ENABLED: bool = os.getenv("FLASK_WTF_CSRF_ENABLED", True)

    # ==== Настройки конфигурации хоста для Flask ====
    TRUSTED_HOSTS: Optional[List[str]] = None
    SERVER_NAME: Optional[str] = None
    APPLICATION_ROOT: str
    PREFERRED_URL_SCHEME: Optional[str]
    STATIC_URL: str
    JSON_SORT_KEYS: bool

    # ==== Настройки шаблонов и авто опций для Flask ====
    TEMPLATES_AUTO_RELOAD: bool
    EXPLAIN_TEMPLATE_LOADING: bool
    PROVIDE_AUTOMATIC_OPTIONS: bool

    # ==== Настройки шаблонов и авто опций для Flask ====
    MAX_CONTENT_LENGTH: Optional[int] = None
    MAX_FORM_MEMORY_SIZE: int
    MAX_FORM_PARTS: int

    # ====  Настройки перехвата ошибок для Flask ====
    PROPAGATE_EXCEPTIONS: bool
    TRAP_HTTP_EXCEPTIONS: bool
    TRAP_BAD_REQUEST_ERRORS: bool

    # ====  Настройки файлы и кэш для Flask ====
    USE_X_SENDFILE: bool
    SEND_FILE_MAX_AGE_DEFAULT: Optional[int] = None

    # ====  Настройки cookie и сессий для Flask ====
    SECRET_KEY: Optional[str] = os.getenv("FLASK_SECRET_KEY_SESSION", None)
    SECRET_KEY_FALLBACKS: Optional[str] = os.getenv("FLASK_SECRET_KEY_FALLBACKS", None)
    SESSION_REDIS: Optional[Redis] = (
        Redis.from_url(os.getenv("FLASK_SESSION_REDIS_URI")) if os.getenv("FLASK_SESSION_REDIS_URI") else None
    )
    SESSION_COOKIE_NAME: str
    SESSION_COOKIE_DOMAIN: Optional[str] = None
    SESSION_COOKIE_PATH: Optional[str] = None
    SESSION_COOKIE_HTTPONLY: bool
    SESSION_COOKIE_SECURE: bool
    SESSION_COOKIE_PARTITIONED: bool
    SESSION_COOKIE_SAMESITE: Optional[str] = None
    MAX_COOKIE_SIZE: int
    SESSION_PERMANENT: bool
    PERMANENT_SESSION_LIFETIME: int
    SESSION_REFRESH_EACH_REQUEST: bool
    SESSION_KEY_PREFIX: str
    SESSION_TYPE: str
    SESSION_USE_SIGNER: bool
    SESSION_CACHE_SIZE: int
    SESSION_POOL_TIMEOUT: int

    # ====  Настройки базы данных SQLALCHEMY для Flask ====
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    SQLALCHEMY_ECHO: bool
    SQLALCHEMY_RECORD_QUERIES: bool
    SQLALCHEMY_MAX_OVERFLOW: int
    SQLALCHEMY_POOL_SIZE: int
    SQLALCHEMY_POOL_RECYCLE: int
    SQLALCHEMY_CONFIG_PATH_INIT: str
    SQLALCHEMY_CONFIG_PATH_QUERIES_POSTGRESQL: str

    # ====  Настройки SWAGGER OPEN API для Flask (Flask-Smorest) ====
    API_TITLE: str
    API_VERSION: str
    OPENAPI_VERSION: str
    OPENAPI_URL_PREFIX: str
    OPENAPI_SWAGGER_UI_PATH: str
    OPENAPI_SWAGGER_UI_URL: str

    # === Конфигурации для логера ===

    @classmethod
    def from_toml(cls) -> "FlaskConfig":
        """
        Загружает конфигурацию для Flask из TOML файла.

        :return: Экземпляр класса FlaskConfig с данными из конфигурационного файла.
        :raises FileNotFoundError: Если не удается найти файл конфигурации.
        :raises IsADirectoryError: Если путь указывает на директорию, а не на файл.
        :raises toml.TomlDecodeError: Если произошла ошибка при разборе TOML файла.
        :raises ValueError: Если возникла ошибка при загрузке данных в модель Pydantic.
        """
        # Получаем путь до конфигурации app_config.toml
        config_toml_path = project_root.joinpath(os.getenv("FLASK_CONFIG_PATH", "config/app_config.toml"))
        # Чтение данных из TOML файла
        try:
            # Открываем файл и загружаем данные из app_config.toml
            with open(config_toml_path, "r") as file:
                config_data = toml.load(file)
            # Извлечение конфигурации для Flask из секции [flask-config]
            flask_config = config_data.get("flask-config", {})
            # Загружаем в Pydantic модель
            return cls(**flask_config)
        except FileNotFoundError as e:
            raise ValueError(f"File not found: {e}")
        except IsADirectoryError as e:
            raise ValueError(f"Expected file, but found a directory: {e}")
        except toml.TomlDecodeError as e:
            raise ValueError(f"Error decoding TOML file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading FlaskConfig from TOML: {e}")


class AppConfig(BaseSettings):
    flask_config: Dict[str, Any] = Field(default_factory=lambda: FlaskConfig.from_toml().model_dump())
    logging_config_app: Dict[str, Dict[str, Any]] = Field(default_factory=lambda: LoggerConfig.from_yaml().model_dump())
