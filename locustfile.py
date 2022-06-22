import uuid
from requests.adapters import HTTPAdapter
import locust.stats
from locust import HttpUser, task, constant, events, between

from ts.requests.irregular_budget import IrregularBudgetRequest
from ts.requests.irregular_normal import IrregularNormalRequest
from ts.requests.irregular_comfort import IrregularComfortRequest
from ts.requests.regular import RegularRequest
from ts.requests.cancel_without_refund import CancelWithoutRefundRequest
from ts.requests.cancel_with_refund import CancelWithRefundRequest

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


class Passenger(HttpUser):
    weight = 1
    wait_time = between(2 * 60 * 60, 24 * 60 * 60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))
        self.irregular_budget_request = IrregularBudgetRequest(
            self.client, "Irregular Budget"
        )
        self.irregular_normal_request = IrregularNormalRequest(
            self.client, "Irregular Normal"
        )
        self.irregular_comfort_request = IrregularComfortRequest(
            self.client, "Irregular Comfort"
        )
        self.regular_request = RegularRequest(self.client, "Regular")
        self.cancel_without_refund_request = CancelWithoutRefundRequest(
            self.client, "Cancel Without Refund"
        )
        self.cancel_with_refund_request = CancelWithRefundRequest(
            self.client, "Cancel With Refund"
        )

    @task(12)
    def irregular_budget(self):
        self.irregular_budget_request.perform_actions()

    @task(10)
    def irregular_normal(self):
        self.irregular_normal_request.perform_actions()

    @task(2)
    def irregular_comfort(self):
        self.irregular_comfort_request.perform_actions()

    @task(24)
    def regular(self):
        self.regular_request.perform_actions()

    @task(1)
    def cancel_without_refund(self):
        self.cancel_without_refund_request.perform_actions()

    @task(1)
    def cancel_with_refund(self):
        self.cancel_with_refund_request.perform_actions()


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
