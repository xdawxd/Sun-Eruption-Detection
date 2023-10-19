# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONUNBUFFERED=true \
    PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY ./pyproject.toml ./poetry.lock ./README.md ./
RUN poetry install --no-root --without dev --sync --no-ansi --no-interaction

COPY ./sun_eruption_detection ./sun_eruption_detection/
CMD ["python3", "-m", "sun_eruption_detection"]
