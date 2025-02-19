import functools
from typing import Any, Callable, Type

from pydantic import BaseModel, ValidationError


def validate_schemas(schemas: Type[BaseModel]) -> Callable:
    """
    Декоратор для автоматической валидации входных данных с помощью Pydantic.

    Этот декоратор:
    - Принимает Pydantic-схему (`schemas`).
    - Преобразует входные данные (`dict`) в указанную Pydantic-модель.
    - Если валидация проходит успешно, передаёт валидированные данные в функцию.
    - Если валидация **не проходит**, возвращает `False`.

    **Использование:**
    ```python
    @validate_schemas(AuthUserSchemas)
    def auth_user(self, data: AuthUserSchemas) -> bool | None:
        ...
    ```

    :param schemas: Класс Pydantic, который будет использоваться для валидации данных.
    :return: Декорированная функция с автоматической валидацией входных данных.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, data: dict[str, Any], *args, **kwargs) -> Any:
            try:
                validated_data = schemas(**data)  # Валидация данных через Pydantic
                return func(self, validated_data, *args, **kwargs)  # Передаём валидированные данные
            except ValidationError:
                return None  # Валидация не пройдена

        return wrapper

    return decorator
