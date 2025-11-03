# Use Python 3.11 slim base image for smaller Docker image size
FROM python:3.11-slim

# Set environment variables to optimize Python in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \    # Prevent Python from writing .pyc files
    PYTHONUNBUFFERED=1 \            # Don't buffer Python output (see logs immediately)
    DEBIAN_FRONTEND=noninteractive  # Use non-interactive mode for package installation

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for PostGIS and GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \    # PostgreSQL client for database connections
    binutils \             # Binary utilities
    libproj-dev \          # Cartographic projection library
    gdal-bin \             # GDAL command-line tools
    libgdal-dev \          # GDAL development libraries
    python3-gdal \         # Python GDAL bindings
    gettext \              # Translation library
    && rm -rf /var/lib/apt/lists/*  # Clean up package cache to reduce image size

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Collect all static files into one directory for production serving
RUN python manage.py collectstatic --noinput || true

# Expose port 8000 so it can be accessed from outside the container
EXPOSE 8000

# Run Gunicorn (Python WSGI HTTP server) to serve the Django application
CMD ["gunicorn", "lbs_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]