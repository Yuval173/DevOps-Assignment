# Optimization: Using Alpine Linux to keep the image size under ~50MB.
FROM python:3.9-alpine

WORKDIR /app

# Install dependencies in a single layer and clear cache
RUN pip install --no-cache-dir requests

COPY test_script.py .

# Run the script
CMD ["python", "test_script.py"]