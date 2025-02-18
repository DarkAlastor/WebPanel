import logging


class ServiceFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, "tags"):
            record.tags = {}
        record.tags["service_name"] = f"flask-app-service"
        return True


class UserFilter(logging.Filter):
    """Фильтр для добавления полей `username`, `role`, `action` в лог-записи."""

    def filter(self, record):
        if not hasattr(record, "tags"):
            record.tags = {}

        # Подставляем `Unknown`, если поля нет
        record.tags["username"] = getattr(record, "username", "Unknown")
        record.tags["role"] = getattr(record, "role", "Unknown")
        record.tags["action"] = getattr(record, "action", "Undefined")

        return True
