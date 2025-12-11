# Use slim python image
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies for Pillow / skimage
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Cloud Run requires listening on $PORT
ENV PORT=8080

# Start FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
