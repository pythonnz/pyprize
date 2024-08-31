# https://docs.astral.sh/uv/guides/integration/fastapi/#deployment

FROM python:slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app
WORKDIR /app

RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
