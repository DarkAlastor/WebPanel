import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
class TestHandleDbHelperErrors:

    @allure.sub_suite("Успешное выполнение DBHelperSQL")
    @allure.title("Успешное выполнение запроса (execute_query)")
    @allure.description("Проверяет, что метод execute_query успешно выполняется и возвращает 'query_success'.")
    def test_success_query(self, dummy_helper_success_query):
        """
        Проверяет, что execute_query успешно выполняется и возвращает 'query_success'.
        """
        with allure.step("Выполнить запрос с валидными параметрами"):
            result = dummy_helper_success_query.execute_query("test_query", {"param": "value"})
        with allure.step("Проверить, что результат равен 'query_success'"):
            assert result == "query_success", f"Ожидалось 'query_success', получено: {result}"

    @allure.sub_suite("Успешное выполнение DBHelperSQL")
    @allure.title("Успешное выполнение обновления (execute_update)")
    @allure.description("Проверяет, что метод execute_update успешно выполняется и возвращает 'update_success'.")
    def test_success_update(self, dummy_helper_success_update):
        """
        Проверяет, что execute_update успешно выполняется и возвращает 'update_success'.
        """
        with allure.step("Выполнить обновление с валидными параметрами"):
            result = dummy_helper_success_update.execute_update("test_update", {"param": "value"})
        with allure.step("Проверить, что результат равен 'update_success'"):
            assert result == "update_success", f"Ожидалось 'update_success', получено: {result}"

    @allure.sub_suite("Обработка OperationalError")
    @allure.title("OperationalError в execute_query возвращает []")
    @allure.description(
        "Проверяет, что при возникновении OperationalError метод execute_query возвращает пустой список."
    )
    def test_operational_error_query(self, dummy_helper_operational_error_query):
        """
        Проверяет, что при OperationalError execute_query возвращает пустой список.
        """
        with allure.step("Выполнить запрос, генерирующий OperationalError"):
            result = dummy_helper_operational_error_query.execute_query("op_query", {"param": "value"})
        with allure.step("Проверить, что результат равен пустому списку"):
            assert result == [], f"Ожидалось пустой список, получено: {result}"

    @allure.sub_suite("Обработка OperationalError")
    @allure.title("OperationalError в execute_update возвращает False")
    @allure.description("Проверяет, что при возникновении OperationalError метод execute_update возвращает False.")
    def test_operational_error_update(self, dummy_helper_operational_error_update):
        """
        Проверяет, что при OperationalError execute_update возвращает False.
        """
        with allure.step("Выполнить обновление, генерирующее OperationalError"):
            result = dummy_helper_operational_error_update.execute_update("op_update", {"param": "value"})
        with allure.step("Проверить, что результат равен False"):
            assert result is False, f"Ожидалось False, получено: {result}"

    @allure.sub_suite("Обработка IntegrityError")
    @allure.title("IntegrityError в execute_query возвращает []")
    @allure.description("Проверяет, что при возникновении IntegrityError метод execute_query возвращает пустой список.")
    def test_integrity_error_query(self, dummy_helper_integrity_error_query):
        """
        Проверяет, что при IntegrityError execute_query возвращает пустой список.
        """
        with allure.step("Выполнить запрос, генерирующий IntegrityError"):
            result = dummy_helper_integrity_error_query.execute_query("int_query", {"param": "value"})
        with allure.step("Проверить, что результат равен пустому списку"):
            assert result == [], f"Ожидалось пустой список, получено: {result}"

    @allure.sub_suite("Обработка IntegrityError")
    @allure.title("IntegrityError в execute_update возвращает False")
    @allure.description("Проверяет, что при возникновении IntegrityError метод execute_update возвращает False.")
    def test_integrity_error_update(self, dummy_helper_integrity_error_update):
        """
        Проверяет, что при IntegrityError execute_update возвращает False.
        """
        with allure.step("Выполнить обновление, генерирующее IntegrityError"):
            result = dummy_helper_integrity_error_update.execute_update("int_update", {"param": "value"})
        with allure.step("Проверить, что результат равен False"):
            assert result is False, f"Ожидалось False, получено: {result}"

    @allure.sub_suite("Обработка ProgrammingError")
    @allure.title("ProgrammingError в execute_query возвращает []")
    @allure.description(
        "Проверяет, что при возникновении ProgrammingError метод execute_query возвращает пустой список."
    )
    def test_programming_error_query(self, dummy_helper_programming_error_query):
        """
        Проверяет, что при ProgrammingError execute_query возвращает пустой список.
        """
        with allure.step("Выполнить запрос, генерирующий ProgrammingError"):
            result = dummy_helper_programming_error_query.execute_query("prog_query", {"param": "value"})
        with allure.step("Проверить, что результат равен пустому списку"):
            assert result == [], f"Ожидалось пустой список, получено: {result}"

    @allure.sub_suite("Обработка ProgrammingError")
    @allure.title("ProgrammingError в execute_update возвращает False")
    @allure.description("Проверяет, что при возникновении ProgrammingError метод execute_update возвращает False.")
    def test_programming_error_update(self, dummy_helper_programming_error_update):
        """
        Проверяет, что при ProgrammingError execute_update возвращает False.
        """
        with allure.step("Выполнить обновление, генерирующее ProgrammingError"):
            result = dummy_helper_programming_error_update.execute_update("prog_update", {"param": "value"})
        with allure.step("Проверить, что результат равен False"):
            assert result is False, f"Ожидалось False, получено: {result}"

    @allure.sub_suite("Обработка DataError")
    @allure.title("DataError в execute_query возвращает []")
    @allure.description("Проверяет, что при возникновении DataError метод execute_query возвращает пустой список.")
    def test_data_error_query(self, dummy_helper_data_error_query):
        """
        Проверяет, что при DataError execute_query возвращает пустой список.
        """
        with allure.step("Выполнить запрос, генерирующий DataError"):
            result = dummy_helper_data_error_query.execute_query("data_query", {"param": "value"})
        with allure.step("Проверить, что результат равен пустому списку"):
            assert result == [], f"Ожидалось пустой список, получено: {result}"

    @allure.sub_suite("Обработка DataError")
    @allure.title("DataError в execute_update возвращает False")
    @allure.description("Проверяет, что при возникновении DataError метод execute_update возвращает False.")
    def test_data_error_update(self, dummy_helper_data_error_update):
        """
        Проверяет, что при DataError execute_update возвращает False.
        """
        with allure.step("Выполнить обновление, генерирующее DataError"):
            result = dummy_helper_data_error_update.execute_update("data_update", {"param": "value"})
        with allure.step("Проверить, что результат равен False"):
            assert result is False, f"Ожидалось False, получено: {result}"

    @allure.sub_suite("Обработка SQLAlchemyError")
    @allure.title("SQLAlchemyError в execute_query возвращает []")
    @allure.description(
        "Проверяет, что при возникновении SQLAlchemyError метод execute_query возвращает пустой список."
    )
    def test_sqlalchemy_error_query(self, dummy_helper_sqlalchemy_error_query):
        """
        Проверяет, что при SQLAlchemyError execute_query возвращает пустой список.
        """
        with allure.step("Выполнить запрос, генерирующий SQLAlchemyError"):
            result = dummy_helper_sqlalchemy_error_query.execute_query("sa_query", {"param": "value"})
        with allure.step("Проверить, что результат равен пустому списку"):
            assert result == [], f"Ожидалось пустой список, получено: {result}"

    @allure.sub_suite("Обработка SQLAlchemyError")
    @allure.title("SQLAlchemyError в execute_update возвращает False")
    @allure.description("Проверяет, что при возникновении SQLAlchemyError метод execute_update возвращает False.")
    def test_sqlalchemy_error_update(self, dummy_helper_sqlalchemy_error_update):
        """
        Проверяет, что при SQLAlchemyError execute_update возвращает False.
        """
        with allure.step("Выполнить обновление, генерирующее SQLAlchemyError"):
            result = dummy_helper_sqlalchemy_error_update.execute_update("sa_update", {"param": "value"})
        with allure.step("Проверить, что результат равен False"):
            assert result is False, f"Ожидалось False, получено: {result}"

    @allure.sub_suite("Обработка Generic Exception")
    @allure.title("Generic Exception в execute_query возвращает []")
    @allure.description(
        "Проверяет, что при возникновении Generic Exception метод execute_query возвращает пустой список."
    )
    def test_generic_exception_query(self, dummy_helper_generic_error_query):
        """
        Проверяет, что при возникновении Generic Exception execute_query возвращает пустой список.
        """
        with allure.step("Выполнить запрос, генерирующий Generic Exception"):
            result = dummy_helper_generic_error_query.execute_query("generic_query", {"param": "value"})
        with allure.step("Проверить, что результат равен пустому списку"):
            assert result == [], f"Ожидалось пустой список, получено: {result}"

    @allure.sub_suite("Обработка Generic Exception")
    @allure.title("Generic Exception в execute_update возвращает False")
    @allure.description("Проверяет, что при возникновении Generic Exception метод execute_update возвращает False.")
    def test_generic_exception_update(self, dummy_helper_generic_error_update):
        """
        Проверяет, что при возникновении Generic Exception execute_update возвращает False.
        """
        with allure.step("Выполнить обновление, генерирующее Generic Exception"):
            result = dummy_helper_generic_error_update.execute_update("generic_update", {"param": "value"})
        with allure.step("Проверить, что результат равен False"):
            assert result is False, f"Ожидалось False, получено: {result}"
