from random import randint
from time import sleep

from ts.requests.passenger import PassengerRequest
from ts.services.travel_service import pick_random_travel, search_ticket
from ts.services.assurance_service import AssuranceType
from ts.services.inside_payment_service import pay_one_order
from ts.services.order_service import refresh_user_orders
from ts.services.visit_page import visit_home
from ts.services.food_service import Food
from ts.services.consign_service import Consign
from ts.services.cancel_service import cancel_one_order, get_refund_amount
from ts.util import gen_random_date
from ts.services.preserve_service import pick_random_seat_type, reserve_one_ticket


class CancelWithRefundRequest(PassengerRequest):
    def _search_ticket_for_a_random_trip(self):
        print(" -- #1")
        visit_home(self.client, self.request_id)

        print(" -- #2")
        # Search concrete destination to find a trip needed
        self.from_station = "Shang Hai"
        self.to_station = "Su Zhou"
        self.departure_date = gen_random_date()
        trips = search_ticket(
            self.client,
            self.departure_date,
            self.from_station,
            self.to_station,
            self.request_id,
        )

        print(" -- #3")
        self.trip = pick_random_travel(trips)

        print(" -- #4")

    def _gen_ticket_info(self):
        self.seat_type = pick_random_seat_type()
        self.seat_price = self.get_seat_price()
        self.contact_id = self.search_contacts()
        self.assurance = AssuranceType.NONE.value
        self.food = Food()
        self.consign = Consign()

    def perform_actions(self):
        print("@1")
        sleep(randint(1, 2))
        self.create_and_login_user()

        print("@2")
        sleep(randint(1, 2))
        self._search_ticket_for_a_random_trip()

        print("@3")
        sleep(randint(1, 2))
        self._gen_ticket_info()

        print("@4")
        sleep(randint(1, 2))

        print("@5")
        sleep(randint(1, 2))
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

        print("@6")
        sleep(randint(1, 2))
        self.order_id = refresh_user_orders(self.client, self.user_id, self.bearer)[-1][
            "id"
        ]

        print("@7")
        sleep(randint(1, 2))
        pay_one_order(
            self.client, self.bearer, self.user_id, self.order_id, self.trip["tripId"]
        )

        print("@8")
        sleep(randint(1, 2))
        get_refund_amount(self.client, self.bearer, self.order_id, self.user_id)

        print("@9")
        sleep(randint(1, 2))
        cancel_one_order(self.client, self.bearer, self.order_id, self.user_id)

        print("@10 ---------------------------------------------------")
