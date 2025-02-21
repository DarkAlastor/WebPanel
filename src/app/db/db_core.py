import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Type

import yaml
from flask import Flask
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.security import generate_password_hash

from src.app.utils.error_handlers import handle_error_for_database

from .models import (AbstractModel, PermissionModel, RoleModel,
                     RolePermissionModel, UserModel)

logger = logging.getLogger("app_db_logger")


class DatabaseInitializer:
    """
    Класс для инициализации базы данных начальными данными.

    Загружает конфигурацию из YAML-файла и добавляет начальные данные:
    - Права доступа (permissions)
    - Роли (roles) и их привязки к правам
    - Пользователей (users) и их привязки к ролям.
    """

    def __init__(self, config_path: str) -> None:
        """
        Инициализация экземпляра DatabaseInitializer.

        :param config_path: Путь к YAML-файлу с начальными данными.
        """
        self.config_path: str = config_path

    def initialize_db(self, session: Session) -> None:
        """
        Инициализирует базу данных начальными данными.

        Загружает конфигурацию и вызывает методы добавления данных.

        :param session: SQLAlchemy-сессия для работы с базой данных.
        """
        logger.info("Старт инициализации базы данных")
        config = self._config_loader()

        default_permissions = config.get("default_permissions", [])
        default_roles = config.get("default_role_name", [])
        default_users = config.get("default_users", [])

        if default_permissions:
            self._add_default_permissions(session=session, permissions=default_permissions)
        if default_roles:
            self._add_default_roles(session=session, roles=default_roles)
        if default_users:
            self._add_default_users(session=session, users=default_users)
        logger.info("Инициализация базы данных завершена")

    def _config_loader(self) -> Dict[str, Any]:
        """
        Загружает конфигурацию из YAML-файла.

        :return: Словарь с конфигурацией.
        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если файл не удалось прочитать или содержимое некорректное.
        """
        try:
            logger.info(f"Загрузка конфигурации из {self.config_path}")
            with open(self.config_path, "r") as file:
                config = yaml.safe_load(file)
                if not isinstance(config, dict):
                    raise ValueError(f"Некорректное содержимое файла {self.config_path}: ожидался словарь.")
                return config
        except FileNotFoundError:
            logger.error(f"Файл конфигурации {self.config_path} не найден!")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Ошибка чтения файла конфигурации {self.config_path}: {e}")
            raise

    def __get_or_create(
        self,
        session: Session,
        model: Type[AbstractModel],
        filters: Dict[str, Any],
        defaults: Dict[str, Any] = {},
    ) -> AbstractModel:
        """
        Получает существующую запись или создаёт новую.

        :param session: Сессия базы данных.
        :param model: Модель базы данных, с которой выполняется работа.
        :param filters: Условия поиска существующей записи.
        :param defaults: Значения по умолчанию для создания новой записи.
        :return: Экземпляр модели (существующий или новый).
        """
        instance = session.query(model).filter_by(**filters).first()
        if instance is None:
            instance = model(**{**filters, **defaults})
            session.add(instance)
            logger.info(f"Добавлена новая запись в {model.__name__}: {filters}")
        return instance  # type: ignore

    @handle_error_for_database
    def _add_default_permissions(self, session: Session, permissions: List[Dict[str, Any]]) -> None:
        """
        Добавляет права доступа в базу данных.

        :param session: Сессия базы данных.
        :param permissions: Список прав доступа для добавления.
        """
        logger.info("Добавление прав доступа")
        for permission_data in permissions:
            self.__get_or_create(
                session,
                PermissionModel,
                {"name": permission_data["name"]},
                {"description": permission_data.get("description", "")},
            )

    @handle_error_for_database
    def _add_default_roles(self, session: Session, roles: List[Dict[str, Any]]) -> None:
        """
        Добавляет роли и их привязки к правам в базу данных.

        :param session: Сессия базы данных.
        :param roles: Список ролей для добавления.
        """
        logger.info("Добавление ролей")
        for role_data in roles:
            role = self.__get_or_create(
                session,
                RoleModel,
                {"role_name": role_data["role_name"]},
                {"description": role_data.get("description", "")},
            )
            for perm_name in role_data.get("permissions", []):
                permission = session.query(PermissionModel).filter_by(name=perm_name).first()
                if permission:
                    self.__get_or_create(
                        session,
                        RolePermissionModel,
                        {"role_id": role.id, "permission_id": permission.id},
                    )

    @handle_error_for_database
    def _add_default_users(self, session: Session, users: List[Dict[str, Any]]) -> None:
        """
        Добавляет пользователей и их привязки к ролям в базу данных.

        :param session: Сессия базы данных.
        :param users: Список пользователей для добавления.
        """
        logger.info("Добавление пользователей")
        for user_data in users:
            role = session.query(RoleModel).filter_by(role_name=user_data["role_name"]).first()
            if not role:
                logger.error(f"Роль '{user_data['role_name']}' не найдена!")
                raise ValueError(f"Роль '{user_data['role_name']}' для пользователя '{user_data['login']}' не найдена")

            hashed_password = generate_password_hash(user_data["password"])
            self.__get_or_create(
                session,
                UserModel,
                {"login": user_data["login"]},
                {"password_hash": hashed_password, "role_id": role.id},
            )


class DatabaseCore:
    """
    Основной класс для управления базой данных, включая создание, удаление таблиц и управление сессиями.
    """

    __slots__ = ("engine", "Session", "instance_initializer")

    def __init__(self, app: Optional[Flask] = None) -> None:
        """
        Инициализирует DatabaseCore.

        :param app: Flask-приложение (если используется).
        """
        self.engine = None
        self.Session = None
        self.instance_initializer: Optional[DatabaseInitializer] = None
        if app is not None:
            self.init_db(app)

    @property
    def metadata(self) -> MetaData:
        """
        Возвращает объект MetaData, содержащий описание всех таблиц и их схем.

        :return: Объект MetaData, связанный с моделью.
        """
        return AbstractModel.metadata  # type: ignore

    @contextmanager
    @handle_error_for_database
    def session_scope(self) -> Session:
        session = self.__get_session()
        logger.debug("Создана новая сессия базы данных")
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Ошибка транзакции: {e}")
            session.rollback()
            raise
        finally:
            logger.debug("Закрытие сессии базы данных")
            session.close()

    @handle_error_for_database
    def __init_database_initializer(self, config_path: str) -> None:
        """
        Инициализация компонента DatabaseInitializer.

        Этот метод создаёт экземпляр `DatabaseInitializer`, который используется
        для выполнения операций инициализации базы данных, таких как создание таблиц
        и наполнение начальными данными.

        :param config_path: Путь к YAML-файлу конфигурации базы данных.
        :raises Exception: Если возникла ошибка при инициализации.
        """
        self.instance_initializer = DatabaseInitializer(config_path=config_path)

    @handle_error_for_database
    def __init_engine(self, database_uri: str) -> None:
        """
        Инициализация движка базы данных.

        Этот метод создаёт объект движка SQLAlchemy, который управляет соединениями
        с базой данных. Движок настраивается с указанным URI базы данных.

        :param database_uri: URI подключения к базе данных (например, "sqlite+pysqlite:///:memory:").
        :raises Exception: Если возникла ошибка при создании движка.
        """
        self.engine = create_engine(database_uri, echo=False)

    @handle_error_for_database
    def __init_session(self) -> None:
        """
        Инициализация фабрики сессий SQLAlchemy.

        Этот метод создаёт объект `sessionmaker`, который используется для создания
        новых сессий базы данных. Сессии привязаны к движку, настроенному ранее.

        :raises Exception: Если возникла ошибка при создании фабрики сессий.
        """
        self.Session = sessionmaker(bind=self.engine)

    @handle_error_for_database
    def init_db(self, app: Flask) -> None:
        """
        Инициализация базы данных с Flask приложением.

        :param app: Flask-приложение.
        """

        database_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
        if not database_uri:
            raise ValueError(
                "Параметр конфигурации 'SQLALCHEMY_DATABASE_URI' не определён. Проверьте конфигурацию приложения."
            )

        config_path = app.config.get("SQLALCHEMY_CONFIG_PATH_INIT")
        if not config_path:
            raise ValueError(
                "Параметр конфигурации 'SQLALCHEMY_CONFIG_PATH_INIT' не определён. Проверьте конфигурацию приложения."
            )

        self.__init_database_initializer(config_path)
        self.__init_engine(database_uri)
        self.__init_session()

    @handle_error_for_database
    def create_tables(self) -> None:
        """
        Создает таблицы в базе данных и заполняет начальными данными.
        """
        logger.info("Создание таблиц в базе данных")
        if self.engine:
            self.metadata.create_all(self.engine)
            with self.session_scope() as session:
                if self.instance_initializer:
                    self.instance_initializer.initialize_db(session=session)
            logger.info("Таблицы успешно созданы")

    @handle_error_for_database
    def drop_tables(self) -> None:
        """
        Удаляет таблицы из базы данных.
        """
        logger.warning("Удаление всех таблиц из базы данных!")
        if self.engine:
            self.metadata.drop_all(self.engine)

    @handle_error_for_database
    def __get_session(self) -> Session:
        """
        Получает сессию для работы с базой данных.

        :return: SQLAlchemy-сессия.
        :raises RuntimeError: Если сессия не инициализирована.
        """
        if self.Session:
            return self.Session()
        logger.critical("Попытка работы с БД без инициализации!")
        raise RuntimeError("DatabaseCore is not initialized. Call 'init_app' first.")
