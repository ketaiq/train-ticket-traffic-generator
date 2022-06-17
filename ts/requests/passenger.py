import random
import uuid
from ts.services.travel_service import search_ticket
from ts.services.visit_page import visit_client_login, visit_home
from ts.services.admin_route_service import EUROPEAN_ROUTES
from ts.services.station_service import EUROPEAN_STATIONS
from ts.util import gen_random_date


class PassengerRequest:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

    def visit_without_login(self, page: str):
        if page == "home":
            visit_home(self.client, self.request_id)
        elif page == "client login":
            visit_client_login(self.client, self.request_id)

    def search_departure_and_return(self):
        departure_int = random.randint(90000, 100000)
        return_int = random.randint(200000, 20000000)
        departure_time = gen_random_date(departure_int)
        return_time = gen_random_date(return_int)
        stations = self._pick_two_random_stations_in_one_route()
        search_ticket(
            self.client, departure_time, stations[0], stations[1], self.request_id
        )
        search_ticket(
            self.client, return_time, stations[1], stations[0], self.request_id
        )

    def _pick_two_random_stations_in_one_route(self) -> list:
        results = []
        picked_route = random.choice(EUROPEAN_ROUTES)
        picked_stations = random.sample(picked_route["stations"], k=2)
        for picked_station in picked_stations:
            for station in EUROPEAN_STATIONS:
                if station["id"] == picked_station:
                    results.append(station["name"])
                    break
        return results
