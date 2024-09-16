lint:
	ruff check --fix .
	black . --exclude 'migrations' --exclude '.venv'

setup-local:
	docker compose up -d
	export FLASK_APP=app.py
	flask db upgrade
	flask run --port 5151

test:
	pytest tests/*

install:
	pip3 install -r requirements.txt