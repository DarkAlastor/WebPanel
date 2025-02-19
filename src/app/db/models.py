from datetime import datetime, timezone
from typing import List

from sqlalchemy import TIMESTAMP, VARCHAR, ForeignKey, String
from sqlalchemy.orm import (Mapped, as_declarative, declared_attr,
                            mapped_column, relationship)


@as_declarative()
class AbstractModel:
    """Базовый класс для всех моделей базы данных, предоставляет автогенерацию имени таблицы."""

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        """Генерирует имя таблицы на основе имени класса (в нижнем регистре)."""
        return cls.__name__.lower()


class UserModel(AbstractModel):
    """Модель пользователя, включает данные для авторизации и связку с сотрудником и ролью."""

    __tablename__ = "users"  # type: ignore

    login: Mapped[str] = mapped_column(VARCHAR(length=150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(length=200), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey(column="role.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    role: Mapped["RoleModel"] = relationship("RoleModel", back_populates="users", uselist=False)


class RoleModel(AbstractModel):
    """Модель роли, используется для группировки прав доступа."""

    __tablename__ = "role"  # type: ignore

    role_name: Mapped[str] = mapped_column(VARCHAR(length=100), nullable=False)
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    users: Mapped["UserModel"] = relationship("UserModel", back_populates="role")

    # Связь с RolePermissionModel
    role_permissions: Mapped[List["RolePermissionModel"]] = relationship(
        "RolePermissionModel",
        back_populates="role",
        cascade="all, delete-orphan",
        overlaps="permissions",
    )

    permissions: Mapped[List["PermissionModel"]] = relationship(
        "PermissionModel",
        secondary="role_permission",
        back_populates="roles",
        viewonly=True,  # Только для чтения
    )


class PermissionModel(AbstractModel):
    """Модель прав доступа, описывает, что разрешено."""

    __tablename__ = "permission"  # type: ignore

    name: Mapped[str] = mapped_column(VARCHAR(length=200), nullable=False)
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Связь с RolePermissionModel
    role_permissions: Mapped[List["RolePermissionModel"]] = relationship(
        "RolePermissionModel",
        back_populates="permission",
        cascade="all, delete-orphan",
        overlaps="roles",
    )

    roles: Mapped[List["RoleModel"]] = relationship(
        "RoleModel",
        secondary="role_permission",
        back_populates="permissions",
        viewonly=True,
    )


class RolePermissionModel(AbstractModel):
    """Промежуточная таблица для связи ролей и прав."""

    __tablename__ = "role_permission"  # type: ignore

    role_id: Mapped[int] = mapped_column(ForeignKey(column="role.id"), nullable=False)
    permission_id: Mapped[int] = mapped_column(ForeignKey(column="permission.id"), nullable=False)
    granted_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))

    role: Mapped["RoleModel"] = relationship("RoleModel", back_populates="role_permissions", overlaps="permissions")

    permission: Mapped["PermissionModel"] = relationship(
        "PermissionModel", back_populates="role_permissions", overlaps="roles"
    )
