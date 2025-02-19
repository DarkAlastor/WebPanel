from functools import wraps
from typing import Any, Callable, Type

from flask_wtf import FlaskForm  # type: ignore


def inject_form(
    form_class: Type[FlaskForm],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для инициализации формы и передачи её в `kwargs` представления.

    Этот декоратор создаёт экземпляр формы и передаёт его в `kwargs`
    декорированной функции.

    :param form_class: Класс формы, который нужно создать.
    :return: Декорированная функция.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            kwargs["form"] = form_class()  # Создаём форму и передаём в kwargs
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
