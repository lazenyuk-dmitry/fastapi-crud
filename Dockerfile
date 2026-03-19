FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

COPY . .

ENTRYPOINT ["./entrypoint.sh"]

CMD ["uv", "run", "fastapi", "run"]
