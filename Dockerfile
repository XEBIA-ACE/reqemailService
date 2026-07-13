FROM alpine:latest

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install runtime dependencies (placeholder; update as needed for your stack)
RUN apk add --no-cache bash

# Expose port (optional; update/remove as needed)
EXPOSE 8080

# Set entrypoint or command (update as appropriate for your application)
CMD ["sh"]