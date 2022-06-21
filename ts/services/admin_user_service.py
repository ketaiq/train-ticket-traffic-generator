"""
This module includes all API calls provided by ts-admin-user-service.
"""

import logging
import requests
from json import JSONDecodeError

ADMIN_USER_SERVICE_URL = "http://130.211.196.121:8080/api/v1/adminuserservice/users"


def add_one_user(
    client,
    admin_bearer: str,
    document_num: str,
    username: str,
    password: str,
):
    client.post(
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
            "password": username,
            "userName": password,
        },
        name="create user",
    )
    logging.info(f"admin adds a new user {username}")


def get_all_users_request(admin_bearer: str, request_id: str) -> list:
    operation = "get all users"
    r = requests.get(
        url=ADMIN_USER_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        if r.json()["msg"] != "Success":
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response"
            )
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")
