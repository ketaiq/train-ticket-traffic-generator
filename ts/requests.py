import uuid
import logging
import datetime

from random import randint
def random_date_generator():
    temp = randint(0, 4)
    random_y = 2000 + temp * 10 + randint(0, 9)
    random_m = randint(1, 12)
    random_d = randint(1, 28)  # to have only reasonable dates
    return str(random_y) + "-" + str(random_m) + "-" + str(random_d)

class IndependentRequests:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

    def visit_home(self):
        self.client.get("/index.html", name="visit home")
        logging.info(
            f"user {self.request_id} visits the home page of train ticket system by running GET /index.html"
        )

    def _search_ticket(self, departure_date, from_station, to_station):
        head = {"Accept": "application/json", "Content-Type": "application/json"}
        json = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date,
        }
        with self.client.post(
            url="/api/v1/travelservice/trips/left",
            headers=head,
            json=json,
            catch_response=True,
            name="search ticket",
        ) as response:
            if response.json()["msg"] != "Success":
                response.failure("Got wrong response")
                logging.error("Got wrong response!")
            elif response.elapsed.total_seconds() > 10:
                response.failure("Request took too long")
                logging.warning("Request took too long!")
        logging.info(
            f"user {self.request_id} searches train tickets from {from_station} to {to_station} on {departure_date} by running POST /api/v1/travelservice/trips/left"
        )

    def search_departure(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        self._search_ticket(now, "Shang Hai", "Su Zhou")

    def search_return(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        self._search_ticket(now, "Su Zhou", "Shang Hai")
