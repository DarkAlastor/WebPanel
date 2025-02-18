import logging.config
from unittest.mock import patch

import allure
import pytest
from dependency_injector import providers


@pytest.mark.unit
@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование CoreContainer")
@allure.sub_suite("Инициализация конфигурации приложения")
@allure.title("Test container configuration")
@allure.description("Checks that the container returns the overridden configuration.")
class TestCoreContainer:

    @pytest.mark.unit
    def test_core_container_config(self, core_container, dummy_config_fixture):
        """
        Verifies that the container returns the dummy configuration.
        """
        config = core_container.config()
        assert config.flask_config == dummy_config_fixture.flask_config
        assert config.logging_config_app == dummy_config_fixture.logging_config_app

    @pytest.mark.unit
    @allure.title("Test logging configuration resource")
    @allure.description(
        "Mocks logging.config.dictConfig to verify it is called with the expected parameters "
        "when the logging resource is initialized."
    )
    def test_core_container_logging_config(self, core_container, dummy_config_fixture):
        with patch("logging.config.dictConfig") as mock_dict_config:
            # Override the logging_config resource so that it explicitly calls dictConfig.
            core_container.logging_config.override(
                providers.Callable(
                    lambda: logging.config.dictConfig(dummy_config_fixture.logging_config_app.get("CONFIG_LOGGER"))
                )
            )
            # Initialize resources.
            core_container.init_resources()
            # Verify that dictConfig was called once with the expected configuration.
            mock_dict_config.assert_called_once_with(dummy_config_fixture.logging_config_app.get("CONFIG_LOGGER"))

    @pytest.mark.unit
    @allure.title("Test Flask settings provider")
    @allure.description("Overrides the settings_flask provider to return the dummy flask configuration and checks it.")
    def test_core_container_settings_flask(self, core_container, dummy_config_fixture):
        # Override the settings_flask provider to exactly return dummy_config.flask_config.
        core_container.settings_flask.override(providers.Object(dummy_config_fixture.flask_config))
        settings = core_container.settings_flask()
        assert settings == dummy_config_fixture.flask_config
