FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd 


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy app code and set ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["sh", "/app/entrypoint.sh"]
