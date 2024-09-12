from bs4 import BeautifulSoup
import json

def scrape_essential_data(response):

    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find('script', string=lambda text: "__NEXT_DATA__" in text if text else False)
    if data:
        string_data = data.text
        start_text = "__NEXT_DATA__ = "
        end_text = ";__NEXT_LOADED_PAGES__="
        stripped = string_data.split(end_text, 1)[0].split(start_text,1)[1]
        json_object = json.loads(stripped)
        result = json_object["props"]["initialState"]["flightTracker"]["flight"]
        return result
    else:
        return None