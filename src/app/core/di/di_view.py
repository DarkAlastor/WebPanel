import logging

from dependency_injector import containers, providers
from flask_smorest import Blueprint  # type: ignore

# Импорт основного маршрута для представлений
from src.app.views.v1.main.routes import MainBlueprint

# Инициализация логирования для контейнера представлений
logger = logging.getLogger(__name__)


# Контейнер для управления зависимостями представлений
class ViewContainer(containers.DynamicContainer):
    """
    Контейнер для представлений (Views).

    Управляет зависимостями для представлений Flask, включая регистрацию маршрутов, создание Blueprint
    и их связывание с контроллерами. Используется для обеспечения модульности и гибкости кода.
    """

    # Контейнер для зависимостей контроллеров, используемых представлениями
    controller = providers.DependenciesContainer()

    # Blueprint для версий API (хардкод рекомендуется заменить на параметризацию)
    v1_bp: providers.Singleton[Blueprint] = providers.Singleton(
        lambda: Blueprint("v1", __name__, url_prefix="/")  # Роутеры 1-ой версии
    )

    # Представление основной функциональности (MainBlueprint)
    main_view: providers.Singleton[MainBlueprint] = providers.Singleton(
        MainBlueprint, controller=controller.main_controller
    )

    def init_resources(self) -> None:
        """
        Инициализирует ресурсы контейнера, регистрируя маршруты и Blueprints.

        Вызывается для настройки всех представлений, их маршрутов и зависимостей.
        """
        logger.info("Инициализация ресурсов контейнера ViewContainer")

        # Регистрируем маршруты основного представления в v1 Blueprint
        self.v1_bp().register_blueprint(self.main_view())
