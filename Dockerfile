# Dockerfile
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY controller/. /app/

# Install the required Python packages
RUN pip install kubernetes

# Set the entrypoint for the container
ENTRYPOINT ["python", "main.py"]