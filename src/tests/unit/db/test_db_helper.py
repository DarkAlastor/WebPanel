import allure


@allure.parent_suite("Database Tests")
@allure.suite("Тестирование DBHelperSQL")
@allure.sub_suite("Тестирование SELECT-запросов")
class TestDBHelperSQLSelectQueries:
    @allure.title("Тест получения всех пользователей через DBHelperSQL")
    def test_execute_query_get_all_users(self, db_helper):
        with allure.step("Выполняем SELECT-запрос для получения всех пользователей"):
            result = db_helper.execute_query("get_all_users")

        with allure.step("Проверяем количество пользователей"):
            assert len(result) == 2, f"Ожидалось 2 пользователя, получено: {len(result)}"

        with allure.step("Проверяем данные первого пользователя"):
            root_user = next((user for user in result if user["login"] == "root"), None)
            assert root_user is not None, "Пользователь root не найден"
            assert root_user["login"] == "root", "Логин первого пользователя должен быть 'root'"

        with allure.step("Проверяем данные второго пользователя"):
            admin_user = next((user for user in result if user["login"] == "admin"), None)
            assert admin_user is not None, "Пользователь admin не найден"
            assert admin_user["login"] == "admin", "Логин второго пользователя должен быть 'admin'"
