# https://docs.astral.sh/uv/guides/integration/fastapi/#deployment

FROM python:slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /pyprize
WORKDIR /pyprize

RUN uv sync --frozen --no-cache

CMD ["/pyprize/.venv/bin/flask", "--app", "pyprize", "run", "--debug", "--host", "0.0.0.0"]
