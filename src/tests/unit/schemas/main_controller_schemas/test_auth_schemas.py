import allure
import pytest
from pydantic import ValidationError

from src.app.schemas.main_controller_schemas import AuthUserSchemas


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование main_controller_schemas")
@allure.sub_suite("Схема AuthUserSchemas")
class TestAuthUserSchemas:

    @allure.title("Тест успешного создания объекта схемы с корректными данными")
    @allure.description("Проверяет успешное создание объекта с валидными данными.")
    def test_valid_auth_user(self, valid_user_data):
        """Тест успешного создания объекта схемы с корректными данными"""
        user = AuthUserSchemas(**valid_user_data)
        assert user.login == valid_user_data["login"]
        assert user.password == valid_user_data["password"]
        assert user.ip_addr == valid_user_data["ip_addr"]

    @allure.title("Тест валидации логина с запрещёнными символами")
    @allure.description("Проверяет, что логин с недопустимыми символами вызывает ошибку.")
    def test_invalid_login(self, invalid_login):
        """Тест валидации логина с запрещёнными символами"""
        with pytest.raises(ValidationError) as e:
            AuthUserSchemas(login=invalid_login, password="ValidPass", ip_addr="8.8.8.8")
        assert any(
            msg in str(e.value)
            for msg in [
                "Login contains invalid characters",
                "Login cannot start with '.' or '-'",
            ]
        )

    @allure.title("Тест валидации логина, если он слишком короткий")
    @allure.description("Проверяет, что логин менее 4 символов вызывает ошибку.")
    def test_short_login(self, short_login):
        """Тест валидации логина, если он слишком короткий"""
        with pytest.raises(ValidationError) as e:
            AuthUserSchemas(login=short_login, password="ValidPass", ip_addr="8.8.8.8")
        assert "String should have at least 4 characters" in str(e.value)

    @allure.title("Тест валидации пароля, если он содержит пробелы")
    @allure.description("Проверяет, что пароль с пробелами вызывает ошибку.")
    def test_invalid_password(self, invalid_password):
        """Тест валидации пароля, если он содержит пробелы"""
        with pytest.raises(ValidationError) as e:
            AuthUserSchemas(login="validUser", password=invalid_password, ip_addr="8.8.8.8")
        assert "Password cannot contain spaces" in str(e.value)
