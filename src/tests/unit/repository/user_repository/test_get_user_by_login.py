import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование UserRepository")
@allure.sub_suite("Метод get_user_by_login")
@allure.title("Тест успешного получения пользователя по логину")
@allure.description("Проверяет, что метод возвращает данные пользователя, если он найден в базе")
def test_get_user_by_login_found(user_repository, db_helper_mock):
    """
    Тест метода get_user_by_login, если пользователь найден.
    """
    # Настройка мока для DBHelperSQL
    mock_result = [{"login": "root", "password_hash": "hashed_password", "role_name": "Root"}]
    db_helper_mock.execute_query.return_value = mock_result

    with allure.step("Вызов метода get_user_by_login с существующим логином"):
        result = user_repository.get_user_by_login(login="root")

    with allure.step("Проверяем возвращённые данные"):
        assert result == mock_result[0], "Возвращаемые данные не совпадают с ожидаемыми"

    with allure.step("Убедиться, что execute_query вызван с правильными аргументами"):
        db_helper_mock.execute_query.assert_called_once_with(query_name="get_user_by_login", params={"login": "root"})


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование UserRepository")
@allure.sub_suite("Метод get_user_by_login")
@allure.title("Тест получения None, если пользователь не найден")
@allure.description("Проверяет, что метод возвращает None, если пользователь отсутствует в базе")
def test_get_user_by_login_not_found(user_repository, db_helper_mock):
    """
    Тест метода get_user_by_login, если пользователь не найден.
    """
    # Настройка мока для DBHelperSQL
    db_helper_mock.execute_query.return_value = []

    with allure.step("Вызов метода get_user_by_login с несуществующим логином"):
        result = user_repository.get_user_by_login(login="non_existent_user")

    with allure.step("Проверяем, что результат равен None"):
        assert result is None, "Результат должен быть None, если пользователь не найден"

    with allure.step("Убедиться, что execute_query вызван с правильными аргументами"):
        db_helper_mock.execute_query.assert_called_once_with(
            query_name="get_user_by_login", params={"login": "non_existent_user"}
        )
