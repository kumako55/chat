FROM python:3.10-slim

# Install system dependencies for pytchat and network
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install pytchat requests

# Copy application
COPY app.py /app.py

# Expose port (optional, for health checks)
EXPOSE 7860

# Run the application
CMD ["python", "/app.py"]
