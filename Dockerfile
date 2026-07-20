# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install requirements, pinning Flask 3.0 and SQLAlchemy 2.x
RUN pip install --upgrade pip && \
    pip install --prefix=/install "Flask>=3.0,<4.0" "SQLAlchemy>=2.0,<3.0" -r requirements.txt

# Copy the rest of the app
COPY . .

FROM python:3.12-slim

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]