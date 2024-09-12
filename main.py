import logging
import os
from datetime import datetime
from fastapi import FastAPI
from celery import Celery
import search_api
from db_init import Base, engine
import app_config
import subprocess

# Create the database schema
Base.metadata.create_all(engine)

# Configure logging
logging.basicConfig(level=app_config.settings.log_level)
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

# Create logs folder if it doesn't exist
logs_folder = 'logs'
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

# Set up logging to log to logs/logs_<date>.log
log_filename = os.path.join(logs_folder, f"logs_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(filename=log_filename, level=logging.INFO)

logging.info("Application started.")

# Initialize FastAPI app
logging.debug("Initializing FastAPI instance.")
app = FastAPI()
app.include_router(search_api.router)

# Initialize Celery app
celery_app = Celery('tasks', broker='redis://redis.flightstatsapiproject.orb.local:6379/0')

# Define a sample task
@celery_app.task
def sample_task():
    return "Sample task executed"

# Example of calling a task or running tests
if __name__ == "__main__":
    # Uncomment the line below to run tests instead of the sample task
    # run_tests()
    sample_task.apply_async()