FROM python:3.12-slim

# Set environment variables for best practices
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create and set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a separate layer for caching
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install "SQLAlchemy>=2.0,<3.0" \
    && if grep -iFxv 'SQLAlchemy' requirements.txt > /tmp/req; then pip install -r /tmp/req; fi

# Copy the rest of the application code
COPY . .

# Use a non-root user for security best practice
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser /app
USER appuser

# Expose the port the app runs on (example: 8000)
EXPOSE 8000

# Define the default command, update as needed for the app
CMD ["python", "app.py"]