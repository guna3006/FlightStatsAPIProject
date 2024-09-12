from fastapi import APIRouter, Query
from flightstats import get_flights_info

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
                description="airline_code",
                examples="SQ",
            ),
            airline_number: str = Query(
                description="airline_number",
                examples="105"
            ),
            departure_date: str = Query(
                description="departure_date",
                examples="2024-09-11"
            )
        ):
            return await get_flights_info(airline_code, airline_number, departure_date)

# Create an instance of the API class to expose the router
flight_search_api = FlightSearchAPI()
router = flight_search_api.router
