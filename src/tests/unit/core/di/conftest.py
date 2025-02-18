import pytest

from src.app.core.config import AppConfig
from src.app.core.di.di_core import CoreContainer

# Dummy конфигурация для тестов
dummy_config = AppConfig()
dummy_config.flask_config = {"key": "dummy_flask_value"}
dummy_config.logging_config_app = {"CONFIG_LOGGER": {"level": "INFO", "handlers": ["console"]}}


@pytest.fixture
def dummy_config_fixture():
    """Фикстура, возвращающая dummy конфигурацию."""
    return dummy_config


@pytest.fixture
def core_container(dummy_config_fixture):
    """
    Создает экземпляр CoreContainer и переопределяет провайдер config dummy-конфигурацией.
    """
    # from src.app.core.di.di_core import CoreContainer
    container = CoreContainer()
    container.config.override(dummy_config_fixture)
    return container
