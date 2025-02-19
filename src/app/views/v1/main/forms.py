from flask_wtf import FlaskForm  # type: ignore
from wtforms import PasswordField, StringField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Length  # type: ignore


class LoginForm(FlaskForm):
    """
    Форма для страницы входа. Используется в Blueprint MainBlueprint.

    Эта форма предназначена для аутентификации пользователей, требуя ввода логина и пароля.
    Содержит поля:
    - login: строка для ввода логина.
    - password: строка для ввода пароля.
    - submit: кнопка отправки формы.

    Валидация:
    - Логин должен содержать от 4 до 50 символов.
    - Пароль должен содержать минимум 4 символа.
    """

    # Поле для ввода логина
    login: StringField = StringField(
        "Login",  # Метка для поля
        validators=[  # Список валидаторов для поля
            DataRequired(message="The login field is required"),  # Обязательное поле
            Length(min=4, max=50, message="Login must be between 3 and 50 charters"),  # Длина логина
        ],
    )

    # Поле для ввода пароля
    password: PasswordField = PasswordField(
        "Password",  # Метка для поля
        validators=[  # Список валидаторов для поля
            DataRequired(message="The password field is required"),  # Обязательное поле
            Length(min=4, message="Password must be at least 6 characters."),  # Длина пароля
        ],
    )

    # Кнопка отправки формы
    submit: SubmitField = SubmitField("Sign In")
