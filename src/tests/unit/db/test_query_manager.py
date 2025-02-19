import tempfile

import allure
import pytest

from src.app.db.query_manager import QueryManager


@allure.parent_suite("Database Tests")
@allure.suite("Тестирование QueryManager")
class TestQueryManager:
    @allure.sub_suite("Инициализация QueryManager")
    @allure.title("Тест инициализации QueryManager с существующим файлом запросов")
    @allure.description("Проверка корректной загрузки запросов из YAML-файла при инициализации QueryManager")
    def test_query_manager_initialization(self, temp_query_file):
        with allure.step("Создаем экземпляр QueryManager"):
            query_manager = QueryManager.from_yaml(file_path_query_yaml=temp_query_file)

        with allure.step("Проверяем зарегистрированные запросы"):
            assert (
                len(query_manager.queries) == 5
            ), f"Ожидалось 5 зарегистрированных запросов, получено {len(query_manager.queries)}"

    @allure.sub_suite("Получение запросов QueryManager")
    @allure.title("Тест получения запроса по имени")
    def test_get_query(self, temp_query_file):
        with allure.step("Создаем экземпляр QueryManager"):
            query_manager = QueryManager.from_yaml(file_path_query_yaml=temp_query_file)

        with allure.step("Получаем запрос по имени"):
            query = query_manager.get_query("get_all_users")
            assert query == "SELECT * FROM users", "Некорректный запрос для 'get_all_users'"

    @allure.sub_suite("Обработка ошибок QueryManager")
    @allure.title("Тест обработки ошибок при отсутствии запроса")
    def test_get_query_not_found(self, temp_query_file):
        with allure.step("Создаем экземпляр QueryManager"):
            query_manager = QueryManager.from_yaml(file_path_query_yaml=temp_query_file)

        with allure.step("Пытаемся получить несуществующий запрос"):
            with pytest.raises(ValueError, match="Запрос с именем 'non_existent_query' не найден."):
                query_manager.get_query("non_existent_query")

    @allure.sub_suite("Инициализация QueryManager")
    @allure.title("Тест инициализации QueryManager с пустым файлом")
    @allure.description("Проверка поведения QueryManager при пустом YAML-файле")
    def test_query_manager_with_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as temp_file:
            temp_file.write("")  # Пустой YAML
            temp_file.flush()

        with allure.step("Проверяем, что инициализация с пустым файлом вызывает ошибку"):
            with pytest.raises(ValueError, match="Некорректный формат YAML"):
                QueryManager.from_yaml(file_path_query_yaml=temp_file.name)
