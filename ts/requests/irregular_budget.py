import random
from ts.requests.passenger import PassengerRequest
from ts.services.admin_route_service import pick_two_random_stations_in_one_route
from ts.services.travel_plan_service import pick_random_strategy_and_search
from ts.services.travel_service import pick_random_travel, search_ticket
from ts.services.preserve_service import (
    pick_random_seat_type,
    SeatType,
    reserve_one_ticket,
)
from ts.services.assurance_service import AssuranceType
from ts.services.inside_payment_service import pay_one_order
from ts.services.order_service import get_orders_by_login_id
from ts.services.execute_service import collect_one_ticket, enter_station
from ts.services.visit_page import visit_ticket_book, visit_home
from ts.services.food_service import Food
from ts.services.consign_service import Consign
from ts.util import gen_random_date

from random import randint
from time import sleep


class IrregularBudgetRequest(PassengerRequest):
    def _search_ticket_for_a_random_trip(self):
        visit_home(self.client, self.request_id)

        # search tickets for 10-20x randomly
        for _ in range(20):
            sleep(randint(10, 20))
            trips = []
            while len(trips) == 0:
                # if doesn't find a trip, find again
                (
                    self.from_station,
                    self.to_station,
                ) = pick_two_random_stations_in_one_route()
                self.departure_date = gen_random_date()
                trips = search_ticket(
                    self.client,
                    self.departure_date,
                    self.from_station,
                    self.to_station,
                    self.request_id,
                )
        # search tickets with advanced filter for 5-20x randomly
        for _ in range(random.randint(5, 15)):
            sleep(randint(20, 60))
            trips = []
            while len(trips) == 0:
                # if doesn't find a trip, find again
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

    def _gen_ticket_info(self):
        self.seat_type = pick_random_seat_type()
        self.seat_price = self.get_seat_price()
        self.contact_id = self.search_contacts()
        self.assurance = AssuranceType.NONE.value
        self.food = Food()
        self.consign = Consign()

    def perform_actions(self):

        # create and login user
        sleep(randint(1, 5))
        self.create_and_login_user()

        # search ticket
        sleep(randint(1, 5))
        self._search_ticket_for_a_random_trip()

        # book without extra services
        sleep(randint(1, 5))
        self._gen_ticket_info()
        visit_ticket_book(
            self.client,
            self.bearer,
            self.user_id,
            self.trip["tripId"],
            self.trip["fromStationName"],
            self.trip["toStationName"],
            self.seat_type,
            self.seat_price,
            self.departure_date,
        )

        sleep(randint(1, 5))
        reserve_one_ticket(
            self.client,
            self.bearer,
            self.user_id,
            self.contact_id,
            self.trip["tripId"],
            self.seat_type,
            self.departure_date,
            self.from_station,
            self.to_station,
            self.assurance,
            self.food,
            self.consign,
        )

        # pay for the booking
        sleep(randint(1, 5))
        self.order_id = get_orders_by_login_id(self.client, self.user_id, self.bearer)[
            -1
        ]["id"]
        pay_one_order(
            self.client, self.bearer, self.user_id, self.order_id, self.trip["tripId"]
        )

        # collect ticket
        sleep(randint(1, 5))
        collect_one_ticket(self.client, self.bearer, self.user_id, self.order_id)

        # enter station
        sleep(randint(1, 5))
        enter_station(self.client, self.bearer, self.user_id, self.order_id)
