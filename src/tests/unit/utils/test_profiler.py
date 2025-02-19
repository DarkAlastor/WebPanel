import logging
from unittest.mock import patch

import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование профилирования SQL-запросов")
@allure.sub_suite("Логирование SQL-запросов")
class TestSqlQueryLogging:
    @allure.title("Тест логирования быстрого SQL-запроса")
    @allure.description("Проверяет, что быстрый SQL-запрос (<1 сек) логируется на уровне INFO")
    def test_fast_query_logging(self, mock_logger, fast_query):
        with allure.step("Мокаем время выполнения запроса (0.5 сек)"):
            with patch("time.time", side_effect=[0, 0.5]):
                result = fast_query("fast_query_name")

        with allure.step("Проверяем, что результат выполнения запроса корректен"):
            assert result == "fast_result"

        with allure.step("Проверяем, что логгер вызван с уровнем INFO"):
            mock_logger.log.assert_called_once_with(logging.INFO, "SQL Query `fast_query_name` executed in 0.5000 sec")

    @allure.title("Тест логирования медленного SQL-запроса")
    @allure.description("Проверяет, что медленный SQL-запрос (>1 сек) логируется на уровне WARNING")
    def test_slow_query_logging(self, mock_logger, slow_query):
        with allure.step("Мокаем время выполнения запроса (1.5 сек)"):
            with patch("time.time", side_effect=[0, 1.5]):
                result = slow_query("slow_query_name")

        with allure.step("Проверяем, что результат выполнения запроса корректен"):
            assert result == "slow_result"

        with allure.step("Проверяем, что логгер вызван с уровнем WARNING"):
            mock_logger.log.assert_called_once_with(
                logging.WARNING, "SQL Query `slow_query_name` executed in 1.5000 sec"
            )

    @allure.title("Тест логирования SQL-запроса с аргументами")
    @allure.description("Проверяет, что SQL-запрос, переданный через args, логируется корректно")
    def test_query_with_args(self, mock_logger, query_with_args):
        with allure.step("Мокаем время выполнения запроса (0.3 сек)"):
            with patch("time.time", side_effect=[0, 0.3]):
                result = query_with_args("query_with_args_name", "SELECT * FROM users")

        with allure.step("Проверяем, что результат выполнения запроса корректен"):
            assert result == "executed SELECT * FROM users"

        with allure.step("Проверяем, что логгер вызван с уровнем INFO"):
            mock_logger.log.assert_called_once_with(
                logging.INFO, "SQL Query `query_with_args_name` executed in 0.3000 sec"
            )
