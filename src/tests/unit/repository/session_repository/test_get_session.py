import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование RepositoryFlaskSessionManager")
class TestRepositoryFlaskSessionManager:

    @allure.sub_suite("Метод get")
    @allure.title("Проверка возвращения строкового значения")
    @allure.description(
        "Проверяет, что метод get возвращает корректное строковое значение, если оно присутствует в сессии."
    )
    def test_get_existing_string(self, fake_session, repo_session_manager):
        """
        Проверяет, что метод get возвращает строковое значение, если оно присутствует.
        """
        fake_session["test_key"] = "test_value"
        result = repo_session_manager.get("test_key")
        assert result == "test_value"

    @allure.sub_suite("Метод get")
    @allure.title("Проверка возвращения None для нестрокового значения")
    @allure.description("Проверяет, что метод get возвращает None, если значение по ключу не является строкой.")
    def test_get_non_string_returns_none(self, fake_session, repo_session_manager):
        """
        Проверяет, что метод get возвращает None, если значение не является строкой.
        """
        fake_session["test_key"] = 123  # не строковое значение
        result = repo_session_manager.get("test_key")
        assert result is None

    @allure.sub_suite("Метод get")
    @allure.title("Проверка возвращения None для отсутствующего ключа")
    @allure.description("Проверяет, что метод get возвращает None, если ключ отсутствует в сессии.")
    def test_get_missing_key_returns_none(self, fake_session, repo_session_manager):
        """
        Проверяет, что метод get возвращает None, если ключ отсутствует.
        """
        result = repo_session_manager.get("nonexistent")
        assert result is None
