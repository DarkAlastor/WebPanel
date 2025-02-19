import allure


@allure.parent_suite("Database Tests")
@allure.suite("Тестирование queries with DBHelperSQL")
class TestDBHelperSQLQueries:
    @allure.sub_suite("Проверка user_queries")
    @allure.title("Тест запроса get_user_by_login через DBHelperSQL")
    def test_get_user_by_login_with_db_helper(self, db_helper_with_real_queries):
        with allure.step("Выполняем запрос get_user_by_login"):
            result = db_helper_with_real_queries.execute_query("get_user_by_login", {"login": "root"})

        with allure.step("Проверяем результат"):
            assert len(result) == 1, "Ожидался один пользователь"
            user = result[0]
            assert user["login"] == "root", "Логин пользователя не совпадает"
            assert user["role_name"] == "Root", "Роль пользователя не совпадает (должен быть Root)"

    @allure.sub_suite("Проверка user_queries")
    @allure.title("Тест запроса get_user_with_role_and_permissions через DBHelperSQL")
    def test_get_user_with_role_and_permissions_with_db_helper(self, db_helper_with_real_queries):
        with allure.step("Выполняем запрос get_user_with_role_and_permissions"):
            result = db_helper_with_real_queries.execute_query(
                "get_user_with_role_and_permissions", {"role_name": "Root"}
            )

        with allure.step("Проверяем результат"):
            assert len(result) > 0, "Ожидался хотя бы один пользователь с ролью Root"
            user = result[0]
            assert user["user_id"] == 1, "ID пользователя не совпадает"
            assert user["login"] == "root", "Логин пользователя не совпадает"
            assert user["role_name"] == "Root", "Имя роли не совпадает"
            assert sorted(user["permissions_names"].split(", ")) == [
                "delete",
                "read",
                "write",
            ], "Названия разрешений не совпадают"

    @allure.sub_suite("Проверка role_queries")
    @allure.title("Тест запроса get_all_roles_and_permissions через DBHelperSQL")
    def test_get_all_roles_and_permissions_with_db_helper(self, db_helper_with_real_queries):
        with allure.step("Выполняем запрос get_all_roles_and_permissions"):
            result = db_helper_with_real_queries.execute_query("get_all_roles_and_permissions")

        with allure.step("Проверяем количество ролей"):
            assert len(result) == 2, f"Ожидалось 2 роли, получено: {len(result)}"

        with allure.step("Проверяем данные для роли Root"):
            root_role = next((r for r in result if r["role_name"] == "Root"), None)
            assert root_role is not None, "Роль Root не найдена"
            root_permissions = sorted(root_role["permission_names"].split(", "))
            assert root_permissions == [
                "delete",
                "read",
                "write",
            ], f"Разрешения для роли Root не совпадают: {root_permissions}"

        with allure.step("Проверяем данные для роли Admin"):
            admin_role = next((r for r in result if r["role_name"] == "Admin"), None)
            assert admin_role is not None, "Роль Admin не найдена"
            admin_permissions = sorted(admin_role["permission_names"].split(", "))
            assert admin_permissions == [
                "read",
                "update",
                "write",
            ], f"Разрешения для роли Admin не совпадают: {admin_permissions}"
