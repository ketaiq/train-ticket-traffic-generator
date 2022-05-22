import uuid
import logging
import json


class IndependentRequest:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

    def visit_home(self):
        self.client.get("/index.html", name="visit home page")
        logging.info(
            f"user {self.request_id} visits the home page of train ticket system by running GET /index.html"
        )

    def search_ticket(self, departure_date, from_station, to_station):
        """
        Send a POST request of seaching tickets to the ts-travel-service to get left trip tickets.
        """
        head = {"Accept": "application/json", "Content-Type": "application/json"}
        json = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date,
        }
        with self.client.post(
            url="/api/v1/travelservice/trips/left",
            headers=head,
            json=json,
            catch_response=True,
            name="search ticket",
        ) as response:
            if response.json()["msg"] != "Success":
                response.failure("Got wrong response")
                logging.error("Got wrong response: {response.json()}!")
            elif response.elapsed.total_seconds() > 10:
                response.failure("Request took too long")
                logging.warning("Request took too long!")
        logging.info(
            f"user {self.request_id} searches train tickets from {from_station} to {to_station} on {departure_date} by running POST /api/v1/travelservice/trips/left"
        )


class DependentRequest:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

    def create_user(self):
        """
        Send a POST request of login to ts-auth-service to check login and dispatch token to user
        and then send a POST request to ts-admin-user-service to add one user entity.

        Dependence: add new user --> login
        """
        document_num = str(uuid.uuid4())
        user_name = str(uuid.uuid4())

        with self.client.post(
            url="/api/v1/users/login",
            json={"username": "admin", "password": "222222"},
            name="admin login",
        ) as response:
            if response.json()["msg"] != "login success":
                response.failure("Got wrong response")
                logging.error(f"Got wrong response: {response.json()}!")
            elif response.elapsed.total_seconds() > 10:
                response.failure("Request took too long")
                logging.warning("Request took too long!")
            else:
                token = response.json()["data"]["token"]
                admin_bearer = "Bearer " + token

                self.client.post(
                    url="/api/v1/adminuserservice/users",
                    headers={
                        "Authorization": admin_bearer,
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    json={
                        "documentNum": document_num,
                        "documentType": 0,
                        "email": "string",
                        "gender": 0,
                        "password": user_name,
                        "userName": user_name,
                    },
                    name="create user",
                )

        logging.info(
            f"user {self.request_id} login as admin and add a new user {user_name} by running POST /api/v1/users/login and POST /api/v1/adminuserservice/users"
        )

        return user_name

    def create_and_login_user(self):
        """
        Send requests of creating a new user and navigating to the client login page
        and then send a POST request of login the new user.
        """
        user_name = self.create_user()
        self.navigate_to_client_login()

        head = {"Accept": "application/json", "Content-Type": "application/json"}
        with self.client.post(
            url="/api/v1/users/login",
            headers=head,
            json={"username": user_name, "password": user_name},
            name="login user",
        ) as response:
            if response.json()["msg"] != "login success":
                response.failure("Got wrong response")
                logging.error(f"Got wrong response: {response.json()}!")
            elif response.elapsed.total_seconds() > 10:
                response.failure("Request took too long")
                logging.warning("Request took too long!")
            else:
                data = response.json()["data"]
                if data is not None:
                    token = data["token"]
                    self.bearer = "Bearer " + token
                    self.user_id = data["userId"]

        logging.info(
            f"user {self.request_id} login as {user_name} by running POST /api/v1/users/login"
        )

    def navigate_to_client_login(self):
        self.client.get("/client_login.html", name="visit client login page")

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
        head = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.bearer,
        }
        self.client.get(
            url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=2022-02-11",
            headers=head,
            name="visit client ticket book page",
        )

        # get assurance types
        self.client.get(
            url="/api/v1/assuranceservice/assurances/types",  # only find /api/v1/assuranceservice/types
            headers=head,
            name="get assurance types",
        )

        # get food
        self.client.get(
            url="/api/v1/foodservice/foods/2022-02-11/Shang%20Hai/Su%20Zhou/D1345",
            headers=head,
            name="get food",
        )

        # select contact
        response_contacts = self.client.get(
            url="/api/v1/contactservice/contacts/account/" + self.user_id,
            headers=head,
            name="select contact",
        )
        response_as_json_contacts = response_contacts.json()["data"]

        if len(response_as_json_contacts) == 0:
            response_contacts = self.client.post(
                url="/api/v1/contactservice/contacts",
                headers=head,
                json={
                    "name": self.user_id,
                    "accountId": self.user_id,
                    "documentType": "1",
                    "documentNumber": self.user_id,
                    "phoneNumber": "123456",
                },
                name="add new contact",
            )

            response_as_json_contacts = response_contacts.json()["data"]
            contact_id = response_as_json_contacts["id"]
        else:
            contact_id = response_as_json_contacts[0]["id"]

        # reserve
        body_for_reservation = {
            "accountId": self.user_id,
            "contactsId": contact_id,
            "tripId": "D1345",
            "seatType": "2",
            "date": "2022-05-20",
            "from": "Shang Hai",
            "to": "Su Zhou",
            "assurance": "0",
            "foodType": 1,
            "foodName": "Bone Soup",
            "foodPrice": 2.5,
            "stationName": "",
            "storeName": "",
        }
        self.client.post(
            url="/api/v1/preserveservice/preserve",
            headers=head,
            json=body_for_reservation,
            catch_response=True,
            name="reserve ticket",
        )

        # Select order
        response_order_refresh = self.client.post(
            url="/api/v1/orderservice/order/refresh",
            name="select order",
            headers=head,
            json={
                "loginId": self.user_id,
                "enableStateQuery": "false",
                "enableTravelDateQuery": "false",
                "enableBoughtDateQuery": "false",
                "travelDateStart": "null",
                "travelDateEnd": "null",
                "boughtDateStart": "null",
                "boughtDateEnd": "null",
            },
        )
        response_as_json = response_order_refresh.json()["data"]
        self.order_id = response_as_json[0]["id"]

        # Pay
        self.client.post(
            url="/api/v1/inside_pay_service/inside_payment",
            headers=head,
            json={"orderId": self.order_id, "tripId": "D1345"},
            name="pay",
        )

    def cancel_last_order_with_no_refund(self):
        head = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.bearer,
        }
        self.client.get(
            url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id,
            headers=head,
            name="cancel last order with no refund",
        )

    def get_voucher_of_last_order(self):
        head = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.bearer,
        }
        self.client.post(
            url="/getVoucher",
            headers=head,
            json={"orderId": self.order_id, "type": 1},
            name="get voucher",
        )

    def pick_up_ticket(self):
        head = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.bearer,
        }
        self.client.get(
            url="/api/v1/consignservice/consigns/order/" + self.order_id,
            headers=head,
            name="query consign order",
        )
        self.client.put(
            url="/api/v1/consignservice/consigns",
            name="update consign order",
            json={
                "accountId": self.user_id,
                "handleDate": "2022-05-20",
                "from": "Shang Hai",
                "to": "Su Zhou",
                "orderId": self.order_id,
                "consignee": self.order_id,
                "phone": "123",
                "weight": "1",
                "id": "",
                "isWithin": "false",
            },
            headers=head,
        )
