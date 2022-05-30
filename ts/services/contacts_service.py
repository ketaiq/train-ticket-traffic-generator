"""
This module includes all API calls provided by ts-contacts-service.
"""

import logging
from locust.clients import HttpSession


def get_contacts_by_account_id(client: HttpSession, user_id: str, bearer: str) -> list:
    data = []
    with client.get(
        url="/api/v1/contactservice/contacts/account/" + user_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="select contact",
    ) as response:
        if response.json()["msg"] != "Success":
            response.failure(
                f"user {user_id} tries to get a contact by account id {user_id} but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to get a contact by account id {user_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to get a contact by account id {user_id} but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to get a contact by account id {user_id} but request takes too long!"
            )
        else:
            data = response.json()["data"]
            if data is not None:
                if len(data) > 0:
                    contact_id = data[0]["id"]
                    logging.info(
                        f"user {user_id} gets a contact by account id {user_id}, its contact id is {contact_id}"
                    )
                else:
                    logging.info(
                        f"user {user_id} tries to get a contact by account id {user_id}, but there is no this contact"
                    )
            else:
                logging.error(
                    f"user {user_id} fails to get a contact by account id {user_id} because there is no response data"
                )

    return data


def add_one_contact(
    client: HttpSession, bearer: str, name: str, account_id: str, document_number: str
) -> dict:
    data = dict()
    with client.post(
        url="/api/v1/contactservice/contacts",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={
            "name": name,
            "accountId": account_id,
            "documentType": "1",
            "documentNumber": document_number,
            "phoneNumber": "123456",
        },
        name="add new contact",
    ) as response:
        if response.json()["msg"] != "Create contacts success":
            response.failure(f"user tries to add one contact but gets wrong response")
            logging.error(
                f"user tries to add one contact but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user tries to add one contact but request takes too long!"
            )
            logging.warning(
                f"user tries to add one contact but request takes too long!"
            )
        else:
            data = response.json()["data"]
            if data is not None:
                contact_id = data["id"]
                logging.info(
                    f"user adds a new contact {name}, its contact id is {contact_id}"
                )
            else:
                logging.error(
                    f"user fails to add a new contact because there is no response data"
                )

    return data
