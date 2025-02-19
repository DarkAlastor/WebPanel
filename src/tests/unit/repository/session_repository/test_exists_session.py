from src.app.repository.repo_session import RepositoryFlaskSessionManager


def test_exists_method(fake_session):
    """
    Проверяет, что метод exists корректно определяет наличие ключа в session.
    """
    fake_session["present_key"] = "value"
    manager = RepositoryFlaskSessionManager()
    assert manager.exists("present_key") is True
    assert manager.exists("absent_key") is False
