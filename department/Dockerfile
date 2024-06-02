# Dockerfile
FROM python:3.10

# Set environment variable to ensure Python output is not buffered
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/
