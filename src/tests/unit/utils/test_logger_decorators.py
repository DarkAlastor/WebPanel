import logging

import allure
import pytest
from flask import Flask


@pytest.mark.unit
@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора log_routes")
@allure.sub_suite("Логирование и сохранение метаданных")
class TestLogRoutes:

    @allure.title("Логирование маршрутов")
    @allure.description("Проверка, что декоратор логирует все маршруты приложения.")
    def test_log_routes_logging(self, caplog, decorated_app, sample_app):
        # Устанавливаем уровень логирования для логгера "web_panel"
        with caplog.at_level(logging.INFO, logger="web_panel"):
            app = decorated_app()

        # Получаем список всех записей лога
        logged_messages = [record.message for record in caplog.records]

        # Для каждого маршрута проверяем, что соответствующее сообщение присутствует в логе
        for rule in app.url_map.iter_rules():
            expected_log = f"Route: {rule}, Endpoint: {rule.endpoint}"
            assert expected_log in logged_messages, f"Не найден лог для маршрута: {expected_log}"

    @allure.title("Сохранение метаданных функции")
    @allure.description("Проверка, что декоратор сохраняет имя и документацию исходной функции.")
    def test_decorator_preserves_metadata(self, decorated_app):
        # Проверяем, что имя функции сохранено
        assert decorated_app.__name__ == "create_app", "Имя функции не сохранено"
        # Проверяем, что документация функции не отсутствует
        assert decorated_app.__doc__ is not None, "Документация функции не сохранена"

    @allure.title("Проверка типа возвращаемого объекта")
    @allure.description("Проверка, что задекорированная функция возвращает экземпляр Flask.")
    def test_decorated_app_returns_flask_instance(self, decorated_app):
        app = decorated_app()
        assert isinstance(app, Flask), "Возвращаемый объект не является экземпляром Flask"
