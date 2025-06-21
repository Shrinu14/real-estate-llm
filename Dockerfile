# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies (for netcat in wait script)
RUN apt-get update \
    && apt-get install -y netcat-openbsd curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure wait script is executable (inside the /app dir)
RUN chmod +x /app/wait-for-services.sh

# Set default command (will be overridden by docker-compose anyway)
CMD ["./wait-for-services.sh", "uvicorn", "cli_main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
