from dependency_injector import containers, providers

from src.app.repository.interface.isession_repo import ISessionManager
# Импорт интерфейсов для репозиториев
from src.app.repository.interface.iuser_repo import IUserRepository
from src.app.repository.repo_session import RepositoryFlaskSessionManager
# Импорт реализаций репозиториев
from src.app.repository.repo_user import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    """
    Контейнер зависимостей для репозиториев.

    Этот контейнер управляет зависимостями для репозиториев, которые предоставляют доступ к данным
    в приложении. Он использует интерфейсы для абстракции логики доступа к данным и провайдеры для
    их реализации. Репозитории зависят от компонента работы с базой данных, предоставляемого внешним
    контейнером.

    Основные атрибуты:
    - db: Зависимость от контейнера базы данных (DbContainer).
    - session_repository: Singleton-провайдер для репозитория сессий. Реализация `ISessionManager`.
    - user_repository: Singleton-провайдер для репозитория пользователей. Реализация `IUserRepository`.
    """

    # Зависим от контенера базы данных
    db = providers.DependenciesContainer()

    # Репозиторий для работы с сессией, предоставляющий реализацию ISessionManager
    session_repository: providers.Singleton[ISessionManager] = providers.Singleton(RepositoryFlaskSessionManager)

    # Репозиторий для работы с пользователями, предоставляющий реализацию IUserRepository
    user_repository: providers.Singleton[IUserRepository] = providers.Singleton(UserRepository, db_helper=db.db_helper)
