# ============================================================================
# Multi-Stage Dockerfile for Flask API
# Optimized for size, security, and performance
# ============================================================================

# ============================================================================
# STAGE 1: Builder
# Purpose: Install dependencies and compile wheels
# This stage is discarded in the final image
# ============================================================================
FROM python:3.11-alpine AS builder

# Set build arguments
ARG APP_VERSION=1.0.0

# Install build dependencies (removed in final image)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    openssl-dev

# Create virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements first (Docker layer caching optimization)
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# ============================================================================
# STAGE 2: Runtime
# Purpose: Minimal runtime environment with only necessary components
# This is the final image
# ============================================================================
FROM python:3.11-alpine

# Metadata labels
LABEL maintainer="Mahamadou DANSOKO <damahadansoko@gmail.com>"
LABEL version="1.0.0"
LABEL description="Optimized Flask API container"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOME=/app \
    ENVIRONMENT=production

# Install only runtime dependencies (minimal!)
RUN apk add --no-cache \
    libffi \
    openssl \
    ca-certificates \
    curl \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
# UID 1000 is standard for non-root users
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Create application directory
RUN mkdir -p ${APP_HOME} && \
    chown -R appuser:appuser ${APP_HOME}

# Set working directory
WORKDIR ${APP_HOME}

# Copy virtual environment from builder stage
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser app/ ${APP_HOME}/app/

# Create logs directory
RUN mkdir -p ${APP_HOME}/logs && \
    chown -R appuser:appuser ${APP_HOME}/logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
# Docker will automatically restart container if health check fails
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set entrypoint (PID 1 problem solution)
ENTRYPOINT ["python"]

# Default command - run with gunicorn for production
# Can be overridden in docker-compose or kubernetes
CMD ["-m", "gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app.api:app"]
# ============================================================================
# Build instructions:
# docker build -t optimized-flask-api:latest .
#
# Run instructions:
# docker run -d -p 5000:5000 --name flask-api optimized-flask-api:latest
#
# Expected final image size: < 80MB
# ============================================================================