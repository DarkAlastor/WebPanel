import logging

from werkzeug.security import check_password_hash

from src.app.repository.interface.isession_repo import ISessionManager
from src.app.repository.interface.iuser_repo import IUserRepository
from src.app.schemas.main_controller_schemas import AuthUserSchemas
from src.app.utils.mapper import validate_schemas

logger = logging.getLogger("app_user_actions_logger")


class MainController:
    """
    Контроллер, обрабатывающий логику аутентификации пользователей и проверки активности сессии.

    Атрибуты:
        session_manger (ISessionManager): Объект для управления сессиями пользователей.
        user_repository (IUserRepository): Репозиторий для взаимодействия с базой данных пользователей.
    """

    __slots__ = ("session_manger", "user_repository")

    def __init__(self, user_repository: IUserRepository, session_manager: ISessionManager):
        """
        Инициализирует MainController с репозиторием пользователей и менеджером сессий.

        :param user_repository: Репозиторий для получения данных о пользователях.
        :param session_manager: Менеджер сессий для управления состоянием сессий.
        """
        self.session_manger = session_manager  # объект для управления сесиями (репозиторий)
        self.user_repository = user_repository  # объект для манипуляции с базой данных (репозиторий)

    @validate_schemas(AuthUserSchemas)
    def auth_user(self, data: AuthUserSchemas) -> bool | None:
        """
        Выполняет аутентификацию пользователя, проверяя его данные и устанавливая соответствующие значения в сессии.

        :return: True, если аутентификация успешна, False, если данные неверны, None в случае ошибки.
        """
        if not data:  # Проверяем преобразовались ли данные в схему
            return False

        # Получаем пользователя по его login
        user = self.user_repository.get_user_by_login(login=data.login)

        if not user:
            logger.warning(
                f"Неуспешная попытка входа: login='{data.login}', ip='{data.ip_addr}' (пользователь не найден)",
                extra={
                    "username": data.login,
                    "role": "Unknown",
                    "action": "login_failed",
                },
            )
            return False  # Если пользователь не найден, возвращаем False

        if check_password_hash(user.get("password_hash"), data.password):
            # Если пароль совпадает, записываем данные в сессию
            self.session_manger.set(
                key="user_id", value=str(user.get("user_id"))
            )  # Устанавливаем user_id в объект сессии
            self.session_manger.set(
                key="role_name", value=str(user.get("role_name"))
            )  # Устанавливаем роль пользователя
            self.session_manger.set(key="ip_addr", value=data.ip_addr)  # Устанавливаем ip-адрес пользователя в сессию
            logger.info(
                f"Успешный вход: "
                f"user_id='{user.get('user_id')}', "
                f"login='{data.login}', "
                f"role='{user.get('role_name')}', "
                f"ip='{data.ip_addr}'",
                extra={
                    "username": data.login,
                    "role": user.get("role_name", "Unknown"),
                    "action": "login_success",
                },
            )
            return True  # Аутентификация успешна
        logger.warning(
            f"Неуспешная попытка входа: login='{data.login}', ip='{data.ip_addr}' (неверный пароль)",
            extra={"username": data.login, "role": "Unknown", "action": "login_failed"},
        )
        return False  # Неверный пароль

    def check_activity_session(self, ip_addr: str) -> bool:
        """
        Проверяет активность сессии пользователя по его идентификатору и IP-адресу.

        :param ip_addr: IP-адрес пользователя для проверки активности сессии.
        :return: True, если сессия активна, False, если сессия не найдена или не активна.
        """
        user_id = self.session_manger.get("user_id")
        session_ip_addr = self.session_manger.get("ip_addr")
        role = self.session_manger.get("role_name")  # Без второго аргумента
        role = role if role is not None else "Unknown"  # Обрабатываем None

        if user_id:
            if session_ip_addr and session_ip_addr != ip_addr:
                logger.warning(
                    f"[ALERT] Изменение IP в активной сессии! user_id='{user_id}', "
                    f"старый IP='{session_ip_addr}', новый IP='{ip_addr}'",
                    extra={
                        "username": user_id,
                        "role": role,
                        "action": "session_ip_change",
                    },
                )
            else:
                logger.info(
                    f"Проверка активности сессии: user_id='{user_id}', ip='{ip_addr}' - Активна",
                    extra={
                        "username": user_id,
                        "role": role,
                        "action": "session_active",
                    },
                )
            return True

        logger.warning(
            f"Проверка активности сессии: ip='{ip_addr}' - Не найдена",
            extra={
                "username": "Unknown",
                "role": "Unknown",
                "action": "session_not_found",
            },
        )
        return False
