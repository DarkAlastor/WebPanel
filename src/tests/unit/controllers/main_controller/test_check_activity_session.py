from unittest.mock import Mock

import allure

from src.app.controllers.main_controller import MainController


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование MainController")
@allure.sub_suite("Проверка активности сессии")
@allure.title("Тест проверки активной сессии")
@allure.description("Проверяет, что сессия пользователя активная")
def test_check_activity_session_success(
    main_controller: MainController,
    mock_session_manager: Mock,
) -> None:

    with allure.step("Настройка mock_session_manager на возвращение user_id и ip_addr"):
        mock_session_manager.get.side_effect = lambda key: {
            "user_id": "123",
            "ip_addr": "127.0.0.1",
            "role_name": "admin",
        }.get(key, None)

    with allure.step("Вызываем метод check_activity_session"):
        result = main_controller.check_activity_session(ip_addr="127.0.0.1")

    with allure.step("Проверка результата"):
        assert result is True

    with allure.step("Проверяем, что метод get вызывался три раза с нужными ключами"):
        mock_session_manager.get.assert_any_call("user_id")
        mock_session_manager.get.assert_any_call("ip_addr")
        mock_session_manager.get.assert_any_call("role_name")


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование MainController")
@allure.sub_suite("Проверка активности сессии")
@allure.title("Тест проверки неактивной сессии")
@allure.description("Проверяет, что сессия пользователя неактивная")
def test_check_activity_session_inactive(main_controller: MainController, mock_session_manager: Mock) -> None:

    with allure.step("Настраиваем mock_session_manager на возвращение None для user_id"):
        mock_session_manager.get.side_effect = lambda key: {
            "user_id": None,
            "ip_addr": "127.0.0.1",
            "role_name": "Unknown",
        }.get(key, None)

    with allure.step("Вызываем метод check_activity_session"):
        result = main_controller.check_activity_session(ip_addr="127.0.0.1")

    with allure.step("Проверка результата"):
        assert result is False

    with allure.step("Проверяем, что метод get вызывался три раза с нужными ключами"):
        mock_session_manager.get.assert_any_call("user_id")
        mock_session_manager.get.assert_any_call("ip_addr")
        mock_session_manager.get.assert_any_call("role_name")
