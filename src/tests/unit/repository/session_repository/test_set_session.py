from src.app.repository.repo_session import RepositoryFlaskSessionManager


def test_set_method(fake_session):
    """
    Проверяет, что метод set сохраняет значение в session.
    """
    manager = RepositoryFlaskSessionManager()
    manager.set("test_key", "test_value")
    assert fake_session.get("test_key") == "test_value"
