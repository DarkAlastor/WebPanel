import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование RepositoryFlaskSessionManager")
class TestRepositoryFlaskSessionManager:

    @allure.sub_suite("Метод set")
    @allure.title("Проверка сохранения строкового значения в сессию")
    @allure.description(
        "Проверяет, что метод set корректно сохраняет строковое значение по указанному ключу в session."
    )
    def test_set_method(self, fake_session, repo_session_manager):
        """
        Тест проверяет, что метод set сохраняет строковое значение по ключу в сессии.
        """
        # Очищаем сессию для гарантии чистого состояния
        fake_session.clear()

        # Сохраняем значение в сессию
        repo_session_manager.set("test_key", "test_value")

        # Проверяем, что значение успешно сохранено
        saved_value = fake_session.get("test_key")
        assert saved_value == "test_value", f"Ожидалось 'test_value', получено: {saved_value}"
