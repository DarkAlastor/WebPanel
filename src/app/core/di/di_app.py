from dependency_injector import containers, providers

# Импорт основных контейнеров для различных слоев приложения
from src.app.core.di.di_controller import ControllerContainer
from src.app.core.di.di_core import CoreContainer
from src.app.core.di.di_database import DbContainer
from src.app.core.di.di_repository import RepositoryContainer
from src.app.core.di.di_view import ViewContainer


class AppContainer(containers.DynamicContainer):
    """
    Контейнер зависимостей для всего приложения.

    Этот контейнер используется для настройки и инициализации всех зависимостей на уровне приложения.
    В нем объединяются все другие контейнеры (для контроллеров, репозиториев и представлений)
    и управляется их инициализация.

    Основные атрибуты:
    - core: Контейнер зависимостей для основной логики приложения (CoreContainer).
    - repo: Контейнер для репозиториев, используемых в приложении.
    - controller: Контейнер для контроллеров.
    - view: Контейнер для представлений (views).
    """

    # Провайдер для инициализации контейнера CoreContainer (основной контейнер зависимостей)
    core = providers.Container(CoreContainer)
    # Провайдер для иницализции контенера DbContainer (базы данных)
    db = providers.Container(DbContainer)
    # Провайдер для инициализации контейнера RepositoryContainer (репозитории)
    repo = providers.Container(RepositoryContainer, db=db)
    # Провайдер для инициализации контейнера ControllerContainer (контроллеры)
    controller = providers.Container(ControllerContainer, repo=repo)
    # Провайдер для инициализации контейнера ViewContainer (представления)
    view = providers.Container(ViewContainer, controller=controller)

    def init_resources(self) -> None:
        """
        Инициализирует все ресурсы внутри контейнера.

        Этот метод вызывает метод `init_resources` внутри контейнеров `CoreContainer` и `ViewContainer`,
        выполняя все необходимые действия для инициализации ресурсов, таких как подключение к базам данных,
        настройка представлений и другие важные процессы.
        """
        # Инициализация ресурсов основного контейнера
        self.core.init_resources()
        # Инициализация ресурсов представлений (views)
        self.view.init_resources()
