.PHONY: run
run:
	uvicorn app.main:app --reload

.PHONY: migrations
migrations:
	alembic revision --autogenerate -m "Initial migration"

.PHONY: update
update:
	alembic upgrade head

.PHONY: lint-fix
lint-fix:
	uv run ruff check --fix .

.PHONY: lint
lint:
	uv run ruff check .
