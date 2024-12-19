# Stage 1: General enviroment
FROM python:3.12-slim-bookworm AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    S6_KILL_GRACETIME=0 \
    S6_OVERLAY_VERSION=3.1.6.2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_SYNC_DISKS=1

ENV PATH="$VENV_PATH/bin:$PATH"

# Stage 2: Install dependencies & build static files
FROM python-base as builder-base

# Install dependencies
WORKDIR $PYSETUP_PATH
COPY ./requirements.txt ./
RUN pip install --upgrade pip uv \
 && python -m uv venv $VENV_PATH && uv pip install -r requirements.txt

# Install s6-overlay
RUN apt-get update && apt-get install -y xz-utils --no-install-recommends
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN mkdir /s6-install
RUN tar -C /s6-install -Jxpf /tmp/s6-overlay-noarch.tar.xz \
 && tar -C /s6-install -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# Build static files
COPY . /app
WORKDIR /app
RUN python manage.py collectstatic --no-input --skip-checks --clear \
 && python manage.py compress

# Stage 3: Run service
FROM python-base as production

COPY --from=builder-base /s6-install /
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base /app/dotfm/staticfiles /app/dotfm/staticfiles
COPY deploy/etc/s6-overlay  /etc/s6-overlay
COPY dotfm /app/dotfm
COPY manage.py /app/manage.py
RUN rm -r /app/dotfm/static/

EXPOSE 8000
ENTRYPOINT ["/init"]
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://0.0.0.0:8000/health
