from fastapi import HTTPException
import requests
from datetime import datetime
from db_init import Flight, session
from scraper import scrape_essential_data
import app_config

async def get_flights_info(airline_code, airline_number, departure_date):

    # validate departure date format
    try:
        datetime.strptime(departure_date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(status_code=422, detail={
            "Error": "InvalidDateTimeFormat",
            "Description": "Invalid departure date format. Use YYYY-MM-DD",
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
                        "Description": "There is an error during data scraping. Flight information cannot be found."
                    })
            except Exception as e:
                raise HTTPException(status_code=422, detail={
                    "Error": "ScrapingError",
                    "Description": "There is an error during data scraping. Flight information cannot be found.",
                    "Details": str(e)
                })   
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=502, detail={
                    "Error": "HTTPConnectionError",
                    "Description": "There is an error connecting to the Flightstats website.",
                    "Details": str(e)
                })
        finally:
            # close session in case of error
            session.close()
    return result