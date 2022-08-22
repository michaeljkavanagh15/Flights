import requests
import os

URL = "https://tequila-api.kiwi.com/"
GET = "locations/query"
SEARCH = "v2/search"
API_KEY = os.environ.get("API_KEY")
HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}


class FlightSearch:
    def __init__(self):
        self.codes = []
        self.params = {}
        self.search_data = None

    # Returns the IATA code for the inputted City
    def get_IATA(self, city):
        self.params["term"] = city
        IATA_response = requests.get(f"{URL}{GET}", params=self.params, headers=HEADERS)
        IATA_response.raise_for_status()
        IATA_data = IATA_response.json()
        IATA_code = IATA_data["locations"][0]["code"]
        return IATA_code

    # Gets flight information for next 6 months for inputted IATA code and returns flights
    def get_flights(self, from_code, to_code, today, future_date, nights_min, nights_max):
        params = {
            "fly_from": from_code,
            "fly_to": to_code,
            "date_from": today,
            "date_to": future_date,
            "flight_type": "round",
            "nights_in_dst_from": nights_min,
            "nights_in_dst_to": nights_max,
            "curr": "USD"
        }
        search_results = requests.get(f"{URL}{SEARCH}", params=params, headers=HEADERS)
        search_results.raise_for_status()
        self.search_data = search_results.json()
        return self.search_data["data"]

