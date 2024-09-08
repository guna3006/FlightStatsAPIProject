
from fastapi import APIRouter, Query
from dependencies.flightstats import get_flights_info

class FlightSearchAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api")
        self.setup_routes()

    def setup_routes(self):
        # Setup the route for fetching flight info
        @self.router.get(
            "/search",
            summary="query flight info",
            status_code=200,
        )
        async def search_flight(
            airline_code: str = Query(
                description="query string",
                example="AK",
            ),
            airline_number: str = Query(
                example="11"
            ),
            departure_date: str = Query(
                description="departure date",
                example="2023-09-08"
            )
        ):
            return await get_flights_info(airline_code, airline_number, departure_date)

# Create an instance of the API class to expose the router
flight_search_api = FlightSearchAPI()
router = flight_search_api.router
