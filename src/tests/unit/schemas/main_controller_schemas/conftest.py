import pytest

# ======== Фикстуры для schemas AuthUserSchemas ========


@pytest.fixture
def valid_user_data():
    """
    Фикстура, возвращающая корректные данные для пользователя.

    Используется для тестирования успешных сценариев аутентификации или регистрации.
    """
    return {
        "login": "validUser",
        "password": "StrongPass1",
        "ip_addr": "8.8.8.8",  # Публичный IP-адрес
    }


@pytest.fixture(params=["user@", "root admin", "username!", "user#name", ".username", "-username"])
def invalid_login(request):
    """
    Фикстура, возвращающая логины, содержащие запрещённые символы.

    Используется для тестирования валидации логина и проверки отказа в регистрации/аутентификации.
    """
    return request.param


@pytest.fixture(params=["usr", "a", "12"])
def short_login(request):
    """
    Фикстура, возвращающая логины, которые слишком короткие.

    Применяется для проверки минимальной длины логина и корректности валидации.
    """
    return request.param


@pytest.fixture(params=["Pass word1", "My Secure Password", " 12345678"])
def invalid_password(request):
    """
    Фикстура, возвращающая пароли, содержащие пробелы.

    Используется для проверки того, что пароли не должны содержать пробелы, если это требуется правилами валидации.
    """
    return request.param
