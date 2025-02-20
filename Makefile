# Переменные
PYTHON := poetry run python
POETRY := poetry
RUN := poetry run
FLASK_MIGRATE = src.app.core.migrate.py


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

.PHONY: unit-tests
unit-tests:
	$(RUN) pytest -v --tb=long --capture=no src/tests/unit/

.PHONY: e2e-tests
e2e-tests:
	$(RUN) pytest -v --tb=long --capture=no src/tests/e2e/

.PHONY: integ-tests
integ-tests:
	$(RUN) pytest -v --tb=long --capture=no src/tests/integ/

.PHONY: blueprints-tests
blueprints-tests:
	$(RUN) pytest -v --tb=long --capture=no src/tests/blueprint/

# ________________БЛОК КОМАНД ДЛЯ МИГРАЦИЙ________________
.PHONY: db-init
db-init:
	FLASK_APP=$(FLASK_MIGRATE) poetry run flask db init

.PHONY: db-migrate
db-migrate:
	FLASK_APP=$(FLASK_MIGRATE) poetry run flask db migrate -m "Auto migration"

.PHONY: db-migrate-empty
db-migrate-empty:
	FLASK_APP=$(FLASK_MIGRATE) poetry run flask db revision -m "Initial empty migration"

.PHONY: db-upgrade
db-upgrade:
	FLASK_APP=$(FLASK_MIGRATE) poetry run flask db upgrade

# ________________БЛОК КОМАНД ДЛЯ СБОРКИ КОНТЕНЕРОВ________________
.PHONY: build-dev
build-dev:
	$(RUN) docker build --target dev -t flask-web-panel:dev .