import logging

from dependency_injector import containers, providers

# Импорт основного контроллера
from src.app.controllers.main_controller import MainController

# Инициализация логирования для контейнера контроллеров
logger = logging.getLogger(__name__)


# Контейнер для управления зависимостями контроллеров
class ControllerContainer(containers.DeclarativeContainer):
    """
    Контейнер для контроллеров (Controllers).

    Управляет созданием и конфигурацией экземпляров контроллеров приложения.
    Используется для управления зависимостями и обеспечивания их инъекции в контроллеры.
    """

    # Контейнер зависимостей, используемых контроллерами (репозитории, менеджеры и другие компоненты)
    repo = providers.DependenciesContainer()

    # Основной контроллер приложения (MainController)
    main_controller: providers.Singleton[MainController] = providers.Singleton(
        MainController,
        user_repository=repo.user_repository,  # Репозиторий пользователей
        session_manager=repo.session_repository,  # Репозиторий для управления сессиями
    )
