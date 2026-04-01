# Stage 1: Build Vue frontend
FROM oven/bun:1 AS frontend-builder

WORKDIR /app/vue
COPY vue/package.json vue/bun.lock ./
RUN bun install --frozen-lockfile

COPY vue/ .
RUN bun run build-only


# Stage 2: Final image — Python backend + nginx + supervisor
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app/python
COPY python/pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy Python source
COPY python/ .

# Copy built Vue frontend
COPY --from=frontend-builder /app/vue/dist /app/static

# Copy nginx and supervisor config
COPY docker/nginx.conf /etc/nginx/sites-available/default
COPY docker/supervisord.conf /etc/supervisor/conf.d/app.conf

# nginx default site cleanup
RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]
