from src.app.repository.repo_session import RepositoryFlaskSessionManager


def test_get_existing_string(fake_session):
    """
    Проверяет, что метод get возвращает строковое значение, если оно присутствует.
    """
    fake_session["test_key"] = "test_value"
    manager = RepositoryFlaskSessionManager()
    result = manager.get("test_key")
    assert result == "test_value"


def test_get_non_string_returns_none(fake_session):
    """
    Проверяет, что метод get возвращает None, если значение не является строкой.
    """
    fake_session["test_key"] = 123  # не строковое значение
    manager = RepositoryFlaskSessionManager()
    result = manager.get("test_key")
    assert result is None


def test_get_missing_key_returns_none(fake_session):
    """
    Проверяет, что метод get возвращает None, если ключ отсутствует.
    """
    manager = RepositoryFlaskSessionManager()
    result = manager.get("nonexistent")
    assert result is None
