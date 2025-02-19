import tempfile

import pytest
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.db.db_core import DatabaseCore, DatabaseInitializer
from src.app.db.db_helper import DBHelperSQL
from src.app.db.models import AbstractModel
from src.app.db.query_manager import QueryManager


# ===== Универсальные фикстуры =====
@pytest.fixture
def temp_yaml_file():
    """
    Фикстура для создания временного YAML-файла.
    Создаёт временный файл с указанными данными и возвращает путь к файлу.
    """

    def _create_temp_yaml(data: dict):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml", encoding="utf-8") as temp_file:
            yaml.dump(data, temp_file, default_flow_style=False, allow_unicode=True)
            temp_file.flush()
            return temp_file.name

    return _create_temp_yaml


# ===== Фикстуры для базы данных =====


@pytest.fixture(scope="session")
def test_engine():
    """
    Создает тестовый движок базы данных с SQLite in-memory.
    """
    engine = create_engine("sqlite:///:memory:")
    AbstractModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def test_session(test_engine):
    """
    Создает сессию для работы с базой данных в тестах.
    """
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def mock_app(mock_config_file):
    """
    Создает мок-приложение с заданной конфигурацией для тестирования.
    Использует SQLite in-memory базу данных и временный конфигурационный файл.
    """
    return type(
        "MockApp",
        (object,),
        {
            "config": {
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_CONFIG_PATH_INIT": str(mock_config_file),
            }
        },
    )()


# ===== Конфигурационные и запросные файлы =====


@pytest.fixture
def mock_config_file(temp_yaml_file):
    """
    Создает временный YAML-файл с конфигурацией.
    Используется для тестов, связанных с инициализацией базы данных.
    """
    config_data = {
        "default_permissions": [
            {"name": "read", "description": "Permission to read resources"},
            {
                "name": "write",
                "description": "Permission to create or update resources",
            },
            {"name": "delete", "description": "Permission to delete resources"},
            {"name": "update", "description": "Permission to update resources"},
        ],
        "default_role_name": [
            {
                "role_name": "Root",
                "description": "Root role",
                "permissions": ["read", "write", "delete"],
            },
            {
                "role_name": "Admin",
                "description": "Admin role",
                "permissions": ["read", "write", "update"],
            },
        ],
        "default_users": [
            {"login": "root", "password": "root", "role_name": "Root"},
            {"login": "admin", "password": "admin", "role_name": "Admin"},
        ],
    }
    return temp_yaml_file(config_data)


@pytest.fixture
def temp_query_file(temp_yaml_file):
    """
    Создает временный YAML-файл с запросами.
    """
    queries = {
        "user_queries": {
            "get_user_by_id": "SELECT * FROM users WHERE id = :id",
            "get_all_users": "SELECT * FROM users",
            "update_user_login": "UPDATE users SET login = :login WHERE id = :id",
        },
        "role_queries": {
            "get_role_by_id": "SELECT * FROM roles WHERE id = :id",
            "get_all_roles": "SELECT * FROM roles",
        },
    }
    return temp_yaml_file(queries)


# ===== Фикстуры для компонентов приложения =====


@pytest.fixture
def db_core(mock_app):
    """
    Создает и инициализирует экземпляр DatabaseCore с SQLite in-memory базой данных.
    Использует мок-приложение для конфигурации.
    """
    # Создаем экземпляр DatabaseCore
    db_core_instance = DatabaseCore()

    # Вызываем init_app для инициализации
    db_core_instance.init_app(mock_app)

    # Создаём таблицы
    db_core_instance.create_tables()

    # Инициализируем данные из конфигурации
    DatabaseInitializer(config_path=mock_app.config["SQLALCHEMY_CONFIG_PATH_INIT"])

    return db_core_instance


@pytest.fixture
def db_helper_with_real_queries(mock_app):
    """
    Создает экземпляр DBHelperSQL с реальными SQL-запросами и настроенным DatabaseCore.
    """
    # Инициализация DatabaseCore
    db_core = DatabaseCore()
    db_core.init_app(mock_app)
    db_core.create_tables()

    # Инициализация данных через DatabaseInitializer
    DatabaseInitializer(config_path=mock_app.config["SQLALCHEMY_CONFIG_PATH_INIT"])

    # Инициализация QueryManager с реальными запросами
    query_manager = QueryManager.from_yaml(
        file_path_query_yaml="./config/db_config/queries_sqlite.yaml"
    )  # для тестов файл

    # Возвращаем DBHelperSQL
    return DBHelperSQL(db_core=db_core, query_manager=query_manager)


@pytest.fixture
def query_manager(temp_query_file):
    """
    Создает экземпляр QueryManager с временным YAML-файлом запросов.
    """
    return QueryManager.from_yaml(file_path_query_yaml=temp_query_file)


@pytest.fixture
def db_helper(db_core, query_manager):
    """
    Создает экземпляр DBHelperSQL с DatabaseCore и QueryManager.
    """
    return DBHelperSQL(db_core=db_core, query_manager=query_manager)


@pytest.fixture
def initializer_with_config(mock_config_file):
    """
    Создает экземпляр DatabaseInitializer с загруженной конфигурацией.
    """
    return DatabaseInitializer(config_path=mock_config_file)
