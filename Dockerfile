# ---- Builder Stage ----
# This stage installs dependencies and builds the application.
FROM python:3.12-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install build-time system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files and install dependencies
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy application code
COPY . .


# ---- Final Stage ----
# This stage creates the final, lean production image.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install run-time system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN addgroup --system app && adduser --system --ingroup app app

# Copy uv from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application code from the builder stage
WORKDIR /app
COPY --from=builder --chown=app:app /app /app

# Create uploads directory
RUN mkdir -p uploads && chown -R app:app uploads

# Activate the virtual environment and switch to the non-root user
ENV PATH="/app/.venv/bin:$PATH"
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
