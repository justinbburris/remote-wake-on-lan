FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Add build argument for requirements file
ARG REQUIREMENTS=requirements.txt

# Copy requirements files
COPY requirements.txt .
COPY requirements-dev.txt .

# Install dependencies
RUN pip install --no-cache-dir -r $REQUIREMENTS

# Copy application code
COPY remote_wake_on_lan/ remote_wake_on_lan/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "remote_wake_on_lan.main:app", "--host", "0.0.0.0", "--port", "8000"]
