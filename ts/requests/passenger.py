import uuid
import requests
from datetime import datetime
from datetime import timedelta

from ts.services.assurance_service import AssuranceType
from ts.services.consign_service import Consign
from ts.services.contacts_service import add_one_contact, gen_random_contact
from ts.services.food_service import Food, search_food_on_trip, pick_random_food
from ts.services.preserve_service import SeatType
from ts.services.preserve_service import pick_random_seat_type
from ts.services.travel_plan_service import pick_random_strategy_and_search
from ts.services.travel_service import pick_random_travel, search_ticket

from ts.config import tt_host


def admin_orders_get_list(bearer: str):
    response = requests.get(
        url="{host}/api/v1/adminorderservice/adminorder".format(host=tt_host),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
    )

    orders_list = response.json()["data"]
    return orders_list


def admin_orders_get_list_by_user_id(bearer: str, account_id: str):
    total_orders_list = admin_orders_get_list(bearer)
    return list(filter(lambda item: item["accountId"] == account_id, total_orders_list))


class PassengerRequest:
    def __init__(self, client, description):
        self.host = tt_host

        self.client = client
        self.description = description

        self.admin_username = "admin"
        self.admin_password = "222222"
        self.admin_bearer = None
        self.admin_user_id = None

        self.username = None
        self.password = None
        self.bearer = None
        self.user_id = None

        self.request_id = str(uuid.uuid4())

        self.test_user_id = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"

        self.departure_date = str(datetime.now().date() + timedelta(days=1))
        self.from_station = "Shang Hai"
        self.to_station = "Su Zhou"

        self.trip = None
        self.seat_type = None
        self.seat_price = None
        self.contact_id = None
        self.assurance = None
        self.food = None
        self.consign = None
        self.order_id = None
        self.admin_bearer = None

    def tickets_search(self, number_of_smpl, number_of_adv):
        trips = []

        for _ in range(number_of_adv):
            trips = pick_random_strategy_and_search(
                self.client,
                self.request_id,
                self.from_station,
                self.to_station,
                self.departure_date,
            )

        for _ in range(number_of_smpl):
            trips = search_ticket(
                self.client,
                self.departure_date,
                self.from_station,
                self.to_station,
                self.request_id,
            )

        self.trip = pick_random_travel(trips)

    def gen_ticket_info(
        self, food_included=False, assurance_included=False, consign_included=False
    ):
        self.seat_type = pick_random_seat_type()
        self.seat_price = self.get_seat_price()
        self.contact_id = self.contact_create_add()

        self.food = Food()
        self.assurance = AssuranceType.NONE.value
        self.consign = Consign()

        if food_included:
            all_food = search_food_on_trip(
                self.client,
                self.bearer,
                self.user_id,
                self.departure_date,
                self.from_station,
                self.to_station,
                self.trip["tripId"],
            )
            if all_food is not None:
                self.food = pick_random_food(all_food)

        if assurance_included:
            self.get_assurance(self.bearer)

        if consign_included:
            self.get_consign(self.bearer, self.user_id)

    def contact_create_add(self) -> str:
        contact_object = gen_random_contact(None, self.user_id)
        contact = add_one_contact(
            self.client, self.bearer, self.user_id, contact_object
        )
        return contact["id"]

    def get_seat_price(self):
        if self.seat_type == SeatType.FIRST_CLASS.value:
            if "priceForFirstClassSeat" in self.trip:
                return self.trip["priceForFirstClassSeat"]
            else:
                return self.trip["priceForConfortClass"]
        else:
            if "priceForSecondClassSeat" in self.trip:
                return self.trip["priceForSecondClassSeat"]
            else:
                return self.trip["priceForEconomyClass"]

    def get_consign(self, user_token: str, user_id: str):
        with self.client.get(
            url="/api/v1/consignservice/consigns/account/{user_id}".format(
                user_id=user_id
            ),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": user_token,
            },
            name="get_consign",
            catch_response=True,
        ) as response:
            pass
            # print("get_consign", response)

        return 0

    def get_assurance(self, user_token: str):
        with self.client.get(
            url="/api/v1/assuranceservice/assurances/types",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": user_token,
            },
            name="get_assurance",
            catch_response=True,
        ) as response:
            pass
            # print("get_assurance", response)

        return 0
