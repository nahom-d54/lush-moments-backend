# ---- Builder Stage ----
# This stage installs dependencies and builds the application.
FROM python:3.12-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install build-time system dependencies and create a virtual environment
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies into the virtual environment
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

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

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code from the builder stage
WORKDIR /app
COPY --from=builder --chown=app:app /app /app

# Copy entrypoint script
COPY --chown=app:app docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Activate the virtual environment and switch to the non-root user
ENV PATH="/opt/venv/bin:$PATH"
USER app

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
