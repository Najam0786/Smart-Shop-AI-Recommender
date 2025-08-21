# =================================================================
# Stage 1: Builder - Install dependencies
# =================================================================
FROM python:3.10-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies needed for building some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy only the files needed to install dependencies
# This optimizes Docker's layer caching.
COPY requirements.txt setup.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# =================================================================
# Stage 2: Final Image - Create the production image
# =================================================================
FROM python:3.10-slim as final

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app
USER app

# Copy the installed virtual environment from the builder stage
COPY --from=builder /app /app

# Copy the rest of the application source code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using a production-ready server (gunicorn)
# Note: You'll need to add gunicorn to your requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]