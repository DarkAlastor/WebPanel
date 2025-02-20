from unittest.mock import patch

import allure

from src.app.core.config import AppConfig, FlaskConfig, LoggerConfig


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование AppConfig")
@allure.sub_suite("Инициализация конфигурации приложения")
class TestAppConfig:

    @allure.title("Тест успешной инициализации AppConfig")
    @allure.description(
        "Проверяет, что AppConfig корректно собирает конфигурацию из FlaskConfig и LoggerConfig, "
        "используя методы from_toml() и from_yaml()."
    )
    def test_app_config_initialization(self, dummy_flask_config, dummy_logger_config):
        """
        Мокаем методы FlaskConfig.from_toml() и LoggerConfig.from_yaml(),
        чтобы они возвращали объекты с методом model_dump(), возвращающим dummy данные.
        Затем проверяем, что AppConfig инициализируется корректно.
        """
        # Создаем dummy объекты, где model_dump возвращает нужные словари.
        DummyFlask = type("DummyFlask", (), {"model_dump": lambda self: dummy_flask_config})
        DummyLogger = type("DummyLogger", (), {"model_dump": lambda self: dummy_logger_config})

        with patch.object(FlaskConfig, "from_toml", return_value=DummyFlask()):
            with patch.object(LoggerConfig, "from_yaml", return_value=DummyLogger()):
                app_config = AppConfig()
                assert app_config.flask_config == dummy_flask_config
                assert app_config.logging_config_app == dummy_logger_config
