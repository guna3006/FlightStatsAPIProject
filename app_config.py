from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    log_level: str
    flightstats_base_url: str

settings = Settings(log_level=os.getenv("LOGLEVEL", "DEBUG"),
                    flightstats_base_url=os.getenv("FLIGHTSTATS_BASE_URL","https://www.flightstats.com/v2/flight-tracker/"))