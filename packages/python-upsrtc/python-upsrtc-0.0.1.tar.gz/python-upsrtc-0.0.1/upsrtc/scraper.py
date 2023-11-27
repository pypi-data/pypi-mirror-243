from .session import ScraperSession
from .models.busStop import BusStop
from .models.ticket import Ticket
from datetime import datetime
from .errors import InvalidSearchSettingsError
from .errors import NoJourneyFoundError

class UPSRTC:

    BUS_STOPS_URL = "https://onlineupsrtc.co.in:8081/upsrtc/api/booking/v1/bus/backofficeinfo"
    SEATS_URL = "https://onlineupsrtc.co.in:8081/upsrtc/api/booking/v2/bus/seats"

    def __init__(self):
        self.session = ScraperSession()

    def get_bus_stops(self):
        response = self.session.get(self.BUS_STOPS_URL, verify = False) # Verify is set to false to avoid ssl certficate error.
        self.bus_stops = []
        for stop in response.json().get('busStops', []):
            self.bus_stops.append(BusStop(stop) )

    def get_journey_bus(self, payload):
        p = self.session.post(self.SEATS_URL, json = payload, verify = False)
        self._last_response = p
        return p.json()

    def validate_search_settings(self):
        if not self.start_station_code :
            raise InvalidSearchSettingsError("Start station code is required")
        if not self.end_station_code:
            raise InvalidSearchSettingsError("End station code is required")
        if not self.start_date:
            raise InvalidSearchSettingsError("Start date is required")
        
        
    def set_start_station(self, station_code):
        self.start_station_code = station_code
    def set_end_station(self, station_code):
        self.end_station_code = station_code
    def set_start_date(self, date : datetime):
        if not isinstance(date, datetime):
            raise TypeError("Date should be of type datetime instead it is of type {}".format(type(date)) )
        formatted_date = date.strftime('%Y%m%d%H%M%S')
        self.start_date = formatted_date

    def find_buses(self):
        self.validate_search_settings()
        payload = self._generate_payload_to_find_buses()
        self.journey = []
        tickets = self.get_journey_bus(payload).get('tickets', [])
        if not tickets:
            raise NoJourneyFoundError("No buses found for given search settings")
        for ticket in tickets:
            self.journey.append( Ticket(ticket) )

    def _generate_payload_to_find_buses(self):
        return {
            'busType': '0',
            'sourceStation': self.start_station_code,
            'destinationStation': self.end_station_code,
            'inboundTripDate': self.start_date,
            'outboundTripDate': None,
            'products': [
                    { "productCode": "1","passengerCount": 1},
                    {"productCode": "2","passengerCount": 0},
                    {"productCode": "3","passengerCount": 0}
                ],
            'qrType': 1,
            'scheduleId': None
        }