class FlightData:

    def __init__(self, price, origin_city, origin_airport, destination_city,
                 destination_airport, outbound_date, inbound_date, flight_type,
                 country_from, country_to, booking_link, stop_overs=0, via_city=""):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.flight_type = flight_type
        self.country_from = country_from
        self.country_to = country_to
        self.stop_overs = stop_overs
        self.via_city = via_city
        self.booking_link = booking_link
