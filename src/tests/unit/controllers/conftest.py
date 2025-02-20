from typing import cast
from unittest.mock import Mock

from pytest import fixture

from src.app.controllers.main_controller import MainController
from src.app.repository.interface.isession_repo import ISessionManager
from src.app.repository.interface.iuser_repo import IUserRepository


# ======== Фикстуры для main_controller ========
@fixture
def mock_user_repository() -> IUserRepository:
    """Создает мок для IUserRepository."""
    return cast(IUserRepository, Mock(spec=IUserRepository))


@fixture
def mock_session_manager() -> ISessionManager:
    """Создает мок для ISessionManager."""
    return cast(ISessionManager, Mock(spec=ISessionManager))


@fixture
def main_controller(mock_user_repository: IUserRepository, mock_session_manager: ISessionManager) -> MainController:
    """Создает экземпляр MainController с моками."""
    return MainController(user_repository=mock_user_repository, session_manager=mock_session_manager)
