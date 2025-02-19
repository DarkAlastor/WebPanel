import logging

import allure
import pytest
from sqlalchemy.exc import SQLAlchemyError

# Фикстуры dummy_success, dummy_sqlalchemy_error и dummy_generic_error будут автоматически найдены


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_error_for_database")
@allure.sub_suite("Обработка ошибок базы данных")
@allure.title("Проверка работы декоратора handle_error_for_database")
class TestHandleErrorForDatabase:
    @allure.title("Успешное выполнение функции")
    @allure.description(
        "Проверяет, что функция, обёрнутая handle_error_for_database, "
        "возвращает корректное значение при отсутствии ошибок"
    )
    def test_success(self, dummy_success):
        result = dummy_success()
        assert result == "success"

    @allure.title("Обработка SQLAlchemyError")
    @allure.description(
        "Проверяет, что функция, обёрнутая handle_error_for_database, " "логирует ошибку и выбрасывает SQLAlchemyError"
    )
    def test_sqlalchemy_error(self, dummy_sqlalchemy_error, caplog):
        with caplog.at_level(logging.ERROR, logger="app_db_logger"):
            with pytest.raises(SQLAlchemyError) as exc_info:
                dummy_sqlalchemy_error()
            assert "Ошибка базы данных" in caplog.text
            assert "sqlalchemy error" in str(exc_info.value)

    @allure.title("Обработка непредвиденной ошибки")
    @allure.description(
        "Проверяет, что функция, обёрнутая handle_error_for_database, "
        "логирует ошибку и выбрасывает непредвиденное исключение"
    )
    def test_generic_error(self, dummy_generic_error, caplog):
        with caplog.at_level(logging.ERROR, logger="app_db_logger"):
            with pytest.raises(ValueError) as exc_info:
                dummy_generic_error()
            assert "Непредвиденная ошибка" in caplog.text
            assert "generic error" in str(exc_info.value)
