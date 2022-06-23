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
from ts.services.food_service import search_food_on_trip, pick_random_food, Food
from ts.services.consign_service import Consign
from ts.util import gen_random_date


class IrregularNormalRequest(PassengerRequest):
    def _search_ticket_for_a_random_trip(self):
        visit_home(self.client, self.request_id)
        trips = []
        # search tickets for 2-5x randomly
        for _ in range(random.randint(2, 5)):
            while len(trips) == 0:
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
        trips = []
        # search tickets with advanced filter for 5-10x randomly
        for _ in range(random.randint(5, 10)):
            while len(trips) == 0:
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
        self.seat_price = "0"
        if self.seat_type == SeatType.FIRST_CLASS.value:
            self.seat_price = self.trip["priceForConfortClass"]
        else:
            self.seat_price = self.trip["priceForEconomyClass"]
        self.contact_id = self.search_contacts()
        self.assurance = AssuranceType.NONE.value
        self.food = Food()
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
        self.consign = Consign()

    def perform_actions(self):
        # create and login user
        self.create_and_login_user()
        self._search_ticket_for_a_random_trip()
        self._gen_ticket_info()
        # book with food
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
        self.order_id = get_orders_by_login_id(self.client, self.user_id, self.bearer)[
            -1
        ]["id"]
        pay_one_order(
            self.client, self.bearer, self.user_id, self.order_id, self.trip["tripId"]
        )
        # collect ticket
        collect_one_ticket(self.client, self.bearer, self.user_id, self.order_id)
        # enter station
        enter_station(self.client, self.bearer, self.user_id, self.order_id)
