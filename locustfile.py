import logging
from requests.adapters import HTTPAdapter
import locust.stats
from locust import HttpUser, task, constant

from ts.requests import IndependentRequests
import datetime

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


class UserNoLogin(HttpUser):
    weight = 50
    wait_time = constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

    @task
    def perfom_task(self):
        requests = IndependentRequests(self.client)
        logging.debug(f"""Running user "no login" with id {requests.request_id}...""")

        requests.visit_home()
        requests.search_departure()
        requests.search_return()


# class UserBooking(HttpUser):
#     weight = 50
#     wait_time = constant(1)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "no booking" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("login")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
