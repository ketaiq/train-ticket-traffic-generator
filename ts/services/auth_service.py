"""
This module includes all API calls provided by ts-auth-service.
"""

import logging
import requests
from typing import Tuple
from json import JSONDecodeError
from ts import TIMEOUT_MAX


def login_user(
    client, username: str, password: str, description: str
) -> Tuple[str, str]:
    admin_bearer = ""
    user_id = ""
    operation = "log in"
    with client.post(
        url="/api/v1/users/login",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"username": username, "password": password},
        name=description,
    ) as response:
        if response.json()["msg"] != "login success":
            log = f"user {username} tries to {operation} but gets wrong response"
            logging.warning(f"{log} {response.json()}")
            response.failure(log)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log = f"user {username} tries to {operation} but request takes too long!"
            logging.warning(log)
            response.failure(log)
        else:
            data = response.json()["data"]
            if data is not None:
                admin_bearer = "Bearer " + data["token"]
                user_id = data["userId"]
                logging.info(f"user {username} logs in")
            else:
                logging.error(
                    f"user {username} fails to log in because there is no response data"
                )

    return admin_bearer, user_id


def login_user_request(
    username: str, password: str, request_id: str
) -> Tuple[str, str]:
    operation = "log in"
    admin_bearer = ""
    user_id = ""
    r = requests.post(
        url="http://34.160.158.68/api/v1/users/login",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={"username": username, "password": password},
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "login success":
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            data = r.json()["data"]
            key = "token"
            admin_bearer = "Bearer " + data["token"]
            key = "userId"
            user_id = data["userId"]
            return admin_bearer, user_id
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")
