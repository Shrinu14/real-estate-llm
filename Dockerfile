# Assuming you use a Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .


# Make wait script executable
COPY wait-for-services.sh /wait-for-services.sh
RUN chmod +x /wait-for-services.sh

CMD ["/wait-for-services.sh", "uvicorn", "cli_main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]


# Default command is overridden in docker-compose
