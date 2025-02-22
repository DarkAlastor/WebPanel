FLASK_MIGRATE = src.app.core.migrate.py

.PHONY: db-upgrade
db-upgrade:
	FLASK_APP=$(FLASK_MIGRATE) poetry run flask db upgrade

.PHONY: run
run:
	gunicorn -b 0.0.0.0:8000 src.app.run:app --reload