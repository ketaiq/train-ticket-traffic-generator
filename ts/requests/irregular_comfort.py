import random
from ts.requests.passenger import PassengerRequest
from ts.services.admin_route_service import pick_two_random_stations_in_one_route
from ts.services.travel_plan_service import pick_random_strategy_and_search
from ts.services.travel_service import pick_random_travel, search_ticket
from ts.services.preserve_service import (
    reserve_one_ticket,
)
from ts.services.inside_payment_service import pay_one_order
from ts.services.order_service import get_orders_by_login_id
from ts.services.execute_service import collect_one_ticket, enter_station
from ts.services.visit_page import visit_ticket_book
from ts.services.food_service import search_food_on_trip, pick_random_food, Food
from ts.services.assurance_service import (
    get_assurance_types,
    pick_random_assurance_type,
)
from ts.services.consign_service import gen_random_consign
from ts.util import gen_random_date


class IrregularComfortRequest(PassengerRequest):
    def perform_actions(self):
        # create and login user
        self.create_and_login_user()
        # search tickets for 2-5x randomly
        trips = []
        from_station, to_station = pick_two_random_stations_in_one_route()
        departure_date = gen_random_date()
        for _ in range(random.randint(2, 5)):
            trips = search_ticket(
                self.client,
                departure_date,
                from_station,
                to_station,
                self.request_id,
            )
        # search tickets with advanced filter for 5-10x randomly
        for _ in range(random.randint(5, 10)):
            trips = pick_random_strategy_and_search(
                self.client, self.request_id, from_station, to_station, departure_date
            )
        # book with assurance, food and consign
        trip = pick_random_travel(trips)
        seat_type = "2"
        seat_price = trip["priceForFirstClassSeat"]
        visit_ticket_book(
            self.client,
            self.bearer,
            self.user_id,
            trip["tripId"],
            trip["fromStationName"],
            trip["toStationName"],
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
            trip["tripId"],
        )
        food = Food()
        if all_food is not None:
            food = pick_random_food(all_food)
        consign = gen_random_consign()
        reserve_one_ticket(
            self.client,
            self.bearer,
            self.user_id,
            contact_id,
            trip["tripId"],
            seat_type,
            departure_date,
            from_station,
            to_station,
            assurance,
            food,
            consign,
        )
        # pay for the booking
        order_id = get_orders_by_login_id(self.client, self.user_id, self.bearer)[-1][
            "id"
        ]
        pay_one_order(self.client, self.bearer, self.user_id, order_id, trip["tripId"])
        # collect ticket
        collect_one_ticket(self.client, self.bearer, self.user_id, order_id)
        # enter station
        enter_station(self.client, self.bearer, self.user_id, order_id)
