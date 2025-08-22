# =================================================================
# Stage 1: Builder - Install dependencies
# =================================================================
FROM python:3.10-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy files needed for installation
COPY requirements.txt setup.py README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# =================================================================
# Stage 2: Final Image - Create the production image
# =================================================================
FROM python:3.10-slim AS final

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app
USER app

# --- THIS IS THE CRITICAL FIX ---
# Copy the installed packages from the builder stage's site-packages
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy the application source code
COPY . .

# Expose the port
EXPOSE 5000

# Run the app using Flask's built-in server
CMD ["python", "app.py"]