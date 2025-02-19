import pytest


# Фикстура: Корректные данные
@pytest.fixture
def valid_user_data():
    return {
        "login": "validUser",
        "password": "StrongPass1",
        "ip_addr": "8.8.8.8",  # Публичный IP-адрес
    }


# Фикстура: Логины с запрещёнными символами
@pytest.fixture(params=["user@", "root admin", "username!", "user#name", ".username", "-username"])
def invalid_login(request):
    return request.param


# Фикстура: Логины, которые слишком короткие
@pytest.fixture(params=["usr", "a", "12"])
def short_login(request):
    return request.param


# Фикстура: Пароли с пробелами
@pytest.fixture(params=["Pass word1", "My Secure Password", " 12345678"])
def invalid_password(request):
    return request.param
