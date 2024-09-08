
# FlightStats API Project

## Overview
This project provides a FastAPI-based application to search for flight information. It includes background task processing using Celery with Redis as the message broker, as well as structured logging.

## Requirements
- Python 3.9 or above
- Redis (running locally or remotely)
- Docker (optional, for containerized deployment)

## Installation

### Step 1: Clone the repository
```
git clone <repository_url>
cd cargobase-api-main
```

### Step 2: Install Dependencies
The dependencies for the project are managed in `requirements.txt`. To install the necessary packages, simply run:

```
python package.py
```

Ensure Redis is running on your local machine or is accessible remotely on `localhost:6379`.

### Step 3: Running the API
To start the FastAPI application:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 4: Running Celery Worker
To start the Celery worker to process background tasks:
```
celery -A main.celery_app worker --loglevel=info
```

## Using Docker (optional)
To build and run the application with Docker, use the following commands:
```
docker build -t flightstats-api .
docker run -p 8000:8000 flightstats-api
```

## API Usage
You can interact with the API using the provided Postman collection (`FlightStats_Postman_Collection.json`), which includes:
- **Search Flight**: `/api/search?airline_code=AK&airline_number=11&departure_date=2023-09-08`

## Logging
Logs are stored in the `logs/` directory, with filenames in the format `logs_<date>.log`.

## Database
The SQLite database is stored in the `db/` directory as `stats.db`.

## Background Tasks
Celery is used for background tasks. A sample task (`sample_task`) is available for demonstration purposes.

## License
This project is licensed under the MIT License.
