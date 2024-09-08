from fastapi import HTTPException
import requests
from datetime import datetime
from models.flight import Flight
from db_init import session
from helpers.scraper import scrape_essential_data
from models import error_message
import app_config

async def get_flights_info(airline_code, airline_number, departure_date):

    # validate departure date format
    try:
        datetime.strptime(departure_date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(status_code=422, detail={
            "Error": "InvalidDateTimeFormat",
            "Description": error_message.InvalidDateTimeMessage,
            "Details": str(e)
        })
    
    # check existing records in db and if its final, if not fetch from web
    flight_from_db = session.query(Flight).filter_by(airline_code=airline_code, airline_number=airline_number, departure_date=departure_date).first()

    if flight_from_db:
        result = flight_from_db.flight_data
        session.close()
        return result
    else:
        # getting latest flight data from website
        try:
            flightstats_base_url = app_config.settings.flightstats_base_url
            full_url = flightstats_base_url + f"{airline_code}/{airline_number}"
            departure_datetime = datetime.strptime(departure_date, "%Y-%m-%d")
            url_params = {
                "year": departure_datetime.year,
                "month": departure_datetime.month,
                "day": departure_datetime.day
            }
            flight_data = requests.get(full_url, params=url_params, verify=False)

            try:
                # massage data for essential value
                result = scrape_essential_data(flight_data)
                
                if result:
                    if result["flightNote"]["final"] == True:
                        # insert only final essential flight data into db
                        flight = Flight(airline_code=airline_code, airline_number=airline_number, departure_date=departure_date, flight_data=result)
                        session.add(flight)
                        session.commit()
                        session.close()
                    else:
                        return result
                else:
                    raise HTTPException(status_code=422, detail={
                        "Error": "JSONError",
                        "Description": error_message.ScrapingErrorMessage
                    })
            except Exception as e:
                raise HTTPException(status_code=422, detail={
                    "Error": "ScrapingError",
                    "Description": error_message.ScrapingErrorMessage,
                    "Details": str(e)
                })   
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=502, detail={
                    "Error": "HTTPConnectionError",
                    "Description": error_message.HTTPConnectionErrorMessage,
                    "Details": str(e)
                })
        finally:
            # close session in case of error
            session.close()
    return result