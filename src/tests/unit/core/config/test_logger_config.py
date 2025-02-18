from unittest.mock import mock_open, patch

import allure
import toml
import yaml

from src.app.core.config import LoggerConfig


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование LoggerConfig")
@allure.sub_suite("Загрузка конфигурации логирования")
class TestLoggerConfig:

    @allure.title("Тест успешной загрузки конфигурации из YAML")
    @allure.description(
        "Проверяет, что при корректном TOML и YAML файлах "
        "LoggerConfig.from_yaml() возвращает ожидаемую конфигурацию."
    )
    def test_logger_config_from_yaml(self, mock_env, valid_toml_config, valid_yaml_config):
        """
        Моки:
         - TOML-файл с секцией [flask-config-logger] и ключом CONFIG_PATH_LOGGER_DEV.
         - YAML-файл с корректными данными логирования.
        Ожидается, что метод вернёт экземпляр LoggerConfig с CONFIG_LOGGER, равным valid_yaml_config.
        """
        toml_str = toml.dumps(valid_toml_config)
        yaml_str = yaml.dump(valid_yaml_config)

        # Симулируем два последовательных вызова open():
        m_open = mock_open(read_data=toml_str)
        with patch("builtins.open", m_open) as mocked_open:
            # Первый вызов: TOML-файл, второй: YAML-файл
            mocked_open.side_effect = [
                m_open.return_value,
                mock_open(read_data=yaml_str).return_value,
            ]
            logger_config = LoggerConfig.from_yaml()

        assert isinstance(logger_config.CONFIG_LOGGER, dict)
        assert logger_config.CONFIG_LOGGER == valid_yaml_config

    @allure.title("Тест отсутствия пути к YAML в TOML")
    @allure.description(
        "Проверяет, что если в секции [flask-config-logger] "
        "отсутствует ключ для текущего режима, возвращается пустой конфиг."
    )
    def test_logger_config_missing_yaml_path(self, mock_env, valid_toml_config):
        # Удаляем ключ CONFIG_PATH_LOGGER_DEV из TOML-файла
        valid_toml_config["flask-config-logger"].pop("CONFIG_PATH_LOGGER_DEV", None)
        toml_str = toml.dumps(valid_toml_config)

        with patch("builtins.open", mock_open(read_data=toml_str)):
            logger_config = LoggerConfig.from_yaml()
            assert logger_config.CONFIG_LOGGER == {}

    @allure.title("Тест FileNotFoundError")
    @allure.description("Проверяет, что если не удаётся открыть файл (TOML или YAML), возвращается пустой конфиг.")
    def test_logger_config_file_not_found(self, mock_env):
        with patch("builtins.open", side_effect=FileNotFoundError):
            logger_config = LoggerConfig.from_yaml()
            assert logger_config.CONFIG_LOGGER == {}

    @allure.title("Тест некорректного YAML")
    @allure.description("Проверяет, что если YAML-файл содержит некорректные данные, метод возвращает пустой конфиг.")
    def test_logger_config_invalid_yaml(self, mock_env, valid_toml_config):
        toml_str = toml.dumps(valid_toml_config)
        invalid_yaml_str = "invalid_yaml: : data"
        with patch("builtins.open") as m_open:
            # Первый вызов возвращает корректный TOML
            # Второй вызов возвращает некорректный YAML
            m_open.side_effect = [
                mock_open(read_data=toml_str).return_value,
                mock_open(read_data=invalid_yaml_str).return_value,
            ]
            logger_config = LoggerConfig.from_yaml()
            assert logger_config.CONFIG_LOGGER == {}
