import time
import uuid

from ts.services.admin_user_service import create_user_request
from ts.services.auth_service import login_user_request
from ts.services.contacts_service import add_one_contact_request, gen_random_contact
from ts.database_driver import db_driver


def init_users_and_contacts(num_users: int):
    request_id = "init data"
    admin_username = "admin"
    admin_password = "222222"
    admin_bearer, admin_user_id = login_user_request(
        admin_username, admin_password, request_id
    )
    for i in range(num_users):
        username = str(uuid.uuid4())
        password = username
        user = create_user_request(
            request_id,
            admin_bearer,
            username,
            password,
        )
        user_bearer, user_id = login_user_request(username, password, request_id)
        contact = add_one_contact_request(
            request_id, admin_bearer, gen_random_contact(None, user_id)
        )
        user["contactId"] = contact["id"]
        db_driver.users.insert_one(user)
        if i % 10 == 0:
            time.sleep(5)


def main():
    init_users_and_contacts(1000)


if __name__ == "__main__":
    main()
