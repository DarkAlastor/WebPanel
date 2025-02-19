import re

from pydantic import BaseModel, Field, field_validator


class AuthUserSchemas(BaseModel):
    """
    Модель пользователя с автоматической валидацией в Pydantic v2.

    Атрибуты:
        login (str): Логин пользователя, должен содержать от 4 до 50 символов.
        password (str): Пароль пользователя, должен содержать минимум 4 символа.
        ip_addr (str): IP-адрес пользователя, строка без строгой валидации.
    """

    login: str = Field(
        ...,
        min_length=4,
        max_length=50,
        description="Login must be between 4 and 50 characters.",
    )
    password: str = Field(..., min_length=4, description="Password must be at least 4 characters long.")
    ip_addr: str = Field(..., description="User's IP address.")  # Теперь просто строка без валидации

    @field_validator("login")
    @classmethod
    def validate_login(cls, value: str) -> str:
        """
        Проверка логина.

        Условия:
        - Логин должен содержать только буквы, цифры, '.', '-', '_'.
        - Логин не должен начинаться с '.' или '-'.

        :param value: Логин пользователя.
        :return: Корректный логин.
        :raises ValueError: Если логин содержит недопустимые символы или начинается с '.' или '-'.
        """
        if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
            raise ValueError("Login contains invalid characters. Only letters, digits, '.', '-', and '_' are allowed.")

        if value.startswith(".") or value.startswith("-"):
            raise ValueError("Login cannot start with '.' or '-'.")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        Проверка пароля.

        Условия:
        - Пароль не должен содержать пробелы.

        :param value: Пароль пользователя.
        :return: Корректный пароль.
        :raises ValueError: Если пароль содержит пробелы.
        """
        if " " in value:
            raise ValueError("Password cannot contain spaces.")
        return value
