# A lightweight Python image
FROM python:3.12-slim

# Set env variables to keep Python from buffering output --->
# This ensures that logs can be viewed in real-time in the terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working dir inside the container
WORKDIR /code

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code
COPY . /code/