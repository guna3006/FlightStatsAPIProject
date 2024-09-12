import json
from fastapi.testclient import TestClient
import pytest
from main import app
from scraper import scrape_essential_data
from unittest.mock import Mock
from flightstats import get_flights_info

client = TestClient(app)

def test_search_endpoint():

    response = client.get("/api/search?airline_code=SQ&airline_number=105&departure_date=2024-09-11")
    assert response.status_code == 200

def test_scrape_essential_data_success():
  
    mock_response = Mock()
    mock_response.text = """
    <html>
    <body>
        <script>__NEXT_DATA__ = {"props":{"initialState":{"flightTracker":{"flight": {"data": "essential flight data"}}}}}</script>
    </body>
    </html>
    """
    result = scrape_essential_data(mock_response)
    assert result == {"data": "essential flight data"}

def test_scrape_essential_data_invalid_json():

    mock_response = Mock()
    mock_response.text = """
    <html>
        <body>
        <script>__NEXT_DATA__ = {"props":{"initialState":{"flightTracker":{"flight": invalid_json}}}}</script>
        </body>
    </html>
    """
    with pytest.raises(json.JSONDecodeError):
        scrape_essential_data(mock_response)

def test_get_flights_info_success():

    result = get_flights_info("SQ", "105", "2024-09-11")
    assert result
