FROM python:3.11-slim

# Install Chrome and required dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -r -s /bin/bash scraper

# Set working directory
WORKDIR /app

# Create necessary directories and set permissions
RUN mkdir -p /app/data /app/logs \
    && chown -R scraper:scraper /app \
    && chmod -R 755 /app \
    && chmod 777 /app/logs  # Ensure logs directory is writable

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Change ownership of all files
RUN chown -R scraper:scraper /app

# Switch to non-root user
USER scraper

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DUMP_PATH=/app/data

# Health check
HEALTHCHECK --interval=1m --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import os; os.path.exists('/app/logs/app.log') and exit(0) or exit(1)"

# Run the application
CMD ["python", "-m", "app.main"]