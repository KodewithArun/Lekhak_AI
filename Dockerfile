# ============================================================
# Lekhak AI - Production Dockerfile
# Multi-stage build for optimized image size and security
# ============================================================

# ------------------------------
# Stage 1: Builder
# ------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Prevent Python from writing bytecode and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency file
COPY pyproject.toml ./

# Install dependencies into virtual environment
RUN pip install --upgrade pip && \
    pip install . && \
    pip install uvicorn[standard]

# ------------------------------
# Stage 2: Production
# ------------------------------
FROM python:3.12-slim AS production

# Labels for container metadata
LABEL maintainer="Lekhak AI Team" \
      version="1.0.0" \
      description="Lekhak AI Backend API"

# Create non-root user for security
RUN groupadd --gid 1000 lekhak && \
    useradd --uid 1000 --gid lekhak --shell /bin/bash --create-home lekhak

WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code with proper ownership
COPY --chown=lekhak:lekhak backend/ ./backend/

# Create logs directory with proper permissions
RUN mkdir -p /app/backend/logs && \
    chown -R lekhak:lekhak /app/backend/logs

# Switch to non-root user
USER lekhak

# Expose application port
EXPOSE 8000

# Set working directory for the application
WORKDIR /app/backend

# Health check - verify the API is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
