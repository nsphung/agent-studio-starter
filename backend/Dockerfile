FROM python:3.13-slim-trixie AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml /tmp/pyproject.toml

RUN apt-get update \
    && apt-get install -y build-essential --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r /tmp/pyproject.toml --index-strategy unsafe-best-match

FROM python:3.13-slim-trixie AS backend

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV VIRTUAL_ENV=/opt/venv
ENV PYTHONUSERBASE=$VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV:$PATH

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

RUN useradd --no-log-init --create-home appuser --shell /bin/bash \
    && apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/appuser
USER appuser

COPY --chown=appuser src/ src/
COPY pyproject.toml ./pyproject.toml
RUN uv pip install -r pyproject.toml --index-strategy unsafe-best-match

ENTRYPOINT ["uv", "run", "src/agent/main.py"]