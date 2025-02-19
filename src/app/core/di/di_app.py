from dependency_injector import containers, providers

from src.app.core.di.di_core import CoreContainer
from src.app.core.di.di_database import DbContainer


class AppContainer(containers.DynamicContainer):
    """
    Контейнер зависимостей для всего приложения.

    Этот контейнер используется для настройки и инициализации всех зависимостей на уровне приложения.
    В нем объединяются все другие контейнеры (для контроллеров, репозиториев и представлений)
    и управляется их инициализация.

    Основные атрибуты:
    - core: Контейнер зависимостей для основной логики приложения (CoreContainer).
    - db: Контейнер для базы данных, используемых в приложении.
    """

    # Провайдер для инициализации контейнера CoreContainer (основной контейнер зависимостей)
    core = providers.Container(CoreContainer)

    # Провайдер для иницализции контенера DbContainer (базы данных)
    db = providers.Container(DbContainer)

    def init_resources(self) -> None:
        """
        Инициализирует все ресурсы внутри контейнера.

        Этот метод вызывает метод `init_resources` внутри контейнеров `CoreContainer` и `ViewContainer`,
        выполняя все необходимые действия для инициализации ресурсов, таких как подключение к базам данных,
        настройка представлений и другие важные процессы.
        """
        # Инициализация ресурсов основного контейнера
        self.core.init_resources()
