# Use the official Python base image from Docker Hub
FROM python:3.11.3-slim


# Set the working directory in the container
WORKDIR /code


# Install Python dependencies
RUN pip install --no-cache-dir redis flask_caching Flask requests

# Copy the application code into the container
COPY . .

# Command to run the Flask application
CMD python main.py
