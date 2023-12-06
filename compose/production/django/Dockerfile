# Python build stage
FROM python:3.11.7-slim-bullseye as python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install dependencies for building Python packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

# Create Python Dependency and Sub-Dependency Wheels.
COPY ./requirements .
RUN pip wheel --wheel-dir /wheels -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage
FROM python:3.11.7-slim-bullseye as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="$APP_HOME:$PATH"

WORKDIR ${APP_HOME}

# Create user and group
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy python dependency wheels from python-build-stage and install
COPY --from=python-build-stage /wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy entrypoint and start scripts
COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
COPY --chown=django:django ./compose/production/django/start /start
RUN chmod +x /entrypoint /start

# Copy application code
COPY --chown=django:django . ${APP_HOME}

# Run as non-root user
USER django

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
