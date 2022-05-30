import uuid
from ts.services.auth_service import login_user
from ts.services.admin_user_service import add_one_user
from ts.services.visit_page import visit_client_login, visit_client_ticket_book
from ts.services.assurance_service import get_assurance_types
from ts.services.food_service import get_all_food
from ts.services.contacts_service import get_contacts_by_account_id, add_one_contact
from ts.services.preserve_service import reserve_one_ticket
from ts.services.order_service import get_orders_by_login_id
from ts.services.inside_payment_service import pay_one_order
from ts.services.cancel_service import cancel_one_order
from ts.services.voucher_service import get_one_voucher
from ts.services.consign_service import (
    add_one_consign_by_order_id,
    get_one_consign_by_order_id,
    update_one_consign_by_order_id,
)


class TrainTicketRequest:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

    def _create_user(self):
        """
        Send a POST request of login to ts-auth-service to check login and dispatch token to user
        and then send a POST request to ts-admin-user-service to add one user entity.

        Dependence: add new user --> login
        """
        document_num = str(uuid.uuid4())
        user_name = str(uuid.uuid4())
        admin_bearer, _ = login_user(
            self.client,
            username="admin",
            password="222222",
            description="login admin user",
        )
        add_one_user(
            self.client,
            admin_bearer,
            document_num,
            username=user_name,
            password=user_name,
        )

        return user_name

    def create_and_login_user(self):
        """
        Send requests of creating a new user and navigating to the client login page
        and then send a POST request of login the new user.
        """
        user_name = self._create_user()
        visit_client_login(self.client)
        self.bearer, self.user_id = login_user(
            self.client,
            username=user_name,
            password=user_name,
            description="login common user",
        )

    def get_a_contact(self):
        contact_id = ""
        # select contact
        response_of_contacts = get_contacts_by_account_id(
            self.client, self.user_id, self.bearer
        )
        if len(response_of_contacts) == 0:
            response_as_json_contacts = add_one_contact(
                self.client, self.bearer, self.user_id, self.user_id, self.user_id
            )
            contact_id = response_as_json_contacts["id"]
        else:
            contact_id = response_of_contacts[0]["id"]
        return contact_id

    def book(self):
        """
        Send a set of requests to book a ticket. Notice that there is no specific book service.
        A booking operation includes:
            visit book page
            get assurance types and food
            select contact
            reserve tickets
            select orders
            pay

        Dependence: book --> login
        """
        visit_client_ticket_book(self.client, self.bearer)
        get_assurance_types(self.client, self.bearer)
        get_all_food(self.client, self.bearer)
        contact_id = self.get_a_contact()
        reserve_one_ticket(self.client, self.user_id, contact_id, self.bearer)
        self.order_id = get_orders_by_login_id(self.client, self.user_id, self.bearer)
        pay_one_order(self.client, self.order_id, self.bearer)

    def cancel_last_order_with_no_refund(self):
        cancel_one_order(
            self.client,
            self.bearer,
            self.order_id,
            self.user_id,
            "cancel last order with no refund",
        )

    def get_voucher_of_last_order(self):
        get_one_voucher(self.client, self.bearer, self.order_id)

    def pick_up_ticket(self):
        add_one_consign_by_order_id(
            self.client, self.bearer, self.user_id, self.order_id
        )
        get_one_consign_by_order_id(self.client, self.bearer, self.order_id)
        update_one_consign_by_order_id(
            self.client, self.bearer, self.user_id, self.order_id
        )
