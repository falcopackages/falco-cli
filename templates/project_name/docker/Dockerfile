FROM python:3.11.0-bullseye as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

FROM python:3.11.0-alpine3.16

WORKDIR /code

RUN apk update \
    && apk add --virtual build-deps build-base \
    && apk add postgresql-client \
    && apk add --no-cache libffi-dev libpq-dev \
    && pip install --upgrade pip \
    && python --version

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 80

CMD ["sh", "/code/docker/entrypoint.sh"]
