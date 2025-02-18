from unittest.mock import mock_open, patch

import allure
import pytest
import toml

from src.app.core.config import FlaskConfig


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование FlaskConfig")
@allure.sub_suite("Загрузка конфигурации из TOML")
class TestFlaskConfig:

    @allure.title("Тест успешной загрузки конфигурации из TOML")
    @allure.description("Проверяет, что TOML конфигурация загружается корректно.")
    def test_flask_config_from_toml(self, mock_toml_config, mock_env):
        """Тест загрузки конфигурации из TOML с использованием мока."""
        with patch("builtins.open", mock_open(read_data=toml.dumps(mock_toml_config))):
            flask_config = FlaskConfig.from_toml()
            assert flask_config.DEBUG is True
            assert flask_config.APPLICATION_ROOT == "/"

    @allure.title("Тест обработки ошибки TOML")
    @allure.description("Проверяет, что некорректный TOML вызывает ValueError.")
    def test_flask_config_invalid_toml(self, mock_env):
        with patch("builtins.open", mock_open(read_data="invalid_toml_data")):
            with pytest.raises(ValueError):
                FlaskConfig.from_toml()

    @allure.title("Тест загрузки реального файла TOML")
    @allure.description("Проверяет, что конфигурация загружается из реального файла.")
    def test_flask_config_real_file(self):
        flask_config = FlaskConfig.from_toml()
        assert flask_config.APPLICATION_ROOT == "/"
