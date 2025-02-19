import allure


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Успешное выполнение DBHelperSQL")
@allure.title("Проверка корректного выполнения методов DBHelperSQL")
class TestHandleDbHelperErrorsSuccess:
    @allure.title("Успешное выполнение запроса (execute_query)")
    def test_success_query(self, dummy_helper_success_query):
        result = dummy_helper_success_query.execute_query("test_query", {"param": "value"})
        assert result == "query_success"

    @allure.title("Успешное выполнение обновления (execute_update)")
    def test_success_update(self, dummy_helper_success_update):
        result = dummy_helper_success_update.execute_update("test_update", {"param": "value"})
        assert result == "update_success"


# Тесты для OperationalError


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Обработка OperationalError")
@allure.title("Проверка обработки OperationalError")
class TestHandleDbHelperErrorsOperationalError:
    @allure.title("OperationalError в execute_query возвращает []")
    def test_operational_error_query(self, dummy_helper_operational_error_query):
        result = dummy_helper_operational_error_query.execute_query("op_query", {"param": "value"})
        assert result == []

    @allure.title("OperationalError в execute_update возвращает False")
    def test_operational_error_update(self, dummy_helper_operational_error_update):
        result = dummy_helper_operational_error_update.execute_update("op_update", {"param": "value"})
        assert result is False


# Тесты для IntegrityError


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Обработка IntegrityError")
@allure.title("Проверка обработки IntegrityError")
class TestHandleDbHelperErrorsIntegrityError:
    @allure.title("IntegrityError в execute_query возвращает []")
    def test_integrity_error_query(self, dummy_helper_integrity_error_query):
        result = dummy_helper_integrity_error_query.execute_query("int_query", {"param": "value"})
        assert result == []

    @allure.title("IntegrityError в execute_update возвращает False")
    def test_integrity_error_update(self, dummy_helper_integrity_error_update):
        result = dummy_helper_integrity_error_update.execute_update("int_update", {"param": "value"})
        assert result is False


# Тесты для ProgrammingError


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Обработка ProgrammingError")
@allure.title("Проверка обработки ProgrammingError")
class TestHandleDbHelperErrorsProgrammingError:
    @allure.title("ProgrammingError в execute_query возвращает []")
    def test_programming_error_query(self, dummy_helper_programming_error_query):
        result = dummy_helper_programming_error_query.execute_query("prog_query", {"param": "value"})
        assert result == []

    @allure.title("ProgrammingError в execute_update возвращает False")
    def test_programming_error_update(self, dummy_helper_programming_error_update):
        result = dummy_helper_programming_error_update.execute_update("prog_update", {"param": "value"})
        assert result is False


# Тесты для DataError


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Обработка DataError")
@allure.title("Проверка обработки DataError")
class TestHandleDbHelperErrorsDataError:
    @allure.title("DataError в execute_query возвращает []")
    def test_data_error_query(self, dummy_helper_data_error_query):
        result = dummy_helper_data_error_query.execute_query("data_query", {"param": "value"})
        assert result == []

    @allure.title("DataError в execute_update возвращает False")
    def test_data_error_update(self, dummy_helper_data_error_update):
        result = dummy_helper_data_error_update.execute_update("data_update", {"param": "value"})
        assert result is False


# Тесты для SQLAlchemyError


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Обработка SQLAlchemyError")
@allure.title("Проверка обработки SQLAlchemyError")
class TestHandleDbHelperErrorsSQLAlchemyError:
    @allure.title("SQLAlchemyError в execute_query возвращает []")
    def test_sqlalchemy_error_query(self, dummy_helper_sqlalchemy_error_query):
        result = dummy_helper_sqlalchemy_error_query.execute_query("sa_query", {"param": "value"})
        assert result == []

    @allure.title("SQLAlchemyError в execute_update возвращает False")
    def test_sqlalchemy_error_update(self, dummy_helper_sqlalchemy_error_update):
        result = dummy_helper_sqlalchemy_error_update.execute_update("sa_update", {"param": "value"})
        assert result is False


# Тесты для Generic Exception


@allure.parent_suite("Unit Tests")
@allure.suite("Тестирование декоратора handle_db_helper_errors")
@allure.sub_suite("Обработка Generic Exception")
@allure.title("Проверка обработки Generic Exception")
class TestHandleDbHelperErrorsGenericException:
    @allure.title("Generic Exception в execute_query возвращает []")
    def test_generic_exception_query(self, dummy_helper_generic_error_query):
        result = dummy_helper_generic_error_query.execute_query("generic_query", {"param": "value"})
        assert result == []

    @allure.title("Generic Exception в execute_update возвращает False")
    def test_generic_exception_update(self, dummy_helper_generic_error_update):
        result = dummy_helper_generic_error_update.execute_update("generic_update", {"param": "value"})
        assert result is False
