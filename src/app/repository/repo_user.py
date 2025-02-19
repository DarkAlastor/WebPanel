from typing import Dict, Optional

from src.app.db.db_helper import DBHelperSQL
from src.app.repository.interface.iuser_repo import IUserRepository


class UserRepository(IUserRepository):
    """
    Реализация интерфейса IUserRepository для взаимодействия с таблицей пользователей.

    :param db_helper: Экземпляр DBHelperSQL для выполнения SQL-запросов.
    """

    def __init__(self, db_helper: DBHelperSQL) -> None:
        """
        Инициализирует репозиторий пользователей.

        :param db_helper: DBHelperSQL для взаимодействия с базой данных.
        """
        self.db_helper = db_helper

    def get_user_by_login(self, login: str) -> Optional[Dict[str, str]]:
        """
        Получает данные пользователя по его логину.

        :param login: Логин пользователя.
        :return: Словарь с данными пользователя, включая логин, пароль и роль,
                 или None, если пользователь не найден.
        """
        # Выполнение SQL-запроса с параметром login.
        result = self.db_helper.execute_query(query_name="get_user_by_login", params={"login": login})

        # Возврат первой записи, если она найдена, иначе None.
        return result[0] if result else None
