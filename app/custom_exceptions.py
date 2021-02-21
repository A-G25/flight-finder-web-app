class IataNotFound(Exception):
    def __init__(self, city):
        self.city = city

    def __str__(self):
        return f"No IATA code was found for the input city: '{self.city}'"

class FlightNotFound(Exception):
    def __init__(self, city_origin, city_destination):
        self.city_origin = city_origin
        self.city_destination = city_destination

    def __str__(self):
        return f"No flight was found for the input cities: '{self.city}'"

