lint:
	ruff check --fix .
	black . --exclude 'migrations' --exclude '.venv'

setup-local:
	docker compose up -d
	export FLASK_APP=app.py
	sleep 30
	flask db upgrade

run-local:
	flask run --port 5151

clean-local:
	docker compose down

test: setup-local test-run clean-local

test-run:
	pytest -rP tests/*

install:
	pip3 install -r requirements.txt