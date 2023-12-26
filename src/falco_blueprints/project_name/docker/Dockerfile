# Stage 1: General enviroment
FROM python:3.12-slim-bookworm AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    TAILWIND_CLI_PATH="/opt/tailwind"

# ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Stage 2: Install dependencies & build static files
FROM python-base as builder-base

# Install poetry
# RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
# RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies required for psycopg
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
WORKDIR $PYSETUP_PATH
COPY ./requirements.txt ./pyproject.toml ./
RUN python -m venv $VENV_PATH && \
    pip install -r requirements.txt

# Build static files
COPY . /app
WORKDIR /app
RUN python manage.py tailwind build
RUN python manage.py collectstatic --no-input

# Stage 3: Run service
FROM python-base as production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base /app/staticfiles /app/staticfiles
COPY . /app

WORKDIR /app
EXPOSE 8000
CMD ["./docker/entrypoint.sh"]
