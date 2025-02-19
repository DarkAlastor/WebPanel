import logging
from functools import wraps
from typing import Any, Callable

from flask import render_template
from werkzeug.exceptions import Forbidden, InternalServerError, Unauthorized

logger = logging.getLogger("app_logger")


def handle_error_for_html_views(
    error_template: str = "error.html",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для обработки ошибок в представлениях (views), возвращающих HTML.

    - **Forbidden (403)** → Рендерит `error_template`
    - **InternalServerError (500)** → Рендерит `error_template`
    - **Unauthorized (401)** → Если передана форма, добавляет ошибку в `form.password.errors`
    - **Другие ошибки** → Логируются и рендерится `error_template`

    :param error_template: Шаблон, который используется для отображения ошибок (по умолчанию `error.html`).
    :return: Декорированная функция.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            """
            Обёртка для обработки ошибок.

            :param self: Экземпляр представления (self, если метод класса).
            :param args: Позиционные аргументы, передаваемые в представление.
            :param kwargs: Ключевые аргументы, передаваемые в представление.
            :return: Либо результат оригинальной функции, либо шаблон ошибки.
            """
            try:
                return func(self, *args, **kwargs)
            except Unauthorized:
                form = kwargs.get("form")
                form.password.errors.append("Invalid login or password.")  # type: ignore
                return render_template("login.html", form=form)  # Возвращаем страницу входа
            except Forbidden as e:
                logger.error(
                    f"Ошибка 403 в {func.__name__}: {e}. Args: {args}, Kwargs: {kwargs}",
                    exc_info=True,
                )
                return (
                    render_template(
                        error_template,
                        error="Forbidden Error 403",
                        message=str("Come back later"),
                    ),
                    403,
                )
            except InternalServerError as e:
                logger.error(
                    f"Ошибка 500 в {func.__name__}: {e}. Args: {args}, Kwargs: {kwargs}",
                    exc_info=True,
                )
                return (
                    render_template(
                        error_template,
                        error="Internal Server Error 500",
                        message=str("Come back later"),
                    ),
                    500,
                )
            except Exception as e:
                logger.error(
                    f"Неизвестная ошибка в {func.__name__}: {e}. Args: {args}, Kwargs: {kwargs}",
                    exc_info=True,
                )
                return (
                    render_template(error_template, error="Internal Error", message=str("Ops.....")),
                    500,
                )

        return wrapper

    return decorator
