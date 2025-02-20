import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование RepositoryFlaskSessionManager")
class TestRepositoryFlaskSessionManager:

    @allure.sub_suite("Метод exists")
    @allure.title("Проверка наличия ключа")
    @allure.description("Проверяет, что метод exists возвращает True для существующего ключа в session.")
    def test_exists_key_present(self, fake_session, repo_session_manager):
        """
        Проверяет, что метод exists корректно определяет наличие ключа в session.
        """
        fake_session.clear()
        fake_session["present_key"] = "value"
        assert repo_session_manager.exists("present_key") is True, "Метод должен вернуть True для существующего ключа"

    @allure.sub_suite("Метод exists")
    @allure.title("Проверка отсутствия ключа")
    @allure.description("Проверяет, что метод exists возвращает False для отсутствующего ключа в session.")
    def test_exists_key_absent(self, fake_session, repo_session_manager):
        """
        Проверяет, что метод exists корректно определяет отсутствие ключа в session.
        """
        fake_session.clear()
        assert repo_session_manager.exists("absent_key") is False, "Метод должен вернуть False для отсутствующего ключа"
