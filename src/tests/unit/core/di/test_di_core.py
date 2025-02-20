import logging.config
from unittest.mock import patch

import allure
import pytest
from dependency_injector import providers


@pytest.mark.unit
@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование CoreContainer")
@allure.sub_suite("Инициализация конфигурации приложения")
class TestCoreContainer:

    @pytest.mark.unit
    @allure.title("Тест конфигурации контейнера")
    @allure.description("Проверяет, что контейнер возвращает переопределённую конфигурацию.")
    def test_core_container_config(self, core_container, dummy_config_fixture):
        """
        Проверяет, что контейнер возвращает тестовую конфигурацию.
        """
        config = core_container.config()
        assert config.flask_config == dummy_config_fixture.flask_config
        assert config.logging_config_app == dummy_config_fixture.logging_config_app

    @pytest.mark.unit
    @allure.title("Тест конфигурации логирования")
    @allure.description(
        "Мокаем logging.config.dictConfig, чтобы проверить, что он вызывается с ожидаемыми параметрами "
        "при инициализации ресурса логирования."
    )
    def test_core_container_logging_config(self, core_container, dummy_config_fixture):
        with patch("logging.config.dictConfig") as mock_dict_config:
            # Переопределяем ресурс logging_config, чтобы он явно вызывал dictConfig.
            core_container.logging_config.override(
                providers.Callable(
                    lambda: logging.config.dictConfig(dummy_config_fixture.logging_config_app.get("CONFIG_LOGGER"))
                )
            )
            # Инициализируем ресурсы.
            core_container.init_resources()
            # Проверяем, что dictConfig был вызван один раз с ожидаемой конфигурацией.
            mock_dict_config.assert_called_once_with(dummy_config_fixture.logging_config_app.get("CONFIG_LOGGER"))

    @pytest.mark.unit
    @allure.title("Тест провайдера настроек Flask")
    @allure.description(
        "Переопределяет провайдер settings_flask, чтобы вернуть тестовую конфигурацию Flask, и проверяет это."
    )
    def test_core_container_settings_flask(self, core_container, dummy_config_fixture):
        # Переопределяем провайдер settings_flask, чтобы он возвращал dummy_config_fixture.flask_config.
        core_container.settings_flask.override(providers.Object(dummy_config_fixture.flask_config))
        settings = core_container.settings_flask()
        assert settings == dummy_config_fixture.flask_config
