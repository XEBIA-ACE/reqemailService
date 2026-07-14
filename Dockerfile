FROM ubuntu:24.04

# Set a working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install common utilities for test suites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        git \
        curl \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Optional: Install Python test tools if requirements.txt exists
COPY requirements.txt ./
RUN if [ -f requirements.txt ]; then pip3 install --no-cache-dir -r requirements.txt; fi

# Default command (override as needed)
CMD ["bash"]