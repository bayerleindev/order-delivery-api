lint:
	ruff check --fix .
	black . --exclude 'migrations' --exclude '.venv'