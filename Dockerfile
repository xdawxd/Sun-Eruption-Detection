FROM ubuntu:latest as base
RUN apt update && apt upgrade -y \
    && apt install -y python3 wget \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM base as poetry
RUN wget -O - https://install.python-poetry.org | python3 - --version 1.5.1
ENV PATH=/root/.local/bin:$PATH \
    POETRY_VIRTUALENVS_IN_PROJECT=true
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root --without dev --sync --no-ansi --no-interaction

FROM base as runtime
ENV PATH=/app/.venv/bin:$PATH
COPY --from=poetry /app/.venv /app/.venv
COPY ./sun_eruption_detection ./sun_eruption_detection/
CMD ["python3", "-m", "sun_eruption_detection"]