import allure

from src.app.db.db_core import DatabaseCore
from src.app.db.models import PermissionModel, RoleModel, UserModel


@allure.parent_suite("Database Tests")
@allure.suite("Тестирование DatabaseCore")
@allure.sub_suite("Инициализация базы данных")
class TestDatabaseCore:
    @allure.title("Тест инициализации базы данных через DatabaseCore")
    @allure.description("Проверка создания движка и сессии для DatabaseCore")
    def test_database_core_initialization(self, mock_app):
        with allure.step("Инициализируем DatabaseCore"):
            db_core = DatabaseCore()
            db_core.init_app(mock_app)

        with allure.step("Проверяем, что движок и сессия созданы"):
            assert db_core.engine is not None, "Движок базы данных не создан"
            assert db_core.Session is not None, "Сессия базы данных не создана"

    @allure.title("Тест создания таблиц и данных через DatabaseCore")
    @allure.description("Проверка создания таблиц и инициализации данных в базе")
    def test_create_tables_with_initializer(self, mock_app):
        with allure.step("Инициализируем DatabaseCore и создаем таблицы"):
            db_core = DatabaseCore()
            db_core.init_app(mock_app)
            db_core.create_tables()

        with allure.step("Проверяем, что данные добавлены в базу"):
            with db_core.session_scope() as session:
                with allure.step("Проверяем добавленные права"):
                    permissions = session.query(PermissionModel).all()
                    assert len(permissions) == 4, f"Ожидалось 4 права, получено: {len(permissions)}"
                    assert {perm.name for perm in permissions} == {
                        "read",
                        "write",
                        "delete",
                        "update",
                    }, "Права не совпадают"

                with allure.step("Проверяем добавленные роли"):
                    roles = session.query(RoleModel).all()
                    assert len(roles) == 2, f"Ожидалось 2 роли, получено: {len(roles)}"

                    root_role = session.query(RoleModel).filter_by(role_name="Root").first()
                    admin_role = session.query(RoleModel).filter_by(role_name="Admin").first()
                    assert root_role is not None, "Роль Root не найдена"
                    assert admin_role is not None, "Роль Admin не найдена"

                    assert {perm.name for perm in root_role.permissions} == {
                        "read",
                        "write",
                        "delete",
                    }, "Права роли Root не совпадают"
                    assert {perm.name for perm in admin_role.permissions} == {
                        "read",
                        "write",
                        "update",
                    }, "Права роли Admin не совпадают"

                with allure.step("Проверяем добавленных пользователей"):
                    users = session.query(UserModel).all()
                    assert len(users) == 2, f"Ожидалось 2 пользователя, получено: {len(users)}"

                    root_user = session.query(UserModel).filter_by(login="root").first()
                    admin_user = session.query(UserModel).filter_by(login="admin").first()
                    assert root_user is not None, "Пользователь root не найден"
                    assert admin_user is not None, "Пользователь admin не найден"

                    assert root_user.role.role_name == "Root", "У пользователя root неверная роль"
                    assert admin_user.role.role_name == "Admin", "У пользователя admin неверная роль"
