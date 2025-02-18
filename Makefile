# Переменные
PYTHON := poetry run python
POETRY := poetry
RUN := poetry run

# Установка зависимостей
.PHONY: install
install:
	$(POETRY) install


# ________________БЛОК КОМАНД ДЛЯ ЗАПУСКА ЛИНТЕРОВ________________
.PHONY: formater
formater:
	$(PYTHON) -m black --line-length=120 .
	$(PYTHON) -m isort .

# Запуск линтеров
.PHONY: lint
lint:
	$(PYTHON) -m flake8 --max-line-length=120 src/

# Запуск проверки типов
.PHONY: typecheck
typecheck:
	$(PYTHON) -m mypy src/app/ \
		--strict \
		--exclude 'src/tests|src/app/core/|src/app/utils' \
		--follow-imports=skip \
		--explicit-package-bases \
		--disable-error-code=misc

# ________________БЛОК КОМАНД ДЛЯ ГЕНЕРАЦИИ ДОКУМЕНТАЦИИ________________
.PHONY: apidoc
apidoc:
	$(RUN) sphinx-apidoc -o docs/ src/app --force

.PHONY: docs
docs:
	$(RUN) sphinx-build -b html docs/ docs/_build/html

.PHONY: start-docs
start-docs:
	$(PYTHON) -m http.server 8000 --directory docs/_build/html


# ________________БЛОК КОМАНД ДЛЯ ТЕСТОВ________________
.PHONY: test-all
test-all:
	$(RUN) pytest -v --tb=long --capture=no src/tests/

.PHONY: test-unit
test-unit:
	$(RUN) pytest -v --tb=long --capture=no src/tests/unit/
