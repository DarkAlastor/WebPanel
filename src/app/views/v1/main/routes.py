from flask import redirect, render_template, request, url_for
from flask_smorest import Blueprint  # type: ignore
from werkzeug.exceptions import Unauthorized
from werkzeug.wrappers import Response

from .forms import LoginForm
from .handler_error import handle_error_for_html_views
from .interface_controller import IMainController
from .schemas import LoginSchema
from .utils import inject_form


class MainBlueprint(Blueprint):
    """
    Главный blueprint для приложения.

    Этот класс реализует основную логику маршрутов и обработки запросов.
    Он регистрирует маршруты для страниц входа, о приложении и основной страницы.
    Взаимодействует с контроллером для проверки активности сессий и аутентификации пользователей.

    Атрибуты:
        controller (IMainController): Контроллер, предоставляющий функциональность для проверки сессий и аутентификации.
    """

    def __init__(self, controller: IMainController, redirect_url: str = "v1.main.about"):
        """
        Инициализирует экземпляр MainBlueprint.

        :param controller: Контроллер для обработки сессий и аутентификации.
        :param redirect_url: Ссылка для переходной страницы
        """
        super().__init__(
            "main",
            __name__,
            template_folder="templates",
            static_folder="static",
            static_url_path="/v1/main/static",
        )
        self.controller = controller
        self.redirect_url = redirect_url

        # Регистрация маршрутов внутри Blueprint
        self.route("/", methods=["GET"], tags=["blueprint_main"])(self.index)
        self.route("/about", methods=["GET"], tags=["blueprint_main"])(self.about)
        self.route("/login", methods=["GET"], tags=["blueprint_main"])(self.login_get)
        self.route("/login", methods=["POST"], tags=["blueprint_main"])(
            self.arguments(LoginSchema, location="form")(self.login_post)
        )

    @handle_error_for_html_views()
    def index(self) -> str | Response:
        """
        Обрабатывает запрос на главную страницу.

        Проверяет активность сессии пользователя по IP-адресу. Если сессия активна, перенаправляет на страницу "about".
        В противном случае отображает страницу входа.

        :return: Страница входа или редирект на страницу "about".
        """
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if self.controller.check_activity_session(ip_addr=ip_address):
            return redirect(url_for(self.redirect_url))
        return redirect(url_for("v1.main.login_get"))  # Тип возвращаемого значения: str | flask.wrappers.Response

    @handle_error_for_html_views()
    def about(self) -> str | Response:
        """
        Обрабатывает запрос на страницу "О приложении".

        :return: Страница "about".
        """
        return render_template("about.html")

    @inject_form(LoginForm)
    @handle_error_for_html_views()
    def login_get(self, form: LoginForm) -> str | Response:
        """
        Обрабатывает GET-запрос на страницу входа.

        Отображает форму входа.
        """
        return render_template("login.html", form=form)

    @inject_form(LoginForm)
    @handle_error_for_html_views(error_template="error.html")
    def login_post(self, schemas: LoginSchema, form: LoginForm) -> str | Response:  # type: ignore
        """
        Обрабатывает POST-запрос на страницу входа.
        """
        ip_address = str(request.headers.get("X-Forwarded-For", request.remote_addr))

        if self.controller.check_activity_session(ip_addr=ip_address):
            return redirect(url_for(self.redirect_url))

        if form.validate_on_submit():
            data = {
                "login": form.login.data,
                "password": form.password.data,
                "ip_addr": ip_address,
            }
            status = self.controller.auth_user(data)

            if status:
                return redirect(url_for(self.redirect_url))

            raise Unauthorized("Invalid login or password.")
