import unittest
from datetime import datetime, timedelta
from app.data_manager import DataManager
from app.flight_data import FlightData
from app.custom_exceptions import IataNotFound


class TestFlightData(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()

    def test_set_origin(self):
        self.data_manager.set_origin('London')
        self.assertEqual('London', self.data_manager.origin['city'])

    def test_set_destinations(self):
        self.data_manager.set_destinations('Berlin, Paris, ZZZZZZZZZZ')
        self.assertIn('Berlin', self.data_manager.destinations)

    def test_valid_iata_search(self):
        iata = self.data_manager.find_iata_codes('London')
        self.assertEqual(iata, 'LON')

    def test_invalid_iata_search(self):
        self.assertRaises(
            IataNotFound, self.data_manager.find_iata_codes, 'ZZZZZZZZZZ',
        )

    def test_valid_flight_search(self):
        self.data_manager.set_origin('London')
        self.data_manager.set_destinations('Berlin, Paris, ZZZZZZZZZZ')
        self.data_manager.check_flights(
            from_time=(datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y"),
            to_time=(datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y"),
            stop_overs=0,
            nights_in_dst_from=7,
            nights_in_dst_to=14,
        )
        self.assertIsInstance(
            self.data_manager.destinations['Berlin']['flight'], FlightData
        )

    def test_invalid_flight_search(self):
        self.data_manager.set_origin('London')
        self.data_manager.set_destinations('ZZZZZZZZZZ')
        self.assertIsNone(self.data_manager.check_flights(
            from_time=(datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y"),
            to_time=(datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y"),
            stop_overs=0,
            nights_in_dst_from=7,
            nights_in_dst_to=14,)
        )


if __name__ == '__main__':
    unittest.main()
