import uuid
from random import randint
from time import sleep
import datetime

from ts.requests.passenger import PassengerRequest, admin_orders_get_list_by_user_id
from ts.services.auth_service import login_user
from ts.services.admin_user_service import user_add
from ts.services.preserve_service import reserve_one_ticket
from ts.services.inside_payment_service import pay_one_order
from ts.services.execute_service import collect_one_ticket, enter_station
from ts.services.visit_page import visit_client_login


class IrregularNormalRequest(PassengerRequest):

    def __init__(self, client, description):
        super().__init__(client, description)
        self.order_creation_time = None
        self.order_completion_time = None

    def perform_actions(self, logger_tasks):

        sleep(randint(1, 2))
        self.admin_bearer, _ = login_user(
            self.client,
            self.request_id,
            username=self.admin_username,
            password=self.admin_password,
            description="admin login"
        )

        sleep(randint(1, 2))
        self.username = str(uuid.uuid4())
        self.password = self.username
        user_add(
            self.client,
            self.request_id,
            self.admin_bearer,
            username=self.username,
            password=self.password,
        )

        visit_client_login(self.client, self.request_id)

        sleep(randint(1, 2))
        self.bearer, self.user_id = login_user(
            client=self.client,
            request_id=self.request_id,
            username=self.username,
            password=self.password,
            description="user login"
        )

        sleep(randint(1, 2))
        self.tickets_search(randint(5, 10), randint(1, 1))

        sleep(randint(1, 2))
        self.gen_ticket_info(True, False, False)

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

        self.order_creation_time = datetime.datetime.now()

        sleep(randint(1, 2))
        user_orders_list = admin_orders_get_list_by_user_id(self.admin_bearer, self.user_id)
        self.order_id = user_orders_list[-1]["id"]

        sleep(randint(1, 2))
        pay_one_order(self.client, self.bearer, self.user_id, self.order_id, self.trip["tripId"])

        sleep(randint(1, 2))
        collect_one_ticket(self.client, self.bearer, self.user_id, self.order_id)

        sleep(randint(1, 2))
        enter_station(self.client, self.bearer, self.user_id, self.order_id)

        self.order_completion_time = datetime.datetime.now()
        order_age = int((self.order_completion_time - self.order_creation_time).total_seconds())
        logger_tasks.info(self.description + ": " + str(order_age))
