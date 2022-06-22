from ts.requests.passenger import PassengerRequest
from ts.services.admin_route_service import pick_two_random_stations_in_one_route
from ts.services.travel_service import pick_random_travel, search_ticket
from ts.services.preserve_service import (
    pick_random_seat_type,
    SeatType,
    reserve_one_ticket,
)
from ts.services.assurance_service import (
    get_assurance_types,
    pick_random_assurance_type,
)
from ts.services.inside_payment_service import pay_one_order
from ts.services.order_service import get_orders_by_login_id
from ts.services.execute_service import collect_one_ticket, enter_station
from ts.services.visit_page import visit_ticket_book
from ts.services.food_service import search_food_on_trip, pick_random_food, Food
from ts.services.consign_service import Consign
from ts.services.voucher_service import get_one_voucher
from ts.util import gen_random_date


class RegularRequest(PassengerRequest):
    def perform_actions(self):
        # login
        self.login_existent_user()
        # search tickets
        trips = []
        from_station, to_station = pick_two_random_stations_in_one_route()
        departure_date = gen_random_date()
        trips = search_ticket(
            self.client,
            departure_date,
            from_station,
            to_station,
            self.request_id,
        )
        # book with food
        trip = pick_random_travel(trips)
        trip_id = trip["tripId"]["type"] + trip["tripId"]["number"]
        seat_type = pick_random_seat_type()
        seat_price = "0"
        if seat_type == SeatType.FIRST_CLASS.value:
            seat_price = trip["priceForConfortClass"]
        else:
            seat_price = trip["priceForEconomyClass"]
        visit_ticket_book(
            self.client,
            self.bearer,
            self.user_id,
            trip_id,
            trip["startingStation"],
            trip["terminalStation"],
            seat_type,
            seat_price,
            departure_date,
        )
        contact_id = self.search_contacts()
        assurance_types = get_assurance_types(self.client, self.bearer, self.user_id)
        assurance = pick_random_assurance_type(assurance_types)
        all_food = search_food_on_trip(
            self.client,
            self.bearer,
            self.user_id,
            departure_date,
            from_station,
            to_station,
            trip_id,
        )
        food = Food()
        if all_food is not None:
            food = pick_random_food(all_food)
        reserve_one_ticket(
            self.client,
            self.bearer,
            self.user_id,
            contact_id,
            trip_id,
            seat_type,
            departure_date,
            from_station,
            to_station,
            assurance,
            food,
            Consign(),
        )
        # pay for the booking
        order_id = get_orders_by_login_id(self.client, self.user_id, self.bearer)[-1][
            "id"
        ]
        pay_one_order(self.client, self.bearer, self.user_id, order_id, trip_id)
        # collect ticket
        collect_one_ticket(self.client, self.bearer, self.user_id, order_id)
        # enter station
        enter_station(self.client, self.bearer, self.user_id, order_id)
        # print voucher
        get_one_voucher(self.client, self.bearer, self.user_id, order_id)
