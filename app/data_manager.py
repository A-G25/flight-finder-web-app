from app.flight_data import FlightData
from app.custom_exceptions import IataNotFound
import requests
import os

TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
TEQUILA_FLIGHT_SEARCH_ENDPOINT = 'https://tequila-api.kiwi.com/v2/search'
TEQUILA_LOCATIONS_ENDPOINT = 'http://tequila-api.kiwi.com/locations/query'
tequila_headers = {'apikey': TEQUILA_API_KEY}


class DataManager:

    def __init__(self):
        self.origin = {}
        self.destinations = {}
        self.trip_type = "oneway"

    def set_origin(self, departure_city):
        self.origin["city"] = departure_city
        try:
            self.origin["iata"] = self.find_iata_codes(departure_city)
        except IataNotFound:
            self.origin["iata"] = None

    def set_destinations(self, destination_cities):
        self.destinations = {city.strip().title(): {} for city in destination_cities.split(',')}
        for city in self.destinations:
            try:
                self.destinations[city]['iata'] = self.find_iata_codes(city)
            except IataNotFound:
                self.destinations[city]['iata'] = None

    @staticmethod
    def find_iata_codes(city):
        try:
            params = {"term": city}
            response = requests.get(
                url=TEQUILA_LOCATIONS_ENDPOINT,
                headers=tequila_headers,
                params=params
            )
            data = response.json()["locations"][0]
            return data["code"]
        except IndexError:
            raise IataNotFound(city)

    def check_flights(self, **kwargs):
        query = {
            "apikey": TEQUILA_API_KEY,
            "fly_from": self.origin["iata"],
            "date_from": kwargs["from_time"],
            "date_to": kwargs["to_time"],
            "curr": "GBP",
            "max_sector_stopovers": kwargs["stop_overs"],
            "one_for_city": 1,
            "nights_in_dst_from": kwargs["nights_in_dst_from"],
            "nights_in_dst_to": kwargs["nights_in_dst_to"]
        }

        for city in self.destinations:
            if self.destinations[city]["iata"]:
                query["fly_to"] = self.destinations[city]["iata"]
                response = requests.get(
                    url=TEQUILA_FLIGHT_SEARCH_ENDPOINT,
                    headers=tequila_headers,
                    params=query
                )
                try:
                    data = response.json()["data"][0]
                except (IndexError, KeyError):
                    self.destinations[city]["flight"] = None
                else:
                    if self.trip_type == "oneway":
                        stopovers = len(data["route"]) - 1
                    else:
                        stopovers = (len(data["route"]) - 2) / 2

                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["cityFrom"],
                        origin_airport=data["routes"][0][0],
                        destination_city=data["cityTo"],
                        destination_airport=data["routes"][0][1],
                        outbound_date=data["route"][0]["local_departure"].split("T")[0],
                        inbound_date=data["route"][-1]["local_departure"].split("T")[0],
                        country_from=data["countryFrom"]['code'],
                        country_to=data["countryTo"]['code'],
                        stop_overs=stopovers,
                        via_city=data["route"][0]["cityTo"],
                        booking_link=data["deep_link"],
                        flight_type=self.trip_type,
                    )
                    self.destinations[city]["flight"] = flight_data
