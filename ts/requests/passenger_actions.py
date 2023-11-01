import uuid
import random
from random import randint
from time import sleep
import datetime

from ts.requests.passenger import PassengerRequest, admin_orders_get_list_by_user_id
from ts.services.auth_service import login_user
from ts.services.admin_user_service import user_add
from ts.services.order_service import refresh_user_orders
from ts.services.preserve_service import reserve_one_ticket
from ts.services.inside_payment_service import delete_payment_by_order_id, pay_one_order
from ts.services.execute_service import collect_one_ticket, enter_station
from ts.services.visit_page import visit_client_login
from ts.services.cancel_service import cancel_one_order, get_refund_amount
from ts.services.admin_order_service import (
    admin_add_order,
    admin_delete_one_order,
    admin_get_all_orders,
    admin_update_order,
    gen_random_order,
)
from ts.role import Role
from ts.database_driver import db_driver


class PassengerActions(PassengerRequest):
    ORDER_MIN_AGE = 60 * 30  # seconds

    def __init__(self, client, description):
        super().__init__(client, description)

        self.order_creation_time = None
        self.order_completion_time = None

    def _sample_user_or_create(self):
        if random.random() < 0.95:
            # sample user from local mongodb
            user = db_driver.sample_user()
            self.username = user["userName"]
            self.password = user["password"]
            self.contact_id = user["contactId"]
            visit_client_login(self.client, self.request_id)
            sleep(randint(5, 10))
            self.bearer, self.user_id = login_user(
                client=self.client,
                request_id=self.request_id,
                username=self.username,
                password=self.password,
                description=f"User Login: {self.description}",
            )
        else:
            # create a new user and contact
            self.username = str(uuid.uuid4())
            self.password = self.username
            user = user_add(
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
                description=f"User Login: {self.description}",
            )
            self.contact_id = self.contact_create_add()
            # save new user to the local mongodb
            user["contactId"] = self.contact_id
            db_driver.users.insert_one(user)

    def _get_order_id_to_pay(self):
        user_orders = refresh_user_orders(self.client, self.user_id, self.bearer)
        user_orders = sorted(user_orders, key=lambda order: order["boughtDate"])
        self.order_id = user_orders[-1]["id"]

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
        self._sample_user_or_create()
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

        sleep(randint(5, 10))
        self._get_order_id_to_pay()

        sleep(randint(5, 10))
        pay_one_order(
            self.client, self.bearer, self.user_id, self.order_id, self.trip["tripId"]
        )

        if self.description == Role.Cancel_With_Refund.name:
            sleep(randint(5, 10))
            get_refund_amount(self.client, self.bearer, self.order_id, self.user_id)

        if (
            self.description == Role.Cancel_No_Refund.name
            or self.description == Role.Cancel_With_Refund.name
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

    def perform_sales_add_order(self):
        sleep(randint(5, 10))
        order_object = gen_random_order(self.test_user_id)
        admin_add_order(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            order_object,
            self.description,
        )

    def perform_sales_add_update_order(self):
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

    def perform_sales_delete_order(self):
        sleep(randint(5, 10))
        all_orders = admin_get_all_orders(self.client, self.admin_bearer)
        orders_deleted = 0
        # iterate through all orders
        for order in all_orders:
            order_id = order["id"]
            order_train_number = order["trainNumber"]
            order_bought_time = order["boughtDate"]
            order_status = order["status"]

            bought_time = datetime.datetime.fromtimestamp(
                round(order_bought_time / 1000)
            )
            current_time = datetime.datetime.now()
            seconds_passed = int((current_time - bought_time).total_seconds())
            # delete used orders or expired orders
            if order_status == 6 or seconds_passed > PassengerActions.ORDER_MIN_AGE:
                admin_delete_one_order(
                    self.client,
                    self.admin_bearer,
                    self.admin_user_id,
                    order_id,
                    order_train_number,
                )
                # delete payment related to the order
                delete_payment_by_order_id(self.client, self.admin_bearer, order_id)
                orders_deleted += 1
            # delete at most 100 orders
            if orders_deleted > 100:
                break
            if orders_deleted % 10 == 0:
                sleep(randint(5, 10))
