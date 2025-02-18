# Переменные
PYTHON := poetry run python
POETRY := poetry
RUN := poetry run

# Установка зависимостей
.PHONY: install
install:
	$(POETRY) install
