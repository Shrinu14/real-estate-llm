# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies (for netcat and curl)
RUN apt-get update \
    && apt-get install -y netcat-openbsd curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure wait script is executable
RUN chmod +x /app/wait-for-services.sh

# Tell Render which port to expose
EXPOSE 8000  # ✅ Use 8000, as Render expects your app to bind here

# Use $PORT env var from Render or default to 8000
CMD ["./wait-for-services.sh", "uvicorn", "cli_main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
