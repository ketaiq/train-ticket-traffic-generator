import logging
import uuid
from requests.adapters import HTTPAdapter
import locust.stats
from locust import HttpUser, task, constant, events

from ts.ts_requests import TrainTicketRequest
from ts.requests.passenger import PassengerRequest
from ts.requests.rail_traffic_controller import RailTrafficControllerRequest

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 30
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 10
locust.stats.PERCENTILES_TO_REPORT = [
    0.25,
    0.50,
    0.75,
    0.80,
    0.90,
    0.95,
    0.98,
    0.99,
    0.999,
    0.9999,
    1.0,
]


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    from ts.services.admin_route_service import init_european_routes
    from ts.services.station_service import init_european_stations
    from ts.services.auth_service import login_user_request

    print("Fetch shared data, including routes, stations")
    request_id = str(uuid.uuid4())
    admin_bearer, admin_user_id = login_user_request(
        username="admin", password="222222", request_id=request_id
    )
    init_european_routes(admin_bearer, request_id)
    init_european_stations(admin_user_id, admin_bearer)


class PassengerWithoutLogin(HttpUser):
    weight = 1
    wait_time = constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))
        self.request = PassengerRequest(self.client)
        logging.debug(
            f"""Running user "no login" with id {self.request.request_id}..."""
        )

    @task(1)
    def visit_home(self):
        self.request.visit_without_login("home")

    @task(1)
    def visit_home(self):
        self.request.visit_without_login("client login")

    @task(5)
    def perfom_task(self):
        self.request.search_departure_and_return()


# class UserLogin(HttpUser):
#     weight = 1
#     wait_time = constant(1)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

#     @task
#     def perform_task(self):
#         ts_request = TrainTicketRequest(self.client)
#         logging.debug(f"""Running user "login" with id {ts_request.request_id}...""")

#         ts_request.create_and_login_user()
#         ts_request.book()
#         ts_request.cancel_last_order_with_no_refund()
#         ts_request.get_voucher_of_last_order()
#         ts_request.consign_ticket()
#         ts_request.get_travel_plans()
#         ts_request.update_contact()


# class RailTrafficController(HttpUser):
#     wait_time = constant(1)
#     weight = 1

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))
#         self.request = RailTrafficControllerRequest(self.client)
#         logging.debug(
#             f"""Running "RailTrafficController" with id {self.request.request_id}..."""
#         )

#     @task(3)
#     def add_station(self):
#         self.request.add_one_station()

#     @task(6)
#     def update_station(self):
#         self.request.update_one_station()

#     @task(1)
#     def delete_station(self):
#         self.request.delete_one_station()

#     @task(3)
#     def add_route(self):
#         self.request.add_one_route()

#     @task(6)
#     def update_route(self):
#         self.request.update_one_route()

#     @task(1)
#     def delete_route(self):
#         self.request.delete_one_route()
