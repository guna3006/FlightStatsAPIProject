# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in package.py (runs requirements.txt installation)
RUN python package.py

# Install Celery and Redis explicitly
RUN pip install celery redis

# Expose the port on which the FastAPI app runs
EXPOSE 8000

# Expose the Redis port (optional, for Redis interaction)
EXPOSE 6379

# Default command to run Celery worker and Uvicorn server (can be overridden by docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
