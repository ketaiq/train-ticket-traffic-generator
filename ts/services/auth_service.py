"""
This module includes all API calls provided by ts-auth-service.
"""

import logging
import requests
from typing import Tuple
from json import JSONDecodeError
from ts import TIMEOUT_MAX, HOST_URL
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_http_error,
    log_timeout_error,
    log_wrong_response_error,
)


def login_user(
    client, request_id: str, username: str, password: str, description: str
) -> Tuple[str, str]:
    admin_bearer = ""
    user_id = ""
    operation = "log in"
    with client.post(
        url="/api/v1/users/login",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"username": username, "password": password},
        name=description,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"username: {username}, password: {password}"
            log_http_error(
                request_id,
                operation,
                response,
                data,
                name="request",
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "login success":
                    log_wrong_response_error(
                        request_id,
                        operation,
                        response.failure,
                        response.json(),
                        name="request",
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(
                        request_id, operation, response.failure, name="request"
                    )
                else:
                    key = "data"
                    data = response.json()["data"]
                    if data is not None:
                        admin_bearer = "Bearer " + data["token"]
                        user_id = data["userId"]
                        logging.info(f"user {username} logs in")
                    else:
                        logging.error(
                            f"user {username} fails to log in because there is no response data"
                        )
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()
    return admin_bearer, user_id


def login_user_request(
    username: str, password: str, request_id: str
) -> Tuple[str, str]:
    operation = "log in"
    admin_bearer = ""
    user_id = ""
    r = requests.post(
        url=f"http://{HOST_URL}/api/v1/users/login",
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
