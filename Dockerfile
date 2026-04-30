# ── Build stage ───────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir build \
    && python -m build --wheel --outdir /dist

# ── Runtime stage ─────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app
COPY --from=builder /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

RUN useradd --create-home appuser
USER appuser

ENTRYPOINT ["mars-rover"]
CMD ["--help"]