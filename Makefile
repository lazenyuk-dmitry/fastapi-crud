dev:
	uv run fastapi dev

makemigrations:
	uv run alembic revision --autogenerate

migrate:
	uv run alembic upgrade head
