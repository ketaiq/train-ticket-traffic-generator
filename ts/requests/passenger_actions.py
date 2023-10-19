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
from ts.services.cancel_service import cancel_one_order, get_refund_amount
from ts.services.admin_order_service import (
    admin_add_order,
    admin_update_order,
    gen_random_order,
)


class PassengerActions(PassengerRequest):
    def __init__(self, client, description):
        super().__init__(client, description)

        self.order_creation_time = None
        self.order_completion_time = None

    def perform_actions(
        self,
        logger_tasks,
        search_simple_fr,
        search_simple_to,
        search_adv_fr,
        search_adv_to,
        food_incl,
        assurance_incl,
        consign_incl,
    ):
        sleep(randint(5, 10))
        self.admin_bearer, _ = login_user(
            self.client,
            self.request_id,
            username=self.admin_username,
            password=self.admin_password,
            description="Admin Login: " + self.description,
        )

        sleep(randint(5, 10))
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

        sleep(randint(5, 10))
        self.bearer, self.user_id = login_user(
            client=self.client,
            request_id=self.request_id,
            username=self.username,
            password=self.password,
            description="user login",
        )
        self.contact_id = self.contact_create_add()

        sleep(randint(5, 10))
        self.tickets_search(
            randint(search_simple_fr, search_simple_to),
            randint(search_adv_fr, search_adv_to),
        )

        sleep(randint(5, 10))
        self.gen_ticket_info(food_incl, assurance_incl, consign_incl)

        sleep(randint(5, 10))
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

        sleep(randint(5, 10))
        user_orders_list = admin_orders_get_list_by_user_id(
            self.admin_bearer, self.user_id
        )
        self.order_id = user_orders_list[-1]["id"]

        sleep(randint(5, 10))
        pay_one_order(
            self.client, self.bearer, self.user_id, self.order_id, self.trip["tripId"]
        )

        if self.description == "Cancel_With_Refund":
            sleep(randint(5, 10))
            get_refund_amount(self.client, self.bearer, self.order_id, self.user_id)

        if (
            self.description == "Cancel_No_Refund"
            or self.description == "Cancel_With_Refund"
        ):
            sleep(randint(5, 10))
            cancel_one_order(self.client, self.bearer, self.order_id, self.user_id)
        else:
            sleep(randint(5, 10))
            collect_one_ticket(self.client, self.bearer, self.user_id, self.order_id)

            sleep(randint(5, 10))
            enter_station(
                self.client, self.bearer, self.user_id, self.order_id, self.description
            )

        self.order_completion_time = datetime.datetime.now()
        order_age = int(
            (self.order_completion_time - self.order_creation_time).total_seconds()
        )
        logger_tasks.info(self.description + ": " + str(order_age))

    def perform_actions_sales(self):
        sleep(randint(5, 10))
        self.admin_bearer, self.admin_user_id = login_user(
            self.client,
            self.request_id,
            username=self.admin_username,
            password=self.admin_password,
            description="Admin Login: " + self.description,
        )

        if self.description == "sales_add_order":
            sleep(randint(5, 10))
            order_object = gen_random_order(self.test_user_id)
            the_order = admin_add_order(
                self.client,
                self.admin_bearer,
                self.admin_user_id,
                order_object,
                self.description,
            )

        if self.description == "sales_update_order":
            sleep(randint(5, 10))
            order_object = gen_random_order(self.test_user_id)
            the_order = admin_add_order(
                self.client,
                self.admin_bearer,
                self.admin_user_id,
                order_object,
                self.description + " add",
            )

            sleep(randint(5, 10))
            order_object.id = the_order["id"]
            order_object.boughtDate = the_order["boughtDate"]
            order_object.contactsName = order_object.contactsName + "__"
            the_order = admin_update_order(
                self.client,
                self.admin_bearer,
                self.admin_user_id,
                order_object,
                self.description + " update",
            )
