import uuid
from ts.services.admin_user_service import add_one_user
from ts.services.visit_page import visit_client_login
from ts.services.auth_service import login_user
from ts.services.contacts_service import (
    get_contacts_by_account_id,
    add_one_contact,
    gen_random_contact
)
from ts.util import gen_random_name, gen_random_document_number


class PassengerRequest:

    def __init__(self, client, description):
        self.client = client
        self.description = description
        self.username = None
        self.password = None
        self.bearer = None
        self.user_id = None
        self.request_id = str(uuid.uuid4())

        self.from_station = None
        self.to_station = None
        self.departure_date = None
        self.trip = None
        self.seat_type = None
        self.seat_price = None
        self.contact_id = None
        self.assurance = None
        self.food = None
        self.consign = None
        self.order_id = None

    def create_and_login_user(self):
        """
        Send requests of creating a new user and navigating to the client login page
        and then send a POST request of login the new user.
        """
        admin_bearer, _ = login_user(
            self.client,
            username="admin",
            password="222222",
            description="login admin user",
        )
        self.username = str(uuid.uuid4())
        self.password = self.username
        add_one_user(
            self.client,
            self.request_id,
            admin_bearer,
            username=self.username,
            password=self.password,
        )
        visit_client_login(self.client, self.request_id)
        self.bearer, self.user_id = login_user(
            client=self.client,
            username=self.username,
            password=self.password,
            description=f"login {self.description} user",
        )

    def login_existent_user(self):
        """
        Login an existent user. If user doesn't exist, it will create one and login.
        """
        if self.username is None or self.password is None:
            self.create_and_login_user()
        else:
            self.bearer, self.user_id = login_user(
                client=self.client,
                username=self.username,
                password=self.password,
                description=f"login {self.description} user",
            )

    def search_contacts(self) -> str:
        contact_id = ""
        # select contact
        response_of_contacts = get_contacts_by_account_id(
            self.client, self.user_id, self.bearer
        )
        if len(response_of_contacts) == 0:
            new_contact = gen_random_contact(None, self.user_id)
            new_contact = add_one_contact(
                self.client, self.bearer, self.user_id, new_contact
            )
            contact_id = new_contact["id"]
        else:
            contact_id = response_of_contacts[0]["id"]
        return contact_id
