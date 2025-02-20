from typing import cast
from unittest.mock import Mock

from pytest import fixture

from src.app.db.db_helper import DBHelperSQL
from src.app.repository.interface.isession_repo import ISessionManager
from src.app.repository.repo_session import RepositoryFlaskSessionManager
from src.app.repository.repo_user import UserRepository


# ======== Фикстуры для session_repository ========
@fixture
def repo_session_manager(mock_session_manager: ISessionManager) -> RepositoryFlaskSessionManager:
    """
    Создает экземпляр RepositoryFlaskSessionManager с использованием mock_session_manager.
    Предполагается, что RepositoryFlaskSessionManager принимает менеджер сессии через конструктор.
    """
    return RepositoryFlaskSessionManager()


# ======== Фикстуры для user_repository ========


@fixture
def mock_session_manager() -> ISessionManager:
    """Создает мок для ISessionManager."""
    return cast(ISessionManager, Mock(spec=ISessionManager))


@fixture
def db_helper_mock() -> Mock:
    """
    Создаёт мок для DBHelperSQL.

    :return: Мок-объект DBHelperSQL.
    """
    return Mock(spec=DBHelperSQL)


@fixture
def fake_session(monkeypatch):
    """
    Фикстура подменяет глобальную переменную `session` в модуле
    RepositoryFlaskSessionManager на обычный словарь для тестирования.
    """
    fake_session = {}
    # Подменяем объект session, импортированный из flask, в модуле repo_flask_session_manager
    monkeypatch.setattr("src.app.repository.repo_session.session", fake_session)
    return fake_session


@fixture
def repo_user_repository(db_helper_mock: Mock) -> UserRepository:
    """
    Создаёт экземпляр UserRepository с моком DBHelperSQL.

    :param db_helper_mock: Мок для DBHelperSQL.
    :return: Экземпляр UserRepository.
    """
    return UserRepository(db_helper=db_helper_mock)
