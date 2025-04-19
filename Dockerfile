FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Secure media storage
RUN mkdir -p /app/media && chmod 700 /app/media
ENV MEDIA_PATH=/app/media

# Non-root user
RUN useradd -m defender
USER defender

COPY --chown=defender . /app
