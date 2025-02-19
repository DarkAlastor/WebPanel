from typing import cast
from unittest.mock import Mock

from pytest import fixture

from src.app.controllers.main_controller import MainController
from src.app.db.db_helper import DBHelperSQL
from src.app.repository.interface.isession_repo import ISessionManager
from src.app.repository.interface.iuser_repo import IUserRepository
from src.app.repository.repo_user import UserRepository


# ===== Фикстуры для контроллеров =====
@fixture
def mock_user_repository() -> IUserRepository:
    """Создает мок для IUserRepository."""
    return cast(IUserRepository, Mock(spec=IUserRepository))


@fixture
def mock_session_manager() -> ISessionManager:
    """Создает мок для ISessionManager."""
    return cast(ISessionManager, Mock(spec=ISessionManager))


# ===== Фикстуры для репозиториев =====
@fixture
def db_helper_mock() -> Mock:
    """
    Создаёт мок для DBHelperSQL.

    :return: Мок-объект DBHelperSQL.
    """
    return Mock(spec=DBHelperSQL)


@fixture
def user_repository(db_helper_mock: Mock) -> UserRepository:
    """
    Создаёт экземпляр UserRepository с моком DBHelperSQL.

    :param db_helper_mock: Мок для DBHelperSQL.
    :return: Экземпляр UserRepository.
    """
    return UserRepository(db_helper=db_helper_mock)


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
def main_controller(mock_user_repository: IUserRepository, mock_session_manager: ISessionManager) -> MainController:
    """Создает экземпляр MainController с моками."""
    return MainController(user_repository=mock_user_repository, session_manager=mock_session_manager)
