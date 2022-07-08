import uuid
import random
from ts.services.admin_route_service import pick_two_random_stations_in_one_route
from ts.services.auth_service import login_user
from ts.services.admin_user_service import add_one_user
from ts.services.contacts_service import gen_random_contact
from ts.services.admin_basic_service import admin_add_one_contact
from ts.services.admin_order_service import (
    admin_add_one_order,
    admin_delete_one_order,
    admin_update_one_order,
    gen_random_order,
)
from ts.services.travel_plan_service import pick_random_strategy_and_search
from ts.services.travel_service import pick_random_travel
from ts.services.visit_page import visit_home
from ts.util import gen_random_date

from random import randint
from time import sleep

class SalesRequest:
    def __init__(self, client):
        self.client = client
        self.admin_bearer = None
        self.admin_user_id = None
        self.request_id = str(uuid.uuid4())
        self.created_user = None
        self.contact = None
        self.from_station = None
        self.to_station = None
        self.departure_date = None
        self.trip = None
        self.orders = []

    def _login_admin_user(self, description):
        self.admin_bearer, self.admin_user_id = login_user(
            client=self.client,
            username="admin",
            password="222222",
            description=f"login {description} admin user",
        )

    def _create_user(self):
        username = str(uuid.uuid4())
        password = username
        self.created_user = add_one_user(
            self.client,
            self.request_id,
            self.admin_bearer,
            username=username,
            password=password,
        )

    def _create_contact(self):
        self.contact = gen_random_contact(
            str(uuid.uuid4()), self.created_user["userId"]
        )
        admin_add_one_contact(
            self.client, self.admin_bearer, self.created_user["userId"], self.contact
        )

    def _search_ticket_for_a_random_trip(self):
        visit_home(self.client, self.request_id)
        trips = []
        while len(trips) == 0:
            (
                self.from_station,
                self.to_station,
            ) = pick_two_random_stations_in_one_route()
            self.departure_date = gen_random_date()
            trips = pick_random_strategy_and_search(
                self.client,
                self.request_id,
                self.from_station,
                self.to_station,
                self.departure_date,
            )
        self.trip = pick_random_travel(trips)

    def _add_order(self):
        new_order = gen_random_order(
            self.trip, self.departure_date, self.created_user["userId"], self.contact
        )
        added_order = admin_add_one_order(
            self.client, self.admin_bearer, self.admin_user_id, new_order
        )
        new_order.id = added_order["id"]
        self.orders.append(new_order)

    def _update_order(self):
        if self.orders:
            new_order = gen_random_order(
                self.trip,
                self.departure_date,
                self.created_user["userId"],
                self.contact,
            )
            picked_order = random.choice(self.orders)
            self.orders.remove(picked_order)
            new_order.id = picked_order.id
            admin_update_one_order(
                self.client, self.admin_bearer, self.admin_user_id, new_order
            )
            self.orders.append(new_order)

    def _delete_order(self):
        if self.orders:
            picked_order = random.choice(self.orders)
            self.orders.remove(picked_order)
            admin_delete_one_order(
                self.client,
                self.admin_bearer,
                self.admin_user_id,
                picked_order.id,
                picked_order.trainNumber,
            )

    def perform_create_order_actions(self):

        sleep(randint(1,5))
        self._login_admin_user("Create Order")

        sleep(randint(1,5))
        self._create_user()

        sleep(randint(1,5))
        self._create_contact()

        sleep(randint(1,5))
        self._search_ticket_for_a_random_trip()

        sleep(randint(1,5))
        self._add_order()

    def perform_update_order_actions(self):

        sleep(randint(1,5))
        self._login_admin_user("Update Order")

        sleep(randint(1,5))
        self._update_order()

    def perform_delete_order_actions(self):

        sleep(randint(1,5))
        self._login_admin_user("Delete Order")

        sleep(randint(1,5))
        self._delete_order()
