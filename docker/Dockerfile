# ====== ЭТАП 1: РАЗРАБОТКА (DEV) ======
FROM python:3.10-slim AS dev
LABEL authors="darkalastor"

# Устанавливаем зависимости для компиляции (например, gcc для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev netcat-openbsd make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Настраиваем рабочую директорию
WORKDIR /app

RUN mkdir -p /app/logs && chown -R 1000:1000 /app/logs

# Копируем только файлы Poetry для установки зависимостей (используется кэширование)
COPY ../pyproject.toml poetry.lock ./
COPY ../README.md ./

# Устанавливаем только основные зависимости (без dev)
RUN poetry config virtualenvs.create false && poetry install --no-root --only main --no-interaction --no-ansi

# Копируем структуру проекта
# специальный Makefile для докера
COPY ./Makefile ./
# специальный shell для докера
COPY ./shell ./shell
# копируем исходники
COPY ../src ./src
# копируем конфиг
COPY ../config ./config
# специальный shell для докера allure
COPY ../shell ./shell
# копируем миграции
COPY ../migrations ./migrations

# Устанавливаем все зависимости (включая dev)
RUN poetry config virtualenvs.create false && poetry install --no-root --all-extras --no-interaction --no-ansi

# Указываем переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем Gunicorn (dev-версия) через shell скрипт
CMD ["/app/shell/start.sh"]