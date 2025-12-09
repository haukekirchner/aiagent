FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for ping
RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .

# Set environment variable for OpenAI API key (should be set at runtime)
ENV PYTHONUNBUFFERED=1

# Default to running the basic agent
CMD ["python", "agent.py"]




