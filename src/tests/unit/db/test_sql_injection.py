import allure
import pytest


@allure.parent_suite("Database Tests")
@allure.suite("Тестирование SQL Injection Protection")
class TestSQLInjectionProtection:
    @allure.sub_suite("Проверка безопасности user_queries")
    @allure.title("Тест защиты от SQL-инъекций в get_user_by_login")
    @pytest.mark.parametrize(
        "malicious_input",
        [
            "' OR '1'='1",  # Универсальный взлом (должен вернуть 0 записей, если защита работает)
            "'; DROP TABLE users; --",  # Попытка удалить таблицу (должен вернуть ошибку или 0 записей)
            "'; SELECT * FROM users; --",  # Попытка получить всех пользователей (должен вернуть 0 записей)
            "'; UPDATE users SET password_hash='hacked' WHERE login='root'; --",  # Попытка изменения данных
            "' UNION SELECT 1, 'hacked', 'root' --",  # Попытка добавить фейковые данные (должен вернуть 0 записей)
        ],
    )
    def test_sql_injection_get_user_by_login(self, db_helper_with_real_queries, malicious_input):
        with allure.step(f"Пробуем выполнить get_user_by_login с вредоносным вводом: {malicious_input}"):
            result = db_helper_with_real_queries.execute_query("get_user_by_login", {"login": malicious_input})

        with allure.step("Проверяем, что SQL-инъекция не сработала"):
            assert result is None or len(result) == 0, "SQL-инъекция удалась! Запрос вернул неожиданные данные"

    @allure.sub_suite("Проверка безопасности user_queries")
    @allure.title("Тест защиты от SQL-инъекций в get_user_with_role_and_permissions")
    @pytest.mark.parametrize(
        "malicious_input",
        [
            "' OR '1'='1",
            "'; DROP TABLE role; --",
            "' UNION SELECT 1, 'hacked', 'root' --",
        ],
    )
    def test_sql_injection_get_user_with_role_and_permissions(self, db_helper_with_real_queries, malicious_input):
        with allure.step(
            f"Пробуем выполнить get_user_with_role_and_permissions с вредоносным вводом: {malicious_input}"
        ):
            result = db_helper_with_real_queries.execute_query(
                "get_user_with_role_and_permissions", {"role_name": malicious_input}
            )

        with allure.step("Проверяем, что SQL-инъекция не сработала"):
            assert result is None or len(result) == 0, "SQL-инъекция удалась! Запрос вернул неожиданные данные"

    @allure.sub_suite("Проверка безопасности role_queries")
    @allure.title("Тест защиты от SQL-инъекций в get_all_roles_and_permissions")
    @pytest.mark.parametrize(
        "malicious_input",
        [
            "' OR '1'='1",
            "'; DROP TABLE permission; --",
            "' UNION SELECT 1, 'hacked', 'root' --",
        ],
    )
    def test_sql_injection_get_all_roles_and_permissions(self, db_helper_with_real_queries, malicious_input):
        with allure.step(f"Пробуем выполнить get_all_roles_and_permissions с вредоносным вводом: {malicious_input}"):
            result = db_helper_with_real_queries.execute_query("get_all_roles_and_permissions")

        with allure.step("Проверяем, что SQL-инъекция не сработала"):
            assert result is not None, "SQL-инъекция удалась! Запрос вернул неожиданные данные"
