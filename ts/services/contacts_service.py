"""
This module includes all API calls provided by ts-contacts-service.
"""

import logging
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
from enum import IntEnum
from ts.util import gen_random_name, gen_random_document_number, gen_random_phone_number
import random


class Contact:
    def __init__(
        self,
        id: str,
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
        elif response.elapsed.total_seconds() > 10:
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
        elif response.elapsed.total_seconds() > 10:
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
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(contact.user_id, operation, response)
        else:
            old_contact = response.json()["data"]
            log = f"from {old_contact} to {contact}"
            log_response_info(contact.user_id, operation, log)


def gen_random_contact(contact_id: str, user_id: str) -> Contact:
    name = gen_random_name()
    document_number = gen_random_document_number()
    document_type = random.choice(list(DocumentType)).value
    phone_number = gen_random_phone_number()
    return Contact(
        contact_id, name, user_id, document_number, document_type, phone_number
    )
