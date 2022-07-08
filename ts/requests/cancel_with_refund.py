from locust import between

from ts.requests.passenger import PassengerRequest
from ts.services.admin_route_service import pick_two_random_stations_in_one_route
from ts.services.travel_service import pick_random_travel, search_ticket
from ts.services.preserve_service import (
    pick_random_seat_type,
    SeatType,
    reserve_one_ticket,
)
from ts.services.assurance_service import AssuranceType
from ts.services.inside_payment_service import pay_one_order
from ts.services.order_service import get_orders_by_login_id
from ts.services.visit_page import visit_ticket_book, visit_home
from ts.services.food_service import Food
from ts.services.consign_service import Consign
from ts.services.cancel_service import cancel_one_order, get_refund_amount
from ts.util import gen_random_date

from random import randint
from time import sleep


class CancelWithRefundRequest(PassengerRequest):

    wait_time = between(2, 10)

    def _search_ticket_for_a_random_trip(self):
        visit_home(self.client, self.request_id)
        trips = []
        while len(trips) == 0:
            self.from_station, self.to_station = pick_two_random_stations_in_one_route()
            self.departure_date = gen_random_date()
            trips = search_ticket(
                self.client,
                self.departure_date,
                self.from_station,
                self.to_station,
                self.request_id,
            )
        self.trip = pick_random_travel(trips)

    def _gen_ticket_info(self):
        self.seat_type = pick_random_seat_type()
        self.seat_price = "0"
        if self.seat_type == SeatType.FIRST_CLASS.value:
            self.seat_price = self.trip["priceForConfortClass"]
        else:
            self.seat_price = self.trip["priceForEconomyClass"]
        self.contact_id = self.search_contacts()
        self.assurance = AssuranceType.NONE.value
        self.food = Food()
        self.consign = Consign()

    def perform_actions(self):

        # login
        sleep(randint(1,5))
        self.login_existent_user()

        # search tickets
        self._search_ticket_for_a_random_trip()

        sleep(randint(1,5))
        self._gen_ticket_info()

        sleep(randint(1,5))
        trip_id = self.trip["tripId"]["type"] + self.trip["tripId"]["number"]
        visit_ticket_book(
            self.client,
            self.bearer,
            self.user_id,
            trip_id,
            self.trip["startingStation"],
            self.trip["terminalStation"],
            self.seat_type,
            self.seat_price,
            self.departure_date,
        )

        sleep(randint(1,5))
        reserve_one_ticket(
            self.client,
            self.bearer,
            self.user_id,
            self.contact_id,
            trip_id,
            self.seat_type,
            self.departure_date,
            self.from_station,
            self.to_station,
            self.assurance,
            self.food,
            self.consign,
        )

        # pay for the booking
        sleep(randint(1,5))
        self.order_id = get_orders_by_login_id(self.client, self.user_id, self.bearer)[
            -1
        ]["id"]
        pay_one_order(self.client, self.bearer, self.user_id, self.order_id, trip_id)

        sleep(randint(1,5))
        get_refund_amount(self.client, self.bearer, self.order_id, self.user_id)

        sleep(randint(1,5))
        cancel_one_order(self.client, self.bearer, self.order_id, self.user_id)
