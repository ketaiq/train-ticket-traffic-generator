import uuid
from random import randint
from time import sleep

from ts.services.contacts_service import gen_random_contact, delete_one_contact_request
from ts.services.admin_basic_service import admin_add_one_contact
from ts.requests.passenger import admin_orders_get_list_by_user_id
from ts.services.auth_service import login_user
from ts.services.admin_user_service import user_add
from ts.services.travel_service import search_ticket, pick_random_travel
from ts.services.travel_plan_service import pick_random_strategy_and_search
from ts.services.admin_order_service import (
    admin_add_one_order,
    admin_delete_one_order,
    admin_update_one_order,
    gen_random_order,
)
from datetime import datetime

class SalesRequest:
    def __init__(self, client):
        self.client = client

        self.admin_username = "admin"
        self.admin_password = "222222"
        self.admin_user_id = None
        self.admin_bearer = None

        self.username = None
        self.password = None
        self.bearer = None
        self.user_id = None

        self.test_user_id = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"

        self.request_id = str(uuid.uuid4())

        self.contact = None

        self.departure_date = str(datetime.now().date())
        self.from_station = "Shang Hai"
        self.to_station = "Su Zhou"

        self.trip = None
        self.order = None

    def _contact_create_add(self):
        self.contact = gen_random_contact(str(uuid.uuid4()), self.user_id)
        admin_add_one_contact(self.client, self.admin_bearer, self.user_id, self.contact)

    def _ticket_search(self):

        trips = []

        for _ in range(randint(5, 10)):
            trips = pick_random_strategy_and_search(
                self.client,
                self.request_id,
                self.from_station,
                self.to_station,
                self.departure_date,
            )

        for _ in range(randint(0, 1)):
            trips = search_ticket(
                self.client,
                self.departure_date,
                self.from_station,
                self.to_station,
                self.request_id,
            )

        self.trip = pick_random_travel(trips)

    def _order_create_add(self):
        new_order_object = gen_random_order(self.trip, self.departure_date, self.admin_user_id, self.contact)
        new_order = admin_add_one_order(self.client, self.admin_bearer, self.admin_user_id, new_order_object)
        self.order = new_order

    def _order_update(self):
        new_order = gen_random_order(
            self.trip,
            self.departure_date,
            self.user_id,
            self.contact
        )
        picked_order = random.choice(self.orders)
        self.orders.remove(picked_order)
        new_order.id = picked_order.id
        admin_update_one_order(
            self.client, self.admin_bearer, self.admin_user_id, new_order
        )
        self.orders.append(new_order)

    def perform_create_order_actions(self):

        sleep(randint(2, 9))
        self.admin_bearer, _ = login_user(
            self.client,
            self.request_id,
            username=self.admin_username,
            password=self.admin_password,
            description="login Create Order admin user"
        )

        sleep(randint(2, 9))
        self.username = str(uuid.uuid4())
        self.password = self.username
        user_add(
            self.client,
            self.request_id,
            self.admin_bearer,
            username=self.username,
            password=self.password,
        )

        sleep(randint(2, 9))
        self._contact_create_add()

        sleep(randint(2, 9))
        self._ticket_search()

        sleep(randint(2, 9))
        self._order_create_add()

        sleep(randint(2, 9))
        admin_delete_one_order(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            self.order.id,
            self.order.trainNumber
        )

        sleep(randint(2, 9))
        _ = delete_one_contact_request(self.request_id, self.admin_bearer, self.contact.id)

    def perform_update_order_actions(self):

        sleep(randint(2, 9))
        self.admin_bearer, self.admin_user_id = login_user(
            self.client,
            self.request_id,
            username=self.admin_username,
            password=self.admin_password,
            description="login Create Order admin user"
        )

        user_orders_list = admin_orders_get_list_by_user_id(self.admin_bearer, self.test_user_id)
        order_id = user_orders_list[-1]["id"]

        admin_update_one_order(self.client, self.admin_bearer, self.test_user_id, self.order)