from unittest.mock import Mock, patch

import allure

from src.app.controllers.main_controller import MainController


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование MainController")
@allure.sub_suite("Аутентификация")
@allure.title("Тест успешной аутентификации")
@allure.description("Проверяет, что пользователь с правильными данными может успешно войти")
@patch("src.app.controllers.main_controller.check_password_hash")
def test_auth_user_success(
    mock_check_password_hash,
    main_controller: MainController,
    mock_user_repository: Mock,
    mock_session_manager: Mock,
) -> None:
    """
    Тест успешной аутентификации пользователя.
    """

    # Настраиваем mock_user_repository
    with allure.step("Настройка mock_user_repository с данными пользователя"):
        mock_user_repository.get_user_by_login.return_value = {
            "user_id": 1,
            "password_hash": "hashed_password",
            "role_name": "admin",
        }

    # Настраиваем мок для check_password_hash
    with allure.step("Настройка mock для check_password_hash"):
        mock_check_password_hash.return_value = True

    data = {
        "login": "test_user",
        "password": "correct_password",
        "ip_addr": "127.0.0.1",
    }
    # Вызываем метод
    with allure.step("Вызов метода auth_user"):
        result = main_controller.auth_user(data)

    # Проверяем результат
    with allure.step("Проверка результата"):
        assert result is True, "Аутентификация должна быть успешной при правильных данных"

    # Проверяем, что методы моков вызваны с правильными аргументами
    with allure.step("Проверка вызовов mock_user_repository и mock_session_manager"):
        mock_user_repository.get_user_by_login.assert_called_once_with(login="test_user")
        mock_session_manager.set.assert_any_call(key="user_id", value="1")
        mock_session_manager.set.assert_any_call(key="role_name", value="admin")
        mock_session_manager.set.assert_any_call(key="ip_addr", value="127.0.0.1")

    # Проверяем вызов check_password_hash
    with allure.step("Проверка вызова check_password_hash"):
        mock_check_password_hash.assert_called_once_with("hashed_password", "correct_password")


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование MainController")
@allure.sub_suite("Аутентификация")
@allure.title("Тест неуспешной аутентификации")
@allure.description("Проверяет, что пользователь с неправильными данными не может войти")
def test_auth_user_is_wrong(
    main_controller: MainController,
    mock_user_repository: Mock,
    mock_session_manager: Mock,
) -> None:
    """Тест аутентификации с неверным логином или паролем."""
    with allure.step("Настройка mock_user_repository для отсутствующего пользователя"):
        mock_user_repository.get_user_by_login.return_value = None
    data = {
        "login": "wrong_test_user",
        "password": "wrong_password",
        "ip_addr": "127.0.0.1",
    }

    with allure.step("Вызов метода auth_user с некорректными данными"):
        result = main_controller.auth_user(data)

    with allure.step("Проверка результата"):
        assert result is False

    with allure.step("Проверка, что сессия не была установлена"):
        mock_session_manager.set.assert_not_called()
