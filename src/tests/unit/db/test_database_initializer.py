import allure

from src.app.db.models import PermissionModel, RoleModel, UserModel


@allure.parent_suite("Database Tests")
@allure.suite("Тестирование DatabaseInitializer")
@allure.sub_suite("Добавление данных в базу")
class TestDatabaseInitializer:
    @allure.title("Тест добавления прав доступа")
    @allure.description("Проверка, что права доступа корректно добавлены в базу данных.")
    def test_add_default_permissions(self, initializer_with_config, test_session):
        with allure.step("Инициализация базы данных"):
            initializer_with_config.initialize_db(test_session)

        with allure.step("Получение списка прав доступа из базы"):
            permissions = test_session.query(PermissionModel).all()

        with allure.step("Проверка количества прав доступа"):
            assert len(permissions) == 4, f"Ожидалось 4 права, получено: {len(permissions)}"

        with allure.step("Проверка имен прав доступа"):
            expected_permissions = {"read", "write", "delete", "update"}
            actual_permissions = {perm.name for perm in permissions}
            assert actual_permissions == expected_permissions, "Права доступа не совпадают с ожидаемыми."

    @allure.title("Тест добавления ролей и привязки прав")
    @allure.description("Проверка, что роли и их права корректно добавлены в базу данных.")
    def test_add_default_roles(self, initializer_with_config, test_session):
        with allure.step("Инициализация базы данных"):
            initializer_with_config.initialize_db(test_session)

        with allure.step("Получение списка ролей из базы"):
            roles = test_session.query(RoleModel).all()

        with allure.step("Проверка количества ролей"):
            assert len(roles) == 2, f"Ожидалось 2 роли, получено: {len(roles)}"

        with allure.step("Получение роли Root из базы"):
            root_role = test_session.query(RoleModel).filter_by(role_name="Root").first()
            assert root_role is not None, "Роль Root не найдена."

        with allure.step("Проверка привязанных прав для роли Root"):
            expected_root_permissions = {"read", "write", "delete"}
            actual_root_permissions = {perm.name for perm in root_role.permissions}
            assert (
                actual_root_permissions == expected_root_permissions
            ), "Права доступа для роли Root не совпадают с ожидаемыми."

        with allure.step("Получение роли Admin из базы"):
            admin_role = test_session.query(RoleModel).filter_by(role_name="Admin").first()
            assert admin_role is not None, "Роль Admin не найдена."

        with allure.step("Проверка привязанных прав для роли Admin"):
            expected_admin_permissions = {"read", "write", "update"}
            actual_admin_permissions = {perm.name for perm in admin_role.permissions}
            assert (
                actual_admin_permissions == expected_admin_permissions
            ), "Права доступа для роли Admin не совпадают с ожидаемыми."

    @allure.title("Тест добавления пользователей и привязки к ролям")
    @allure.description("Проверка, что пользователи и их роли корректно добавлены в базу данных.")
    def test_add_default_users(self, initializer_with_config, test_session):
        with allure.step("Инициализация базы данных"):
            initializer_with_config.initialize_db(test_session)

        with allure.step("Получение списка пользователей из базы"):
            users = test_session.query(UserModel).all()

        with allure.step("Проверка количества пользователей"):
            assert len(users) == 2, f"Ожидалось 2 пользователя, получено: {len(users)}"

        with allure.step("Получение пользователя root из базы"):
            root_user = test_session.query(UserModel).filter_by(login="root").first()
            assert root_user is not None, "Пользователь root не найден."

        with allure.step("Проверка роли пользователя root"):
            assert root_user.role.role_name == "Root", f"У пользователя root неверная роль: {root_user.role.role_name}."

        with allure.step("Получение пользователя admin из базы"):
            admin_user = test_session.query(UserModel).filter_by(login="admin").first()
            assert admin_user is not None, "Пользователь admin не найден."

        with allure.step("Проверка роли пользователя admin"):
            assert (
                admin_user.role.role_name == "Admin"
            ), f"У пользователя admin неверная роль: {admin_user.role.role_name}."
