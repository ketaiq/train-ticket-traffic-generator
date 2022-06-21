"""
This module includes all API calls provided by ts-contacts-service.
"""

import logging
import requests
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
from enum import IntEnum
from ts.util import gen_random_name, gen_random_document_number, gen_random_phone_number
import random
from json import JSONDecodeError
from ts import TIMEOUT_MAX

CONTACTS_SERVICE_URL = "http://130.211.196.121:8080/api/v1/contactservice/contacts"
ORIGINAL_CONTACTS = [
    {
        "id": "3fcb512a-339d-4cf2-ad62-744558353adb",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "Contacts_One",
        "documentType": 1,
        "documentNumber": "DocumentNumber_One",
        "phoneNumber": "ContactsPhoneNum_One",
    },
    {
        "id": "014acb13-6433-4ca4-9246-d38b1d493638",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "Contacts_Two",
        "documentType": 1,
        "documentNumber": "DocumentNumber_Two",
        "phoneNumber": "ContactsPhoneNum_Two",
    },
]


class Contact:
    def __init__(
        self,
        id: str | None,
        name: str,
        user_id: str,
        document_number: str,
        document_type: int,
        phone_number: str,
    ):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.document_number = document_number
        self.document_type = document_type
        self.phone_number = phone_number


class DocumentType(IntEnum):
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-contacts-service/src/main/java/contacts/entity/DocumentType.java
    """

    ID_CARD = 1
    PASSPORT = 2
    OTHER = 3


def get_contacts_by_account_id(client, user_id: str, bearer: str) -> list:
    operation = "get a contact by user id"
    data = []
    with client.get(
        url="/api/v1/contactservice/contacts/account/" + user_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Success":
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response)
        else:
            data = response.json()["data"]
            if data is not None:
                if len(data) > 0:
                    contact_id = data[0]["id"]
                    log_response_info(user_id, operation, contact_id)
                else:
                    logging.warning(
                        f"user {user_id} tries to get a contact by account id {user_id}, but there is no this contact"
                    )
            else:
                logging.warning(
                    f"user {user_id} fails to get a contact by account id {user_id} because there is no response data"
                )

    return data


def get_all_contacts_request(request_id: str, bearer: str):
    operation = "get all contacts"
    r = requests.get(
        url=CONTACTS_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            contacts = r.json()["data"]
            return contacts
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def add_one_contact(
    client, bearer: str, name: str, user_id: str, document_number: str
) -> dict:
    operation = "add new contact"
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
            "accountId": user_id,
            "documentType": "1",
            "documentNumber": document_number,
            "phoneNumber": "123456",
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Create contacts success":
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response)
        else:
            data = response.json()["data"]
            if data is not None:
                contact_id = data["id"]
                log_response_info(user_id, operation, contact_id)
            else:
                logging.warning(
                    f"user fails to add a new contact because there is no response data"
                )

    return data


def add_one_contact_request(
    request_id: str, admin_bearer: str, contact: Contact
) -> dict:
    operation = "delete one contact"
    r = requests.post(
        url=CONTACTS_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "name": contact.name,
            "accountId": contact.user_id,
            "documentType": contact.document_type,
            "documentNumber": contact.document_number,
            "phoneNumber": contact.phone_number,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            added_contact = r.json()["data"]
            logging.info(f"request {request_id} {operation} {added_contact}")
            return added_contact
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def update_one_contact(client, bearer: str, contact: Contact):
    operation = "update a contact"
    with client.put(
        url="/api/v1/contactservice/contacts",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={
            "id": contact.id,
            "name": contact.name,
            "accountId": contact.user_id,
            "documentType": contact.document_type,
            "documentNumber": contact.document_number,
            "phoneNumber": contact.phone_number,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Modify success":
            log_wrong_response_warning(contact.user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(contact.user_id, operation, response)
        else:
            old_contact = response.json()["data"]
            log = f"from {old_contact} to {contact}"
            log_response_info(contact.user_id, operation, log)


def update_one_contact_request(
    request_id: str, admin_bearer: str, contact: Contact
) -> dict:
    operation = "update one contact"
    r = requests.put(
        url=CONTACTS_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": contact.id,
            "name": contact.name,
            "accountId": contact.user_id,
            "documentType": contact.document_type,
            "documentNumber": contact.document_number,
            "phoneNumber": contact.phone_number,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            contact = r.json()["data"]
            logging.info(f"request {request_id} {operation} {contact}")
            return contact
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def delete_one_contact(client, admin_bearer: str, admin_user_id: str, contact_id: str):
    operation = "delete one contact"
    with client.delete(
        url=f"/api/v1/contactservice/contacts/{contact_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Delete success":
            log_wrong_response_warning(admin_user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(admin_user_id, operation, response)
        else:
            deleted_contact_id = response.json()["data"]
            log_response_info(admin_user_id, operation, deleted_contact_id)


def delete_one_contact_request(
    request_id: str, admin_bearer: str, contact_id: str
) -> str:
    operation = "delete one contact"
    r = requests.delete(
        url=CONTACTS_SERVICE_URL + "/" + contact_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            deleted_contact_id = r.json()["data"]
            logging.info(f"request {request_id} {operation} {deleted_contact_id}")
            return deleted_contact_id
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def restore_original_contacts(request_id: str, admin_bearer: str):
    contacts = get_all_contacts_request(request_id, admin_bearer)
    for contact in contacts:
        if contact not in ORIGINAL_CONTACTS:
            deleted_contact_id = delete_one_contact_request(
                request_id, admin_bearer, contact["id"]
            )
            print(f"Delete contact {deleted_contact_id}")


def gen_random_contact(contact_id: str | None, user_id: str) -> Contact:
    name = gen_random_name()
    document_number = gen_random_document_number()
    document_type = random.choice(list(DocumentType)).value
    phone_number = gen_random_phone_number()
    return Contact(
        contact_id, name, user_id, document_number, document_type, phone_number
    )
