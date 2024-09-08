import logging
import app_config
from fastapi import FastAPI
from routers import resources
from db_init import Base, engine

# create the database schema
Base.metadata.create_all(engine)

# remove existing log handlers if any and instantiate logging config
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(level=app_config.settings.log_level)

# create the application and config
logging.debug("Initializing FastAPI instance.")
app_wrapper = FastAPI()
app = FastAPI(title="Cargobase Technical Assessment",
              description="Web Scraping Flight Information Data",
              version="0.0.1")

# include routers for the app

app.include_router(resources.router)

from celery import Celery

# Initialize Celery app
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# Define a sample task
@celery_app.task
def sample_task():
    return "Sample task executed"

# Example of calling a task
if __name__ == "__main__":
    sample_task.apply_async()


import logging
import os
from datetime import datetime

# Create logs folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to log to logs/logs_<date>.log
log_filename = f"logs/logs_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO)

logging.info("Application started.")
