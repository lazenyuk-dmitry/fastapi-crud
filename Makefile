dev:
	uv run fastapi dev

run:
	uv run fastapi run

makemigrations:
	uv run alembic revision --autogenerate

migrate:
	uv run alembic upgrade head
